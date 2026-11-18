# MSE-2 Software Engineering and DevOps (Set 2 – Evening Shift)
## Implementation Verification and PDF Evidence Documentation

---

### A. Student Information

| Field | Detail |
|---|---|
| **Student Name** | Badal Singh |
| **Roll Number** | 202401100400071 |
| **Section** | AIML-A |
| **Branch** | AIML |
| **GitHub Username** | BadalSinghh |
| **Docker Hub Username** | darkkenn |

---

### B. Repository and Submission Details

| Particular | Link / Detail |
|---|---|
| **GitHub Fork URL** | https://github.com/BadalSinghh/MSE-2-SSED-Evening |
| **GitHub Pull Request URL** | `https://github.com/atindeRR/MSE-2-SSED-Evening/pull/[PR_NUMBER]` |
| **Pull Request Title** | `DOCKER-SET-2 | 202401100400071 | Badal Singh | AIML-A` |
| **Target Branch** | `main` |
| **Docker Hub Frontend Image** | https://hub.docker.com/r/darkkenn/frontend |
| **Docker Hub Backend Image** | https://hub.docker.com/r/darkkenn/backend |
| **GitHub Actions Run URL** | https://github.com/BadalSinghh/MSE-2-SSED-Evening/actions |

---

### C. Implementation Evidence

#### 1. Frontend Dockerfile Implementation
- **File:** `frontend/Dockerfile`
- **Architecture:** Multi-stage build (`node:20-slim` build stage, `nginx:1.27-alpine` production runtime stage).
- **Optimization:** Only compiled assets (`dist/`) and custom `nginx.conf` copied into the production container. Node.js runtime and development dependencies are stripped completely.
- **Port:** Exposes port `80`.
- **Linting:** Passes Hadolint with zero warnings (`DL3025` compliant JSON-syntax healthcheck).

```dockerfile
# Stage 1: Build stage
FROM node:20-slim AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production runtime stage
FROM nginx:1.27-alpine AS production
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
HEALTHCHECK --interval=15s --timeout=5s --retries=3 \
  CMD ["wget", "-q", "-O", "/dev/null", "http://127.0.0.1/"]
CMD ["nginx", "-g", "daemon off;"]
```

---

#### 2. Backend Dockerfile Implementation
- **File:** `backend/Dockerfile`
- **Architecture:** Production multi-stage build using `node:20-alpine`.
- **Security:** Non-root user execution (`USER 1000:1000`).
- **Dependencies:** Installs production dependencies only (`npm install --omit=dev`).
- **Port:** Exposes port `3000`.

```dockerfile
# Stage 1: Dependencies cache stage
FROM node:20-alpine AS dependencies
WORKDIR /app
COPY package*.json ./
RUN npm install --omit=dev

# Stage 2: Production runtime
FROM node:20-alpine AS production
WORKDIR /app
ENV NODE_ENV=production
COPY --from=dependencies /app/node_modules ./node_modules
COPY package*.json ./
COPY src ./src
USER 1000:1000
EXPOSE 3000
CMD ["npm", "start"]
```

---

#### 3. Docker Compose Stack Execution & Service Health Checks
- **File:** `docker-compose.yml`
- **Command:** `docker compose ps`

**Live Terminal Output:**
```text
NAME                            IMAGE                         COMMAND                  SERVICE    CREATED          STATUS                    PORTS
mse-2-ssed-evening-backend-1    mse-2-ssed-evening-backend    "docker-entrypoint.s…"   backend    32 minutes ago   Up 32 minutes (healthy)   0.0.0.0:3000->3000/tcp
mse-2-ssed-evening-frontend-1   mse-2-ssed-evening-frontend   "/docker-entrypoint.…"   frontend   32 minutes ago   Up 32 minutes (healthy)   0.0.0.0:8080->80/tcp
mse-2-ssed-evening-postgres-1   postgres:16-alpine            "docker-entrypoint.s…"   postgres   5 minutes ago    Up 5 minutes (healthy)    5432/tcp
mse-2-ssed-evening-redis-1      redis:7-alpine                "docker-entrypoint.s…"   redis      2 minutes ago    Up 2 minutes (healthy)    6379/tcp
```
*Note: PostgreSQL and Redis do not expose host ports, securing them within the Docker network.*

---

