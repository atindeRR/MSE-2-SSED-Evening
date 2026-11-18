# MSE-2 Software Engineering and DevOps — Set 2

## A. Cover page

**Assignment:** MSE-2 Software Engineering and DevOps
**Assignment:** Set 2 — Evening Shift
**Student name:** Vishal Prajapati
**Roll number:** 2400291530214
**Section:** AIML-C
**Branch:** AIML
**GitHub username:** VishalPrajapati3112
**Docker Hub username:** vishalprajapati214
**Submission date:** 18 November 2026



## B. Introduction

This assignment containerizes the provided TaskFlow full-stack application for repeatable development and deployment. Its React/Vite frontend is built into static assets and served by Nginx. Nginx forwards API and health requests to an Express backend. The backend stores users and tasks in PostgreSQL and uses Redis for task caching. Docker Compose provides service discovery, health checks, isolated networking, and persistent PostgreSQL storage. Docker Hub distributes the frontend/backend images, while GitHub Actions builds and publishes them and verifies an image-based deployment on its temporary runner.

## C. Application architecture

```text
                         Custom Docker bridge network: taskflow
 Browser :8080     frontend (Nginx :80) -- /api, /health --> backend (Express :3000)
                                                                  |              |
                                                    postgres:5432  |              | redis:6379
                                                    PostgreSQL     |              | Redis cache
                                                         |
                                               named volume: postgres_data

 Host API verification: localhost:3000 -> backend:3000
 Host UI: localhost:8080 -> frontend:80
```

The browser calls relative `/api` paths. Nginx resolves `backend` through Compose DNS and proxies those requests. The backend resolves `postgres` and `redis` using their Compose service names. Database and cache ports are not published on the host.

## D. Dockerfile implementation

### Frontend

`frontend/Dockerfile` has two stages. Node 22 slim installs locked build dependencies with `npm ci` and runs `npm run build`. Node Alpine failed to parse `react-dom/client.js` during the Linux build; changing only the build-stage base to Node slim fixed the actual image build. The Nginx 1.27 Alpine runtime receives only the compiled `dist/` directory and reverse-proxy configuration. Port 80 is exposed. The image health check requests `/`. There is no frontend API build-time variable. Nginx dynamically re-resolves Docker DNS name `backend` for `/api/` and `/health`, including after container recreation.

### Backend

`backend/Dockerfile` uses Node 22 Alpine, installs production dependencies, copies application source and SQL schema, changes to the unprivileged `node` user, and starts with `node src/server.js` on port 3000. Startup waits for PostgreSQL, applies the idempotent SQL schema, connects Redis, then starts Express. Its health check calls `/health`, which checks both PostgreSQL and Redis. The backend uses `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, and `PGPASSWORD` in Compose; `DATABASE_URL` remains supported for local development.

Both `.dockerignore` files exclude Git metadata, environment files, node_modules, generated output, logs and tests where appropriate. This avoids copying secrets or unnecessary files into build contexts.

```dockerfile
# Frontend production boundary
FROM node:22-slim AS build
# npm install; copy app; npm run build
FROM nginx:1.27-alpine AS runtime
COPY --from=build /app/dist /usr/share/nginx/html
```

```dockerfile
# Backend production image
FROM node:22-alpine
ENV NODE_ENV=production
WORKDIR /app
# Install production dependencies; copy src and db
USER node
EXPOSE 3000
CMD ["node", "src/server.js"]
```

## E. Docker Compose

`docker-compose.yml` defines four services: `frontend`, `backend`, `postgres`, and `redis`. Frontend and backend are built from their local Dockerfiles. The services share the custom bridge network `taskflow`. PostgreSQL data is stored in named volume `postgres_data`. PostgreSQL uses `pg_isready`; Redis uses `redis-cli ping`; the backend image checks `/health`; and frontend checks its Nginx response. Backend depends on healthy PostgreSQL and Redis; frontend depends on a healthy backend.

Configuration is supplied from an ignored `.env` file copied from `.env.example`. Compose sends database variables to both the PostgreSQL container and backend's standard PostgreSQL client environment. PostgreSQL/Redis have no host port mappings. The host publishes the application on 8080 and API on 3000. The backend image contains and applies `backend/db/init.sql`, allowing deployment without bind-mounting application source.

## F. Docker Hub publishing

The public Docker Hub repositories are named `frontend` and `backend` under `vishalprajapati214`. All four required tags have been pushed and inspected successfully. Repository URLs:

- Frontend: `https://hub.docker.com/r/vishalprajapati214/frontend`
- Backend: `https://hub.docker.com/r/vishalprajapati214/backend`

