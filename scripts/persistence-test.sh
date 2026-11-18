#!/usr/bin/env bash
set -e

echo "Testing PostgreSQL persistence..."

# Stop and remove the postgres container
docker compose stop postgres
docker compose rm -f postgres

# Recreate and start postgres container
docker compose up -d postgres

# Wait for healthy
echo "Waiting for postgres to become healthy..."
for attempt in $(seq 1 30); do
  if docker compose ps postgres | grep -q "healthy"; then
    echo "Postgres is healthy"
    break
  fi
  sleep 2
done

# Verify database connection and tables
docker compose exec -T postgres psql -U taskflow_user -d taskflow -c "SELECT COUNT(*) FROM users;"
echo "PostgreSQL persistence test passed successfully."
