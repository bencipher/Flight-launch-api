FROM python:3.9

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

COPY . /tasks
WORKDIR /tasks

RUN pip install -U setuptools pip
RUN pip install -r requirements.txt
