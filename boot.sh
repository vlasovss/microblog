#!/bin/sh
source venv/bin/activate
flask db upgrade
flask translate compile
flask elastic reindex post
exec gunicorn -b :5000 --access-logfile - --error-logfile - microblog:app