#!/bin/bash

./manage.py bower install
./manage.py collectstatic --noinput
./manage.py migrate

gunicorn documenter.wsgi:application -b 0.0.0.0:8000 --workers=10
