FROM python:3.6

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN ["chmod", "+x", "/entrypoint.sh"]

WORKDIR /home/web/codes
# COPY . /code/
# WORKDIR /code/codes
# RUN chown -R celery:celery celerybeat

EXPOSE 8040