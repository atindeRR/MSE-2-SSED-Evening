# Moodle Screenshot Guide

Do not use mockups or old terminal output. Capture each item from your own completed implementation and add a short caption in the report.

1. **01-frontend-image-build** — set `$frontendImage = "your-dockerhub-username/frontend"`, then run `docker build -t "${frontendImage}:v1" ./frontend` in PowerShell. Show the successful multi-stage build and image tag. Proves Task 1 and Task 3.
2. **02-backend-image-build** — set `$backendImage = "your-dockerhub-username/backend"`, then run `docker build -t "${backendImage}:v1" ./backend`. Show the successful image build/tag. Proves Task 1 and Task 3.
3. **03-compose-services** — run `docker compose up -d --build` then `docker compose ps`. Show all four services and their healthy/running states. Proves Task 2.
4. **04-custom-network** — run `docker network inspect taskflow_taskflow-network`. Show its bridge driver and attached containers. Proves Task 2 and Task 5.
5. **05-postgres-redis-health** — run `docker compose ps`, `docker compose exec -T postgres sh -c 'pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"'`, and `docker compose exec -T redis redis-cli ping`. Show health plus the accepting-connections/PONG results. Proves Task 2 and Task 5.
6. **06-persistence-before-recreate** — run `.\scripts\verify-compose.ps1` in PowerShell (or `bash scripts/verify-compose.sh`) and capture the marker insertion/select output before the PostgreSQL recreation. Proves Task 5.
7. **07-persistence-after-recreate** — capture the same script showing `Recreating only the PostgreSQL container` and the matching marker returned afterwards. Proves Task 2 and Task 5. Never use `docker compose down -v` for this evidence.
8. **08-docker-hub-tags** — open `https://hub.docker.com/u/<your-dockerhub-username>` and open both `frontend` and `backend` repositories. Show `v1` and `latest` for each. Proves Task 3.
9. **09-image-deployment** — set image variables in `.env`, run `docker compose -f docker-compose.deploy.yml up -d`, then `docker compose -f docker-compose.deploy.yml ps`. Show the image-only deployment services. Proves Task 4.
10. **10-working-frontend** — open `http://localhost:8080` in a browser. Show the TaskFlow login/register page (and, ideally, a logged-in task list). Proves Task 2 and Task 4.
11. **11-backend-api** — open `http://localhost:3000/health` in a browser or run `curl http://localhost:3000/health`. Show `{ "status": "ok", "postgres": "ok", "redis": "ok" }`. Proves Task 5.
12. **12-github-actions** — open the successful `TaskFlow CI/CD` workflow run in the fork’s Actions tab. Show test/build, Docker Hub publication, and image-deployment verification stages. Proves Task 6.
13. **13-pull-request-checks** — open the PR’s Checks tab. Show the instructor CI/evaluation and TaskFlow CI/CD check status, if available. Proves the submission requirement.

Use the image filenames above (for example, `01-frontend-image-build.png`) in `docs/screenshots/` and reference those exact names in the final PDF.
