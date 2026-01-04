#!/usr/bin/env bash
set -euo pipefail

echo "=== Applying database migrations ==="
python manage.py migrate --noinput

echo "=== Bootstrapping admin user (idempotent) ==="
python manage.py bootstrap_admin || true

echo "=== Starting ASGI server ==="
python -m gunicorn SurgeryStatusBoard.asgi:application \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:${PORT} \
  --workers ${WEB_CONCURRENCY:-2} \
  --log-level info


# so these scripts run when the start command is called for the render service, by applying migrations, bootstrapping an admin user, and starting the ASGI server with Gunicorn and Uvicorn.
# 