```powershell
docker login --username vishalprajapati214
docker build -t vishalprajapati214/frontend:v1 -t vishalprajapati214/frontend:latest ./frontend
docker build -t vishalprajapati214/backend:v1 -t vishalprajapati214/backend:latest ./backend
docker push vishalprajapati214/frontend:v1
docker push vishalprajapati214/frontend:latest
docker push vishalprajapati214/backend:v1
docker push vishalprajapati214/backend:latest
docker manifest inspect vishalprajapati214/frontend:v1
docker manifest inspect vishalprajapati214/frontend:latest
docker manifest inspect vishalprajapati214/backend:v1
docker manifest inspect vishalprajapati214/backend:latest
```

Docker Hub username: `vishalprajapati214`. The four requested tags are present. Do not put a password or access token in this document or repository.

## G. Image-based deployment

`docker-compose.deploy.yml` references `${DOCKERHUB_USERNAME}/frontend:latest` and `${DOCKERHUB_USERNAME}/backend:latest`, has no build instructions for those services, and uses official PostgreSQL and Redis images. The deployment host needs Docker/Compose, this deployment YAML, and a private `.env`; it does not need frontend/backend source code. The backend image includes the schema used at startup.

```powershell
docker login --username vishalprajapati214
docker compose -f docker-compose.deploy.yml pull
docker compose -f docker-compose.deploy.yml up -d
docker compose -f docker-compose.deploy.yml ps
curl.exe http://localhost:3000/health
curl.exe http://localhost:8080/health
```

## H. Networking and persistence

Compose creates the `taskflow` bridge network (runtime name `mse-2-ssed-evening_taskflow`); internal service DNS names are `backend`, `postgres`, and `redis`. The Nginx frontend sends API requests to `backend:3000`; the backend connects to PostgreSQL at `postgres:5432` and Redis at `redis:6379`. Health-conditioned dependencies gate startup order, and restart policies restart stopped services. The `postgres_data` named volume (runtime name `mse-2-ssed-evening_postgres_data`) persists database files independently of the PostgreSQL container lifecycle. Redis has no persistence requirement in this assignment and can be restarted independently.

A safe persistence check is to write a sentinel value to a table, remove/recreate only the PostgreSQL container, and query the value again. Do not remove the named volume during this test.

## I. GitHub Actions CI/CD

Workflow: `.github/workflows/cd.yml`. It triggers on pushes to `main` (and manual dispatch), checks out source, sets up Docker Buildx, authenticates to Docker Hub through the official login action, builds and pushes `v1` and `latest` tags for each image, validates Compose configurations, then pulls and starts the published images and checks the frontend/backend routes. It shuts down the temporary stack afterward.

Required repository secrets:

| Secret | Purpose |
| --- | --- |
| `DOCKERHUB_USERNAME` | Docker Hub account name |
| `DOCKERHUB_TOKEN` | Docker Hub token with image push permission |
| `POSTGRES_PASSWORD` | Password for the runner's temporary PostgreSQL service |

The workflow's JWT secret is generated for the ephemeral CI stack. The GitHub-hosted runner is not a permanent deployment server; a real always-on deployment requires a server and separately managed credentials. No server was specified, so this workflow verifies deployment on the runner only.

## J. Testing and verification

