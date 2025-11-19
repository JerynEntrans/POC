#!/bin/bash
set -e

DB_HOST=${DATABASE_HOST:-localhost}
DB_PORT=${DATABASE_PORT:-5432}
WAIT_FOR_DB=${WAIT_FOR_DB:-false}

TIMEOUT=300
WAIT_INTERVAL=5
ELAPSED=0

if [ "$WAIT_FOR_DB" == "true" ]; then
  echo "⏳ Waiting for Postgres at $DB_HOST:$DB_PORT (timeout: $TIMEOUT seconds)..."
  until nc -z "$DB_HOST" "$DB_PORT"; do
    if [ "$ELAPSED" -ge "$TIMEOUT" ]; then
      >&2 echo "❌ Timed out after $TIMEOUT seconds waiting for Postgres at $DB_HOST:$DB_PORT"
      exit 1
    fi
    >&2 echo "🕑 Postgres is unavailable - sleeping..."
    sleep $WAIT_INTERVAL
    ELAPSED=$((ELAPSED + WAIT_INTERVAL))
  done
  echo "✅ Postgres is up!"
else
  echo "⚠️ Skipping Postgres wait as WAIT_FOR_DB is set to '$WAIT_FOR_DB'"
fi

echo "🚀 Starting FastAPI with Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
