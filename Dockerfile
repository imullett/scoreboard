FROM python:3.10-slim

WORKDIR /app

COPY backend/ /app

RUN pip install -r requirements.txt

ENV FLASK_APP=app.py

EXPOSE 5000

RUN chmod +x /app/ingest_teams.py /app/ingest_scores.py /app/entry.sh

ENTRYPOINT ["/app/entry.sh"]