FROM python:3.9.4-slim-buster

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["./run.sh"]
