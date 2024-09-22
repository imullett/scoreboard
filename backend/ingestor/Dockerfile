FROM python:3.10-slim

WORKDIR /app

COPY ./ingestor/ ./ingestor
COPY ./lib/ ./lib
COPY ./ingestor/requirements.txt .

RUN pip install -r requirements.txt

RUN mv /app/ingestor/entry.sh /app
RUN ls -l
RUN chmod +x /app/lib/ingest_teams.py /app/lib/ingest_scores.py /app/entry.sh

ENTRYPOINT [ "/app/entry.sh" ]

