#!/usr/bin/env bash
# Task 5 verification: networking, health checks and PostgreSQL persistence.
# Usage: ./scripts/verify.sh [docker-compose.yml|docker-compose.deploy.yml]
set -euo pipefail

cd "$(dirname "$0")/.."

COMPOSE_FILE="${1:-docker-compose.yml}"
PROJECT="taskflow"
BASE_URL="${BASE_URL:-http://localhost:8080}"
PG_USER="${POSTGRES_USER:-taskflow_user}"
PG_DB="${POSTGRES_DB:-taskflow}"
EVIDENCE_DIR="${EVIDENCE_DIR:-evidence}"

mkdir -p "$EVIDENCE_DIR"
LOG="$EVIDENCE_DIR/task5-verification.log"
exec > >(tee -a "$LOG") 2>&1

compose() { docker compose -p "$PROJECT" -f "$COMPOSE_FILE" "$@"; }

step() { printf '\n===== %s =====\n' "$*"; }

container_of() { compose ps -q "$1"; }

wait_for_healthy() {
  local service="$1" attempts="${2:-60}" status
  for _ in $(seq 1 "$attempts"); do
    status="$(docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "$(container_of "$service")" 2>/dev/null || echo unknown)"
    if [ "$status" = "healthy" ]; then
      printf '%s is healthy\n' "$service"
      return 0
    fi
    sleep 2
  done
  printf '%s did not become healthy (last status: %s)\n' "$service" "$status" >&2
  return 1
}

login_token() {
  curl -fsS -X POST "$BASE_URL/api/auth/login" \
    -H 'Content-Type: application/json' \
    -d "{\"email\":\"$1\",\"password\":\"$2\"}" |
    python3 -c 'import json,sys; print(json.load(sys.stdin)["token"])'
}

step "Service status"
compose ps

step "1. Frontend can communicate with the backend (Nginx proxy)"
curl -fsS "$BASE_URL/health"; echo
curl -fsS "$BASE_URL/" | grep -o '<title>[^<]*</title>'

step "2. Backend resolves and connects to PostgreSQL by service name"
compose exec -T backend node --input-type=module -e "
import dns from 'node:dns/promises';
import net from 'node:net';
const addresses = await dns.lookup('postgres', { all: true });
console.log('DNS postgres ->', addresses.map(a => a.address).join(', '));
await new Promise((resolve, reject) => {
  const socket = net.connect({ host: 'postgres', port: 5432 }, () => { socket.end(); resolve(); });
  socket.on('error', reject);
});
console.log('TCP postgres:5432 reachable from backend');
"

step "3. Backend resolves and connects to Redis by service name"
compose exec -T backend node --input-type=module -e "
import dns from 'node:dns/promises';
import net from 'node:net';
const addresses = await dns.lookup('redis', { all: true });
console.log('DNS redis ->', addresses.map(a => a.address).join(', '));
await new Promise((resolve, reject) => {
  const socket = net.connect({ host: 'redis', port: 6379 }, () => { socket.end(); resolve(); });
  socket.on('error', reject);
});
console.log('TCP redis:6379 reachable from backend');
"

step "4. PostgreSQL data persists across container removal and recreation"
EMAIL="verify-$(date +%s)@example.com"
PASSWORD="student123"
TASK_TITLE="Persistence check $(date +%s)"

curl -fsS -X POST "$BASE_URL/api/auth/register" -H 'Content-Type: application/json' \
  -d "{\"name\":\"Verification User\",\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}" > /dev/null
TOKEN="$(login_token "$EMAIL" "$PASSWORD")"
curl -fsS -X POST "$BASE_URL/api/tasks" -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"title\":\"$TASK_TITLE\",\"description\":\"must survive postgres recreation\"}" > /dev/null

echo "Rows in PostgreSQL before removal:"
compose exec -T postgres psql -U "$PG_USER" -d "$PG_DB" -tAc \
  "SELECT id || ' | ' || title FROM tasks WHERE title = '$TASK_TITLE';"

echo "Removing the PostgreSQL container (volume is kept):"
compose rm -sf postgres
echo "Recreating the PostgreSQL container:"
compose up -d postgres
wait_for_healthy postgres

echo "Rows in PostgreSQL after recreation:"
compose exec -T postgres psql -U "$PG_USER" -d "$PG_DB" -tAc \
  "SELECT id || ' | ' || title FROM tasks WHERE title = '$TASK_TITLE';"

for _ in $(seq 1 30); do
  if curl -fsS "$BASE_URL/health" > /dev/null; then break; fi
  sleep 2
done
TOKEN="$(login_token "$EMAIL" "$PASSWORD")"
echo "Tasks returned by the API after recreation:"
curl -fsS "$BASE_URL/api/tasks" -H "Authorization: Bearer $TOKEN" |
  python3 -c 'import json,sys; print(json.dumps([t["title"] for t in json.load(sys.stdin)["tasks"]], indent=2))'

step "5. Redis service can be restarted successfully"
compose restart redis
wait_for_healthy redis
compose exec -T redis redis-cli ping
curl -fsS "$BASE_URL/health"; echo

step "6. Health checks report service status"
docker ps --filter "name=${PROJECT}-" \
  --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'

step "Custom network configuration"
docker network inspect "${PROJECT}-net" \
  --format '{{range $id, $c := .Containers}}{{$c.Name}} {{end}}'

step "PostgreSQL named volume"
docker volume inspect "${PROJECT}_postgres_data" \
  --format '{{.Name}} -> {{.Mountpoint}}'

echo
echo "Task 5 verification finished successfully."
