#!/usr/bin/env sh

RUNSERVER_BIND_HOST=0.0.0.0
RUNSERVER_BIND_PORT=8000

# Apply migrations
python manage.py migrate

# Run development server
python manage.py runserver $RUNSERVER_BIND_HOST:$RUNSERVER_BIND_PORT
