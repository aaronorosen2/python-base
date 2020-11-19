FROM ubuntu:xenial

ENV PYTHONIOENCODING=utf-8

RUN apt-get update --fix-missing
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

RUN apt-get install -y locales
RUN apt-get install -y ffmpeg
RUN apt-get install -y libav-tools
RUN pip3 install --upgrade pip

COPY ./requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN ["chmod", "+x", "/entrypoint.sh"]

WORKDIR /home/web/codes

