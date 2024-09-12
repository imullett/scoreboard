from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import TeamData, GameData, MatchupData, CurrentWeek
from sqlalchemy.orm import aliased
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import func
from statistics import median

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ingestor:memesbowl123@localhost:3306/ff' 

db = SQLAlchemy(app)

@app.route('/matchups', methods=['GET'])
@app.route('/matchups/<int:week_number>', methods=['GET'])
def get_matchups(week_number=None):
    if week_number is None:
        week_number = db.session.query(func.max(CurrentWeek.number)).scalar()

    game1 = aliased(GameData)
    game2 = aliased(GameData)
    game3 = aliased(GameData)
    team1 = aliased(TeamData)
    team2 = aliased(TeamData)
    team3 = aliased(TeamData)

    query = db.session.query(
        MatchupData,
        game1, game2, game3, 
        team1, team2, team3 
    ).join(
        game1, (MatchupData.team1Id == game1.teamId) & (game1.weekNumber == MatchupData.weekNumber), isouter=True
    ).join(
        team1, MatchupData.team1Id == team1.teamId
    ).join(
        game2, (MatchupData.team2Id == game2.teamId) & (game2.weekNumber == MatchupData.weekNumber), isouter=True
    ).join(
        team2, MatchupData.team2Id == team2.teamId
    ).join(
        game3, (MatchupData.team3Id == game3.teamId) & (game3.weekNumber == MatchupData.weekNumber), isouter=True
    ).join(
        team3, MatchupData.team3Id == team3.teamId
    ).filter(MatchupData.weekNumber == week_number)

    results = []
    scores = []
    proj = []
    for matchup, g1, g2, g3, t1, t2, t3 in query.all():
        results.append({
            "team1": {**t1.to_dict(), **(g1.to_dict() if g1 else {})},
            "team2": {**t2.to_dict(), **(g2.to_dict() if g2 else {})},
            "team3": {**t3.to_dict(), **(g3.to_dict() if g3 else {})}
        })

        scores.append(g1.totalPoints)
        scores.append(g2.totalPoints)
        scores.append(g3.totalPoints)

        proj.append(g1.projectedPoints)
        proj.append(g2.projectedPoints)
        proj.append(g3.projectedPoints)

    med = {
        'current': median(scores),
        'projected': median(proj)
    }
    return jsonify({'results':results, 'median': med, 'week': week_number})

@app.route('/scoreboard', methods=['GET'])
def get_scoreboard():
    query = text('''
        with wins as (
            select mt.* , 
            m.weekNumber, t.manager, t.teamName, g.totalPoints, g.projectedPoints ,
            ROW_NUMBER() OVER (PARTITION BY mt.matchupId ORDER BY g.totalPoints ASC) - 1 +
            IF(g.totalPoints > MEDIAN(g.totalPoints) OVER (PARTITION BY m.weekNumber), 1 , 0) as wins
            from matchupteam mt
            join team t on t.teamId = mt.teamId
            join matchup m on m.matchupId = mt.matchupId
                join game g on g.teamId = mt.teamId and m.weekNumber = g.weekNumber
                order by  weekNumber, matchupId
            )
            select sum(wins) as wins, sum(totalPoints) as totalPoints, teamName 
            from wins
            where weekNumber < (SELECT MAX(number) from currentweek)
            group by teamName ;
    ''')
    res = db.session.execute(query)
    keys = res.keys()

    results = res.fetchall()

    return jsonify(
        [dict(zip(keys, r)) for r in results]
    )
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)