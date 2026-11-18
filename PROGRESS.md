# Implementation Progress — MSE-2 SET 2 (TaskFlow)

Checkpoint: 2026-11-18 (~16:05 local). Repository: `C:\Users\SAKSHI\MSE-2-SSED-Evening`.
Student: Sakshi | 202401100400162 | SEC_C | CSE(AIML).
PR: https://github.com/atindeRR/MSE-2-SSED-Evening/pull/60 (title corrected to `DOCKER-SET-2 | 202401100400162 | Sakshi | SEC_C`).
PDF: `202401100400162_Sakshi_SET2.pdf` generated and verified (9 pages, exact declaration, no secrets).
`origin` = `https://github.com/spirals-coder/MSE-2-SSED-Evening.git` (correct).
`upstream` = `https://github.com/atindeRR/MSE-2-SSED-Evening.git` (configured).

## DONE

### Implementation
- Multi-stage frontend Dockerfile: `node:20-alpine` build → `nginx:1.27-alpine`; `npm ci`; Rollup pinned 4.34.9 (newer musl build fails on Alpine); non-root numeric UID `101:101`; writable Nginx caches; PID in /tmp; Nginx `resolver 127.0.0.11` + variable `proxy_pass` survives backend IP changes.
- Backend Dockerfile: `node:20-alpine`; `npm ci --omit=dev`; numeric UID `1000:1000`; only src/ + db/ + prod node_modules; `node src/server.js`.
- Both Dockerfiles now pass `hadolint/hadolint` with exit 0 (DL3066 fixed by numeric USER). Instructor CI uses this exact hadolint image.
- `docker-compose.yml`: 4 services, custom bridge `taskflow-net`, named volume `postgres_data`, health checks, health-based `depends_on`, ports 8080/3000, PG/Redis internal only.
- `docker-compose.deploy.yml`: published `latest` images only, NO `build:`, custom network, named volume, health checks.
- `backend/src/db.js`: idempotent `ensureSchema()` (bundled init.sql) + PG pool error handler; `server.js` calls it → image-only deploy works with empty PG volume.
- Lockfiles generated for frontend and backend; `.env.example` updated; `.env` local-only/gitignored.

### Verification / evidence
- Local source-build stack: 4 containers healthy; 12/12 API tests pass; health OK; frontend serves TaskFlow.
- Docker Hub: all four tags pushed and verified via `docker manifest inspect`: `1sakshi2/frontend:v1|latest`, `1sakshi2/backend:v1|latest`.
- Image-based deployment: pulled `latest` images from Hub, all services healthy, 12/12 API tests pass; inspect confirms Hub image IDs in use.
- Networking/persistence genuine evidence in `C:\Users\SAKSHI\AppData\Local\Temp\opencode\mse2-evidence\phase7-evidence.txt`: custom network members, DNS by service name, frontend→backend proxy, register→PG record before/after postgres container recreation, login after recreation, volume exists, Redis restart, final health. Contains JWT — redact in PDF.
- Other evidence files: `build-frontend.txt`, `build-backend.txt`, `deploy-ps.txt`, `deploy-config.txt`, `network.txt`, `health.txt`, `dockerhub.txt`, `tests.txt`, `github-actions.txt`.

### GitHub Actions CD
- First verified run: https://github.com/spirals-coder/MSE-2-SSED-Evening/actions/runs/44278429222 → **success**, every stage success (secrets validation, Buildx, Hub login, both builds/pushes, manifest verification, secret-backed .env, deploy config, pull, deploy, health, service statuses, API smoke tests, cleanup). Evidence saved in `github-actions.txt`.
- After numeric-UID Dockerfile fix, commit `e527b7c` was pushed to `main`. Second CD run: https://github.com/spirals-coder/MSE-2-SSED-Evening/actions/runs/44279433007 → **success**, every stage success. Evidence in `github-actions.txt`.
- Fresh Hub manifests verified after rebuild (v1 == latest digests): frontend `sha256:f229b522...`, backend `sha256:848f1f2c...`. Local image-based redeploy from these images: all services healthy, 12/12 tests pass. Evidence files refreshed.
- Both Dockerfiles validated with `docker run --rm -i hadolint/hadolint` → exit 0 (evidence `hadolint.txt`).
- PR #60 created via GitHub REST API to `atindeRR:main`. Instructor CI runs show `action_required` (workflow approval pending from upstream maintainer) — NOT a pass; must report honestly.

### Environment notes
- Host 127.0.0.1:8080 is occupied by Oracle TNSLSNR; use `http://10.21.128.113:8080` locally. GitHub runners unaffected.
- `gh` CLI absent; GitHub API via stored Git credential works (token never displayed).
- `reportlab` and `pypdf` installed locally for PDF generation / question-paper parsing.
- Instructor question paper confirmed: PR title `DOCKER-SET-2 | ROLL-NUMBER | STUDENT-NAME | SECTION`; PDF name `ROLL_NUMBER_STUDENT_NAME_SET2.pdf`; PDF sections A–D (declaration exact) + evidence items 1–11; PDF upload to Moodle AND attach to PR.

## PENDING

1. Confirm latest CD run (after `e527b7c`) completed successfully and all steps passed; refresh `github-actions.txt`.
2. Re-verify Docker Hub manifests after the CD rebuild; re-capture image-based deployment evidence with new image IDs.
3. **PR title** — DONE: patched to `DOCKER-SET-2 | 202401100400162 | Sakshi | SEC_C`. Instructor CI is `action_required` (upstream maintainer approval) — cannot be forced; reported honestly. Local replication of every instructor CI step passed with a clean volume (`instructor-ci-local.txt`).
4. **PDF** — DONE: `202401100400162_Sakshi_SET2.pdf` generated with reportlab; verified A/B/C/D sections, exact declaration, 12/12 tests, Hub tags, workflows, PR URL; JWT/password redaction confirmed. To do: commit/push to fork, add PR comment linking the PDF, and user must upload it to Moodle manually.
5. Final report with Completed/Failed/Pending checklist.

## REMAINING EXTERNAL ACTIONS
- Instructor must approve the PR workflow run on atindeRR (GitHub first-time contributor gate). Cannot be done from student account.
- Student must upload `202401100400162_Sakshi_SET2.pdf` to Moodle manually; GitHub API cannot attach arbitrary files to a PR, so a PR comment links to the committed PDF.

## GOTCHAS
- Never commit `.env`, `node_modules/`, `dist/`, evidence temp files, tokens, or passwords.
- Leave instructor `ci.yml` untouched; it creates its own `.env` with `POSTGRES_PASSWORD=ci_test_password_123`, so compose must keep `${POSTGRES_PASSWORD}` interpolation.
- Keep numeric USER in Dockerfiles — named USER fails hadolint DL3066 with current `hadolint:latest`.
- Frontend Rollup override is required for Alpine builds — do not remove.
