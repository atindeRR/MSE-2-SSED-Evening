# TaskFlow – Docker Implementation Notes (DOCKER-SET-2)

This file explains what was implemented for each task and how to run and verify it.

## Files added or changed

| File | Purpose |
|---|---|
| `frontend/Dockerfile` | Multi-stage build: `node:22-slim` builds the Vite bundle, `nginx:1.27-alpine` serves only `dist/` |
| `backend/Dockerfile` | `node:22-alpine`, `npm ci --omit=dev`, `NODE_ENV=production`, non-root user, `HEALTHCHECK` |
| `frontend/.dockerignore`, `backend/.dockerignore` | Keep `node_modules`, `.env`, tests, VCS files out of the build context |
| `frontend/package-lock.json`, `backend/package-lock.json` | Reproducible installs with `npm ci` |
| `frontend/nginx.conf` | SPA routing plus a reverse proxy for `/api` and `/health` to `backend:3000` |
| `backend/src/db.js` | Added a `pool.on('error')` listener so the API survives a PostgreSQL restart |
| `docker-compose.yml` | Local build and run: 4 services, custom network, named volume, health checks |
| `docker-compose.deploy.yml` | Deployment from Docker Hub images (`latest`), no `build:` |
| `.github/workflows/cd.yml` | CI/CD: build, tag `v1` and `latest`, push, deploy, verify |
| `.env.example` | Template for the `.env` file (the real `.env` is git-ignored) |

## Task 1 – Dockerfiles

**Frontend (multi-stage)**

1. `build` stage (`node:22-slim`). It copies the `package*.json` files first and runs `npm ci`, so the dependency layer is cached. Then it copies the sources and runs `npm run build`.
   The Debian slim image is used because Vite's Rollup native parser fails on Alpine's musl libc ("Code is nested too deeply"). This stage is discarded, so its size does not matter.
2. `runtime` stage (`nginx:1.27-alpine`, about 48 MB). Only `/app/dist` and `nginx.conf` are copied. No Node.js, no `node_modules` and no source code end up in the final image. It exposes port 80.

**Backend**

- `node:22-alpine` base, `NODE_ENV=production`.
- Manifests are copied first, then `npm ci --omit=dev && npm cache clean --force` installs production dependencies only.
- Only `src/` is copied. `.dockerignore` excludes tests, `.env` and `node_modules`.
- Runs as the unprivileged `node` user (uid 1000), exposes 3000, and has a `HEALTHCHECK` that calls `/health`.

Both Dockerfiles pass `hadolint` with no warnings.

## Task 2 – Compose networking and health checks

- **Custom network.** `taskflow-network` is a bridge network. Docker's embedded DNS (127.0.0.11) resolves service names on it, so the backend uses `postgres:5432` and `redis:6379`.
- **Named volume.** `taskflow-postgres-data` is mounted at `/var/lib/postgresql/data`. Data lives outside the container, so `docker compose rm -s -f postgres` followed by `up` keeps the data.
- **Schema.** `backend/db/init.sql` is mounted into `/docker-entrypoint-initdb.d`. It runs only the first time the volume is initialised.
- **Health checks.**
  - PostgreSQL uses `pg_isready`.
  - Redis uses `redis-cli ping`.
  - The backend uses `GET /health`, which itself checks PostgreSQL and Redis.
  - The frontend uses `wget` on `/`.
- **Startup order.** The backend waits for `service_healthy` on postgres and redis. The frontend waits for `service_healthy` on the backend.
- **Ports.** Only the frontend (8080→80) and backend (3000) are published. PostgreSQL and Redis have no `ports:` entry and are reachable only inside the network.
- **Environment.** All values come from `.env`. `POSTGRES_PASSWORD` and `JWT_SECRET` are mandatory (`${VAR:?}`), and nothing secret is hardcoded.
- **Nginx.** Nginx uses `resolver 127.0.0.11` with a variable upstream. It re-resolves `backend` at request time, so it keeps working after the backend container is recreated with a new IP.

## Task 3 – Docker Hub images

The workflow (and the manual commands below) publish these tags:

```
<DOCKERHUB_USERNAME>/frontend:v1    <DOCKERHUB_USERNAME>/frontend:latest
<DOCKERHUB_USERNAME>/backend:v1     <DOCKERHUB_USERNAME>/backend:latest
```

Manual publishing:

```bash
docker login -u <DOCKERHUB_USERNAME>
docker build -t <DOCKERHUB_USERNAME>/frontend:v1 -t <DOCKERHUB_USERNAME>/frontend:latest ./frontend
docker build -t <DOCKERHUB_USERNAME>/backend:v1  -t <DOCKERHUB_USERNAME>/backend:latest  ./backend
docker push <DOCKERHUB_USERNAME>/frontend:v1 && docker push <DOCKERHUB_USERNAME>/frontend:latest
docker push <DOCKERHUB_USERNAME>/backend:v1  && docker push <DOCKERHUB_USERNAME>/backend:latest
```

## Task 4 – Image-based deployment

`docker-compose.deploy.yml` uses `image: ${DOCKERHUB_USERNAME}/frontend:latest` and `.../backend:latest` with `pull_policy: always`. It has no `build:` entries. PostgreSQL and Redis use the official `postgres:16-alpine` and `redis:7-alpine` images. It keeps the same network, volume, health checks and dependencies as the local file.

```bash
cp .env.example .env        # set DOCKERHUB_USERNAME, POSTGRES_PASSWORD, JWT_SECRET
docker compose -f docker-compose.deploy.yml up -d
docker compose -f docker-compose.deploy.yml ps
```

The app is served at http://localhost:8080 and the API at http://localhost:3000/health.

## Task 5 – Verification commands

```bash
# 1. frontend -> backend
curl http://localhost:8080/health
docker compose exec frontend wget -qO- http://backend:3000/health
# 2 & 3. backend resolves postgres / redis by service name
docker compose exec backend getent hosts postgres
docker compose exec backend getent hosts redis
# 4. persistence
docker compose exec postgres psql -U taskflow_user -d taskflow -c "SELECT id,title FROM tasks;"
docker compose rm -s -f postgres
docker compose up -d postgres
docker compose exec postgres psql -U taskflow_user -d taskflow -c "SELECT id,title FROM tasks;"
# 5. redis restart
docker compose restart redis && docker compose exec redis redis-cli ping
# 6. health status
docker inspect --format '{{.Name}} {{.State.Health.Status}}' $(docker compose ps -q)
```

## Task 6 – GitHub Actions (`.github/workflows/cd.yml`)

The workflow triggers on `push` to `main` (and on manual dispatch). Its steps are numbered to match the exam:

1. Checkout.
2. Set up Buildx.
3. Build the frontend.
4. Build the backend.
5. Log in to Docker Hub with secrets.
6. Tag `v1` and `latest`.
7. Push all four tags.
8. Deploy with `docker-compose.deploy.yml`, after deleting the local images so they must be pulled from Docker Hub.
9. Verify: every service is healthy, `/health` responds, the frontend responds, the frontend→backend proxy works, and service DNS resolves. Then run the API test suite.

Required repository secrets are `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` and `POSTGRES_PASSWORD`. `JWT_SECRET` is generated randomly on each run, so no credential appears in the repository.
