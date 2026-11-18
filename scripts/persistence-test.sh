#!/usr/bin/env bash
set -e

echo "=== Testing PostgreSQL Data Persistence ==="

# 1. Insert an evaluation persistence test record
docker compose exec -T postgres psql -U taskflow_user -d taskflow -c "
  CREATE TABLE IF NOT EXISTS _ci_persistence_check (
    id SERIAL PRIMARY KEY,
    marker VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
  );
  INSERT INTO _ci_persistence_check (marker) VALUES ('ci_test_marker');
"

# 2. Restart PostgreSQL container without deleting volumes
echo "Restarting PostgreSQL container..."
docker compose restart postgres

# 3. Wait for PostgreSQL to become healthy again
echo "Waiting for PostgreSQL to be ready..."
for i in $(seq 1 30); do
  if docker compose exec -T postgres pg_isready -U taskflow_user -d taskflow; then
    echo "PostgreSQL is ready."
    break
  fi
  sleep 1
done

# 4. Verify the test record still exists
echo "Verifying test record survived container restart..."
RECORD_COUNT=$(docker compose exec -T postgres psql -U taskflow_user -d taskflow -t -A -c "SELECT COUNT(*) FROM _ci_persistence_check WHERE marker = 'ci_test_marker';")

echo "Found $RECORD_COUNT persisted record(s)."

if [ "$RECORD_COUNT" -ge 1 ]; then
  echo "PostgreSQL persistence verification PASSED!"
  # Clean up test table
  docker compose exec -T postgres psql -U taskflow_user -d taskflow -c "DROP TABLE IF EXISTS _ci_persistence_check;"
  exit 0
else
  echo "PostgreSQL persistence verification FAILED: Record was not found after restart."
  exit 1
fi
