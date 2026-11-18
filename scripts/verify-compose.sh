#!/usr/bin/env bash
# Reproducible networking, health, and PostgreSQL-volume persistence verification.
# Run from the repository root after copying .env.example to .env and setting real values.
set -euo pipefail

compose=(docker compose)

"${compose[@]}" up -d
"${compose[@]}" ps

echo 'Checking frontend-to-backend reverse proxy:'
curl --fail --silent http://localhost:8080/health
echo

echo 'Checking backend health and its PostgreSQL/Redis connectivity:'
curl --fail --silent http://localhost:3000/health
echo

echo 'Inspecting the custom bridge network:'
docker network inspect taskflow_taskflow-network

echo 'Checking PostgreSQL and Redis directly:'
"${compose[@]}" exec -T postgres sh -c 'pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
"${compose[@]}" exec -T redis redis-cli ping

marker="persistence-$(date +%s)"
echo "Inserting persistence marker: $marker"
"${compose[@]}" exec -T postgres sh -c 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "CREATE TABLE IF NOT EXISTS persistence_checks (marker TEXT PRIMARY KEY);"'
"${compose[@]}" exec -T postgres sh -c "psql -v ON_ERROR_STOP=1 -U \"\$POSTGRES_USER\" -d \"\$POSTGRES_DB\" -c \"INSERT INTO persistence_checks (marker) VALUES ('$marker');\""
"${compose[@]}" exec -T postgres sh -c "psql -U \"\$POSTGRES_USER\" -d \"\$POSTGRES_DB\" -c \"SELECT marker FROM persistence_checks WHERE marker = '$marker';\""

echo 'Recreating only the PostgreSQL container; the named volume is retained.'
"${compose[@]}" rm -sf postgres
"${compose[@]}" up -d postgres
until [ "$("${compose[@]}" inspect -f '{{.State.Health.Status}}' postgres 2>/dev/null || true)" = 'healthy' ]; do sleep 2; done
"${compose[@]}" exec -T postgres sh -c "psql -U \"\$POSTGRES_USER\" -d \"\$POSTGRES_DB\" -c \"SELECT marker FROM persistence_checks WHERE marker = '$marker';\""

echo 'Restarting Redis and confirming it returns PONG:'
"${compose[@]}" restart redis
"${compose[@]}" exec -T redis redis-cli ping

echo 'Verification complete. No docker compose down -v command was used.'
