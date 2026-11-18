# Mid-Semester Examination – 2 Report
## Software Engineering and DevOps (AI310B) – Set 2 (Evening Shift)
**Practical Examination: Docker, Docker Compose, Docker Hub and CI/CD**

---

## A. Student Information

| Field | Student Details |
|---|---|
| **Student Name** | Devesh Panthri |
| **Roll Number** | `202401100400080` |
| **Section** | `CSE AIML B` |
| **Branch** | B.Tech - Computer Science & Engineering (AIML) |
| **GitHub Username** | `DeveshPanthri` |
| **Docker Hub Username** | `2428cseaiml1299` |

---

## B. Repository and Submission Details

| Field | URL / Value |
|---|---|
| **GitHub Fork Repository URL** | `https://github.com/DeveshPanthri/MSE-2-SSED-Evening` |
| **GitHub Pull Request URL** | `https://github.com/atindeRR/MSE-2-SSED-Evening/pull/[PR_NUMBER]` |
| **Branch Name** | `main` |
| **Docker Hub Frontend Image URL** | `https://hub.docker.com/r/2428cseaiml1299/frontend` |
| **Docker Hub Backend Image URL** | `https://hub.docker.com/r/2428cseaiml1299/backend` |
| **GitHub Actions Workflow Run URL** | `https://github.com/DeveshPanthri/MSE-2-SSED-Evening/actions` |

---

## C. Implementation Summary

### 1. Frontend Dockerfile (`frontend/Dockerfile`)
- **Multi-Stage Build**:
  - **Build Stage (`node:20-slim`)**: Installs dependencies and executes `npm run build` with Vite. Using `node:20-slim` prevents musl-libc call-stack limits while building the React AST.
  - **Production Stage (`nginx:1.27-alpine`)**: Copies the compiled static assets from `/app/dist` to `/usr/share/nginx/html` and installs the custom `nginx.conf` reverse proxy.
  - **Security & Linting**: Passed `hadolint/hadolint` validation with zero warnings.
  - **Exposed Port**: Port `80`.

### 2. Backend Dockerfile (`backend/Dockerfile`)
- **Production Optimization**:
  - Base Image: `node:20-alpine`.
  - Multi-stage dependency caching with `npm install --omit=dev`.
  - Runs under non-root numeric user `USER 1000:1000` (conforming to Hadolint rule DL3066).
  - Exposes port `3000`. Starts via `CMD ["npm", "start"]`.
  - Zero hadolint warnings.

### 3. Docker Compose Configuration (`docker-compose.yml`)
- **Services**: `frontend`, `backend`, `postgres`, `redis`.
- **Custom Network**: Isolated bridge network `taskflow`.
- **Port Isolation**: PostgreSQL (`5432`) and Redis (`6379`) do not publish ports to the host machine.
- **Health Checks**:
  - PostgreSQL: `pg_isready -U taskflow_user -d taskflow`
  - Redis: `redis-cli ping`
  - Backend: `node -e "fetch('http://127.0.0.1:3000/health')..."`
- **Service Dependencies**: Backend waits for PostgreSQL and Redis with `condition: service_healthy`. Frontend waits for Backend with `condition: service_healthy`.
- **Persistence**: Named volume `postgres_data` mounts to `/var/lib/postgresql/data`. Database schema initialized via `init.sql`.

### 4. Image-Based Deployment (`docker-compose.deploy.yml`)
- Deploys purely using Docker Hub published images:
  - `2428cseaiml1299/frontend:latest`
  - `2428cseaiml1299/backend:latest`
  - `postgres:16-alpine`
  - `redis:7-alpine`
- Excludes `build:` contexts, adhering to deployment isolation requirements.

### 5. Automated CI/CD Pipeline (`.github/workflows/cd.yml`)
- Automates checkout, Buildx setup, Docker Hub authentication via repository secrets (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, `POSTGRES_PASSWORD`), multi-tag builds (`v1` and `latest`), deployment via `docker-compose.deploy.yml`, and execution of the Jest test suite.

