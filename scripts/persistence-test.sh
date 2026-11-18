#!/bin/bash
set -e

echo "Testing PostgreSQL persistence..."
docker compose exec -T postgres psql -U taskflow_user -d taskflow -c "INSERT INTO users (name, email, password_hash) VALUES ('Persistence Test', 'persist@test.com', 'hash123') ON CONFLICT (email) DO NOTHING;"

echo "Restarting PostgreSQL container..."
docker compose stop postgres
docker compose rm -f postgres
docker compose up -d postgres

for i in $(seq 1 30); do
  if docker compose exec -T postgres pg_isready -U taskflow_user -d taskflow > /dev/null 2>&1; then
    echo "PostgreSQL is ready"
    break
  fi
  sleep 1
done

COUNT=$(docker compose exec -T postgres psql -U taskflow_user -d taskflow -t -A -c "SELECT COUNT(*) FROM users WHERE email='persist@test.com';")
if [ "$COUNT" -ge 1 ]; then
  echo "✓ Data persistence verified successfully: record exists after container recreation."
else
  echo "✗ Data persistence failed!"
  exit 1
fi
