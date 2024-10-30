FROM python:3.10-bookworm

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN pip install --upgrade pip
RUN pip install pip-tools