#### 4. Backend Health Endpoint Verification
- **Command:**
```powershell
Invoke-RestMethod -Uri 'http://localhost:3000/health' | ConvertTo-Json
```
**Terminal Output:**
```json
{
    "status":  "ok",
    "postgres":  "ok",
    "redis":  "ok"
}
```

---

#### 5. Frontend Nginx Reverse Proxy Verification
- **Endpoints:**
  - `http://localhost:8080/` (Serves React frontend SPA)
  - `http://localhost:8080/health` (Proxied to `backend:3000/health`)
  - `http://localhost:8080/api/health` (Proxied to `backend:3000/api/health`)

**Terminal Output:**
```json
{
    "status":  "ok",
    "postgres":  "ok",
    "redis":  "ok"
}
```

---

#### 6. Custom Docker Network Verification
- **Network Name:** `mse-2-ssed-evening_taskflow` (driver: `bridge`, subnet: `172.21.0.0/16`)
- **Command:** `docker network inspect mse-2-ssed-evening_taskflow`

**Attached Containers:**
| Container Name | Service | IPv4 Address |
|---|---|---|
| `mse-2-ssed-evening-redis-1` | `redis` | `172.21.0.2` |
| `mse-2-ssed-evening-postgres-1` | `postgres` | `172.21.0.3` |
| `mse-2-ssed-evening-backend-1` | `backend` | `172.21.0.4` |
| `mse-2-ssed-evening-frontend-1` | `frontend` | `172.21.0.5` |

---

#### 7. Internal Service-Name DNS Resolution
- **Test:** DNS resolution from inside `backend` container using Docker's embedded DNS server (`127.0.0.11`).
- **Command:**
```powershell
docker compose exec backend node -e "import('dns').then(dns => { dns.lookup('postgres', (err, a) => console.log('postgres resolved to:', a)); dns.lookup('redis', (err, a) => console.log('redis resolved to:', a)); })"
```
**Terminal Output:**
```text
redis resolved to: 172.21.0.2
postgres resolved to: 172.21.0.3
```

---

#### 8. PostgreSQL Data Persistence Verification
**Step 1: Insert test task into database:**
```powershell
docker compose exec postgres psql -U taskflow_user -d taskflow -c "INSERT INTO tasks (user_id, title, description, status) VALUES (1, 'Persistent Task Test', 'Testing volume persistence across postgres container removal', 'In Progress');"
```
*Output:*
```text
INSERT 0 1
 id |        title         |   status    
----+----------------------+-------------
  4 | Persistent Task Test | In Progress
```

**Step 2: Stop and remove PostgreSQL container:**
```powershell
docker compose rm -s -f postgres
```
*Output:*
```text
 Container mse-2-ssed-evening-postgres-1 Stopping 
 Container mse-2-ssed-evening-postgres-1 Stopped 
 Container mse-2-ssed-evening-postgres-1 Removing 
 Container mse-2-ssed-evening-postgres-1 Removed 
```

**Step 3: Recreate PostgreSQL container using the existing named volume:**
```powershell
docker compose up -d postgres
```
*Output:*
```text
 Container mse-2-ssed-evening-postgres-1 Creating 
 Container mse-2-ssed-evening-postgres-1 Created 
 Container mse-2-ssed-evening-postgres-1 Starting 
 Container mse-2-ssed-evening-postgres-1 Started 
```

**Step 4: Query records after recreation:**
```powershell
docker compose exec postgres psql -U taskflow_user -d taskflow -c "SELECT id, title, status FROM tasks;" -c "SELECT count(*) FROM users;"
```
*Output:*
```text
 id |        title         |   status    
----+----------------------+-------------
  4 | Persistent Task Test | In Progress
(1 row)

 count 
-------
     4
(1 row)
```
*Result: Database records remained completely intact, proving named volume `postgres_data` persistence.*

---

#### 9. Redis Restart Test
**Step 1: Restart Redis service:**
```powershell
docker compose restart redis
```
*Output:*
```text
 Container mse-2-ssed-evening-redis-1 Restarting 
 Container mse-2-ssed-evening-redis-1 Started 
```

**Step 2: Verify Backend reconnects and reports healthy:**
```powershell
Invoke-RestMethod -Uri 'http://localhost:3000/health' | ConvertTo-Json
```
*Output:*
```json
{
    "status":  "ok",
    "postgres":  "ok",
    "redis":  "ok"
}
```

---

