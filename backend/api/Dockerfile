FROM python:3.10-slim

WORKDIR /app

COPY ./api/ ./api
COPY ./lib/ ./lib

RUN pip install -r api/requirements.txt

ENV FLASK_APP=app.py

EXPOSE 5000


# ENTRYPOINT ["/app/entry.sh"]
CMD ["python", "-u", "-m", "api.app"]