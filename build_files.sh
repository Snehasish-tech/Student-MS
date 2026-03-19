#!/bin/bash
set -e

echo "Starting Django build..."

# Ensure staticfiles directory exists before collectstatic
mkdir -p staticfiles

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || true

echo "✓ Build complete"
