#!/usr/bin/env bash
# Verifies: health checks, frontend->backend proxy, PostgreSQL persistence across
# container removal/recreation, and Redis restart.
# Usage: bash scripts/verify-persistence.sh [compose-file]
set -euo pipefail

COMPOSE_FILE="${1:-docker-compose.deploy.yml}"
API="${API_URL:-http://localhost:3000}"
WEB="${WEB_URL:-http://localhost:8080}"
dc() { docker compose -f "$COMPOSE_FILE" "$@"; }

wait_healthy() {
  local svc="$1" cid status
  for _ in $(seq 1 40); do
    cid="$(dc ps -q "$svc" 2>/dev/null || true)"
    status="missing"
    if [ -n "$cid" ]; then
      status="$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' "$cid" 2>/dev/null || echo missing)"
    fi
    if [ "$status" = "healthy" ]; then echo "[ok] $svc is healthy"; return 0; fi
    sleep 3
  done
  echo "[fail] $svc did not become healthy"; dc logs --no-color --tail 50 "$svc" || true
  return 1
}

wait_api() {
  for _ in $(seq 1 40); do
    if curl -fsS "$API/health" > /dev/null 2>&1; then echo "[ok] backend /health responding"; return 0; fi
    sleep 3
  done
  echo "[fail] backend /health not responding"; dc logs --no-color --tail 50 backend || true
  return 1
}

token_for() {
  curl -fsS -X POST "$API/api/auth/login" -H 'Content-Type: application/json' \
    -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}" | sed -n 's/.*"token":"\([^"]*\)".*/\1/p'
}

echo "== 1. Health checks =="
wait_healthy postgres
wait_healthy redis
wait_healthy backend
curl -fsS "$API/health" | grep -q '"postgres":"ok"' && curl -fsS "$API/health" | grep -q '"redis":"ok"'
echo "[ok] backend reports postgres=ok redis=ok (service-name resolution works)"

echo "== 2. Frontend -> backend =="
curl -fsS "$WEB/" > /dev/null
curl -fsS "$WEB/health" | grep -q '"status":"ok"'
echo "[ok] frontend serves UI and proxies to backend"

echo "== 3. Create data =="
STAMP="$(date +%s)"
EMAIL="persist-${STAMP}@example.com"
PASSWORD="persist-check-${STAMP}"
TITLE="persistence-check-${STAMP}"
curl -fsS -X POST "$API/api/auth/register" -H 'Content-Type: application/json' \
  -d "{\"name\":\"Persist Check\",\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}" > /dev/null
TOKEN="$(token_for)"
test -n "$TOKEN"
curl -fsS -X POST "$API/api/tasks" -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d "{\"title\":\"$TITLE\",\"description\":\"survives container recreation\"}" > /dev/null
echo "[ok] user and task created"

echo "== 4. Remove and recreate PostgreSQL container =="
dc rm -sf postgres
dc up -d postgres
wait_healthy postgres
dc up -d
wait_api
dc exec -T redis redis-cli FLUSHALL > /dev/null   # clear cache so data must come from PostgreSQL
TOKEN="$(token_for)"
test -n "$TOKEN"
RESP="$(curl -fsS "$API/api/tasks" -H "Authorization: Bearer $TOKEN")"
echo "$RESP" | grep -q "$TITLE"
echo "$RESP" | grep -q '"source":"postgres"'
echo "[ok] data persisted in named volume after PostgreSQL container recreation"

echo "== 5. Restart Redis =="
dc restart redis
wait_healthy redis
wait_api
dc exec -T redis redis-cli ping | grep -q PONG
curl -fsS "$API/health" | grep -q '"redis":"ok"'
echo "[ok] Redis restarted and backend reconnected"

echo "ALL CHECKS PASSED"
