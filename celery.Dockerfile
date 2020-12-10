FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt


COPY . /code/
WORKDIR /code/codes
# RUN chown -R celery:celery celerybeat

EXPOSE 8040