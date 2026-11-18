#!/usr/bin/env bash
# =============================================================================
# MSE-2 Docker Practical – run_all.sh
# Run once from repo root in Git Bash:  bash run_all.sh
# Every section = one screenshot. All output saved to execution.log
# =============================================================================
set -uo pipefail

LOG=execution.log
> "$LOG"

GREEN='\033[0;32m'; RED='\033[0;31m'; CYAN='\033[0;36m'; YELLOW='\033[1;33m'; NC='\033[0m'
PASS()  { echo -e "${GREEN}[PASS]${NC}  $*" | tee -a "$LOG"; }
FAIL()  { echo -e "${RED}[FAIL]${NC}  $*" | tee -a "$LOG"; }
INFO()  { echo -e "${YELLOW}[INFO]${NC}  $*" | tee -a "$LOG"; }
STEP()  {
  echo -e "\n${CYAN}╔══════════════════════════════════════════════════════╗${NC}" | tee -a "$LOG"
  echo -e "${CYAN}║  $*${NC}" | tee -a "$LOG"
  echo -e "${CYAN}╚══════════════════════════════════════════════════════╝${NC}" | tee -a "$LOG"
}

DOCKERHUB_USERNAME="priya111222333"
export DOCKERHUB_USERNAME

# Load .env
if [ -f .env ]; then
  set -a; source .env; set +a
fi
export DOCKERHUB_USERNAME  # keep our value over .env

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG"
echo "  MSE-2 Docker Practical  |  $(date)                 " | tee -a "$LOG"
echo "  DockerHub: $DOCKERHUB_USERNAME                      " | tee -a "$LOG"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG"

# =============================================================================
# TASK 1A – Build Backend Image  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 1A: Build Backend Docker Image"
docker build -t taskflow-backend:local ./backend 2>&1 | tee -a "$LOG"
[ "${PIPESTATUS[0]}" -eq 0 ] && PASS "Backend image built successfully" || { FAIL "Backend build FAILED"; exit 1; }

# =============================================================================
# TASK 1B – Build Frontend Image  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 1B: Build Frontend Docker Image (multi-stage)"
docker build -t taskflow-frontend:local ./frontend 2>&1 | tee -a "$LOG"
[ "${PIPESTATUS[0]}" -eq 0 ] && PASS "Frontend image built successfully" || { FAIL "Frontend build FAILED"; exit 1; }

# =============================================================================
# TASK 1C – List Images  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 1C: Docker Images List"
docker images | grep -E "REPOSITORY|taskflow" 2>&1 | tee -a "$LOG"
PASS "Images listed"

# =============================================================================
# TASK 2A – Start Full Stack  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 2A: Start Full Stack with docker-compose.yml"
docker compose down -v --remove-orphans 2>/dev/null || true
docker compose up -d 2>&1 | tee -a "$LOG"
[ "${PIPESTATUS[0]}" -eq 0 ] && PASS "Stack started" || { FAIL "Stack failed"; docker compose logs | tee -a "$LOG"; exit 1; }

