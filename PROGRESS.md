# Implementation Progress — MSE-2 SET 2 (TaskFlow)

Last checkpoint: 2026-11-18 (~15:05 local). Repository root:
`C:\Users\SAKSHI\MSE-2-SSED-Evening`. Current branch: `feat/docker-cicd` (committed `2e5de04`, pushed to origin).
`origin` = `https://github.com/spirals-coder/MSE-2-SSED-Evening.git` (personal fork — correct).
`upstream` = NOT yet configured. Add: `https://github.com/atindeRR/MSE-2-SSED-Evening.git`.

## DONE

### Phase 1 — Inspection
- App: React 18 + Vite 5 SPA (`frontend/`), Express 4 ESM API (`backend/`), PostgreSQL 16, Redis 7.
- Frontend uses relative `/api`; `frontend/nginx.conf` proxies `/api/` and `/health` to `backend:3000`.
- Backend already has `/health` (checks PG + Redis) and listens on `0.0.0.0:3000`.
- Schema: `backend/db/init.sql` (`users`, `tasks`). Test suite: `tests/api.test.js` (12 tests).
- Instructor `ci.yml` (PR evaluator) must stay untouched. Old `cd.yml` must be replaced.
- Tooling: Node 24/npm 11, Docker 29.9.3 + Compose v5.7, Python 3.14 (NO pdf libs installed), `gh` CLI NOT installed, Git Credential Manager present, Docker Desktop logged into Docker Hub as `1sakshi2`.
- Host note: TCP 8080 on 127.0.0.1 is occupied by Oracle TNSLSNR (PID 6540). Docker's 0.0.0.0:8080 mapping works via LAN IP `10.21.128.113` (use this for local frontend tests). GitHub runners have no such conflict.

### Files created/modified so far
- `frontend/Dockerfile` — multi-stage `node:20-alpine` (build) → `nginx:1.27-alpine`; npm ci with lockfile; non-root `nginx` user; writable cache dirs; PID moved to /tmp via sed; dynamic Docker DNS resolver in nginx.conf.
- `frontend/package-lock.json`, `backend/package-lock.json` — generated (lockfileVersion 3). Frontend has `"overrides": { "rollup": "4.34.9" }` in `package.json` ( Rollup 4.68.x native musl binding breaks Vite build on Alpine).
- `frontend/nginx.conf` — added `resolver 127.0.0.11 valid=10s ipv6=off;` and variable-based `proxy_pass` so a restarted backend IP is picked up. SPA fallback preserved.
- `backend/Dockerfile` — 2-stage `node:20-alpine`; `npm ci --omit=dev`; copies only `src/` and `db/`; `USER node`; `EXPOSE 3000`.
- `backend/src/db.js` — added idempotent `ensureSchema()` (runs bundled `db/init.sql` at startup) and a `pool.on('error', ...)` handler so backend survives DB container recreation.
- `backend/src/server.js` — calls `ensureSchema()` after `waitForDatabase()`.
- `docker-compose.yml` — 4 services on custom bridge `taskflow-net`, named volume `postgres_data`, healthchecks, `depends_on: service_healthy`, PG/Redis no host ports, ports 3000/8080.
- `docker-compose.deploy.yml` — same but `image: ${DOCKERHUB_USERNAME}/frontend:latest` and backend; NO `build:`, NO source mounts.
- `.env.example` — added `DOCKERHUB_USERNAME` placeholder.
- `.env` — LOCAL ONLY (gitignored). Contains local test values incl. `DOCKERHUB_USERNAME=1sakshi2`. NEVER COMMIT.
- `.dockerignore` files — added `.git`.
- `PROGRESS.md` — this file.

### Phase 2/3 — Images built and tested
- Both images build successfully: `taskflow-frontend:local`, `taskflow-backend:local`.
- Errors fixed: Rollup musl parser bug (pinned 4.34.9); nginx non-root cache dir + PID path; stale nginx upstream IP after backend restart.

### Phase 4 — Compose
- `docker compose config` and deploy `config --quiet` pass; no `build:` in deploy file.
- `docker compose up -d --build` → all 4 containers healthy/running.

### Phase 5 — Docker Hub
- Tagged and pushed all four tags: `1sakshi2/frontend:v1`, `1sakshi2/frontend:latest`, `1sakshi2/backend:v1`, `1sakshi2/backend:latest`.
- Verified with `docker manifest inspect` — all AVAILABLE.

