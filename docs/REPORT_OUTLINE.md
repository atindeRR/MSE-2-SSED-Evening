# MSE-2 Software Engineering and DevOps — Set 2 Report

**PDF filename:** `ROLL_NUMBER_STUDENT_NAME_SET2.pdf`

## 1. Student Information

| Field | Value |
| --- | --- |
| Student Name | |
| Roll Number | |
| Section | |
| Branch | |
| GitHub Username | |
| Docker Hub Username | |

## 2. Repository and Submission Details

| Field | Value |
| --- | --- |
| Fork repository URL | |
| Pull Request URL | |
| Branch name | |
| Frontend Docker Hub image URL | |
| Backend Docker Hub image URL | |
| GitHub Actions workflow URL | |

## 3. Implementation Summary

Describe the React/Vite frontend, Nginx reverse proxy, Express backend, PostgreSQL volume, Redis cache, custom bridge network, health checks, and image-based deployment.

## 4. Dockerfiles

Explain the frontend multi-stage build and non-root Nginx runtime. Explain the backend production dependencies, non-root Node user, and `/health` health check.

**Evidence:** `01-frontend-image-build.png`, `02-backend-image-build.png`.

## 5. Docker Compose, Networking, and Health Checks

Explain service-name communication, the `taskflow-network` bridge, dependencies, and PostgreSQL named volume.

**Evidence:** `03-compose-services.png`, `04-custom-network.png`, `05-postgres-redis-health.png`.

## 6. Docker Hub Publishing and Image-based Deployment

State the actual Docker Hub image URLs and show both `v1` and `latest`. Explain that `docker-compose.deploy.yml` has no frontend/backend `build:` entries.

**Evidence:** `08-docker-hub-tags.png`, `09-image-deployment.png`.

## 7. Networking and Persistence Verification

Describe frontend proxy/API health, PostgreSQL and Redis service-name connectivity, Redis restart, and the PostgreSQL record surviving a container recreation.

**Evidence:** `06-persistence-before-recreate.png`, `07-persistence-after-recreate.png`, `11-backend-api.png`.

## 8. CI/CD and Pull Request

Describe the main-branch publication behavior and pull-request build/test behavior. Include the real Actions and PR URLs.

**Evidence:** `12-github-actions.png`, `13-pull-request-checks.png`.

## 9. Working Application

**Evidence:** `10-working-frontend.png`.

## 10. Declaration

> I hereby declare that the submitted implementation has been completed by me. I have tested the Docker configurations, Docker Compose deployment, Docker Hub image publishing and GitHub Actions CI/CD pipeline. The screenshots and evidence included in this document represent my actual implementation.