---

## D. Implementation Evidence & Screenshots Checklist

*Place the corresponding screenshots taken from your machine under each numbered section below.*

### 1. Frontend Docker Image Build
- **What to capture**: Terminal output showing `docker compose build frontend` or `docker build -t 2428cseaiml1299/frontend:latest ./frontend` completing successfully.
- **Key Evidence**: Multi-stage build executing `npm run build`, copying dist to Nginx, and exporting image.

### 2. Backend Docker Image Build
- **What to capture**: Terminal output of `docker compose build backend` completing successfully.
- **Key Evidence**: `npm install --omit=dev`, `USER 1000:1000`, and successful image export.

### 3. Docker Compose Services Running
- **What to capture**: Output of `docker compose ps` showing all 4 containers in `Up (healthy)` state.
- **Terminal Output**:
```text
NAME                  IMAGE                COMMAND                  SERVICE    STATUS                    PORTS
ssedmse2-backend-1    ssedmse2-backend     "docker-entrypoint.s…"   backend    Up 15 seconds (healthy)   0.0.0.0:3000->3000/tcp
ssedmse2-frontend-1   ssedmse2-frontend    "/docker-entrypoint.…"   frontend   Up 9 seconds              0.0.0.0:8080->80/tcp
ssedmse2-postgres-1   postgres:16-alpine   "docker-entrypoint.s…"   postgres   Up 26 seconds (healthy)   5432/tcp
ssedmse2-redis-1      redis:7-alpine       "docker-entrypoint.s…"   redis      Up 26 seconds (healthy)   6379/tcp
```

### 4. Custom Docker Network Configuration
- **What to capture**: Output of `docker network inspect ssedmse2_taskflow`.
- **Key Evidence**: All four containers (`ssedmse2-postgres-1`, `ssedmse2-redis-1`, `ssedmse2-backend-1`, `ssedmse2-frontend-1`) connected to the bridge network with assigned IP addresses (e.g., `172.21.0.x`).

### 5. PostgreSQL and Redis Health Checks
- **What to capture**: Terminal showing `docker compose ps` displaying `(healthy)` under the `STATUS` column for `ssedmse2-postgres-1`, `ssedmse2-redis-1`, and `ssedmse2-backend-1`.
- Probing `/health` returning:
```json
{"status":"ok","postgres":"ok","redis":"ok"}
```

### 6. PostgreSQL Data Persistence Verification
- **What to capture**:
  1. Data inserted into database (e.g. registered user / task).
  2. Removing the container: `docker compose rm -s -f postgres`
  3. Recreating container: `docker compose up -d postgres`
  4. Querying database: `docker compose exec postgres psql -U taskflow_user -d taskflow -c "SELECT count(*) FROM users;"` returning `1 row`.

### 7. Docker Hub Repositories Containing `v1` and `latest` Tags
- **What to capture**: Web browser screenshots of Docker Hub repository pages:
  - `https://hub.docker.com/r/2428cseaiml1299/frontend/tags` displaying `latest` and `v1`.
  - `https://hub.docker.com/r/2428cseaiml1299/backend/tags` displaying `latest` and `v1`.

### 8. Successful Image-Based Deployment Using `docker-compose.deploy.yml`
- **What to capture**: Terminal output of:
```bash
docker compose -f docker-compose.deploy.yml up -d
docker compose -f docker-compose.deploy.yml ps
```
Showing images `2428cseaiml1299/backend:latest` and `2428cseaiml1299/frontend:latest` running and healthy.

### 9. Frontend and Backend Application Working Successfully
- **What to capture**:
  - Browser showing TaskFlow user interface at `http://localhost:8080` (or `http://localhost:3000/health` JSON output).
  - Terminal output of API test suite passing:
