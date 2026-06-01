#!/bin/sh

set -e

echo "Waiting for database..."
while ! nc -z db 5432; do
    sleep 0.1
done
echo "Database started"

echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Collecting fixed data and static files..."
python manage.py loaddata fixtures/users.json
python manage.py loaddata fixtures/categories.json
python manage.py loaddata fixtures/offers.json
python manage.py loaddata fixtures/offers_media.json
python manage.py loaddata fixtures/deals.json
python manage.py collectstatic --noinput

exec "$@"
