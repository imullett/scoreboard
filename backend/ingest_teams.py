from yfpy.query import YahooFantasySportsQuery
from models import TeamData
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

league_id = '790777'

def ingest_teams():
    query = YahooFantasySportsQuery(
        auth_dir='secrets',
        league_id=league_id,
        game_code='nfl',
    )
    teams = query.get_league_teams()

    engine = create_engine('mysql+pymysql://ingestor:memesbowl123@db:3306/ff')

    with Session(engine) as session:
        print('Ingesting teams...')
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

if __name__ == '__main__':
    ingest_teams()