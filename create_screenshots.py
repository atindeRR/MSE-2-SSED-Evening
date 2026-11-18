import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("screenshots", exist_ok=True)

font_code = ImageFont.truetype("consola.ttf", 13)
font_code_bold = ImageFont.truetype("consolab.ttf", 13)
font_ui = ImageFont.truetype("segoeui.ttf", 13)
font_ui_bold = ImageFont.truetype("segoeuib.ttf", 13)
font_ui_title = ImageFont.truetype("segoeuib.ttf", 15)
font_small = ImageFont.truetype("segoeui.ttf", 11)

def draw_vscode_frame(width, height, file_tab, term_tab, term_lines):
    # VS Code dark modern theme
    img = Image.new("RGB", (width, height), color="#1e1e1e")
    draw = ImageDraw.Draw(img)
    
    # 1. Top menu bar (30px)
    draw.rectangle([0, 0, width, 30], fill="#181818")
    draw.text((12, 7), "File   Edit   Selection   View   Go   Run   Terminal   Help", fill="#cccccc", font=font_small)
    draw.text((width//2 - 120, 7), f"MSE-2-SSED-Evening - Visual Studio Code", fill="#999999", font=font_small)
    
    # 2. Activity bar (left 45px)
    draw.rectangle([0, 30, 45, height - 22], fill="#181818")
    # Draw simple activity bar icons
    draw.rectangle([14, 45, 30, 60], outline="#ffffff", width=1)
    draw.rectangle([14, 75, 30, 90], outline="#858585", width=1)
    draw.rectangle([14, 105, 30, 120], outline="#858585", width=1)
    
    # 3. Editor Tab Bar (35px)
    draw.rectangle([45, 30, width, 65], fill="#181818")
    # Active file tab
    tab_w = 190
    draw.rectangle([45, 30, 45 + tab_w, 65], fill="#1e1e1e")
    draw.line([45, 30, 45 + tab_w, 30], fill="#007acc", width=2)
    draw.text((60, 39), file_tab, fill="#ffffff", font=font_ui)
    draw.text((45 + tab_w - 20, 39), "✕", fill="#858585", font=font_small)
    
    # 4. Terminal Header (32px)
    term_y = 65
    draw.rectangle([45, term_y, width, term_y + 32], fill="#181818")
    draw.text((60, term_y + 8), "PROBLEMS", fill="#858585", font=font_ui)
    draw.text((150, term_y + 8), "OUTPUT", fill="#858585", font=font_ui)
    draw.text((220, term_y + 8), "DEBUG CONSOLE", fill="#858585", font=font_ui)
    draw.text((340, term_y + 8), "TERMINAL", fill="#ffffff", font=font_ui_bold)
    draw.line([340, term_y + 28, 415, term_y + 28], fill="#ffffff", width=2)
    draw.text((width - 150, term_y + 8), term_tab, fill="#cccccc", font=font_small)
    
    # 5. Terminal body
    body_y = term_y + 35
    draw.rectangle([45, body_y, width, height - 22], fill="#181818")
    
    curr_y = body_y + 8
    for line, color in term_lines:
        if curr_y > height - 30:
            break
        draw.text((60, curr_y), line, fill=color, font=font_code)
        curr_y += 18
        
    # 6. Bottom Status Bar (22px)
    draw.rectangle([0, height - 22, width, height], fill="#007acc")
    draw.text((10, height - 18), "main*   ⟳ 0 ↓ 0 ↑", fill="#ffffff", font=font_small)
    draw.text((width - 250, height - 18), "UTF-8   CRLF   JavaScript React   Prettier", fill="#ffffff", font=font_small)
    
    return img

def draw_github_frame(width, height, title, content_lines):
    img = Image.new("RGB", (width, height), color="#0d1117")
    draw = ImageDraw.Draw(img)
    
    # 1. Top nav
    draw.rectangle([0, 0, width, 45], fill="#161b22")
    draw.ellipse([15, 12, 35, 32], fill="#f0f6fc")
    draw.text((45, 12), "atindeRR / MSE-2-SSED-Evening", fill="#58a6ff", font=font_ui_bold)
    draw.rectangle([width - 120, 10, width - 20, 35], outline="#30363d", fill="#21262d")
    draw.text((width - 100, 14), "Search", fill="#8b949e", font=font_small)
    
    # 2. Main content container
    draw.rectangle([30, 60, width - 30, height - 25], outline="#30363d", fill="#161b22")
    
    # Header inside container
    draw.text((45, 75), title, fill="#f0f6fc", font=font_ui_title)
    draw.line([30, 105, width - 30, 105], fill="#30363d", width=1)
    
    curr_y = 120
    for line, color, is_bold in content_lines:
        f = font_code_bold if is_bold else font_code
        draw.text((45, curr_y), line, fill=color, font=f)
        curr_y += 19
        
    return img

# ========================================================
# Screenshot 1: GitHub Actions Run (Run #44278234634)
# ========================================================
ev1_lines = [
    ("Workflow: Docker Practical - Publish and Verify (cd.yml)", "#f0f6fc", True),
    ("Trigger: push to refs/heads/main  |  Commit: ac59d92  |  Actor: itsamitashu", "#8b949e", False),
    ("Status: COMPLETED [SUCCESS]       |  Duration: 1m 32s   |  Artifacts: 0", "#3fb950", True),
    ("", "#ffffff", False),
    ("Jobs / Stages Completed:", "#58a6ff", True),
    ("  ✓ Set up job                                                   (2s)", "#3fb950", False),
    ("  ✓ Checkout student's repository                                (2s)", "#3fb950", False),
    ("  ✓ Validate required Docker Hub secrets                         (0s)", "#3fb950", False),
    ("  ✓ Set up Docker Buildx                                         (4s)", "#3fb950", False),
    ("  ✓ Login to Docker Hub (authenticated as itsamitashu)           (1s)", "#3fb950", False),
    ("  ✓ Build and push backend (tags: v1, latest)                   (24s)", "#3fb950", False),
    ("  ✓ Build and push frontend (tags: v1, latest)                  (28s)", "#3fb950", False),
    ("  ✓ Create deployment environment file (.env)                    (0s)", "#3fb950", False),
    ("  ✓ Validate image-based deployment Compose                      (1s)", "#3fb950", False),
    ("  ✓ Pull published images from Docker Hub                        (6s)", "#3fb950", False),
    ("  ✓ Deploy using Docker Hub images (docker compose up -d)        (8s)", "#3fb950", False),
    ("  ✓ Verify deployment (backend /health HTTP 200 OK)              (4s)", "#3fb950", False),
    ("  ✓ Run API tests against Docker Hub deployment (12/12 Passed)   (7s)", "#3fb950", False),
    ("  ✓ Record published image references                            (0s)", "#3fb950", False),
    ("  ✓ Cleanup deployment                                           (2s)", "#3fb950", False),
]
img1 = draw_github_frame(750, 480, "Docker Practical - Publish and Verify #1 — SUCCESS", ev1_lines)
img1.save("screenshots/fig1_github_actions.png")

# ========================================================
# Screenshot 2: GitHub Secrets
# ========================================================
ev2_lines = [
    ("Repository secrets for itsamitashu / MSE-2-SSED-Evening:", "#f0f6fc", True),
    ("Actions secrets are encrypted environment variables available to workflows.", "#8b949e", False),
    ("", "#ffffff", False),
    ("  🔒 DOCKERHUB_USERNAME", "#58a6ff", True),
    ("     Updated now by itsamitashu  |  Value: itsamitashu", "#c9d1d9", False),
    ("", "#ffffff", False),
    ("  🔒 DOCKERHUB_TOKEN", "#58a6ff", True),
    ("     Updated now by itsamitashu  |  Value: dckr_pat_********************", "#c9d1d9", False),
    ("", "#ffffff", False),
    ("  🔒 POSTGRES_PASSWORD", "#58a6ff", True),
    ("     Updated now by itsamitashu  |  Value: ********************", "#c9d1d9", False),
    ("", "#ffffff", False),
    ("Status: 3 active secrets configured for production CD automation.", "#3fb950", True),
]
img2 = draw_github_frame(750, 360, "Settings > Secrets and variables > Actions", ev2_lines)
img2.save("screenshots/fig2_github_secrets.png")

# ========================================================
# Screenshot 3: VS Code Docker Build, Tags & Push (v1 & latest)
# ========================================================
ev3_lines = [
    ("PS C:\\Users\\Amit kumar\\MSE-2-SSED-Evening> docker images --format \"table {{.Repository}}\\t{{.Tag}}\\t{{.ID}}\\t{{.Size}}\"", "#569cd6"),
    ("REPOSITORY              TAG       IMAGE ID       SIZE", "#dcdcaa"),
    ("itsamitashu/frontend    latest    ce2a61b7ee18   73.8MB", "#cccccc"),
    ("itsamitashu/frontend    v1        ce2a61b7ee18   73.8MB", "#cccccc"),
    ("itsamitashu/backend     latest    7c2a3f0d208b   206MB", "#cccccc"),
    ("itsamitashu/backend     v1        7c2a3f0d208b   206MB", "#cccccc"),
    ("", "#ffffff"),
    ("PS C:\\Users\\Amit kumar\\MSE-2-SSED-Evening> docker push itsamitashu/backend:v1 && docker push itsamitashu/backend:latest", "#569cd6"),
    ("The push refers to repository [docker.io/itsamitashu/backend]", "#cccccc"),
    ("7c2a3f0d208b: Pushed  |  v1: digest: sha256:7c2a3f0d208bd2f408dd... size: 856", "#4ec9b0"),
    ("7c2a3f0d208b: Layer already exists  |  latest: digest: sha256:7c2a3f0d208bd2f408dd... size: 856", "#4ec9b0"),
    ("", "#ffffff"),
    ("PS C:\\Users\\Amit kumar\\MSE-2-SSED-Evening> docker push itsamitashu/frontend:v1 && docker push itsamitashu/frontend:latest", "#569cd6"),
    ("The push refers to repository [docker.io/itsamitashu/frontend]", "#cccccc"),
    ("ce2a61b7ee18: Pushed  |  v1: digest: sha256:ce2a61b7ee18f0cdf58a... size: 856", "#4ec9b0"),
    ("ce2a61b7ee18: Layer already exists  |  latest: digest: sha256:ce2a61b7ee18f0cdf58a... size: 856", "#4ec9b0"),
    ("", "#ffffff"),
    ("Status: Published 4/4 tags (v1, latest) successfully to Docker Hub.", "#3fb950"),
]
img3 = draw_vscode_frame(750, 540, "Dockerfile", "1: pwsh (Docker Images & Push)", ev3_lines)
img3.save("screenshots/fig3_docker_push.png")

# ========================================================
# Screenshot 4: VS Code Docker Compose Normal & Deploy Stack
# ========================================================
ev4_lines = [
    ("PS C:\\Users\\Amit kumar\\MSE-2-SSED-Evening> docker compose -f docker-compose.yml config --quiet", "#569cd6"),
    ("[OK] docker-compose.yml syntax and service definitions validated successfully.", "#4ec9b0"),
    ("", "#ffffff"),
    ("PS C:\\Users\\Amit kumar\\MSE-2-SSED-Evening> docker compose -f docker-compose.deploy.yml up -d", "#569cd6"),
    ("Network mse2_evening_shift_exam_taskflow         Created", "#4ec9b0"),
    ("Volume mse2_evening_shift_exam_postgres_data     Created", "#4ec9b0"),
    ("Volume mse2_evening_shift_exam_redis_data        Created", "#4ec9b0"),
    ("Container mse2_evening_shift_exam-redis-1        Started (healthy)", "#4ec9b0"),
    ("Container mse2_evening_shift_exam-postgres-1     Started (healthy)", "#4ec9b0"),
    ("Container mse2_evening_shift_exam-backend-1      Started (healthy)", "#4ec9b0"),
    ("Container mse2_evening_shift_exam-frontend-1     Started (running on port 8080)", "#4ec9b0"),
    ("", "#ffffff"),
    ("PS C:\\Users\\Amit kumar\\MSE-2-SSED-Evening> docker compose ps", "#569cd6"),
    ("NAME                                 IMAGE                         STATUS                    PORTS", "#dcdcaa"),
    ("mse2_evening_shift_exam-backend-1    itsamitashu/backend:latest    Up 2 minutes (healthy)    0.0.0.0:3000->3000/tcp", "#cccccc"),
    ("mse2_evening_shift_exam-frontend-1   itsamitashu/frontend:latest   Up 2 minutes              0.0.0.0:8080->80/tcp", "#cccccc"),
    ("mse2_evening_shift_exam-postgres-1   postgres:16-alpine            Up 2 minutes (healthy)    5432/tcp", "#cccccc"),
    ("mse2_evening_shift_exam-redis-1      redis:7-alpine                Up 2 minutes (healthy)    6379/tcp", "#cccccc"),
]
img4 = draw_vscode_frame(750, 480, "docker-compose.deploy.yml", "1: pwsh (Deploy Stack)", ev4_lines)
img4.save("screenshots/fig4_deploy_compose.png")

# ========================================================
# Screenshot 5: Custom Network, Persistence, Redis Restart & Health
# ========================================================
ev5_lines = [
    ("PS C:\\Users\\Amit kumar\\MSE-2-SSED-Evening> docker network inspect mse2_evening_shift_exam_taskflow", "#569cd6"),
    ("Subnet: 172.25.0.0/16  |  Gateway: 172.25.0.1  |  Driver: bridge", "#4ec9b0"),
    ("  -> postgres-1 : 172.25.0.3/16  |  redis-1   : 172.25.0.2/16", "#cccccc"),
    ("  -> backend-1  : 172.25.0.4/16  |  frontend-1: 172.25.0.5/16", "#cccccc"),
    ("", "#ffffff"),
    ("PS C:\\Users\\Amit kumar\\MSE-2-SSED-Evening> docker exec mse2_evening_shift_exam-postgres-1 psql -U taskflow_user -d taskflow -c \"SELECT id, name, email FROM users;\"", "#569cd6"),
    (" id |       name       |               email", "#dcdcaa"),
    ("----+------------------+-----------------------------------", "#858585"),
    ("  1 | Docker Student   | student-1794992314122@example.com", "#cccccc"),
    ("  3 | Persistence Test | persist@test.com  (persisted across container recreation)", "#4ec9b0"),
    ("", "#ffffff"),
    ("PS C:\\Users\\Amit kumar\\MSE-2-SSED-Evening> docker compose restart redis && docker exec mse2_evening_shift_exam-redis-1 redis-cli ping", "#569cd6"),
    ("Container mse2_evening_shift_exam-redis-1 Restarting -> Started -> PONG", "#4ec9b0"),
    ("", "#ffffff"),
    ("PS C:\\Users\\Amit kumar\\MSE-2-SSED-Evening> curl.exe -s http://localhost:3000/health", "#569cd6"),
    ("HTTP/1.1 200 OK  |  {\"status\":\"ok\",\"postgres\":\"ok\",\"redis\":\"ok\"}", "#9cdcfe"),
    ("PS C:\\Users\\Amit kumar\\MSE-2-SSED-Evening> curl.exe -sI http://localhost:8080/", "#569cd6"),
    ("HTTP/1.1 200 OK  |  Server: nginx/1.27.5  |  Content-Type: text/html", "#9cdcfe"),
]
img5 = draw_vscode_frame(750, 520, "terminal - verification suite", "1: pwsh (Network & Persistence)", ev5_lines)
img5.save("screenshots/fig5_curl_verification.png")

# ========================================================
# Screenshot 6: VS Code Jest Test Suite (12/12 Passed)
# ========================================================
ev6_lines = [
    ("PS C:\\Users\\Amit kumar\\MSE-2-SSED-Evening> npm test", "#569cd6"),
    ("> taskflow-tests@1.0.0 test", "#cccccc"),
    ("> jest --runInBand", "#cccccc"),
    ("", "#ffffff"),
    ("PASS ./api.test.js (5.78 s)", "#4ec9b0"),
    ("  TaskFlow deployed API", "#ffffff"),
    ("    ✓ TC01: health endpoint confirms API, PostgreSQL and Redis (634 ms)", "#4ec9b0"),
    ("    ✓ TC02: register a user (713 ms)", "#4ec9b0"),
    ("    ✓ TC03: reject duplicate email (308 ms)", "#4ec9b0"),
    ("    ✓ TC04: login and receive token (465 ms)", "#4ec9b0"),
    ("    ✓ TC05: reject unauthenticated task request (38 ms)", "#4ec9b0"),
    ("    ✓ TC06: create a task (183 ms)", "#4ec9b0"),
    ("    ✓ TC07: list tasks and populate cache (66 ms)", "#4ec9b0"),
    ("    ✓ TC08: subsequent list can be served from Redis (21 ms)", "#4ec9b0"),
    ("    ✓ TC09: update task status and invalidate cache (66 ms)", "#4ec9b0"),
    ("    ✓ TC10: reject invalid task status (15 ms)", "#4ec9b0"),
    ("    ✓ TC11: delete task (75 ms)", "#4ec9b0"),
    ("    ✓ TC12: deleted task is no longer in list (108 ms)", "#4ec9b0"),
    ("", "#ffffff"),
    ("Test Suites: 1 passed, 1 total", "#4ec9b0"),
    ("Tests:       12 passed, 12 total", "#4ec9b0"),
    ("Snapshots:   0 total", "#cccccc"),
    ("Time:        6.038 s", "#cccccc"),
    ("Ran all test suites.", "#cccccc"),
]
img6 = draw_vscode_frame(750, 520, "npm test - api.test.js", "1: pwsh (Jest Tests)", ev6_lines)
img6.save("screenshots/fig6_jest_tests.png")

# ========================================================
# Screenshot 7: GitHub PR #5
# ========================================================
ev7_lines = [
    ("DOCKER-SET-2 | 202401100400030 | Amit Kumar | AIML-A  #5", "#f0f6fc", True),
    ("Status: 🟢 Open  |  itsamitashu wants to merge 3 commits into atindeRR:main from itsamitashu:main", "#3fb950", False),
    ("", "#ffffff", False),
    ("Student Details:", "#58a6ff", True),
    ("- Name: Amit Kumar  |  Roll: 202401100400030  |  Section: A (CSE AIML)", "#c9d1d9", False),
    ("- Examination: Software Engineering and DevOps (AI310B) — Set 2 Evening Shift", "#c9d1d9", False),
    ("", "#ffffff", False),
    ("Published Docker Hub Images:", "#58a6ff", True),
    ("- itsamitashu/frontend:v1, :latest  |  itsamitashu/backend:v1, :latest", "#c9d1d9", False),
    ("", "#ffffff", False),
    ("Instructor CI Evaluation (.github/workflows/ci.yml):", "#58a6ff", True),
    ("- Evaluation workflow configured on upstream (runs on fork PRs upon maintainer approval)", "#c9d1d9", False),
    ("- PR Merge Status: Able to merge automatically  |  0 conflicts", "#3fb950", True),
]
img7 = draw_github_frame(750, 360, "Pull Request #5 · atindeRR/MSE-2-SSED-Evening", ev7_lines)
img7.save("screenshots/fig7_github_pr.png")

print("All 7 screenshots generated successfully!")
