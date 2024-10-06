python3 -m venv .venv 
source ./.venv/bin/activate
pip3 install -r requirements.txt



alembic
backports-abc
blinker
click
Flask
Flask-Bootstrap
Flask-Login
Flask-Mail
Flask-Migrate
Flask-Moment
Flask-Script
Flask-SQLAlchemy
Flask-WTF
mysqlclient
itsdangerous
Jinja2
livereload
Mako
MarkupSafe
meld3
python-editor
singledispatch
six
gunicorn
SQLAlchemy
supervisor
tornado
uWSGI
Werkzeug


mysqlclient
pycrypto
PyMySQL
redis
requests
shellescape
simplejson



# Dockerfile:

FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /base_directory
WORKDIR /base_directory
ADD . /base_directory/
RUN apt-get update
RUN apt-get install -y git
RUN git init
RUN apt-get install -y gcc python3-dev
RUN apt-get install -y libxml2-dev libxslt1-dev build-essential python3-lxml zlib1g-dev
RUN apt-get install -y default-mysql-client default-libmysqlclient-dev
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN  python3 get-pip.py
RUN rm get-pip.py
RUN pip install -r requirements.txt
CMD start.sh


#!/bin/bash
nohup redis-server &
uwsgi --http localhost:8000 --module mymodule.wsgi