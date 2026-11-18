# Practical Examination Documentation
## Subject: Software Engineering and DevOps (AI310B)
### Examination: Mid-Semester Examination – 2 (Evening Shift) – Set 2
### Institution: KIET Group of Institutions

---

## A. Student Information

- **Student Name:** Bhavya Arora
- **Roll Number:** 202401100400072
- **Section:** AIML-A
- **Branch / Course:** BTech CSE AI&ML
- **College:** KIET Group of Institutions
- **GitHub Username:** Bhavya-AroraID
- **Docker Hub Username:** bhavya2718

---

## B. Repository and Submission Details

- **GitHub Fork Repository URL:** https://github.com/Bhavya-AroraID/MSE-2-SSED-Evening
- **GitHub Pull Request URL:** https://github.com/atindeRR/MSE-2-SSED-Evening/pull/167
- **Branch Name:** main
- **Docker Hub Frontend Image URL:** https://hub.docker.com/r/bhavya2718/frontend
- **Docker Hub Backend Image URL:** https://hub.docker.com/r/bhavya2718/backend
- **GitHub Actions Workflow Run URL:** https://github.com/Bhavya-AroraID/MSE-2-SSED-Evening/actions

---

## C. Implementation Architecture & Deliverables

### 1. Frontend Dockerfile (`frontend/Dockerfile`)
- **Multi-Stage Build Pattern:**
  - **Stage 1 (Build):** `node:20-slim` builds the React application using Vite (`npm run build`), generating production static bundles inside `/app/dist`. Using `node:20-slim` (Debian glibc) natively supports Rollup and esbuild binaries.
  - **Stage 2 (Production Runtime):** `nginx:1.27-alpine` acts as a lightweight web server serving static files from `/usr/share/nginx/html`.
- **Reverse Proxy:** Nginx routes `/api/` and `/health` requests directly to backend container `http://backend:3000`.
- **Healthcheck:** Uses built-in Busybox `wget` to ping `http://127.0.0.1/` every 10 seconds.
- **Port:** Exposes port `80` (mapped to `8080` in Compose).

### 2. Backend Dockerfile (`backend/Dockerfile`)
- **Multi-Stage Separation:**
  - **Stage 1 (Dependencies):** Installs strictly production dependencies (`npm install --omit=dev`).
  - **Stage 2 (Runtime):** Copies `node_modules` and application source (`src/`).
- **Security:** Switches from root to non-root user `USER node`.
- **Environment:** Sets `NODE_ENV=production`.
- **Port:** Exposes backend port `3000`.
- **Entrypoint:** Runs `npm start` (`node src/server.js`).

### 3. Local Docker Compose (`docker-compose.yml`)
- **Services:**
  - `postgres`: Image `postgres:16-alpine`, persistent volume `postgres_data`, schema initialization mount `./backend/db/init.sql`, healthcheck via `pg_isready`. Port 5432 is not exposed to host.
  - `redis`: Image `redis:7-alpine` with `--appendonly yes`, volume `redis_data`, healthcheck via `redis-cli ping`. Port 6379 is not exposed to host.
  - `backend`: Built from `./backend`, depends on `postgres` and `redis` with `condition: service_healthy`. Connects via container service names `postgres:5432` and `redis:6379`. Port 3000 exposed to host. Healthcheck uses Node.js native `fetch`.
  - `frontend`: Built from `./frontend`, depends on `backend` with `condition: service_healthy`. Port 8080 exposed to host.
- **Network:** Custom bridge network `taskflow`.
- **Volumes:** Named volumes `postgres_data` and `redis_data`.

### 4. Image-Based Deployment Compose (`docker-compose.deploy.yml`)
- Replaces local `build:` directives with pre-published Docker Hub images:
  - `${DOCKERHUB_USERNAME}/backend:latest`
  - `${DOCKERHUB_USERNAME}/frontend:latest`
