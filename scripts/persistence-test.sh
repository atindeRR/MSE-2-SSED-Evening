#!/bin/bash
set -e

echo "=== Running PostgreSQL Persistence Test ==="

DB_USER="${POSTGRES_USER:-taskflow_user}"
DB_NAME="${POSTGRES_DB:-taskflow}"

# Insert test record into PostgreSQL container
echo "Inserting test record into database..."
docker compose exec -T postgres psql -U "$DB_USER" -d "$DB_NAME" -c "
  CREATE TABLE IF NOT EXISTS _persistence_check (
    id INT PRIMARY KEY,
    marker TEXT NOT NULL
  );
  INSERT INTO _persistence_check (id, marker)
  VALUES (1, 'persistence_verified')
  ON CONFLICT (id) DO UPDATE SET marker = EXCLUDED.marker;
"

# Restart PostgreSQL container
echo "Restarting PostgreSQL container..."
docker compose stop postgres
docker compose start postgres

# Wait for PostgreSQL to become healthy
echo "Waiting for PostgreSQL to restart..."
for i in $(seq 1 30); do
  if docker compose exec -T postgres pg_isready -U "$DB_USER" -d "$DB_NAME" > /dev/null 2>&1; then
    echo "PostgreSQL is ready."
    break
  fi
  sleep 2
done

# Verify data persisted across container restart
echo "Verifying test record persists..."
RECORD=$(docker compose exec -T postgres psql -U "$DB_USER" -d "$DB_NAME" -tAc "SELECT marker FROM _persistence_check WHERE id = 1;" | tr -d '\r\n')

if [ "$RECORD" = "persistence_verified" ]; then
  echo "✓ PostgreSQL Persistence Test Passed: Data persisted across container restart."
  exit 0
else
  echo "✗ PostgreSQL Persistence Test Failed: Marker not found (got: '$RECORD')."
  exit 1
fi
