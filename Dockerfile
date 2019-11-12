FROM python:3
LABEL maintainer="Brian Goode <bjgoode.vt.edu>"

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update &&\
    apt-get -y upgrade &&\
    apt-get -y dist-upgrade

RUN apt-get -y install nodejs npm
RUN echo '{"allow_root": true}' > /root/.bowerrc

COPY ./code .

RUN npm install bower

RUN pip install -r requirements.txt



RUN ./manage.py bower_install
RUN ./manage.py migrate
RUN ./manage.py collectstatic

EXPOSE 8000
