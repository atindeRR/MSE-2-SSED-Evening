# MSE-2 Set 2 Implementation Guide

This repository packages TaskFlow (Vite/React frontend and Express API) with PostgreSQL and Redis. The frontend uses `/api` and Nginx proxies `/api/` and `/health` to the backend, so browser requests are same-origin and do not need CORS or a build-time API URL.

## Files

- `frontend/Dockerfile`, `frontend/.dockerignore`, `frontend/package-lock.json`: multi-stage Vite build, locked dependencies, and small Nginx runtime.
- `backend/Dockerfile`, `backend/.dockerignore`: production Node runtime and health check.
- `docker-compose.yml`: local source builds, internal bridge network, services and persistent database volume.
- `docker-compose.deploy.yml`: the same runtime stack using Docker Hub `latest` images only.
- `.github/workflows/cd.yml`: build, publish, deploy, verify, and exercise the API on pushes to `main`.
- `.env.example`: variable names and local setup hints; copy to `.env` and replace the values. `.env` is ignored by Git.

## Local source build and run

PowerShell:

```powershell
Copy-Item .env.example .env
notepad .env
```

Set `POSTGRES_PASSWORD` to a unique URL-safe password (letters and digits) and `JWT_SECRET` to a long random value. Then:

```powershell
docker compose config
docker compose build
docker compose up -d
docker compose ps
```

Open <http://localhost:8080>. The API health endpoint is <http://localhost:3000/health>; the frontend proxy exposes it at <http://localhost:8080/health>.

To stop while preserving PostgreSQL data, run `docker compose down`. `docker compose down -v` also deletes the database volume and all its data.

## Docker Hub publishing

Create public Docker Hub repositories named `frontend` and `backend`, then sign in with `docker login`. Replace `YOUR_DOCKERHUB_USERNAME` with your actual account name:

```powershell
docker build -t YOUR_DOCKERHUB_USERNAME/frontend:v1 -t YOUR_DOCKERHUB_USERNAME/frontend:latest ./frontend
docker build -t YOUR_DOCKERHUB_USERNAME/backend:v1 -t YOUR_DOCKERHUB_USERNAME/backend:latest ./backend
docker push YOUR_DOCKERHUB_USERNAME/frontend:v1
docker push YOUR_DOCKERHUB_USERNAME/frontend:latest
docker push YOUR_DOCKERHUB_USERNAME/backend:v1
docker push YOUR_DOCKERHUB_USERNAME/backend:latest
```

Alternatively, after configuring the GitHub secrets below, pushing to `main` publishes all four tags automatically.

## Image-based deployment

Set `DOCKERHUB_USERNAME` in `.env` to the Docker Hub account holding both repositories. Set a unique URL-safe `POSTGRES_PASSWORD` and a strong `JWT_SECRET` as above. The deployment does not build frontend or backend source:

```powershell
docker compose -f docker-compose.deploy.yml config
docker compose -f docker-compose.deploy.yml pull
docker compose -f docker-compose.deploy.yml up -d
docker compose -f docker-compose.deploy.yml ps
```

Open <http://localhost:8080>. PostgreSQL and Redis are reachable only inside the custom Compose network; the frontend and API are mapped to host ports 8080 and 3000.

## Networking and health verification

Run these commands against the local source-built stack (omit `-f docker-compose.yml`, since that is the default Compose filename):

```powershell
# Frontend responds, and its /health proxy reaches the backend.
curl.exe -i http://localhost:8080/
curl.exe -i http://localhost:8080/health

# Direct backend check; response should contain status, postgres, and redis all set to "ok".
curl.exe -i http://localhost:3000/health

# Resolve the postgres service name, connect through the configured DATABASE_URL, and run SQL.
docker compose exec backend node -e "import('pg').then(async ({default: pg}) => { const p = new pg.Client({connectionString: process.env.DATABASE_URL}); await p.connect(); console.log('postgres:', (await p.query('SELECT 1 AS connected')).rows[0]); await p.end(); })"
# Resolve the redis service name and expect PONG.
docker compose exec backend node -e "import('redis').then(async ({createClient}) => { const c=createClient({url:'redis://redis:6379'}); await c.connect(); console.log('redis ping:', await c.ping()); await c.quit(); })"

# All services should report healthy (frontend health is also defined in its image).
docker compose ps
$ids = docker compose ps -q postgres redis backend frontend
docker inspect --format '{{.Name}} {{.State.Health.Status}}' $ids

# Restart Redis; backend health should recover once its Redis connection is usable.
docker compose restart redis
docker compose ps
curl.exe -i http://localhost:3000/health
```

