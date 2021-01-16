#!/bin/sh
python3 /home/web/codes/manage.py makemigrations
python3 /home/web/codes/manage.py migrate
exec "$@"
