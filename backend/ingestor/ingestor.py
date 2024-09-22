from apscheduler.schedulers.blocking import BlockingScheduler
from lib.ingest_teams import ingest_teams
from lib.ingest_scores import ingest_scores

# Run backfills on startup
ingest_teams()
ingest_scores(start_week=1)

scheduler = BlockingScheduler()
scheduler.add_job(
    func=ingest_teams,
    trigger='interval',
    days=7,
    id='ingest_teams',
)

scheduler.add_job(
    func=ingest_scores,
    trigger='interval',
    minutes=5,
    id='ingest_scores',
)

scheduler.start()