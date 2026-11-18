# Submission evidence status

Thirteen genuine screenshots are included:

- `01-frontend-build.png` and `02-backend-build.png` - fresh Docker Compose image builds and local image inspection.
- `03-compose-services.png` - four image-deployment services running and healthy.
- `04-docker-network.png` - Compose bridge network name, driver, scope, and connected container count.
- `05-postgres-health.png`, `06-redis-health.png`, and `07-backend-health.png` - live container health and backend health route.
- `08-postgres-persistence.png` - a fresh sentinel survived PostgreSQL container removal and recreation; the named volume was retained.
- `09-redis-restart.png` - Redis restarted, became healthy, and returned `PONG`.
- `10-dockerhub-frontend.png` and `11-dockerhub-backend.png` - public Docker Hub tags.
- `12-image-deployment.png` - image pull, health-gated deployment, four healthy services, and both health routes.
- `13-application-browser.png` - TaskFlow served by the published-image deployment.

All terminal captures show live command output from this audit. They were captured from the full desktop terminal view without editing or adding output to the images.

Still unavailable (not fabricated):

- `14-github-actions.png` - the actual run succeeded, but no local Actions screenshot file is available.
- `15-github-repository.png` - the attempted page capture did not render repository contents.
- `16-pull-request.png` - a genuine PR screenshot was provided in chat, but it is not saved in this folder.
- `17-instructor-ci.png` - pending instructor-side checks; the PR is open but instructor checks have not run.

Repository: https://github.com/VishalPrajapati3112/MSE-2-SSED-Evening
Workflow run: https://github.com/VishalPrajapati3112/MSE-2-SSED-Evening/actions/runs/44292072593 (SUCCESS)
Pull Request: https://github.com/atindeRR/MSE-2-SSED-Evening/pull/176 (OPEN; not merged)
PR description/screenshot attachment: pending; GitHub integration write requests returned HTTP 403 and the chat screenshot is not available as a local file to upload.

Regenerate the PDF with `python scripts/generate_submission_pdf.py`; matching numbered PNGs are embedded automatically.