The local Compose stack, production builds, API tests, service connectivity, PostgreSQL persistence, Redis restart, Docker Hub tags, and image-based deployment have been exercised. A real proxy issue after backend recreation was fixed by enabling periodic Docker DNS resolution in Nginx. Thirteen genuine screenshots are saved in `submission-evidence/` and embedded below: ten terminal captures for builds, Compose status, networking, health, persistence, Redis restart and image-based deployment, plus browser captures of the application and both Docker Hub repositories. The image-based deployment health routes return `status: ok`, `postgres: ok`, and `redis: ok`. The final documentation and PDF updates are pushed to the fork. GitHub Actions run [44292072593](https://github.com/VishalPrajapati3112/MSE-2-SSED-Evening/actions/runs/44292072593) completed successfully. Pull Request [#176](https://github.com/atindeRR/MSE-2-SSED-Evening/pull/176) is open with the required title and correct fork-to-original branches.

| Test | Command | Expected result | Actual result/status |
| --- | --- | --- | --- |
| Build Compose configuration | `docker compose config --quiet` | Exit code 0 | PASS — executed successfully with temporary placeholder environment values |
| Deployment Compose configuration | `docker compose -f docker-compose.deploy.yml config --quiet` | Exit code 0 | PASS — executed successfully with temporary placeholder environment values |
| YAML syntax | PyYAML parse of both Compose files and the CD workflow | All files parse | PASS — executed successfully |
| Backend JavaScript syntax | `node.exe --check src/server.js` and checks for `db.js`, `app.js` | Exit code 0 for each file | PASS — executed successfully |
| Frontend production build | `npm ci; npm run build` | Vite emits production `dist/` | PASS — Vite 5.4.21 built the production bundle |
| Frontend/backend image builds | `docker compose build` | Both images build | PASS — frontend Node slim/Nginx and backend Node Alpine images built |
| Existing API integration tests | `npm test` against local Compose API | 12 tests pass | PASS — 12/12 passed |
| Compose startup | `docker compose up -d --build` | Four services start | PASS — all services started |
| PostgreSQL/Redis/backend/frontend health | `docker compose ps` | Each reports healthy | PASS — all four healthy |
| Frontend to backend | `curl.exe http://localhost:8080/health` | JSON status `ok` | PASS after Nginx DNS fix — returned PostgreSQL and Redis OK |
| PostgreSQL DNS/connectivity | Backend `pg` query via `PGHOST=postgres` | Query returns successfully | PASS — PostgreSQL query succeeded via Compose DNS |
| Redis DNS/connectivity | Backend `redis` client via `redis://redis:6379` | `PONG` | PASS — Redis returned PONG via Compose DNS |
| PostgreSQL persistence | Insert sentinel, remove/recreate postgres, query again | Sentinel row remains | PASS — sentinel survived; named volume retained |
| Redis restart | `docker compose restart redis`, then `redis-cli ping` | Redis returns healthy and `PONG` | PASS — Redis healthy and returned PONG |
| Docker Hub publishing | Four `docker push` commands and `docker manifest inspect` | Four tags exist | PASS — frontend/backend `v1` and `latest` tags verified |
| Image-based deployment | `docker compose -f docker-compose.deploy.yml pull/up -d` | Published image stack healthy | PASS — images pulled; frontend/backend health routes passed after DNS fix |
| GitHub Actions | Push to `main`; inspect Actions run | Workflow passes all steps | PASS — run [44292072593](https://github.com/VishalPrajapati3112/MSE-2-SSED-Evening/actions/runs/44292072593) completed successfully; required secrets, frontend/backend builds and pushes, Compose validation, image-based startup, service health/routes, and cleanup all succeeded |

## K. Screenshot evidence checklist

Thirteen genuine screenshots are embedded below: ten terminal captures listed in items 1-9 and 12, plus the application and Docker Hub browser captures in items 10, 11, and 13. No Actions screenshot is embedded because no local capture file is available. The repository capture did not render repository contents. A genuine PR screenshot was provided in chat but is not stored as an evidence file in this workspace. Instructor CI evidence remains pending instructor-side checks.

1. **Frontend Docker build** - CAPTURED: `submission-evidence/01-frontend-build.png` (embedded below)
2. **Backend Docker build** - CAPTURED: `submission-evidence/02-backend-build.png` (embedded below)
3. **Compose services running** - CAPTURED: `submission-evidence/03-compose-services.png` (embedded below)
4. **Custom network** - CAPTURED: `submission-evidence/04-docker-network.png` (embedded below)
5. **PostgreSQL healthy** - CAPTURED: `submission-evidence/05-postgres-health.png` (embedded below)
6. **Redis healthy** - CAPTURED: `submission-evidence/06-redis-health.png` (embedded below)
7. **Backend healthy** - CAPTURED: `submission-evidence/07-backend-health.png` (embedded below)
8. **PostgreSQL persistence** - CAPTURED: `submission-evidence/08-postgres-persistence.png` (embedded below)
9. **Redis restart** - CAPTURED: `submission-evidence/09-redis-restart.png` (embedded below)
10. **Docker Hub frontend tags** — CAPTURED: `submission-evidence/10-dockerhub-frontend.png` (embedded below)
11. **Docker Hub backend tags** — CAPTURED: `submission-evidence/11-dockerhub-backend.png` (embedded below)
12. **Image-based deployment** - CAPTURED: `submission-evidence/12-image-deployment.png` (embedded below)
13. **Application browser view** — CAPTURED: `submission-evidence/13-application-browser.png` (embedded below)
14. **GitHub Actions success** — [RUN VERIFIED: run 44292072593 succeeded; no Actions screenshot file is embedded]
15. **GitHub repository/branch** — [NOT AVAILABLE: repository content was not rendered in the attempted capture]
16. **Pull Request page** — [PR #176 is open; genuine screenshot supplied in chat but not stored in this evidence folder]
17. **Instructor CI checks** — [PENDING: instructor-side checks have not run]

## L. GitHub submission information

- Original repository: https://github.com/atindeRR/MSE-2-SSED-Evening
- Fork repository: `https://github.com/VishalPrajapati3112/MSE-2-SSED-Evening`
- Working branch: `main` (pushed to the fork)
- Submission PDF: `2400291530214_Vishal_Prajapati_SET2.pdf`
- Pull Request URL: https://github.com/atindeRR/MSE-2-SSED-Evening/pull/176 (OPEN; not merged)
- Pull Request title: `DOCKER-SET-2 | 2400291530214 | Vishal Prajapati | AIML-C`
- Pull Request description and screenshot attachment: PENDING — the GitHub integration rejects write operations with HTTP 403, and the screenshot provided in chat is not available as a local image file to upload.
- GitHub Actions run: https://github.com/VishalPrajapati3112/MSE-2-SSED-Evening/actions/runs/44292072593 (SUCCESS; push event, run 1)
- Docker Hub frontend repository: vishalprajapati214/frontend
- Docker Hub backend repository: vishalprajapati214/backend

## M. Conclusion

The application builds and runs with four healthy Compose services, passes all 12 API integration tests, connects to PostgreSQL and Redis through Compose DNS, preserves PostgreSQL data across container recreation, and has all requested Docker Hub tags published and verified. The image-only deployment works through both frontend and backend health routes after the Nginx DNS refresh fix. The final documentation/PDF commit is pushed to the fork. GitHub Actions run 44292072593 succeeded, and PR #176 is open with no merge conflicts. Thirteen genuine screenshots are embedded; the Actions screenshot and repository-page screenshot are unavailable locally. The PR screenshot was supplied in chat but is not stored in the evidence folder. Instructor-side CI checks remain pending.

## N. Declaration

"I hereby declare that the submitted implementation has been completed by me. I have tested the Docker configurations, Docker Compose deployment, Docker Hub image publishing and GitHub Actions CI/CD pipeline. The screenshots and evidence included in this document represent my actual implementation."
