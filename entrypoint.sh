#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${DJANGO_APP_DIR:-/app/cdcwaiv}"

echo "Applying database migrations..."
cd "$APP_DIR"
python manage.py migrate --noinput || true

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

echo "Starting app: $*"
exec "$@"
