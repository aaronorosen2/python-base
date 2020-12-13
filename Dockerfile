FROM python:3.6

ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENV PYTHONIOENCODING=utf-8

COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN ["chmod", "+x", "/entrypoint.sh"]

WORKDIR /home/web/codes
# COPY . /code/
# WORKDIR /code/codes
# RUN chown -R celery:celery celerybeat

EXPOSE 8040
# FROM ubuntu:xenial
# FROM ubuntu:latest
# ENV TZ=Europe/Kiev
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
#
# ENV PYTHONIOENCODING=utf-8
#
# RUN apt-get update --fix-missing
# # RUN apt-get install -y software-properties-common
# # RUN add-apt-repository ppa:deadsnakes/ppa
#
# RUN apt-get update --fix-missing
# RUN apt-get install -y python3
# RUN apt-get install -y python3-pip
#
# RUN apt-get install -y locales
# RUN apt-get install -y ffmpeg
# # RUN apt-get install -y libav-tools
# RUN pip3 install --upgrade pip
#
# COPY ./requirements.txt /tmp/requirements.txt
#
# RUN pip3 install -r /tmp/requirements.txt
#
# COPY entrypoint.sh /entrypoint.sh
# RUN ["chmod", "+x", "/entrypoint.sh"]
#
# WORKDIR /home/web/codes