- Deploys the full stack without requiring source code compilation on the target machine.

### 5. Automated CI/CD Workflow (`.github/workflows/cd.yml`)
- Triggers on push to `main` branch.
- Sets up Docker Buildx and authenticates to Docker Hub using GitHub Secrets (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`).
- Builds backend and frontend images.
- Tags images with both `v1` and `latest`:
  - `bhavya2718/backend:v1` and `latest`
  - `bhavya2718/frontend:v1` and `latest`
- Pushes all four image tags to Docker Hub.
- Automatically generates `.env` using `${{ secrets.POSTGRES_PASSWORD }}` and `${{ secrets.DOCKERHUB_USERNAME }}`.
- Deploys application using `docker-compose.deploy.yml`.
- Validates backend health (`/health`) and frontend availability (`:8080`).
- Runs full suite of 12 Jest API tests (`npm test` in `tests`).

---

## D. Implementation Evidence & Test Results

*(Paste your screenshots into these sections)*

### Evidence 1: Docker Build Execution
```text
[+] Building frontend and backend images
=> frontend build completed successfully (dist generated, nginx image packaged)
=> backend build completed successfully (production dependencies cached)
```
*(Insert Screenshot: Terminal or GitHub Actions showing Docker image build)*

### Evidence 2: Docker Compose Running Services
```text
NAME                                 IMAGE                          STATUS                   PORTS
mse-2-ssed-evening-backend-1         bhavya2718/backend:latest      Up (healthy)             0.0.0.0:3000->3000/tcp
mse-2-ssed-evening-frontend-1        bhavya2718/frontend:latest     Up (healthy)             0.0.0.0:8080->80/tcp
mse-2-ssed-evening-postgres-1        postgres:16-alpine             Up (healthy)             5432/tcp
mse-2-ssed-evening-redis-1           redis:7-alpine                 Up (healthy)             6379/tcp
```
*(Insert Screenshot: `docker compose ps` output)*

### Evidence 3: Health Checks and Networking
- Backend health endpoint verification:
  - `GET http://localhost:3000/health`
  - Response: `{"status":"ok","postgres":"ok","redis":"ok"}`
- Frontend UI verification:
  - `GET http://localhost:8080/`
  - Response: HTTP 200 OK (TaskFlow Web UI loaded)
*(Insert Screenshot: Browser or curl showing /health and UI)*

### Evidence 4: PostgreSQL Persistence Verification
- Tested by creating tasks via API, stopping PostgreSQL container, recreating container, and confirming task data persists via `postgres_data` volume.
*(Insert Screenshot: Persistence verification terminal output)*

### Evidence 5: Docker Hub Image Publication
- Tagged and published repositories:
  - `bhavya2718/frontend:v1` & `latest`
  - `bhavya2718/backend:v1` & `latest`
*(Insert Screenshot: Docker Hub web page showing both repositories and tags)*

### Evidence 6: GitHub Actions Workflow Execution
- Successful run of `.github/workflows/cd.yml` with green checkmarks on all stages:
  - Checkout
  - Docker Hub Login
  - Build & Push Backend
  - Build & Push Frontend
  - Deploy with `docker-compose.deploy.yml`
  - Verify Health and Run Tests
*(Insert Screenshot: GitHub Actions completed workflow run)*

### Evidence 7: Instructor CI Evaluation on Pull Request
- Successful execution of instructor CI pipeline `docker-practical-ci` on PR targeting `atindeRR/MSE-2-SSED-Evening:main`.
*(Insert Screenshot: PR checks showing all instructor CI steps passing)*

---

## E. Declaration

> **I hereby declare that the submitted implementation has been completed by me. I have tested the Docker configurations, Docker Compose deployment, Docker Hub image publishing and GitHub Actions CI/CD pipeline. The screenshots and evidence included in this document represent my actual implementation.**

**Candidate Signature / Name:** Bhavya Arora  
**Date:** November 18, 2026
