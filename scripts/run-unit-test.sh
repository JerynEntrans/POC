#!/bin/bash
set -e

DB_HOST=${DATABASE_HOST}
DB_PORT=${DATABASE_PORT}
TIMEOUT=300
WAIT_INTERVAL=5
ELAPSED=0

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

# ✅ NEW: Wait for Flyway to complete
echo "⏳ Waiting for Flyway to finish migrations (via shared volume)..."
ELAPSED=0
TIMEOUT=300
WAIT_INTERVAL=5

while [ ! -f /flyway_status/.migrations_complete ]; do
  if [ "$ELAPSED" -ge "$TIMEOUT" ]; then
    >&2 echo "❌ Timed out after $TIMEOUT seconds waiting for Flyway to complete migrations"
    exit 1
  fi
  >&2 echo "🕑 Migrations not done yet - sleeping..."
  sleep $WAIT_INTERVAL
  ELAPSED=$((ELAPSED + WAIT_INTERVAL))
done

echo "✅ Migrations are complete"

# 🌱 Optional: Seed data
if [ "$CREATE_SEED_DATA" = "1" ]; then
  echo "🌱 Seeding initial data..."
  SEED_OUTPUT=$(python3 scripts/seed_data.py)
  echo "$SEED_OUTPUT"

  export SEEDED_TALONIFY_CASE_UUID=$(echo "$SEED_OUTPUT" | grep -oP 'talonify_case_uuid=\K[0-9a-fA-F-]+')

  echo "📌 Exported talonify_case_uuid: $SEEDED_TALONIFY_CASE_UUID"
fi

echo "✅ DB, migrations, and seed data are ready. Running tests..."
python -m pytest --durations=100 \
  --junitxml=/code/tests/report/pytest/test-results-junit.xml \
  --html=/code/tests/report/pytest/pytest_report.html \
  --self-contained-html \
  tests/
