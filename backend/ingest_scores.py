from yfpy.query import YahooFantasySportsQuery
from models import GameData, CurrentWeek
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from argparse import ArgumentParser

league_id = '790777'

def ingest_scores(start_week):
    query = YahooFantasySportsQuery(
        auth_dir='secrets',
        league_id=league_id,
        game_code='nfl',
    )
    current_week = query.get_league_metadata().current_week 

    if start_week is None:
        start_week = current_week

    teams = query.get_league_teams()

    engine = create_engine('mysql+pymysql://ingestor:memesbowl123@db:3306/ff')

    with Session(engine) as session:
        print(f'Ingesting scores from ${start_week} to {current_week}...')
        for week in range(start_week, current_week + 1):
            for team in teams:
                game = GameData(
                    teamId=team.team_id,
                    weekNumber=week
                )
                data = query.get_team_stats_by_week(team.team_id, week)
                game.projectedPoints = data['team_projected_points'].total
                game.totalPoints = data['team_points'].total
                session.merge(game)

        session.merge(CurrentWeek(id=1,number=current_week)) 
        session.commit()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--start_week', type=int)
    
    args = parser.parse_args()

    ingest_scores(args.start_week)