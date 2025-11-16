#!/usr/bin/env sh
set -e

echo "Waiting for Postgres at ${POSTGRES_HOST}:${POSTGRES_PORT}..."
until python - <<'PYCODE'
import os
import psycopg2
import time
host = os.environ.get("POSTGRES_HOST", "db")
port = int(os.environ.get("POSTGRES_PORT", "5432"))
db = os.environ.get("POSTGRES_DB", "qa_db")
user = os.environ.get("POSTGRES_USER", "qa_user")
password = os.environ.get("POSTGRES_PASSWORD", "qa_password")
try:
    psycopg2.connect(host=host, port=port, dbname=db, user=user, password=password)
except Exception:
    raise SystemExit(1)
else:
    raise SystemExit(0)
PYCODE
do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Running migrations..."
python manage.py migrate --noinput

exec "$@"