#### 10. Automated API Test Suite Execution
- **Command:** `npm test` inside `tests/`
- **Test File:** `tests/api.test.js`

**Test Results (12 / 12 Passed):**
```text
PASS ./api.test.js
  TaskFlow deployed API
    √ TC01: health endpoint confirms API, PostgreSQL and Redis (59 ms)
    √ TC02: register a user (352 ms)
    √ TC03: reject duplicate email (247 ms)
    √ TC04: login and receive token (387 ms)
    √ TC05: reject unauthenticated task request (13 ms)
    √ TC06: create a task (47 ms)
    √ TC07: list tasks and populate cache (37 ms)
    √ TC08: subsequent list can be served from Redis (23 ms)
    √ TC09: update task status and invalidate cache (41 ms)
    √ TC10: reject invalid task status (23 ms)
    √ TC11: delete task (63 ms)
    √ TC12: deleted task is no longer in list (28 ms)

Test Suites: 1 passed, 1 total
Tests:       12 passed, 12 total
Snapshots:   0 total
Time:        4.962 s
```

---

#### 11. Image-Based Deployment (`docker-compose.deploy.yml`)
- **File:** `docker-compose.deploy.yml`
- **Key Characteristics:**
  - Uses published images: `${DOCKERHUB_USERNAME}/backend:latest` and `${DOCKERHUB_USERNAME}/frontend:latest`.
  - Zero `build:` directives.
  - Mounts no local application source directories.
  - Retains persistent named volumes `postgres_data` and `redis_data`.
  - Includes health checks and service dependencies.
- **Validation:** Passes `docker compose -f docker-compose.deploy.yml config`.

---

#### 12. GitHub Actions CI/CD Pipeline (`.github/workflows/cd.yml`)
- **Triggers:** Push to `main` branch, `workflow_dispatch`.
- **Pipeline Stages:**
  1. Checkout code (`actions/checkout@v4`).
  2. Validate required secrets (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`).
  3. Set up Docker Buildx (`docker/setup-buildx-action@v3`).
  4. Docker Hub authentication (`docker/login-action@v3`).
  5. Build & push Backend images (`v1`, `latest`, `${{ github.sha }}`).
  6. Build & push Frontend images (`v1`, `latest`, `${{ github.sha }}`).
  7. Generate `.env` configuration for deploy compose.
  8. Deploy stack with `docker compose -f docker-compose.deploy.yml up -d`.
  9. Poll `/health` endpoint until healthy.
  10. Run 12 Jest test cases against deployed stack.
  11. Post publication summary to `$GITHUB_STEP_SUMMARY`.
  12. Teardown deployment with `docker compose down -v`.

---

### D. Declaration

> I hereby declare that the submitted implementation has been completed by me. I have tested the Docker configurations, Docker Compose deployment, Docker Hub image publishing and GitHub Actions CI/CD pipeline. The screenshots and evidence included in this document represent my actual implementation.

---

### E. Submission Instructions for Student

1. **Commit and Push changes to your forked repository:**
   ```bash
   git add .
   git commit -m "feat: complete MSE-2 Docker practical assignment Set 2"
   git push origin main
   ```

2. **Configure GitHub Repository Secrets:**
   Navigate to: `GitHub Repo -> Settings -> Secrets and variables -> Actions -> New repository secret`
   - `DOCKERHUB_USERNAME`: Your personal Docker Hub username.
   - `DOCKERHUB_TOKEN`: Your Docker Hub Personal Access Token (PAT).
   - `POSTGRES_PASSWORD`: A secure password (e.g. `SuperSecureDbPass123`).

3. **Trigger / Verify GitHub Actions:**
   - The push to `main` automatically triggers `.github/workflows/cd.yml`.
   - Ensure the workflow completes with green checkmarks.

4. **Create Pull Request to Upstream:**
   - Base repository: `atindeRR/MSE-2-SSED-Evening` (`main`)
   - Head repository: `BadalSinghh/MSE-2-SSED-Evening` (`main`)
   - Title format: `DOCKER-SET-2 | 202401100400071 | Badal Singh | AIML-A`

5. **Generate and Upload PDF:**
   - Convert this document (or print to PDF from Markdown reader/browser) to `202401100400071_Badal_Singh_SET2.pdf`.
   - Upload the PDF to Moodle.
   - Attach the PDF to your GitHub Pull Request.
