# TaskFlow – Docker and DevOps

TaskFlow is a small full-stack task manager used to demonstrate Docker image
builds, Compose networking, persistent PostgreSQL storage, Redis caching,
Docker Hub publishing, and GitHub Actions CI/CD.

## Architecture

| Component | Technology | Container port | Host port |
|---|---|---:|---:|
| Frontend | React 18, Vite, Nginx | 80 | 8080 |
| Backend | Node.js 22, Express | 3000 | 3000 |
| Database | PostgreSQL 16 | 5432 | Not published |
| Cache | Redis 7 | 6379 | Not published |

The browser sends `/api` requests to Nginx. Nginx proxies those requests to the
`backend` Compose service; `/health` is proxied the same way. The backend
connects to PostgreSQL at `postgres:5432` and Redis at `redis:6379` over the
custom bridge network. At startup it waits for PostgreSQL, initializes the
schema included in the backend image, and then connects to Redis.

## Repository structure

```text
backend/
  Dockerfile
  db/init.sql
  src/                 Express API, PostgreSQL, Redis and auth
frontend/
  Dockerfile
  nginx.conf
  src/                 React application
docker-compose.yml     Local source builds and four-service stack
docker-compose.deploy.yml
                       Image-only deployment stack
.github/workflows/
  ci.yml               Instructor PR evaluation
  cd.yml               Build, publish and runner deployment on main
```

## Dockerfiles

The frontend Dockerfile uses a Node.js build stage to install the verified
frontend dependencies and run `npm run build`. A separate lightweight Nginx
runtime stage receives only the generated `dist` files and the existing proxy
and SPA-routing configuration.

The backend Dockerfile uses Node.js 22, installs production dependencies only,
and copies the API source and database schema. `npm start` runs the existing
backend start script. Each application has a `.dockerignore` to exclude local
dependencies, environment files, and other non-image content.

## Local setup (Windows PowerShell)

1. Install and start Docker Desktop with Linux containers enabled.
2. From the repository root, create a local environment file:

   ```powershell
   Copy-Item .env.example .env
   notepad .env
   ```

3. Replace `POSTGRES_PASSWORD` and `JWT_SECRET` with unique values. Keep `.env`
   local; it is ignored by Git.
4. Build and start the local stack:

   ```powershell
   docker compose up -d --build
   docker compose ps
   docker compose logs
   ```

If host port 8080 is already in use, set an alternate port for that PowerShell
session before starting the stack (for example, `$env:FRONTEND_PORT = '8081'`);
the default remains 8080.

The local Compose stack contains exactly four services: `frontend`, `backend`,
`postgres`, and `redis`. The `taskflow-network` bridge network provides
service-name DNS. PostgreSQL data is stored in the named `postgres_data`
volume. PostgreSQL and Redis are not published to host ports.

PostgreSQL and Redis health checks gate backend startup; the frontend waits for
the backend health check. The backend health endpoint checks both database and
cache connectivity. The frontend has its own Nginx health check.

## Access and basic verification

- Frontend: <http://localhost:8080>
- Backend health: <http://localhost:3000/health>
- Frontend-to-backend proxy: <http://localhost:8080/health>

PowerShell checks:

```powershell
Invoke-WebRequest http://localhost:8080/
Invoke-RestMethod http://localhost:3000/health
Invoke-RestMethod http://localhost:8080/health
docker compose exec -T backend node -e "require('dns').lookup('postgres', console.log); require('dns').lookup('redis', console.log)"
docker network inspect taskflow-network
docker compose ps
```

When using an alternate `FRONTEND_PORT`, replace `8080` in the frontend URLs
with that port.

The health response reports `status`, `postgres`, and `redis`. The frontend
application supports registration, login, and task management.

## Persistence and Redis restart verification

Run the following while the local stack is up. This creates a harmless sample
user record; it does not rely on the record being used to log in.

