#!/bin/bash
set -e

if [ -n "$DATABASE_URL" ]; then
	python manage.py migrate --noinput
fi

python manage.py collectstatic --noinput
