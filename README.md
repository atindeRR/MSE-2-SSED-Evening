# TaskFlow - Full-Stack Multi-Tier DevOps Containerization Project

## Examination Details
- **Subject:** Software Engineering and DevOps (Mid-Semester Examination – 2)
- **Set:** Set 2 – Evening Shift
- **Student Name:** Akshat Anand
- **Roll Number:** 202401100400022
- **Section:** A
- **Branch:** CSE(AIML)
- **Repository:** [Akshat-Anand-Mse2-](https://github.com/AkshatAnand007/Akshat-Anand-Mse2-)
- **Working Branch:** `devops-implementation`
- **Docker Hub Profile:** [akshatanand007](https://hub.docker.com/u/akshatanand007)

---

## 1. Project Overview & Architecture

**TaskFlow** is an enterprise-grade full-stack task management web application built with modern cloud-native DevOps principles. The system implements a robust 4-tier microservices architecture containerized using Docker and orchestrated using Docker Compose.

```
                           [ Web Browser / Client ]
                                      │
                         (Port 8080)  │  (Port 3000 - API)
                                      ▼
             ┌──────────────────────────────────────────────────┐
             │             Frontend Service (Nginx)             │
             │   • Serves compiled React 18 SPA static assets   │
             │   • Reverse proxies `/api/*` and `/health`       │
             └────────────────────────┬─────────────────────────┘
                                      │ (taskflow bridge network)
                                      ▼
             ┌──────────────────────────────────────────────────┐
             │              Backend API (Node.js)               │
             │   • Express REST API                             │
             │   • JWT Authentication & bcrypt password hashing │
             │   • Dynamic task caching with invalidation       │
             │   • Health check endpoint (`/health`)            │
             └─────────────────┬──────────────┬─────────────────┘
                               │              │
                               ▼              ▼
             ┌───────────────────────┐  ┌───────────────────────┐
             │   PostgreSQL DB 16    │  │     Redis 7 Cache     │
             │  • Persistent Volume  │  │  • Fast Task Caching  │
             │  • User & Task Schema │  │  • 30-sec TTL & Purge │
             │  • Port 5432 (int)    │  │  • Port 6379 (int)    │
             └───────────────────────┘  └───────────────────────┘
```

### Key Architectural Characteristics
- **Network Isolation:** Internal services (`postgres`, `redis`) do not expose their ports to the host machine. Only `frontend` (port 8080) and `backend` (port 3000) are mapped to the host.
- **Service Discovery:** All containers communicate via service names (`postgres`, `redis`, `backend`) over an isolated custom bridge network (`taskflow`).
- **Data Durability:** Relational database data persists independently of container lifecycles through a named Docker volume (`postgres_data`).
- **Resilient Startup:** Compose `depends_on` rules with `condition: service_healthy` prevent race conditions by ensuring the database and cache are ready before the backend starts.

---

## 2. Technology Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **Frontend** | React, Vite | React 18.3.1, Vite 5.4.11 | Single Page Application (SPA) UI |
| **Web Server / Proxy** | Nginx Alpine | 1.27-alpine | High-performance static web server & reverse proxy |
| **Backend API** | Node.js, Express | Node 20, Express 4.21.2 | RESTful API backend handling auth & business logic |
| **Database** | PostgreSQL Alpine | 16-alpine | ACID-compliant relational persistence store |
| **Cache Store** | Redis Alpine | 7-alpine | In-memory key-value cache for API speedup |
| **Containerization** | Docker, Compose | Engine v29+, Compose v5+ | Multi-stage image build & multi-container orchestration |
| **CI/CD** | GitHub Actions | Workflows `ci.yml`, `cd.yml` | Automated Hadolint validation, build, Hub push & deploy |
| **Testing** | Jest, Supertest | Jest 29.7, Supertest 7.0 | Automated end-to-end API integration tests |

---

## 3. Project Directory Structure

```
Akshat-Anand-Mse2-/
├── .github/
│   └── workflows/
│       ├── ci.yml                 # Instructor evaluation & Hadolint validation pipeline
│       └── cd.yml                 # Automated Docker Hub push & image deploy pipeline
├── backend/
│   ├── db/
│   │   └── init.sql               # PostgreSQL initial schema (users and tasks tables)
│   ├── src/
│   │   ├── app.js                 # Express routes, controllers, and cache logic
│   │   ├── auth.js                # JWT verification middleware
│   │   ├── config.js              # Environment variable configurations
│   │   ├── db.js                  # PostgreSQL pool and connection retry loop
│   │   ├── redis.js               # Redis client connection and error handling
│   │   └── server.js              # Application entrypoint & graceful shutdown handlers
│   ├── .dockerignore              # Excludes node_modules, .env, tests
│   ├── Dockerfile                 # Optimized multi-stage Node.js production container
│   └── package.json               # Backend dependencies (pg, redis, bcryptjs, jwt, etc.)
├── frontend/
│   ├── src/
│   │   ├── main.jsx               # React UI component tree & API client calls
│   │   └── style.css              # Custom styling
│   ├── .dockerignore              # Excludes node_modules, dist, .env
│   ├── Dockerfile                 # Multi-stage build (Node build + Nginx runtime)
│   ├── index.html                 # Single page application HTML shell
│   ├── nginx.conf                 # Nginx reverse proxy configuration
│   ├── package.json               # Frontend dependencies (React, Vite)
│   └── vite.config.js             # Vite build settings
├── tests/
│   ├── api.test.js                # 12 Automated integration test cases (TC01-TC12)
│   ├── jest.config.js             # Jest configuration
│   └── package.json               # Test dependencies (jest, supertest)
├── .env.example                   # Environment configuration template
├── .gitignore                     # Git ignore rules (.env, node_modules, etc.)
├── docker-compose.yml             # Local build & multi-service development compose
├── docker-compose.deploy.yml      # Production deployment compose using Docker Hub images
├── submission.json                # Student identity metadata
└── README.md                      # Complete project documentation
```

---

## 4. Dockerfiles Implementation & Explanations

### Frontend Dockerfile (`frontend/Dockerfile`)
The frontend uses a **multi-stage build** to optimize image size and security:
- **Build Stage (`node:20-slim`):** Installs package dependencies, copies source files, and runs `npm run build` with Vite.
- **Production Stage (`nginx:1.27-alpine`):** Copies only the compiled HTML/JS/CSS artifacts from `/app/dist` to `/usr/share/nginx/html`.
- **Reverse Proxy:** Includes `nginx.conf` to route `/api/*` and `/health` requests to `backend:3000` internally, avoiding cross-origin issues and eliminating hardcoded backend hostnames.
- **Port & Health Check:** Exposes port `80` and includes a `wget` healthcheck.
- **Hadolint Compliance:** Passes Hadolint with zero warnings (proper JSON notation, pinned base tags).

### Backend Dockerfile (`backend/Dockerfile`)
The backend is packaged into a lean, secure production container:
- **Dependencies Stage:** Uses `node:20-alpine`, copies `package*.json`, and runs `npm install --omit=dev` to install only production dependencies.
- **Production Runtime Stage:** Sets `NODE_ENV=production`, copies the pruned `node_modules` and `src/` source code.
- **Non-Root Execution:** Runs under non-root numeric user `USER 1000:1000` (Node user) for container security hardening.
- **Port & Entrypoint:** Exposes port `3000` and executes `CMD ["npm", "start"]`.
- **Hadolint Compliance:** Passes Hadolint with zero warnings.

---

## 5. Docker Compose Configurations

### Local Build Orchestration (`docker-compose.yml`)
Builds services from local source code:
- **`postgres`:** Official `postgres:16-alpine` image with healthcheck `pg_isready -U taskflow_user -d taskflow`. Mounts `./backend/db/init.sql` to initialize tables automatically on first start.
- **`redis`:** Official `redis:7-alpine` with `--appendonly yes` persistence and `redis-cli ping` healthcheck.
- **`backend`:** Builds `./backend`, connects to postgres and redis using internal DNS service names. Health check runs Node HTTP probe against `/health`.
- **`frontend`:** Builds `./frontend`, maps port `8080:80`. Depends on backend health.

### Production Image-Based Deployment (`docker-compose.deploy.yml`)
Deploys pre-built images published on Docker Hub without building from local source:
```yaml
services:
  backend:
    image: akshatanand007/backend:latest
    ...
  frontend:
    image: akshatanand007/frontend:latest
    ...
```

---

## 6. Docker Hub Image Publishing

The Docker images have been built, tagged, and published to Docker Hub under the username `akshatanand007`:

| Service | Repository & Tags | Docker Hub Direct Link |
|---|---|---|
| **Frontend** | `akshatanand007/frontend:v1`<br>`akshatanand007/frontend:latest` | [hub.docker.com/r/akshatanand007/frontend](https://hub.docker.com/r/akshatanand007/frontend) |
| **Backend** | `akshatanand007/backend:v1`<br>`akshatanand007/backend:latest` | [hub.docker.com/r/akshatanand007/backend](https://hub.docker.com/r/akshatanand007/backend) |

### Tagging and Publishing Commands:
```bash
# Frontend
docker tag akshat-anand-mse2--frontend akshatanand007/frontend:v1
docker tag akshat-anand-mse2--frontend akshatanand007/frontend:latest
docker push akshatanand007/frontend:v1
docker push akshatanand007/frontend:latest

# Backend
docker tag akshat-anand-mse2--backend akshatanand007/backend:v1
docker tag akshat-anand-mse2--backend akshatanand007/backend:latest
docker push akshatanand007/backend:v1
docker push akshatanand007/backend:latest
```

---

## 7. Networking, Persistence & Health Check Verification

### A. Health Checks
All services implement native Docker health checks:
```bash
docker compose ps
```
Output:
```
NAME                            IMAGE                         STATUS
akshat-anand-mse2--backend-1    akshat-anand-mse2--backend    Up (healthy)
akshat-anand-mse2--frontend-1   akshat-anand-mse2--frontend   Up (healthy)
akshat-anand-mse2--postgres-1   postgres:16-alpine            Up (healthy)
akshat-anand-mse2--redis-1      redis:7-alpine                Up (healthy)
```

### B. Service DNS Resolution
Verified from within the backend container:
```bash
docker compose exec backend getent hosts postgres
# Output: 172.18.0.2 postgres postgres

docker compose exec backend getent hosts redis
# Output: 172.18.0.3 redis redis
```

### C. PostgreSQL Data Persistence Test
1. Inserted a test record into PostgreSQL database:
   ```bash
   docker compose exec postgres psql -U taskflow_user -d taskflow -c "SELECT id, title, status FROM tasks;"
   # Output: id: 2 | Persistence Test Task | Completed
   ```
2. Stopped and removed the PostgreSQL container:
   ```bash
   docker compose stop postgres
   docker compose rm -f postgres
   ```
3. Recreated and started the PostgreSQL container using the named volume `postgres_data`:
   ```bash
   docker compose up -d postgres
   ```
4. Queried the database again:
   ```bash
   docker compose exec postgres psql -U taskflow_user -d taskflow -c "SELECT id, title, status FROM tasks;"
   # Output: id: 2 | Persistence Test Task | Completed (1 row) -> Verified Persisted!
   ```

### D. Redis Restart Test
```bash
docker compose restart redis
docker compose exec redis redis-cli ping
# Output: PONG
```

---

## 8. Automated Integration Testing

The project includes 12 automated Jest + Supertest integration tests in `tests/api.test.js`:

```bash
cd tests
npm install
$env:NODE_OPTIONS="--experimental-vm-modules"
npm test
```

### Test Suite Results:
- **`TC01`**: `GET /health` confirms API, PostgreSQL and Redis are healthy (Status 200).
- **`TC02`**: `POST /api/auth/register` creates new user (Status 201).
- **`TC03`**: Rejects duplicate email registration (Status 409).
- **`TC04`**: `POST /api/auth/login` verifies credentials and issues JWT token (Status 200).
- **`TC05`**: Rejects unauthenticated task requests (Status 401).
- **`TC06`**: `POST /api/tasks` creates a task associated with user (Status 201).
- **`TC07`**: `GET /api/tasks` retrieves tasks from PostgreSQL and caches in Redis.
- **`TC08`**: Subsequent `GET /api/tasks` is served directly from `redis-cache`.
- **`TC09`**: `PATCH /api/tasks/:id` updates status and invalidates Redis cache.
- **`TC10`**: Rejects invalid task status updates (Status 400).
- **`TC11`**: `DELETE /api/tasks/:id` deletes task and invalidates cache (Status 200).
- **`TC12`**: Confirms deleted task is no longer present in task list.

**Result: 12 passed, 12 total (100% pass rate).**

---

## 9. GitHub Actions CI/CD Pipeline

The repository provides two GitHub Actions workflows:

### 1. `ci.yml` (Instructor Continuous Integration)
Triggered on Pull Requests to `main`:
- Checks for required files (`Dockerfile`, `docker-compose.yml`, `submission.json`).
- Validates Dockerfiles with **Hadolint**.
- Builds images and starts stack with Docker Compose.
- Awaits backend and frontend health.
- Runs the 12 automated API tests.
- Verifies PostgreSQL volume persistence.

### 2. `cd.yml` (Continuous Delivery & Deployment)
Triggered on push to `main`:
- Authenticates with Docker Hub using repository secrets (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`).
- Builds frontend and backend images via Docker Buildx.
- Tags images with `v1` and `latest`.
- Pushes all 4 tags to Docker Hub.
- Deploys the stack using `docker-compose.deploy.yml` with pre-built Docker Hub images.
- Validates health endpoints and executes the full test suite against the live deployment.

---

## 10. How to Run the Application

### Option A: Image-Based Deployment (Recommended)
```bash
# 1. Clone repository
git clone https://github.com/AkshatAnand007/Akshat-Anand-Mse2-.git
cd Akshat-Anand-Mse2-

# 2. Deploy using published Docker Hub images
docker compose -f docker-compose.deploy.yml up -d

# 3. Access the application in your browser:
#    Frontend: http://localhost:8080
#    Backend API Health: http://localhost:3000/health
```

### Option B: Local Source Build
```bash
# 1. Copy sample environment file
cp .env.example .env

# 2. Build and start containers
docker compose up -d --build

# 3. View running containers and logs
docker compose ps
docker compose logs -f
```

---

## 11. Final Submission Verification Checklist
- [x] Repository forked into personal account (`AkshatAnand007`).
- [x] Dedicated branch `devops-implementation` created and maintained.
- [x] Frontend Dockerfile implemented (multi-stage build, Nginx runtime, Hadolint compliant).
- [x] Backend Dockerfile implemented (production Node.js, non-root user, Hadolint compliant).
- [x] `docker-compose.yml` configured with custom network, named volume, healthchecks.
- [x] Images built and tagged with `v1` and `latest`.
- [x] All 4 tags pushed to Docker Hub (`akshatanand007/frontend`, `akshatanand007/backend`).
- [x] `docker-compose.deploy.yml` tested with image-based deployment (no `build:` directives).
- [x] Networking, DNS resolution, and Redis restart verified.
- [x] PostgreSQL persistence verified after container removal.
- [x] All 12 automated API integration tests passed.
- [x] GitHub Actions CD pipeline configured.
- [x] Examination PDF documentation generated.
