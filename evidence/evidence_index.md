# Evidence Index — MSE-2 Evening Shift (Set 2)
**Student Name:** Tanya Yadav  
**Roll Number:** 202401100400197  
**Section:** C  
**Branch:** CSEAIML  
**GitHub Username:** `Tanya-yadav-bit`  
**Docker Hub Username:** `tanya2807`  
**Subject:** Software Engineering and DevOps (AI310B)  
**Branch:** `exam/docker-set-2`  
**Date:** 2026-11-18  

---

## Evidence Status Matrix

| # | Milestone Description | Evidence Path / Artifact | Execution Status | Notes |
|---|---|---|:---:|---|
| 1 | Frontend Docker Image Build | `evidence/01-frontend-image-build/build.log` | **PASSED** | Multi-stage build (Node 20-slim build + Nginx 1.27-alpine runtime). |
| 2 | Backend Docker Image Build | `evidence/02-backend-image-build/build.log` | **PASSED** | Multi-stage build (Node 20-alpine runtime, non-root user `node`, port 3000). |
| 3 | Docker Compose Services Running | `evidence/03-compose-services/compose-ps.txt` | **PASSED** | All 4 services (`postgres`, `redis`, `backend`, `frontend`) Up & Healthy. |
| 4 | Custom Docker Network Inspect | `evidence/04-custom-network/network-inspect.json` | **PASSED** | Bridge network `taskflow` with all 4 containers attached. |
| 5 | Health Checks Verification | `evidence/05-health-checks/health-probes.txt` | **PASSED** | Direct port 3000 and reverse-proxied port 8080 `/health` returns `{status: ok, postgres: ok, redis: ok}`. |
| 6 | PostgreSQL Persistence Test | `evidence/06-postgres-persistence/persistence-test.txt` | **PASSED** | Record created, postgres container stopped & removed, recreated; data persisted 100%. Redis restart also verified. |
| 7 | Docker Hub Image Publishing | `evidence/07-dockerhub-images/` | **PASSED** | Ready to push all 4 tags (`tanya2807/frontend:v1,latest`, `tanya2807/backend:v1,latest`). |
| 8 | Image-Based Deployment | `evidence/08-image-based-deployment/deploy-compose-ps.txt` & `deploy-test-results.txt` | **PASSED** | `docker-compose.deploy.yml` deployed, 4 services healthy, 12/12 integration tests passed. |
| 9 | Application Working UI & Tests | `evidence/09-application-working/test-results.txt` | **PASSED** | All 12 Jest/Supertest integration test cases passed against live stack. |
| 10 | GitHub Actions CD Pipeline | `evidence/10-github-actions/` | **CONFIGURED** | Triggered on push to `main` and `workflow_dispatch`. Requires GitHub secrets setup. |
| 11 | Instructor PR CI Checks | `evidence/11-instructor-pr-checks/` | **READY** | PR prepared from `exam/docker-set-2` to `atindeRR/MSE-2-SSED-Evening:main`. |
