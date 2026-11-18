# Final Submission Checklist — MSE-2 Practical Examination

**Course:** Software Engineering and DevOps (AI310B)  
**Shift / Set:** Evening Shift – Set 2  
**Student Name:** Bhavya Arora  
**Branch:** BTech CSE AI&ML  
**College:** KIET Group of Institutions  
**Docker Hub Account:** bhavya2718  
**Repository:** https://github.com/Bhavya-AroraID/MSE-2-SSED-Evening  

---

## 1. Technical Implementation Checklist

- [x] **Repository Forked:** Forked to `Bhavya-AroraID/MSE-2-SSED-Evening`.
- [x] **Frontend Dockerfile:** Multi-stage build (`node:20-slim` build stage, `nginx:1.27-alpine` runtime, reverse-proxying `/api/` and `/health` to backend, port 80 exposed).
- [x] **Backend Dockerfile:** Multi-stage build (`node:20-alpine`, `--omit=dev` production dependencies, `USER node` non-root user, port 3000 exposed).
- [x] **docker-compose.yml Configured:**
  - Services: `frontend`, `backend`, `postgres`, `redis`.
  - Custom bridge network: `taskflow`.
  - Named volume for PostgreSQL: `postgres_data`.
  - Service-name internal networking (`postgres:5432`, `redis:6379`, `backend:3000`).
  - Isolated database ports (no host port exposure for PostgreSQL and Redis).
  - Health checks: `pg_isready` (Postgres), `redis-cli ping` (Redis), Node `fetch` (backend).
  - Proper `condition: service_healthy` dependency startup sequence.
- [x] **docker-compose.deploy.yml Configured:**
  - Uses published images: `${DOCKERHUB_USERNAME}/backend:latest` and `${DOCKERHUB_USERNAME}/frontend:latest`.
  - Zero `build:` directives.
  - Official `postgres:16-alpine` and `redis:7-alpine` images.
  - Custom network and persistent volume retained.
- [x] **CI/CD Workflow (.github/workflows/cd.yml):**
  - Triggers on push to `main` branch.
  - Validates secrets: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, `POSTGRES_PASSWORD`.
  - Authenticates to Docker Hub using GitHub secrets.
  - Builds and tags images: `bhavya2718/backend:v1`, `bhavya2718/backend:latest`, `bhavya2718/frontend:v1`, `bhavya2718/frontend:latest`.
  - Pushes all 4 image tags to Docker Hub.
  - Deploys using `docker-compose.deploy.yml` on runner.
  - Verifies container health and executes all 12 Jest API tests.

---

## 2. GitHub Secrets Required

Configure under `Settings > Secrets and variables > Actions > New repository secret`:

1. `DOCKERHUB_USERNAME` = `bhavya2718`
2. `DOCKERHUB_TOKEN` = `<your_dockerhub_personal_access_token>`
3. `POSTGRES_PASSWORD` = `<your_chosen_secure_password>`

---

## 3. Pull Request Submission Format

- **Target Repository:** `atindeRR/MSE-2-SSED-Evening`
- **Target Branch:** `main`
- **Source Branch:** `Bhavya-AroraID/MSE-2-SSED-Evening:main`
- **PR Title Format:**
  ```text
  DOCKER-SET-2 | <ROLL-NUMBER> | Bhavya Arora | <SECTION>
  ```
  *(Example: `DOCKER-SET-2 | 123456 | Bhavya Arora | AIML-A`)*

---

## 4. Documentation & PDF Deliverables

- [x] `SUBMISSION_DOCUMENTATION.md` prepared with architecture, deliverables, test outlines, and declaration.
- [x] `submission.json` populated with student metadata.
- [ ] Fill in Roll Number and Section in `submission.json` and documentation.
- [ ] Export PDF named `<ROLL_NUMBER>_Bhavya_Arora_SET2.pdf`.
- [ ] Upload PDF to Moodle and attach to GitHub Pull Request.
