from yfpy.query import YahooFantasySportsQuery
from models import GameData, CurrentWeek
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

query = YahooFantasySportsQuery(
    './secrets',
    # '730448',
    '790777',
    'nfl',
    #  game_id=423,
)

current_week = query.get_league_metadata().current_week 

teams = query.get_league_teams()

engine = create_engine('mysql+pymysql://ingestor:memesbowl123@localhost:3306/ff')

with Session(engine) as session:
    for team in teams:
        game = GameData(
            teamId=team.team_id,
            weekNumber=current_week
        )
        data = query.get_team_stats_by_week(team.team_id, current_week)
        game.projectedPoints = data['team_projected_points'].total
        game.totalPoints = data['team_points'].total
        session.merge(game)

    session.merge(CurrentWeek(id=1,number=current_week)) 
    session.commit()