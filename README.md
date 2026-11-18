# TaskFlow — MSE-2 Set 2

Full-stack task management application used for the Software Engineering and DevOps practical.

## Stack

- Frontend: React 18 + Vite, served by Nginx
- Backend: Node.js 22 + Express
- Database: PostgreSQL 16
- Cache: Redis 7

## Local Docker Compose deployment

1. Copy `.env.example` to `.env`.
2. Set a strong `POSTGRES_PASSWORD` and `JWT_SECRET`.
3. Set `DOCKERHUB_USERNAME` to your Docker Hub username (for local builds this can remain `local`).
4. Build and start:

```bash
docker compose up -d --build
docker compose ps
```

Open the frontend at http://localhost:8080. The backend health endpoint is http://localhost:3000/health.

## Image-based deployment

After publishing `frontend:v1`, `frontend:latest`, `backend:v1`, and `backend:latest` to your Docker Hub account, set `DOCKERHUB_USERNAME` in `.env` and run:

```bash
docker compose -f docker-compose.deploy.yml pull
docker compose -f docker-compose.deploy.yml up -d
```

The deployment Compose file uses only published frontend/backend images; it contains no `build:` instructions.

## Useful verification commands

```bash
docker compose ps
docker network inspect taskflow-network
docker compose exec postgres pg_isready -U taskflow_user -d taskflow
docker compose exec redis redis-cli ping
curl http://localhost:3000/health
curl -I http://localhost:8080/
```

To verify PostgreSQL persistence, create a test account/task through the application, remove and recreate only the PostgreSQL container (do not remove the volume), then verify the data remains:

```bash
docker compose rm -sf postgres
docker compose up -d postgres
```

Do not use `docker compose down -v` during persistence verification because `-v` deletes named volumes.

## GitHub Actions

Add these repository Actions secrets:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `POSTGRES_PASSWORD`

Pushing to `main` builds and pushes both Docker Hub repositories with `v1` and `latest` tags, deploys the published images, and runs API tests.

## Ports

- Frontend: host `8080` → container `80`
- Backend API: host `3000` → container `3000`
- PostgreSQL and Redis are internal to the Compose network and are not published to the host.
