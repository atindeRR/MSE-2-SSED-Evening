# Implementation Log

## 2026-11-18

### Architecture confirmed
- Frontend: React 18 SPA built by Vite, served by Nginx.
- Backend: Node.js 22 runtime with Express; `backend/src/server.js` waits for PostgreSQL and Redis before listening on port 3000.
- PostgreSQL stores users and tasks from `backend/db/init.sql`; Redis caches authenticated task lists.
- Nginx forwards `/api/` and `/health` to the backend Compose service.

### Changes made
- Added `backend/package-lock.json` and synchronized the existing frontend lockfile with its package override.
- Updated both Dockerfiles to use Node.js 22 and reproducible `npm ci` installs.
- Made image-deployment host ports configurable while preserving defaults 3000 and 8080.
- Updated the GitHub Actions release workflow to use the required secrets, build before registry login, push `latest` and `v1`, verify an image-based deployment, emit failure logs, and clean up without `down -v`.

### Verified locally
- Docker Compose build and startup completed successfully; PostgreSQL, Redis, and backend reported healthy.
- Existing API test suite passed: 12/12 against the local build and 12/12 against the separately pulled Docker Hub deployment.
- Frontend returned HTTP 200; its `/health` reverse proxy returned `status=ok`, `postgres=ok`, and `redis=ok`.
- PostgreSQL probe `docker-volume-persistence-2026-11-18` remained present after removing and recreating only the PostgreSQL container. The named volume was retained.
- Redis restarted successfully and returned `PONG`.
- Docker Hub tags pushed: `aryantomar09/frontend:{latest,v1}` (digest `sha256:78120e9eb9f2041d3ed6c736b148f4e85bc7b091b5a5e5ff1632e7399c2bcd08`) and `aryantomar09/backend:{latest,v1}` (digest `sha256:4bcf55d2fa3b1889abb490f0b014c0db4d6142135e8428fa2d2775016987854e`).
- GitHub Actions workflow passed local `actionlint` validation. A GitHub-hosted run has not yet been triggered.

### Still pending
- Commit and push implementation changes to the personal fork to trigger GitHub Actions.
- Confirm repository secrets are present and review the hosted workflow result.
- Prepare the PDF after collecting the hosted run URL and genuine screenshots; academic branch and PR URL are not yet known.
- Obtain approval before creating a Pull Request.