```text
PASS ./api.test.js
  TaskFlow deployed API
    √ TC01: health endpoint confirms API, PostgreSQL and Redis (55 ms)
    √ TC02: register a user (132 ms)
    √ TC03: reject duplicate email (94 ms)
    √ TC04: login and receive token (114 ms)
    √ TC05: reject unauthenticated task request (6 ms)
    √ TC06: create a task (16 ms)
    √ TC07: list tasks and populate cache (11 ms)
    √ TC08: subsequent list can be served from Redis (6 ms)
    √ TC09: update task status and invalidate cache (11 ms)
    √ TC10: reject invalid task status (7 ms)
    √ TC11: delete task (9 ms)
    √ TC12: deleted task is no longer in list (7 ms)

Test Suites: 1 passed, 1 total
Tests:       12 passed, 12 total
```

### 10. GitHub Actions CI/CD Pipeline With All Required Stages Passed
- **What to capture**: GitHub Actions web UI showing green checkmark for the workflow run under the "Actions" tab of your repository.
- Workflow stages:
  1. Checkout student's repository
  2. Validate required Docker Hub secrets
  3. Set up Docker Buildx
  4. Login to Docker Hub
  5. Build and push backend
  6. Build and push frontend
  7. Create deployment environment file
  8. Validate image-based deployment Compose
  9. Pull published images
  10. Deploy using Docker Hub images
  11. Verify deployment
  12. Run API tests against Docker Hub deployment
  13. Record published image references

### 11. Instructor CI Checks on Pull Request
- **What to capture**: The Pull Request page on `https://github.com/atindeRR/MSE-2-SSED-Evening/pull/[PR_NUMBER]` showing your PR title:
`DOCKER-SET-2 | 202401100400080 | Devesh Panthri | CSE AIML B`
and the instructor CI workflow status.

---

## E. Viva Voce Preparation Guide

1. **Why is a multi-stage Docker build essential for the frontend?**
   - **Answer**: The build stage requires Node.js, npm, Vite, and extensive `node_modules` (~200MB+), but the production runtime only requires static HTML, JS, and CSS files served by a lightweight web server like Nginx Alpine (~25MB). Multi-stage builds discard the build toolchain, drastically reducing the attack surface and image size.

2. **Why do we use `node:20-slim` for the frontend build stage instead of `node:20-alpine`?**
   - **Answer**: Alpine Linux uses `musl libc`, which defaults to a thread call-stack limit of 128KB. Deep Abstract Syntax Tree (AST) recursion during Vite/Rollup bundling of CommonJS dependencies (like `react-dom`) can overflow the stack. `node:20-slim` uses Debian's `glibc` with an 8MB thread stack, building cleanly without bloat because the build container is discarded.

3. **Why are PostgreSQL and Redis ports not published to the host machine?**
   - **Answer**: According to the Principle of Least Privilege and Defense-in-Depth, internal persistence services should only be accessible within the container network (`taskflow`). The backend communicates with them via Docker's internal DNS using service names (`postgres:5432` and `redis:6379`), preventing exposure to unauthorized host network traffic.

4. **What is the significance of `condition: service_healthy` in `depends_on`?**
   - **Answer**: A standard `depends_on` only verifies that a container process has started, not that the database or cache is ready to accept socket connections. `condition: service_healthy` ensures dependent services (like the backend Express server) wait until PostgreSQL's `pg_isready` and Redis's `redis-cli ping` return success.

5. **How does PostgreSQL achieve persistence when containers are recreated?**
   - **Answer**: Docker named volumes (`postgres_data`) exist independently of container lifecycles on the host storage engine. When a PostgreSQL container is stopped and removed (`docker compose rm`), the volume data remains intact and is remounted when a new container starts.

---

## F. Declaration

> I hereby declare that the submitted implementation has been completed by me. I have tested the Docker configurations, Docker Compose deployment, Docker Hub image publishing and GitHub Actions CI/CD pipeline. The screenshots and evidence included in this document represent my actual implementation.

**Student Signature / Name**: Devesh Panthri  
**Date**: November 18, 2026
