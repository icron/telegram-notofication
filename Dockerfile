FROM arbuscula/flask-spacy-nltk:python3.8-alpine

COPY ./app /app
COPY ./app/supervisor-cli.ini /etc/supervisor.d/supervisor-cli.ini
COPY ./app/static /app/static