FROM python:3
LABEL maintainer="Brian Goode <bjgoode.vt.edu>"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get -y update &&\
    apt-get -y upgrade &&\
    apt-get -y dist-upgrade

RUN apt-get -y install libsasl2-dev
RUN apt-get -y install libldap2-dev

RUN apt-get -y install nodejs npm
RUN echo '{"allow_root": true}' > /root/.bowerrc

COPY ./code/requirements.txt ./code/requirements.txt

RUN npm install bower

WORKDIR ./code

RUN pip install -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=documenter.settings.prod

COPY ./code .
COPY ./start_django.sh .

RUN chmod +x start_django.sh

EXPOSE 8000
