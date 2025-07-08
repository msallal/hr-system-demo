#!/bin/bash

set -e

echo "=== Django Entrypoint ==="

# Wait for database
sleep 10

# Run migrations
python manage.py migrate --noinput
echo "Migrations completed!"

# Collect static files
#python manage.py collectstatic --noinput --clear

# Start Gunicorn instead of development server
echo "=== Starting Django Development Server ==="
exec "$@"