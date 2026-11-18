# TaskFlow - Docker & DevOps Viva Preparation Guide

**Subject:** Software Engineering and DevOps (AI310B)  
**Examination:** MSE-2 Practical Examination (Set 2 – Evening Shift)  
**Student:** Anubhav Singh  
**Repository:** [Anubhavspeaks01/MSE-2-SSED-Evening](https://github.com/Anubhavspeaks01/MSE-2-SSED-Evening)  
**Docker Hub:** `anubha9889`

---

## 1. Core Concepts & Practical Implementation

### 1. Why is Docker used?
Docker provides lightweight, OS-level virtualization through containers. It solves the classic *"it works on my machine"* problem by packaging the application code, runtime, system tools, and dependencies into an immutable container image that runs identically on development, CI/CD runners, and production servers.
- **In our project:** We containerized the React frontend, Node/Express backend, PostgreSQL database, and Redis cache so the entire multi-tier stack runs with a single command without installing Node.js, Postgres, or Redis on the host.

### 2. What is a Dockerfile?
A text file containing declarative instructions that the Docker engine reads sequentially to assemble a container image.
- **In our project:** We wrote `frontend/Dockerfile` and `backend/Dockerfile`.

### 3. What is a multi-stage build?
A Docker build pattern using multiple `FROM` instructions. Intermediate stages compile code or install dependencies, and only the final artifacts are copied into a clean, minimal runtime image.
- **In our frontend:** 
  - *Build stage (`node:20-slim`):* Installs all dependencies via `npm ci` and runs `npm run build` using Vite.
  - *Runtime stage (`nginx:stable-alpine`):* Copies only the compiled static `/dist` directory to `/usr/share/nginx/html`. Node.js and build tools are completely discarded, keeping image size around 25MB.
- **In our backend:**
  - *Dependencies stage (`node:20-alpine`):* Installs production dependencies (`npm install --omit=dev`).
  - *Production stage (`node:20-alpine`):* Copies only `node_modules`, `src`, and `package.json`.

### 4. Difference between CMD and ENTRYPOINT
- **ENTRYPOINT:** Sets the default executable that will always run when the container starts.
- **CMD:** Supplies default arguments to ENTRYPOINT or acts as the fallback command. Parameters passed to `docker run` easily override `CMD`, but append to `ENTRYPOINT`.
- **In our project:** 
  - Backend: `CMD ["npm", "start"]` runs `node src/server.js`.
  - Frontend: `CMD ["nginx", "-g", "daemon off;"]` starts Nginx in foreground mode.

### 5. Difference between COPY and ADD
- **COPY:** Safely copies files and directories from the local build context into the container filesystem.
- **ADD:** Does everything COPY does, but also automatically extracts local `.tar` archives and can download files from remote URLs.
- *Best practice:* Always prefer `COPY` unless automatic tar extraction is explicitly required.

---

## 2. Docker Compose & Container Architecture

### 6. What is Docker Compose?
A tool for defining and running multi-container Docker applications using a single YAML configuration file (`docker-compose.yml`). It orchestrates services, networks, volumes, and health dependencies together.
docker network inspect mse-2-ssed-evening_app-network --format '{{json .Containers}}'ess.
- **In our project:** 
  - Backend connects to DB using `postgresql://taskflow_user:password@postgres:5432/taskflow`.
  - Backend connects to Redis using `redis://redis:6379`.
  - Nginx reverse proxies API calls to `http://backend:3000/api/`.

### 9. What is a Docker volume?
A persistent data storage mechanism managed directly by Docker on the host filesystem (in `/var/lib/docker/volumes/` on Linux). Volume lifecycle is decoupled from container lifecycle: data persists even if the container is stopped, deleted, or upgraded.

### 10. Difference between Volume and Bind Mount
- **Named Volume (e.g., `postgres_data`):** Managed entirely by Docker. Portable, safe from accidental deletion, optimal performance on all platforms.
- **Bind Mount (e.g., `./backend/db/init.sql:/docker-entrypoint-initdb.d/init.sql:ro`):** Directly maps a specific host directory or file into the container. Ideal for configuration files or live source-code development.

### 11. What are health checks?
Commands executed periodically inside a container to determine if the application is running correctly and ready to receive traffic (beyond merely checking if the PID is alive).
- **In our project:**
  - `postgres`: `pg_isready -U taskflow_user -d taskflow`
  - `redis`: `redis-cli ping` (returns `PONG`)
  - `backend`: `node -e "fetch('http://127.0.0.1:3000/health').then(...)"` checks API, Postgres pool, and Redis connection.

### 12. What is `depends_on` with `condition: service_healthy`?
Controls service startup order and dependency readiness. Standard `depends_on` only waits for a container to reach the *running* state. With `condition: service_healthy`, Docker Compose waits until the prerequisite service's health check passes before launching the dependent service.
- **In our project:**
  - `backend` waits for `postgres` and `redis` to be healthy before starting.
  - `frontend` waits for `backend` to be healthy before starting.

### 13. Difference between `build` and `image` in Docker Compose
- **`build:`** Tells Compose to build a container image locally from a Dockerfile path before running.
- **`image:`** Tells Compose to directly pull or run a pre-built image from a registry (e.g., Docker Hub).
- **In our project:**
  - `docker-compose.yml` uses `build:` for frontend and backend (development).
  - `docker-compose.deploy.yml` uses `image: anubha9889/frontend:latest` and `image: anubha9889/backend:latest` without any `build:` section (production deployment).

---

## 3. Deployment, Security & CI/CD

### 14. What is Docker Hub?
A cloud-based container registry service for storing, sharing, and distributing container images publicly or privately.
- **In our project:** We publish:
  - `anubha9889/frontend:v1` and `anubha9889/frontend:latest`
  - `anubha9889/backend:v1` and `anubha9889/backend:latest`

### 15. What is CI/CD?
- **CI (Continuous Integration):** Automates linting, building, and running automated tests whenever code is pushed or a PR is opened.
- **CD (Continuous Delivery / Deployment):** Automates packaging images, tagging them, publishing to a registry, and deploying to a production or staging environment.

### 16. What are GitHub Actions?
A native CI/CD workflow automation platform integrated into GitHub. Workflows are defined in `.github/workflows/*.yml` and run on GitHub-hosted Ubuntu runners triggered by events like `push`, `pull_request`, or `workflow_dispatch`.

### 17. What are GitHub Secrets?
Encrypted environment variables stored securely in GitHub repository settings (`Settings → Secrets and variables → Actions`). They protect sensitive credentials (e.g., `DOCKERHUB_TOKEN`, `POSTGRES_PASSWORD`) from being exposed in git history, pull requests, or workflow execution logs.

### 18. Why use Nginx?
Nginx is a high-performance, asynchronous web server and reverse proxy with low memory footprint (~10MB).
- **In our frontend:**
  1. Serves static compiled React assets efficiently.
  2. Handles SPA client-side routing via `try_files $uri $uri/ /index.html;`.
  3. Acts as a reverse proxy: requests to `/api/*` are forwarded to the internal `backend:3000`, eliminating browser CORS issues.

### 19. Why use Alpine images?
Alpine Linux is a security-oriented, ultra-minimal Linux distribution based on musl libc and BusyBox. Its base image is only ~5MB (compared to ~100MB+ for Ubuntu/Debian). Using Alpine minimizes attack surface and drastically reduces build and download times.

### 20. What happens when a PostgreSQL container is deleted?
Because database data is stored in the named volume `postgres_data` mapped to `/var/lib/postgresql/data`, stopping or removing the PostgreSQL container (`docker rm -f`) **does not delete the database**. When a new container is created with the same named volume attached, all tables and records remain intact.

### 21. How does image-based deployment work?
The deployment server only needs `docker-compose.deploy.yml` and a `.env` file. It does not need the application source code, git repository, or development compilers. It simply pulls pre-built, tested images directly from Docker Hub (`docker compose -f docker-compose.deploy.yml up -d`).