```powershell
docker compose exec -T postgres psql -U taskflow_user -d taskflow -c "INSERT INTO users (name,email,password_hash) VALUES ('Persistence Test','persistence@example.test','not-used') ON CONFLICT (email) DO UPDATE SET name=EXCLUDED.name"
docker compose exec -T postgres psql -U taskflow_user -d taskflow -c "SELECT id,email FROM users WHERE email='persistence@example.test'"
docker compose stop postgres
docker compose rm -f postgres
docker compose up -d postgres
docker compose ps
docker compose exec -T postgres psql -U taskflow_user -d taskflow -c "SELECT id,email FROM users WHERE email='persistence@example.test'"
docker compose restart redis
docker compose ps
Invoke-RestMethod http://localhost:3000/health
```

Wait for PostgreSQL and Redis to report `healthy` before continuing. Do not use
`docker compose down -v` during the persistence exercise; `-v` deletes the
named database volume.

## Docker Hub publishing

Create public Docker Hub repositories named `frontend` and `backend` in the
`gauridhingra` account before pushing. Sign in locally with `docker login`;
never place a Docker Hub password or access token in this repository or chat.
Then run:

```powershell
docker compose build frontend backend
docker image tag gauridhingra/frontend:latest gauridhingra/frontend:v1
docker image tag gauridhingra/backend:latest gauridhingra/backend:v1
docker image push gauridhingra/frontend:v1
docker image push gauridhingra/frontend:latest
docker image push gauridhingra/backend:v1
docker image push gauridhingra/backend:latest
```

Expected repository pages:

- Frontend: <https://hub.docker.com/r/gauridhingra/frontend>
- Backend: <https://hub.docker.com/r/gauridhingra/backend>

Both repositories are public and have been verified with active `v1` and
`latest` tags.

## Image-based deployment

`docker-compose.deploy.yml` uses only the `gauridhingra/frontend:latest` and
`gauridhingra/backend:latest` images; it has no application `build:` entries.
It also uses the official PostgreSQL and Redis images, its own custom network,
health checks, and a separate named PostgreSQL volume.

After setting `.env` as described above and publishing both images:

```powershell
docker compose -f docker-compose.deploy.yml pull
docker compose -f docker-compose.deploy.yml up -d
docker compose -f docker-compose.deploy.yml ps
docker compose -f docker-compose.deploy.yml logs
Invoke-WebRequest http://localhost:8080/
Invoke-RestMethod http://localhost:3000/health
```

The deployment file and image contain everything needed to run the app;
frontend/backend source code is not required on a deployment machine.

## GitHub Actions CI/CD

`.github/workflows/cd.yml` runs on pushes to `main` and can also be started
manually. It checks out the source, sets up Buildx, builds both app images,
authenticates with Docker Hub, tags and pushes `v1` and `latest`, pulls and
deploys the image-only Compose stack, then verifies all four container health
checks and frontend/backend endpoints before running the API tests.

Add these repository secrets under **Settings → Secrets and variables →
Actions**:

| Secret | Purpose |
|---|---|
| `DOCKERHUB_USERNAME` | Docker Hub account name (`gauridhingra`) |
| `DOCKERHUB_TOKEN` | Docker Hub access token |
| `POSTGRES_PASSWORD` | CI deployment database password |

The workflow generates a separate random JWT signing key on its runner.
Credentials are not committed or printed. The workflow deployment is
ephemeral on a GitHub-hosted runner; it verifies the deployment but does not
provide permanent public application hosting.

The existing `ci.yml` workflow performs the instructor's pull-request checks
when a PR is opened against the examination repository.

## Environment variables

Copy `.env.example` to `.env` and set `DOCKERHUB_USERNAME`, `POSTGRES_DB`,
`POSTGRES_USER`, `POSTGRES_PASSWORD`, and `JWT_SECRET`. Compose passes database
connection settings to the API as PostgreSQL environment variables and uses
the internal service address `redis://redis:6379`.

Do not commit `.env`, passwords, or access tokens. The checked-in `.env.example`
contains only replacement values, not real credentials.