The backend-to-PostgreSQL Node command exercises hostname resolution and a SQL query using the backend's configured connection string. The Redis command resolves `redis` and expects `redis ping: PONG`. A successful API health response confirms both dependencies are available. For Docker CLI portability, `docker compose ps` also shows health status.

### PostgreSQL persistence check

Create one user through the running API, record the returned email, recreate only PostgreSQL, and query that email after startup:

```powershell
$email = "persist-$([DateTimeOffset]::UtcNow.ToUnixTimeSeconds())@example.com"
curl.exe -sS -X POST http://localhost:3000/api/auth/register -H "Content-Type: application/json" -d "{`"name`":`"Persistence Check`",`"email`":`"$email`",`"password`":`"student123`"}"
docker compose stop postgres
docker compose rm -f postgres
docker compose up -d postgres
docker compose exec postgres sh -c 'until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do sleep 1; done'
docker compose exec postgres psql -U taskflow_user -d taskflow -c "SELECT email FROM users WHERE email LIKE 'persist-%@example.com' ORDER BY id DESC LIMIT 1;"
```

The final query should return the exact email created before container recreation. Do not run `down -v` before this check; the named `postgres_data` volume is what preserves the records.

## GitHub Actions and secrets

In the repository, open **Settings → Secrets and variables → Actions → New repository secret**, then add:

- `DOCKERHUB_USERNAME`: your Docker Hub username.
- `DOCKERHUB_TOKEN`: a Docker Hub access token with permission to push to both repositories.
- `POSTGRES_PASSWORD`: a unique URL-safe password for the ephemeral CI deployment.

Push or merge to `main` to run `.github/workflows/cd.yml`. It builds and pushes `frontend:v1`, `frontend:latest`, `backend:v1`, and `backend:latest`; then it starts the image-based Compose deployment, checks backend and frontend routes, and runs `tests/api.test.js`. The workflow generates a temporary JWT secret and removes its deployment and volume when it finishes. No credentials should be committed.

## Pull request handoff

After reviewing the diff and successful local checks, you can submit from your fork with your own chosen branch and commit message:

```powershell
git switch -c docker-devops-practical
git add .env.example .github/workflows/cd.yml backend/Dockerfile backend/.dockerignore backend/src/db.js frontend/Dockerfile frontend/.dockerignore frontend/package.json frontend/package-lock.json docker-compose.yml docker-compose.deploy.yml MSE2_IMPLEMENTATION_GUIDE.md
git commit -m "Implement Docker and DevOps practical"
git push -u origin docker-devops-practical
```

Then open a pull request in GitHub from your branch to `atindeRR/MSE-2-SSED-Evening:main`, using the required title pattern `DOCKER-SET-2 | ROLL-NUMBER | STUDENT-NAME | SECTION`. Fill in your own identity fields and attach the completed evidence PDF; do not include `.env` or credentials.

## Troubleshooting

- **Missing variable errors:** create `.env` from `.env.example`; define `POSTGRES_PASSWORD` and `JWT_SECRET`. Image deployment also needs `DOCKERHUB_USERNAME`.
- **Database URL/auth errors:** use a URL-safe password containing letters and digits; it is embedded in `DATABASE_URL`.
- **Backend stays unhealthy:** inspect `docker compose logs backend postgres redis`; the health endpoint checks both PostgreSQL and Redis.
- **Frontend shows 502:** wait for backend health, then inspect `docker compose logs frontend backend`. Compose starts Nginx only after the backend is healthy.
- **Port already in use:** stop the other service on host port 8080 or 3000, or adjust the left side of the corresponding Compose port mapping.
- **No published image:** confirm both Docker Hub repositories exist and `docker login` or the GitHub token can push to them.
- **Database appears reset:** ensure the named `postgres_data` volume is present and avoid `docker compose down -v`.

## Final submission checklist

- [ ] Build and run the source Compose stack; save genuine terminal/browser evidence.
- [ ] Verify frontend/backend access, dependency health, Redis restart, and PostgreSQL persistence.
- [ ] Create Docker Hub `frontend` and `backend` repositories; publish and verify both `v1` and `latest` tags.
- [ ] Configure the three GitHub Actions secrets and confirm a successful `main` workflow run.
- [ ] Commit and push your work to your fork, then open the required pull request to the instructor repository.
- [ ] Prepare the required PDF with your identity, repository/image/workflow URLs, and genuine screenshots; upload it to Moodle and attach it to the pull request.
