#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Only run migrations if DATABASE_URL is set (production)
if [ -n "$DATABASE_URL" ]; then
    echo "Running database migrations..."
    python manage.py migrate --noinput
else
    echo "DATABASE_URL not set - skipping migrations (local development)"
fi

echo "Build complete!"
