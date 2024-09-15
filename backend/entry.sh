#!/bin/bash
echo "Running teams backfill"
python /app/ingest_teams.py

# Run second script: ingest_scores.py with argument
echo "Running scores backfill"
python /app/ingest_scores.py --start_week=1

flask run --host=0.0.0.0