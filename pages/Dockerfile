FROM ubuntu:latest

WORKDIR /usr/app/src

ARG LANG="en_US.UTF-8"

#downloads and installations

RUN apt-get update\ && apt-get install -y --no-install-recommends \apt -utils \
locales \
python3-pip \
python3-yaml \
rsyslog systemd systemd-cron sudo \ && apt-get clean


COPY requirements.txt ./
RUN pip3 install --upgrade pip \ && pip3 intsall -r requirements.txt

COPY ./ ./

CMD ["streamlit","run","🏠home.py"]