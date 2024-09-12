from yfpy.query import YahooFantasySportsQuery
from models import GameData, TeamData
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

query = YahooFantasySportsQuery(
    './secrets',
    # '730448',
    '790777',
    'nfl',
    #  game_id=423,
)
teams = query.get_league_teams()

engine = create_engine('mysql+pymysql://ingestor:memesbowl123@localhost:3306/ff')

with Session(engine) as session:
    for team in teams:
        t = TeamData(
            teamId = team.team_id,
            teamName=team.name.decode('UTF-8'),
            yahooId=team.team_key,
            profilePicture=team.team_logos[0].url,
            manager=team.managers[0].nickname
        )
        session.merge(t)
        
    session.commit()