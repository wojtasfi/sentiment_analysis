FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /sentiment_analysis

WORKDIR /sentiment_analysis

ADD . /sentiment_analysis/

RUN pip install -r requirements.txt