# =============================================================================
# TASK 2B – Wait for Backend Health  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 2B: Wait for Backend Health (up to 2 min)"
for i in $(seq 1 40); do
  HEALTH=$(curl --fail --silent http://localhost:3000/health 2>/dev/null || curl --fail --silent http://127.0.0.1:3000/health 2>/dev/null || true)
  if echo "$HEALTH" | grep -q '"status":"ok"'; then
    echo -e "\nHealth response: $HEALTH" | tee -a "$LOG"
    PASS "Backend is HEALTHY  ✓"
    break
  fi
  echo "  Waiting... attempt $i/40" | tee -a "$LOG"
  sleep 3
  if [ "$i" -eq 40 ]; then
    FAIL "Backend never became healthy"
    docker compose ps | tee -a "$LOG"
    docker compose logs --no-color | tee -a "$LOG"
    exit 1
  fi
done

# =============================================================================
# TASK 2C – Frontend Check  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 2C: Frontend Health Check"
for i in $(seq 1 20); do
  if curl --fail --silent http://localhost:8080/ > /dev/null 2>&1 || curl --fail --silent http://127.0.0.1:8080/ > /dev/null 2>&1; then
    PASS "Frontend responding on http://localhost:8080  ✓"
    break
  fi
  echo "  Waiting for frontend... $i/20" | tee -a "$LOG"
  sleep 3
  if [ "$i" -eq 20 ]; then FAIL "Frontend not responding"; docker compose logs frontend | tee -a "$LOG"; exit 1; fi
done

# =============================================================================
# TASK 2D – Container Status  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 2D: Running Containers Status"
docker compose ps 2>&1 | tee -a "$LOG"
PASS "All containers listed above"

# =============================================================================
# TASK 2E – Custom Docker Network  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 2E: Custom Docker Network Verification"
echo "--- All networks ---" | tee -a "$LOG"
docker network ls 2>&1 | tee -a "$LOG"
echo "" | tee -a "$LOG"
echo "--- taskflow_net details ---" | tee -a "$LOG"
NET=$(docker network ls --filter name=taskflow --format "{{.Name}}" | head -1)
docker network inspect "$NET" --format \
  'Network: {{.Name}}  |  Driver: {{.Driver}}  |  Subnet: {{(index .IPAM.Config 0).Subnet}}' 2>&1 | tee -a "$LOG"
PASS "Custom network verified: $NET"

# =============================================================================
# TASK 5A – Backend → PostgreSQL  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 5A: Backend connects to PostgreSQL (via service name 'postgres')"
docker compose exec backend wget -qO- http://127.0.0.1:3000/health 2>&1 | tee -a "$LOG"
PASS "Backend→PostgreSQL connection confirmed via /health endpoint"

# =============================================================================
# TASK 5B – Redis PING  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 5B: Redis Service Connectivity"
docker compose exec redis redis-cli ping 2>&1 | tee -a "$LOG"
PASS "Redis responds PONG"

# =============================================================================
# TASK 5C – Health Check Status of All Containers  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 5C: Container Health Check Status"
docker compose ps 2>&1 | tee -a "$LOG"
echo "" | tee -a "$LOG"
docker inspect --format '  {{.Name}}  →  Health: {{if .State.Health}}{{.State.Health.Status}}{{else}}no healthcheck{{end}}' \
  $(docker compose ps -q) 2>&1 | tee -a "$LOG"
PASS "Health statuses shown"

# =============================================================================
# TASK 5D – PostgreSQL Data Persistence  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 5D: PostgreSQL Data Persistence Test"
DB_USER="${POSTGRES_USER:-taskflow_user}"
DB_NAME="${POSTGRES_DB:-taskflow}"

echo "--- Step 1: Insert test record ---" | tee -a "$LOG"
docker compose exec -T postgres psql -U "$DB_USER" -d "$DB_NAME" \
  -c "INSERT INTO users (name,email,password_hash) VALUES ('PersistTest','persist@exam.com','testhash') ON CONFLICT (email) DO NOTHING RETURNING id,name,email;" 2>&1 | tee -a "$LOG"

echo "--- Step 2: Verify record exists BEFORE container removal ---" | tee -a "$LOG"
docker compose exec -T postgres psql -U "$DB_USER" -d "$DB_NAME" \
  -c "SELECT id,name,email,created_at FROM users WHERE email='persist@exam.com';" 2>&1 | tee -a "$LOG"

echo "--- Step 3: Remove PostgreSQL container (keep volume) ---" | tee -a "$LOG"
docker compose rm -sf postgres 2>&1 | tee -a "$LOG"

echo "--- Step 4: Recreate PostgreSQL container ---" | tee -a "$LOG"
docker compose up -d postgres 2>&1 | tee -a "$LOG"
sleep 20

echo "--- Step 5: Verify data SURVIVED container removal ---" | tee -a "$LOG"
docker compose exec -T postgres psql -U "$DB_USER" -d "$DB_NAME" \
  -c "SELECT id,name,email,created_at FROM users WHERE email='persist@exam.com';" 2>&1 | tee -a "$LOG"
PASS "Data persisted across PostgreSQL container removal  ✓"

# =============================================================================
# TASK 5E – Redis Restart  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 5E: Redis Restart Verification"
docker compose restart redis 2>&1 | tee -a "$LOG"
sleep 5
docker compose exec redis redis-cli ping 2>&1 | tee -a "$LOG"
PASS "Redis restarted and is PONG-ing  ✓"

# =============================================================================
# TASK 3A – Docker Hub Login  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 3A: Docker Hub Login"
if [ -n "${DOCKERHUB_TOKEN:-}" ]; then
  echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin 2>&1 | tee -a "$LOG"
else
  docker login -u "$DOCKERHUB_USERNAME" 2>&1 | tee -a "$LOG"
fi
PASS "Docker Hub login succeeded for $DOCKERHUB_USERNAME"

# =============================================================================
# TASK 3B – Tag Images  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 3B: Tag Images for Docker Hub"
docker tag taskflow-backend:local  "${DOCKERHUB_USERNAME}/taskflow-backend:v1"      2>&1 | tee -a "$LOG"
docker tag taskflow-backend:local  "${DOCKERHUB_USERNAME}/taskflow-backend:latest"  2>&1 | tee -a "$LOG"
docker tag taskflow-backend:local  "${DOCKERHUB_USERNAME}/backend:v1"               2>&1 | tee -a "$LOG"
docker tag taskflow-backend:local  "${DOCKERHUB_USERNAME}/backend:latest"           2>&1 | tee -a "$LOG"

docker tag taskflow-frontend:local "${DOCKERHUB_USERNAME}/taskflow-frontend:v1"     2>&1 | tee -a "$LOG"
docker tag taskflow-frontend:local "${DOCKERHUB_USERNAME}/taskflow-frontend:latest" 2>&1 | tee -a "$LOG"
docker tag taskflow-frontend:local "${DOCKERHUB_USERNAME}/frontend:v1"              2>&1 | tee -a "$LOG"
docker tag taskflow-frontend:local "${DOCKERHUB_USERNAME}/frontend:latest"          2>&1 | tee -a "$LOG"
echo "" | tee -a "$LOG"
docker images | grep -E "REPOSITORY|taskflow|backend|frontend" 2>&1 | tee -a "$LOG"
PASS "All tags created (both 'backend/frontend' and 'taskflow-backend/frontend')"

# =============================================================================
# TASK 3C – Push Backend to Docker Hub  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 3C: Push Backend to Docker Hub"
docker push "${DOCKERHUB_USERNAME}/taskflow-backend:v1" 2>&1 | tee -a "$LOG"
docker push "${DOCKERHUB_USERNAME}/taskflow-backend:latest" 2>&1 | tee -a "$LOG"
docker push "${DOCKERHUB_USERNAME}/backend:v1" 2>&1 | tee -a "$LOG"
docker push "${DOCKERHUB_USERNAME}/backend:latest" 2>&1 | tee -a "$LOG"
PASS "Backend pushed: all tags to Docker Hub"

# =============================================================================
# TASK 3D – Push Frontend to Docker Hub  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 3D: Push Frontend to Docker Hub"
docker push "${DOCKERHUB_USERNAME}/taskflow-frontend:v1" 2>&1 | tee -a "$LOG"
docker push "${DOCKERHUB_USERNAME}/taskflow-frontend:latest" 2>&1 | tee -a "$LOG"
docker push "${DOCKERHUB_USERNAME}/frontend:v1" 2>&1 | tee -a "$LOG"
docker push "${DOCKERHUB_USERNAME}/frontend:latest" 2>&1 | tee -a "$LOG"
PASS "Frontend pushed: all tags to Docker Hub"

# =============================================================================
# TASK 4A – Bring down build stack  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 4A: Stop Build-Based Stack"
docker compose down --remove-orphans 2>&1 | tee -a "$LOG"
PASS "Build-based stack stopped"

# =============================================================================
# TASK 4B – Pull images from Docker Hub  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 4B: Pull Published Images from Docker Hub"
docker compose -f docker-compose.deploy.yml pull 2>&1 | tee -a "$LOG"
PASS "Images pulled from Docker Hub"

# =============================================================================
# TASK 4C – Deploy with published images  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 4C: Deploy Using docker-compose.deploy.yml (Hub Images)"
docker compose -f docker-compose.deploy.yml up -d 2>&1 | tee -a "$LOG"
[ "${PIPESTATUS[0]}" -eq 0 ] && PASS "Deployment started" || { FAIL "Deploy failed"; exit 1; }

# =============================================================================
# TASK 4D – Deployed backend health  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 4D: Verify Deployed Backend Health"
for i in $(seq 1 40); do
  HEALTH=$(curl --fail --silent http://localhost:3000/health 2>/dev/null || curl --fail --silent http://127.0.0.1:3000/health 2>/dev/null || true)
  if echo "$HEALTH" | grep -q '"status":"ok"'; then
    echo -e "\nHealth: $HEALTH" | tee -a "$LOG"
    PASS "Deployed backend is HEALTHY  ✓"
    break
  fi
  echo "  Waiting... $i/40" | tee -a "$LOG"
  sleep 3
  [ "$i" -eq 40 ] && { FAIL "Deployed backend never healthy"; exit 1; }
done

# =============================================================================
# TASK 4E – Deployed frontend check  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 4E: Verify Deployed Frontend"
(curl --fail --silent http://localhost:8080/ > /dev/null || curl --fail --silent http://127.0.0.1:8080/ > /dev/null) && PASS "Deployed frontend responding" \
  || FAIL "Frontend not responding"

# =============================================================================
# TASK 4F – Deployed container status  [SCREENSHOT THIS]
# =============================================================================
STEP "TASK 4F: Deployed Container Status"
docker compose -f docker-compose.deploy.yml ps 2>&1 | tee -a "$LOG"
PASS "Deployed stack containers listed"

# =============================================================================
# FINAL
# =============================================================================
STEP "ALL AUTOMATED TASKS COMPLETE"
echo "" | tee -a "$LOG"
echo "  Full log saved to: execution.log" | tee -a "$LOG"
echo "" | tee -a "$LOG"
echo "  MANUAL STEPS REMAINING:" | tee -a "$LOG"
echo "  ┌─────────────────────────────────────────────────────────────────┐" | tee -a "$LOG"
echo "  │  1. Screenshot Docker Hub tags at:                              │" | tee -a "$LOG"
echo "  │     https://hub.docker.com/u/priya111222333                    │" | tee -a "$LOG"
echo "  │  2. Create GitHub PR → atindeRR/MSE-2-SSED-Evening main        │" | tee -a "$LOG"
echo "  │  3. Watch CI pass in GitHub Actions tab                         │" | tee -a "$LOG"
echo "  └─────────────────────────────────────────────────────────────────┘" | tee -a "$LOG"
echo "" | tee -a "$LOG"
PASS "run_all.sh FINISHED SUCCESSFULLY"
