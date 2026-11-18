# TaskFlow – Docker & CI/CD Implementation (Set 2, Evening Shift)

Implementation of the MSE-2 practical: containerised full-stack application with
Docker Compose, health checks, persistent storage, Docker Hub publishing and a
GitHub Actions CD pipeline.

## Student

| Field | Value |
|---|---|
| Name | Satyam Kumar |
| Roll number | 202401100400167 |
| Section | C |
| Branch | AIML |
| GitHub | [Satyam-1o](https://github.com/Satyam-1o) |
| Docker Hub | [satyam3120](https://hub.docker.com/u/satyam3120) |

## Architecture

```
                       host :8080                    host :3000
                           |                             |
                     +-----v------+               +------v------+
                     |  frontend  |               |   backend   |
                     | nginx:1.27 |               | node:20     |
                     +-----+------+               +---+-----+---+
                           |  /api/, /health proxy    |     |
                           +--------------------------+     |
                                    taskflow-net           |
                              +-------------+--------------+
                              |                            |
                        +-----v-----+                +-----v-----+
                        | postgres  |                |   redis   |
                        | 16-alpine |                | 7-alpine  |
                        +-----+-----+                +-----------+
                              |
                    volume taskflow_postgres_data
```

| Service | Image | Host port | Internal |
|---|---|---|---|
| frontend | `satyam3120/frontend` (Nginx) | 8080 → 80 | taskflow-net |
| backend | `satyam3120/backend` (Node 20) | 3000 → 3000 | taskflow-net |
| postgres | `postgres:16-alpine` | none | taskflow-net, volume `taskflow_postgres_data` |
| redis | `redis:7-alpine` | none | taskflow-net |

## Files

| File | Purpose |
|---|---|
| `backend/Dockerfile` | Two-stage build: production-only `npm ci`, runs as `node` user, health check on `/health` |
| `frontend/Dockerfile` | Multi-stage: Vite build on Node, Nginx serves only `dist/` |
| `frontend/nginx.conf` | Serves the SPA and proxies `/api/` and `/health` to `backend:3000` |
| `docker-compose.yml` | Build-based stack for local development and the instructor CI |
| `docker-compose.deploy.yml` | Image-based stack using Docker Hub images, no `build:` |
| `.env.example` | Template for all configuration; `.env` is git-ignored |
| `.github/workflows/cd.yml` | Build, publish (`v1` + `latest`), deploy and verify |
| `scripts/publish.sh` | Builds both images with `v1` and `latest` tags and pushes them |
| `scripts/verify.sh` | Task 5 networking/health/persistence verification, writes `evidence/` |
| `submission.json` | Student, repository and image metadata |

## Local build and run

```bash
cp .env.example .env          # set a real POSTGRES_PASSWORD and JWT_SECRET
docker compose build
docker compose up -d
docker compose ps
```

- Frontend: http://localhost:8080
- Backend health: http://localhost:3000/health (also proxied at http://localhost:8080/health)

`docker compose up -d --wait` is also supported because every service has a
health check and the application services use `depends_on` with
`condition: service_healthy`.

## Publish images to Docker Hub

```bash
docker login -u satyam3120
./scripts/publish.sh
```

`scripts/publish.sh` builds `satyam3120/backend:v1`, `satyam3120/backend:latest`,
`satyam3120/frontend:v1` and `satyam3120/frontend:latest`, then pushes all four
tags. The equivalent manual commands are:

```bash
docker build -t satyam3120/backend:v1 -t satyam3120/backend:latest ./backend
docker build -t satyam3120/frontend:v1 -t satyam3120/frontend:latest ./frontend
docker push satyam3120/backend:v1
docker push satyam3120/backend:latest
docker push satyam3120/frontend:v1
docker push satyam3120/frontend:latest
```

## Image-based deployment

```bash
docker compose -f docker-compose.deploy.yml pull
docker compose -f docker-compose.deploy.yml up -d
```

Only `docker-compose.deploy.yml`, `.env` and `backend/db/init.sql` (mounted for
first-time schema creation) are needed; no application source is built.

## Verification (Task 5)

```bash
./scripts/verify.sh                        # against docker-compose.yml
BASE_URL=http://localhost:8080 ./scripts/verify.sh docker-compose.deploy.yml
```

The script proves, and saves the output under `evidence/`:

1. Frontend → backend through the Nginx `/api/` and `/health` proxy.
2. Backend resolves `postgres` with Docker DNS and opens TCP 5432.
3. Backend resolves `redis` with Docker DNS and opens TCP 6379.
4. A task row survives `docker compose rm -sf postgres` followed by recreation.
5. `docker compose restart redis` returns a healthy cache and `/health` stays OK.
6. `docker ps` shows healthy states for every service.
7. Custom network membership and the named PostgreSQL volume.

API tests: `cd tests && npm install && BASE_URL=http://localhost:8080 npm test`.

## CI/CD (Task 6)

`.github/workflows/cd.yml` runs on every push to `main`:

1. Checkout, secret validation, Buildx setup.
2. Build and push `backend:v1`, `backend:latest`, `backend:<sha>`.
3. Build and push `frontend:v1`, `frontend:latest`, `frontend:<sha>`.
4. Generate `.env` from GitHub Secrets (random `JWT_SECRET`).
5. Validate that the deploy Compose file has no `build:` and pull images.
6. `docker compose -f docker-compose.deploy.yml up -d`.
7. Verify four running services, backend health via the frontend proxy, frontend response.
8. Run the API tests against the deployment and publish a summary.

Required repository secrets: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`,
`POSTGRES_PASSWORD`. No credentials are committed anywhere.

## Notes

- PostgreSQL and Redis publish no host ports; they are only reachable on `taskflow-net`.
- The password is interpolated into the database URL, so use URL-safe characters
  (letters, digits, `-`, `_`) for `POSTGRES_PASSWORD`.
- Backend waits for PostgreSQL and Redis on startup; health checks double as
  readiness gates for `depends_on`.
- Nginx uses Docker's embedded DNS (`resolver 127.0.0.11 valid=10s`) with a
  variable `proxy_pass`, so a restarted backend container is re-resolved instead
  of leaving a stale upstream IP (which caused 502s in testing).
- `backend/src/db.js` logs PostgreSQL pool `error` events so recreation of the
  database container does not terminate the API process.
- `frontend/package.json` pins `rollup` to `4.34.8`: newer Rollup builds fail to
  parse `react-dom/client.js` inside Alpine/musl containers.
- Base images are `node:22-alpine` (maintained LTS) and `nginx:1.27-alpine`.

## Verification results

- Both Dockerfiles build successfully and pass Hadolint with no findings.
- All four services report `healthy` with only 8080/3000 published to the host.
- `scripts/verify.sh` passes on both Compose files: proxy communication, DNS
  resolution and TCP connectivity to `postgres`/`redis`, persistence across
  container removal, Redis restart and health reporting.
- The 12-test API suite passes against the image-based deployment through the
  frontend proxy (`BASE_URL=http://localhost:8080`).
- Raw outputs are in `evidence/`.
