#!/bin/bash
set -e

if [ "$RUN_MIGRATIONS" != "1" ]; then
  echo "RUN_MIGRATIONS is not set to 1. Skipping Flyway migration."
  exit 0
fi

echo "Waiting for Postgres to be reachable by Flyway..."

until flyway \
  -url=jdbc:postgresql://${DATABASE_HOST}:5432/${POSTGRES_DB} \
  -user=${POSTGRES_USER} \
  -password=${POSTGRES_PASSWORD} \
  info > /dev/null 2>&1; do
  echo "Postgres not ready... retrying..."
  sleep 2
done

echo "Postgres is reachable!"

echo "Checking if Flyway schema history table exists..."

FLYWAY_OUTPUT=$(flyway \
  -X \
  -url=jdbc:postgresql://${DATABASE_HOST}:5432/${POSTGRES_DB} \
  -user=${POSTGRES_USER} \
  -password=${POSTGRES_PASSWORD} \
  -defaultSchema=${SCHEMA_NAME:-public} \
  info 2>&1)

if echo "$FLYWAY_OUTPUT" | grep -q "Found non-empty schema(s).*but no schema history table"; then
  echo "Non-empty schema without history detected. Running migrate with -baselineOnMigrate=true"
  flyway \
    -X \
    -url=jdbc:postgresql://${DATABASE_HOST}:5432/${POSTGRES_DB} \
    -user=${POSTGRES_USER} \
    -password=${POSTGRES_PASSWORD} \
    -defaultSchema=${SCHEMA_NAME:-public} \
    -baselineOnMigrate=true \
    migrate
else
  echo "Running regular Flyway migrate"
  flyway \
    -X \
    -url=jdbc:postgresql://${DATABASE_HOST}:5432/${POSTGRES_DB} \
    -user=${POSTGRES_USER} \
    -password=${POSTGRES_PASSWORD} \
    -defaultSchema=${SCHEMA_NAME:-public} \
    migrate
fi

touch /flyway_status/.migrations_complete