### Phase 6 — Image-based deployment
- `docker compose down` (no -v), then `-f docker-compose.deploy.yml config/pull/up -d` succeeded.
- `ps` shows `1sakshi2/frontend:latest` and `1sakshi2/backend:latest` with correct image IDs; 12 API tests pass against it.
- CURRENT STATE: deployment stack is RUNNING from Docker Hub images.

### Phase 7 — Functional evidence (genuine, captured)
Evidence dir: `C:\Users\SAKSHI\AppData\Local\Temp\opencode\mse2-evidence\`
- `phase7-evidence.txt` — full verification: 4 network members, DNS `postgres -> 172.19.0.4`, `redis -> 172.19.0.3`, frontend proxy health OK, register via proxy OK, SQL record id=4 present before and after removing/recreating ONLY postgres container, API login still works, named volume still exists, Redis restart healthy, final all healthy.
- `build-frontend.txt`, `build-backend.txt`, `deploy-ps.txt`, `deploy-config.txt`, `network.txt`, `health.txt`, `dockerhub.txt`, `tests.txt`.
- NOTE: `phase7-evidence.txt` contains a test JWT token — REDACT when putting into PDF.

## PENDING

1. **Phase 8 — `.github/workflows/cd.yml`**: replace existing file. On push to main: checkout → validate secrets (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, `POSTGRES_PASSWORD`) → Buildx with GHA cache → Docker Hub login → build/push 4 tags (frontend/backend with v1 + latest) → create `.env` from secrets (NO hardcoded password) → assert no `build:` in deploy compose → `config`/`pull`/`up -d` → health + API smoke tests + `ps` → cleanup `down -v` under `if: always()`. Fail explicitly. Leave `ci.yml` untouched. Validate YAML.
2. **Phase 9 — GitHub**: DONE: `upstream` remote added; branch `feat/docker-cicd` committed (`2e5de04`) and pushed to origin. PENDING: PR creation needs personal info for exact title `DOCKER-SET-2 | ROLL-NUMBER | STUDENT-NAME | SECTION`. `gh` unavailable → PR via REST API using stored Git credential (never echo) or pre-filled browser URL. Target `atindeRR/MSE-2-SSED-Evening:main`. Verify instructor CI checks. Never merge/force-push.
3. **Phase 8 status — CD workflow**: `.github/workflows/cd.yml` replaced with full build→publish→deploy→test→cleanup pipeline; PyYAML syntax validation passed. NOT YET RUN: checked GitHub API and the fork has **zero Actions secrets configured**. User must add `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, `POSTGRES_PASSWORD` at `https://github.com/spirals-coder/MSE-2-SSED-Evening/settings/secrets/actions` before any workflow run can pass. Do not ask for the token value in chat.

4. **Phase 10 — PDF**: `ROLL_NUMBER_STUDENT_NAME_SET2.pdf` with sections A–E, exact declaration, genuine evidence, unavailable items marked Pending. Need: student name, roll number, section, branch (Git config only gives `Sakshi` / `sakshi.2428cseaiml62@kiet.edu` — do NOT guess). Install PDF lib locally (`pip install reportlab`) — no PDF libs currently installed. Commit PDF so it appears in PR; explain manual Moodle upload / PR attachment.
4. **Final report** with checklist (Completed/Failed/Pending), URLs, statuses.

## BLOCKERS / INFO NEEDED FROM USER
- Exact student name, roll number, section, branch.
- Confirm GitHub username `spirals-coder` and Docker Hub username `1sakshi2` (both inferred locally).
- Confirm Docker Hub login is active (push already worked, so yes).
- Preference for PR creation method (REST API with stored credential vs pre-filled browser URL).

## IMPORTANT NEXT STEPS / GOTCHAS
- Do NOT commit `.env`, `node_modules/`, `dist/`, evidence temp files, or any token.
- `.gitignore` already covers `node_modules`, `.env`, `dist`, `coverage`.
- Instructor `ci.yml` runs hadolint on both Dockerfiles — current Dockerfiles use tagged bases, `npm ci`, `USER`, no root final user; keep it that way.
- Instructor CI creates its own `.env` with `POSTGRES_PASSWORD=ci_test_password_123`; compose must keep `${POSTGRES_PASSWORD}` interpolation.
- Backend `ensureSchema()` is what makes source-less deployment work with an empty PG volume.
- `frontend/package.json` override for rollup is required for Alpine builds — do not remove.
- Local host port 8080 conflict is environmental only; do not change compose port mappings (instructor expects 8080/3000).
