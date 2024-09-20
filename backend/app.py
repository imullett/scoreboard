from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import TeamData, GameData, MatchupData, CurrentWeek
from sqlalchemy.orm import aliased
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import func
from statistics import median
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from ingest_scores import ingest_scores
from ingest_teams import ingest_teams


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://ingestor:memesbowl123@db:3306/ff"
)

db = SQLAlchemy(app)

scheduler = BackgroundScheduler()
scheduler.add_job(ingest_scores,IntervalTrigger(minutes=15), next_run_time=None)

@app.route("/matchups", methods=["GET"])
@app.route("/matchups/<int:week_number>", methods=["GET"])
def get_matchups(week_number=None):
    if week_number is None:
        week_number = db.session.query(func.max(CurrentWeek.number)).scalar()

    game1 = aliased(GameData)
    game2 = aliased(GameData)
    game3 = aliased(GameData)
    team1 = aliased(TeamData)
    team2 = aliased(TeamData)
    team3 = aliased(TeamData)

    query = (
        db.session.query(MatchupData, game1, game2, game3, team1, team2, team3)
        .join(
            game1,
            (MatchupData.team1Id == game1.teamId)
            & (game1.weekNumber == MatchupData.weekNumber),
            isouter=True,
        )
        .join(team1, MatchupData.team1Id == team1.teamId)
        .join(
            game2,
            (MatchupData.team2Id == game2.teamId)
            & (game2.weekNumber == MatchupData.weekNumber),
            isouter=True,
        )
        .join(team2, MatchupData.team2Id == team2.teamId)
        .join(
            game3,
            (MatchupData.team3Id == game3.teamId)
            & (game3.weekNumber == MatchupData.weekNumber),
            isouter=True,
        )
        .join(team3, MatchupData.team3Id == team3.teamId)
        .filter(MatchupData.weekNumber == week_number)
    )

    results = []
    scores = []
    proj = []
    for matchup, g1, g2, g3, t1, t2, t3 in query.all():
        results.append(
            {
                "team1": {**t1.to_dict(), **(g1.to_dict() if g1 else {})},
                "team2": {**t2.to_dict(), **(g2.to_dict() if g2 else {})},
                "team3": {**t3.to_dict(), **(g3.to_dict() if g3 else {})},
            }
        )

        if g1 and g2 and g3:
            scores.append(g1.totalPoints)
            scores.append(g2.totalPoints)
            scores.append(g3.totalPoints)

            proj.append(g1.projectedPoints)
            proj.append(g2.projectedPoints)
            proj.append(g3.projectedPoints)

    med = {
        "current": median(scores) if scores else 0,
        "projected": median(proj) if proj else 0,
    }
    return jsonify({"results": results, "median": med, "week": week_number})


@app.route("/scoreboard", methods=["GET"])
def get_scoreboard():
    query = text("""
        WITH wins AS (
            SELECT m.weekNumber, t.*, g.totalPoints, g.projectedPoints,
            ROW_NUMBER() OVER (PARTITION BY mt.matchupId ORDER BY g.totalPoints ASC) - 1 +
            IF(g.totalPoints > MEDIAN(g.totalPoints) OVER (PARTITION BY m.weekNumber), 1, 0) AS wins
            FROM matchupteam mt
            JOIN team t ON t.teamId = mt.teamId
            JOIN matchup m ON m.matchupId = mt.matchupId
            JOIN game g ON g.teamId = mt.teamId AND m.weekNumber = g.weekNumber
            ORDER BY m.weekNumber, m.matchupId
        )
        SELECT SUM(wins) AS wins, SUM(totalPoints) AS totalPoints, teamName, division
        FROM wins
        WHERE weekNumber < (SELECT MAX(number) FROM currentweek)
        GROUP BY teamName, division;
    """)
    res = db.session.execute(query)
    keys = res.keys()

    results = res.fetchall()

    return jsonify([dict(zip(keys, r)) for r in results])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
