#!/bin/bash
pwd
echo "Running teams backfill"
python -m lib.ingest_teams

echo "Running scores backfill"
python -m lib.ingest_scores --start_week=1

echo "Starting ingestor"
python -u -m ingestor.ingestor