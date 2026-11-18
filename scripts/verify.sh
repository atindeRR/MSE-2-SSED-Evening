#!/usr/bin/env bash
# Task 5: networking and persistence checks. Run after the stack is up.
# Usage: bash scripts/verify.sh                          (uses docker-compose.yml)
#        bash scripts/verify.sh docker-compose.deploy.yml
set -euo pipefail
FILE="${1:-docker-compose.yml}"
dc() { docker compose -f "$FILE" "$@"; }
set -a; [ -f .env ] && . ./.env; set +a
PGUSER="${POSTGRES_USER:-taskflow_user}"; PGDB="${POSTGRES_DB:-taskflow}"

wait_healthy() {
  for _ in $(seq 1 40); do
    s=$(docker inspect --format '{{.State.Health.Status}}' "$(dc ps -q "$1")" 2>/dev/null || true)
    [ "$s" = "healthy" ] && { echo "$1 is healthy"; return 0; }
    sleep 3
  done
  echo "$1 did not become healthy"; return 1
}

echo "== 6. Health status of containers =="
dc ps
for c in $(dc ps -q); do docker inspect --format '{{.Name}}: {{.State.Health.Status}}' "$c"; done

echo; echo "== Custom network =="
docker network inspect "$(docker inspect --format '{{range $k,$v := .NetworkSettings.Networks}}{{$k}}{{end}}' "$(dc ps -q backend)")" \
  --format '{{.Name}} ({{.Driver}}): {{range .Containers}}{{.Name}} {{end}}'

echo; echo "== 1. Frontend -> backend (nginx proxy) =="
curl -fsS http://localhost:8080/health; echo
dc exec -T frontend wget -qO- http://backend:3000/health; echo

echo; echo "== 2/3. Backend resolves postgres and redis by service name =="
dc exec -T backend node -e "const d=require('dns');for(const h of ['postgres','redis'])d.lookup(h,(e,a)=>console.log(h,'->',e?e.message:a))"
curl -fsS http://localhost:3000/health; echo

echo; echo "== 4. PostgreSQL persistence across container removal =="
MARK="persist-$(date +%s)"
dc exec -T postgres psql -U "$PGUSER" -d "$PGDB" -c \
  "CREATE TABLE IF NOT EXISTS persistence_check(v TEXT); INSERT INTO persistence_check VALUES ('$MARK');"
dc rm -s -f postgres
dc up -d postgres
wait_healthy postgres
dc exec -T postgres psql -U "$PGUSER" -d "$PGDB" -tAc "SELECT v FROM persistence_check WHERE v='$MARK';" | grep -q "$MARK" \
  && echo "PASS: row '$MARK' survived container recreation" || { echo "FAIL: data lost"; exit 1; }

echo; echo "== 5. Redis restart =="
dc restart redis
wait_healthy redis
dc exec -T redis redis-cli ping

echo; echo "== Backend still healthy after restarts =="
wait_healthy backend
curl -fsS http://localhost:3000/health; echo
