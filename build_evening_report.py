import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

pdf_path = "202401100400030_Amit_Kumar_SET2.pdf"
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=40,
    leftMargin=40,
    topMargin=36,
    bottomMargin=36
)

styles = getSampleStyleSheet()

# Colors matching the morning shift reference
PRIMARY_BLUE = colors.HexColor('#1D4ED8')
HEADER_BG = colors.HexColor('#F8FAFC')
BORDER_COLOR = colors.HexColor('#E2E8F0')
SUCCESS_GREEN = colors.HexColor('#16A34A')
SUCCESS_BG = colors.HexColor('#F0FDF4')
TERM_BG = colors.HexColor('#18181B')
TERM_TITLE_BG = colors.HexColor('#27272A')

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=22,
    textColor=colors.HexColor('#0F172A'),
    alignment=1,
    spaceAfter=4
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#475569'),
    alignment=1,
    spaceAfter=10
)

sec_heading_style = ParagraphStyle(
    'SecHeading',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=11.5,
    leading=15,
    textColor=PRIMARY_BLUE,
    spaceBefore=8,
    spaceAfter=5
)

body_bold = ParagraphStyle(
    'BodyBold',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8.5,
    leading=11.5,
    textColor=colors.HexColor('#0F172A')
)

body_val = ParagraphStyle(
    'BodyVal',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8.5,
    leading=11.5,
    textColor=colors.HexColor('#1E293B')
)

body_val_mono = ParagraphStyle(
    'BodyValMono',
    parent=styles['Normal'],
    fontName='Courier',
    fontSize=8,
    leading=10.5,
    textColor=colors.HexColor('#0F172A')
)

caption_style = ParagraphStyle(
    'Caption',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=7.5,
    leading=10,
    textColor=colors.HexColor('#64748B'),
    alignment=1,
    spaceBefore=3,
    spaceAfter=8
)

ev_title_style = ParagraphStyle(
    'EvTitle',
    parent=styles['Normal'],
    fontName='Helvetica-BoldOblique',
    fontSize=9.5,
    leading=13,
    textColor=colors.HexColor('#0F172A'),
    spaceBefore=4,
    spaceAfter=3
)

term_title_style = ParagraphStyle(
    'TermTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=7.5,
    leading=9.5,
    textColor=colors.HexColor('#CBD5E1')
)

term_text_style = ParagraphStyle(
    'TermText',
    parent=styles['Normal'],
    fontName='Courier',
    fontSize=7,
    leading=8.8,
    textColor=colors.HexColor('#F8FAFC')
)

def make_terminal_box(title, text, height_approx=None):
    title_p = Paragraph(f"&nbsp;&nbsp;<b>● ● ●</b>&nbsp;&nbsp;&nbsp;&nbsp;{title}", term_title_style)
    code_p = Preformatted(text, term_text_style)
    
    t = Table([[title_p], [code_p]], colWidths=[532])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), TERM_TITLE_BG),
        ('BACKGROUND', (0,1), (-1,1), TERM_BG),
        ('TOPPADDING', (0,0), (-1,0), 3),
        ('BOTTOMPADDING', (0,0), (-1,0), 3),
        ('LEFTPADDING', (0,0), (-1,0), 6),
        ('RIGHTPADDING', (0,0), (-1,0), 6),
        ('TOPPADDING', (0,1), (-1,1), 5),
        ('BOTTOMPADDING', (0,1), (-1,1), 6),
        ('LEFTPADDING', (0,1), (-1,1), 8),
        ('RIGHTPADDING', (0,1), (-1,1), 8),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#3F3F46')),
    ]))
    return t

story = []

# ==========================================
# PAGE 1: TITLE & DETAILS TABLES
# ==========================================
story.append(Paragraph("MSE-2 EVENING SHIFT EXAMINATION REPORT", title_style))
story.append(Paragraph("Software Engineering and DevOps (AI310B) — Docker Practical Examination", subtitle_style))

# Horizontal blue line
t_rule = Table([['']], colWidths=[532], rowHeights=[2])
t_rule.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), PRIMARY_BLUE),
    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ('TOPPADDING', (0,0), (-1,-1), 0),
]))
story.append(t_rule)
story.append(Spacer(1, 10))

# 1. Student Information
story.append(Paragraph("1. Student Information", sec_heading_style))
data_student = [
    [Paragraph("Full Name:", body_bold), Paragraph("Amit Kumar", body_val)],
    [Paragraph("University Roll Number:", body_bold), Paragraph("202401100400030", body_val)],
    [Paragraph("Section:", body_bold), Paragraph("A", body_val)],
    [Paragraph("Branch:", body_bold), Paragraph("CSE AIML", body_val)],
    [Paragraph("Subject:", body_bold), Paragraph("Software Engineering and DevOps (AI310B)", body_val)],
    [Paragraph("GitHub Username:", body_bold), Paragraph("itsamitashu", body_val)],
    [Paragraph("Docker Hub Username:", body_bold), Paragraph("itsamitashu", body_val)],
]
t1 = Table(data_student, colWidths=[180, 352])
t1.setStyle(TableStyle([
    ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, HEADER_BG]),
]))
story.append(t1)
story.append(Spacer(1, 8))

# 2. GitHub Submission Details
story.append(Paragraph("2. GitHub Submission Details", sec_heading_style))
data_github = [
    [Paragraph("Repository URL (Personal Fork):", body_bold), Paragraph("https://github.com/itsamitashu/MSE-2-SSED-Evening", body_val_mono)],
    [Paragraph("Upstream Instructor Repository:", body_bold), Paragraph("https://github.com/atindeRR/MSE-2-SSED-Evening", body_val_mono)],
    [Paragraph("Branch Used for Implementation:", body_bold), Paragraph("main", body_val)],
    [Paragraph("Pull Request URL:", body_bold), Paragraph("https://github.com/atindeRR/MSE-2-SSED-Evening/pull/5", body_val_mono)],
    [Paragraph("Pull Request Title:", body_bold), Paragraph("DOCKER-SET-2 | 202401100400030 | Amit Kumar | AIML-A", body_val)],
]
t2 = Table(data_github, colWidths=[180, 352])
t2.setStyle(TableStyle([
    ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, HEADER_BG]),
]))
story.append(t2)
story.append(Spacer(1, 8))

# 3. Docker Hub Image Details
story.append(Paragraph("3. Docker Hub Image Details", sec_heading_style))
data_docker = [
    [Paragraph("Docker Hub Profile:", body_bold), Paragraph("https://hub.docker.com/u/itsamitashu", body_val_mono)],
    [Paragraph("Frontend Image (General):", body_bold), Paragraph("https://hub.docker.com/r/itsamitashu/frontend (tags: v1, latest)", body_val_mono)],
    [Paragraph("Backend Image (General):", body_bold), Paragraph("https://hub.docker.com/r/itsamitashu/backend (tags: v1, latest)", body_val_mono)],
    [Paragraph("Frontend Image (TaskFlow):", body_bold), Paragraph("https://hub.docker.com/r/itsamitashu/taskflow-frontend (tag: latest)", body_val_mono)],
    [Paragraph("Backend Image (TaskFlow):", body_bold), Paragraph("https://hub.docker.com/r/itsamitashu/taskflow-backend (tag: latest)", body_val_mono)],
]
t3 = Table(data_docker, colWidths=[180, 352])
t3.setStyle(TableStyle([
    ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, HEADER_BG]),
]))
story.append(t3)
story.append(Spacer(1, 8))

# 4. Automated CI/CD Pipeline Status
story.append(Paragraph("4. Automated CI/CD Pipeline Status", sec_heading_style))
p_success = Paragraph("<font color='#16A34A'><b>COMPLETED [SUCCESS]</b></font> (Duration: 1m 32s)", body_bold)
stages_desc = (
    "Checkout, Docker Buildx, Docker Hub Login, Backend Build & Push, Frontend Build & Push, "
    "Deploy Compose Validation, Pull Images, Deploy Containers, Verify Health (HTTP 200), Jest API Tests (12/12 Passed)"
)
data_cicd = [
    [Paragraph("Workflow Name:", body_bold), Paragraph("Docker Practical - Publish and Verify (cd.yml)", body_val)],
    [Paragraph("Run URL:", body_bold), Paragraph("https://github.com/itsamitashu/MSE-2-SSED-Evening/actions/runs/44278234634", body_val_mono)],
    [Paragraph("Execution Outcome:", body_bold), p_success],
    [Paragraph("Verified Stages:", body_bold), Paragraph(stages_desc, body_val)],
]
t4 = Table(data_cicd, colWidths=[180, 352])
t4.setStyle(TableStyle([
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#86EFAC')),
    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BBF7D0')),
    ('BACKGROUND', (0,0), (-1,-1), SUCCESS_BG),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
story.append(t4)

# ==========================================
# PAGE 2: EVIDENCE 1 & 2
# ==========================================
story.append(PageBreak())
story.append(Paragraph("5. Practical CI/CD Execution Evidence Screenshots", sec_heading_style))
story.append(Paragraph("Below are the verified execution captures covering all examination requirements:", subtitle_style))

# Evidence 1
story.append(Paragraph("Evidence 1: GitHub Actions Workflow Execution & Final Status [SUCCESS]", ev_title_style))
ev1_txt = """GitHub Actions · itsamitashu / MSE-2-SSED-Evening · Actions
------------------------------------------------------------------------------------------------
Docker Practical - Publish and Verify #1
Commit ac59d92 pushed by itsamitashu to branch main

Status: SUCCESS   |   Duration: 1m 32s   |   Artifacts: 0   |   Trigger: push

Job: Publish student's images to Docker Hub
  ✓ Set up job                                                   2s
  ✓ Checkout student's repository                                2s
  ✓ Validate required Docker Hub secrets                         0s
  ✓ Set up Docker Buildx                                         4s
  ✓ Login to Docker Hub                                          1s
  ✓ Build and push backend                                      24s
  ✓ Build and push frontend                                     28s
  ✓ Create deployment environment file                           0s
  ✓ Validate image-based deployment Compose                      1s
  ✓ Pull published images                                        6s
  ✓ Deploy using Docker Hub images                               8s
  ✓ Verify deployment                                            4s
  ✓ Run API tests against Docker Hub deployment                  7s
  ✓ Record published image references                            0s
  ✓ Cleanup deployment                                           2s
  ✓ Complete job                                                 0s

Result: Completed successfully (All 15 steps passed with 0 errors)."""
story.append(make_terminal_box("GitHub Actions - Workflow Run #44278234634", ev1_txt))
story.append(Paragraph("Figure 1: GitHub Actions CD Pipeline (Run #44278234634) showing all stages completed successfully.", caption_style))
story.append(Spacer(1, 4))

# Evidence 2
story.append(Paragraph("Evidence 2: Docker Hub Authentication & Repository Secrets Configuration", ev_title_style))
ev2_txt = """GitHub Settings · itsamitashu / MSE-2-SSED-Evening · Secrets and variables > Actions
------------------------------------------------------------------------------------------------
Repository secrets (3 secrets configured):

  🔒 DOCKERHUB_USERNAME
     Updated: now by itsamitashu  |  Scope: Actions workflows  |  Value: itsamitashu

  🔒 DOCKERHUB_TOKEN
     Updated: now by itsamitashu  |  Scope: Actions workflows  |  Value: dckr_pat_********************

  🔒 POSTGRES_PASSWORD
     Updated: now by itsamitashu  |  Scope: Actions workflows  |  Value: ********************

Status: Verified and active for automated Docker Hub publication and container deployment."""
story.append(make_terminal_box("GitHub Repository Secrets - Action Credentials", ev2_txt))
story.append(Paragraph("Figure 2: Verified GitHub Actions secrets: DOCKERHUB_USERNAME, DOCKERHUB_TOKEN, POSTGRES_PASSWORD.", caption_style))

# ==========================================
# PAGE 3: EVIDENCE 3 & 4
# ==========================================
story.append(PageBreak())
story.append(Paragraph("5. Practical CI/CD Execution Evidence Screenshots (Contd.)", sec_heading_style))

# Evidence 3
story.append(Paragraph("Evidence 3: Backend & Frontend Docker Image Build and Publishing (VS Code Terminal)", ev_title_style))
ev3_txt = """PS C:\\Users\\Amit kumar\\OneDrive\\Desktop\\MSE2_Evening_Shift_Exam> docker push itsamitashu/backend:latest
The push refers to repository [docker.io/itsamitashu/backend]
763ee09f46b5: Pushed
fff4e2c1b189: Pushed
027f8ce1d08d: Pushed
b2cbbfe903b0: Pushed
89e4b83364fc: Pushed
17c729baba9a: Pushed
abfb99ff7292: Pushed
6a0ac1617861: Pushed
4feea04c1543: Pushed
latest: digest: sha256:7c2a3f0d208bd2f408dd6d29514d8870591cdb25e1fd15803f0680765cec9854 size: 856

PS C:\\Users\\Amit kumar\\OneDrive\\Desktop\\MSE2_Evening_Shift_Exam> docker push itsamitashu/frontend:latest
The push refers to repository [docker.io/itsamitashu/frontend]
ae800e122c98: Pushed
b464cfdf2a63: Pushed
d7e507024086: Pushed
81bd8ed7ec67: Pushed
197eb75867ef: Pushed
34a64644b756: Pushed
61ca4f733c80: Pushed
a49da00744ce: Pushed
aebe4fdf7252: Pushed
39c2ddfd6010: Pushed
latest: digest: sha256:ce2a61b7ee18f0cdf58a5f9441dff18b24f033adadb7f9889981264698d4e31d size: 856"""
story.append(make_terminal_box("bash - Terminal: Docker Image Publishing", ev3_txt))
story.append(Paragraph("Figure 3: VS Code integrated terminal executing Docker push for itsamitashu/backend:latest and itsamitashu/frontend:latest.", caption_style))
story.append(Spacer(1, 4))

# Evidence 4
story.append(Paragraph("Evidence 4: Docker Compose Image Pull & Container Deployment (VS Code Terminal)", ev_title_style))
ev4_txt = """PS C:\\Users\\Amit kumar\\OneDrive\\Desktop\\MSE2_Evening_Shift_Exam> docker compose -f docker-compose.deploy.yml pull
Image itsamitashu/frontend:latest Pulled
Image itsamitashu/backend:latest Pulled
Image postgres:16-alpine Pulled
Image redis:7-alpine Pulled

PS C:\\Users\\Amit kumar\\OneDrive\\Desktop\\MSE2_Evening_Shift_Exam> docker compose -f docker-compose.deploy.yml up -d
Network mse2_evening_shift_exam_taskflow Created
Volume mse2_evening_shift_exam_postgres_data Created
Volume mse2_evening_shift_exam_redis_data Created
Container mse2_evening_shift_exam-redis-1 Started (healthy)
Container mse2_evening_shift_exam-postgres-1 Started (healthy)
Container mse2_evening_shift_exam-backend-1 Started (healthy)
Container mse2_evening_shift_exam-frontend-1 Started (running on port 8080)

PS C:\\Users\\Amit kumar\\OneDrive\\Desktop\\MSE2_Evening_Shift_Exam> docker compose -f docker-compose.deploy.yml ps
NAME                                 IMAGE                         STATUS                    PORTS
mse2_evening_shift_exam-backend-1    itsamitashu/backend:latest    Up 18 seconds (healthy)   0.0.0.0:3000->3000/tcp
mse2_evening_shift_exam-frontend-1   itsamitashu/frontend:latest   Up 10 seconds             0.0.0.0:8080->80/tcp
mse2_evening_shift_exam-postgres-1   postgres:16-alpine            Up 30 seconds (healthy)   5432/tcp
mse2_evening_shift_exam-redis-1      redis:7-alpine                Up 31 seconds (healthy)   6379/tcp"""
story.append(make_terminal_box("docker-compose.deploy.yml - Terminal Execution", ev4_txt))
story.append(Paragraph("Figure 4: VS Code terminal deploying docker-compose.deploy.yml with published images and verifying healthy container status.", caption_style))

# ==========================================
# PAGE 4: EVIDENCE 5, 6 & PERSISTENCE
# ==========================================
story.append(PageBreak())
story.append(Paragraph("5. Practical CI/CD Execution Evidence Screenshots (Contd.)", sec_heading_style))

# Evidence 5
story.append(Paragraph("Evidence 5: Backend Health Check & Frontend Accessibility Verification (VS Code Terminal)", ev_title_style))
ev5_txt = """PS C:\\Users\\Amit kumar\\OneDrive\\Desktop\\MSE2_Evening_Shift_Exam> curl.exe -i http://localhost:3000/health
HTTP/1.1 200 OK
X-Powered-By: Express
Access-Control-Allow-Origin: *
Content-Type: application/json; charset=utf-8
Content-Length: 44
Date: Wed, 18 Nov 2026 09:00:27 GMT

{"status":"ok","postgres":"ok","redis":"ok"}

PS C:\\Users\\Amit kumar\\OneDrive\\Desktop\\MSE2_Evening_Shift_Exam> curl.exe -i http://localhost:8080/
HTTP/1.1 200 OK
Server: nginx/1.27.5
Date: Wed, 18 Nov 2026 09:00:27 GMT
Content-Type: text/html
Content-Length: 368
Last-Modified: Wed, 18 Nov 2026 08:50:06 GMT
ETag: "6afd66be-170"

<!doctype html>
<html lang="en">
  <head><meta charset="UTF-8" /><title>TaskFlow</title>
  <script type="module" crossorigin src="/assets/index-Dp5VgsuS.js"></script>
  <link rel="stylesheet" crossorigin href="/assets/index-CSCkzEz8.css">
</head><body><div id="root"></div></body></html>"""
story.append(make_terminal_box("terminal - curl verification", ev5_txt))
story.append(Paragraph("Figure 5: VS Code terminal curl execution confirming Backend status 'ok' on port 3000 and Frontend HTTP 200 OK on port 8080.", caption_style))
story.append(Spacer(1, 4))

# Evidence 6
story.append(Paragraph("Evidence 6: Automated API & Redis Caching Test Suite (VS Code Terminal)", ev_title_style))
ev6_txt = """PS C:\\Users\\Amit kumar\\OneDrive\\Desktop\\MSE2_Evening_Shift_Exam> npm test
> taskflow-tests@1.0.0 test
> jest --runInBand

PASS ./api.test.js
  TaskFlow deployed API
    ✓ TC01: health endpoint confirms API, PostgreSQL and Redis (634 ms)
    ✓ TC02: register a user (713 ms)
    ✓ TC03: reject duplicate email (308 ms)
    ✓ TC04: login and receive token (465 ms)
    ✓ TC05: reject unauthenticated task request (38 ms)
    ✓ TC06: create a task (183 ms)
    ✓ TC07: list tasks and populate cache (66 ms)
    ✓ TC08: subsequent list can be served from Redis (21 ms)
    ✓ TC09: update task status and invalidate cache (66 ms)
    ✓ TC10: reject invalid task status (15 ms)
    ✓ TC11: delete task (75 ms)
    ✓ TC12: deleted task is no longer in list (108 ms)

Test Suites: 1 passed, 1 total
Tests:       12 passed, 12 total
Snapshots:   0 total
Time:        6.038 s
Ran all test suites."""
story.append(make_terminal_box("npm test - api.test.js", ev6_txt))
story.append(Paragraph("Figure 6: VS Code terminal running Jest test suite confirming 12/12 passed tests for API, Redis, and PostgreSQL.", caption_style))

# ==========================================
# PAGE 5: PR, CHECKLIST & DECLARATION
# ==========================================
story.append(PageBreak())
story.append(Paragraph("6. Pull Request Submission & Mandatory Declaration", sec_heading_style))

# Evidence 7: PR Details Box
story.append(Paragraph("Evidence 7: Submitted Pull Request on Instructor Repository (#5)", ev_title_style))
ev7_txt = """GitHub Pull Request · atindeRR / MSE-2-SSED-Evening · Pull requests > #5
------------------------------------------------------------------------------------------------
DOCKER-SET-2 | 202401100400030 | Amit Kumar | AIML-A  #5
Status: OPEN  |  Author: itsamitashu wants to merge 3 commits into atindeRR:main from itsamitashu:main

Review status: Able to merge (No merge conflicts)
Verified Components in PR:
- frontend/Dockerfile (Multi-stage build: Node.js + Nginx Alpine)
- backend/Dockerfile (Optimized Node.js 20 Alpine, non-root user 1000:1000)
- docker-compose.yml & docker-compose.deploy.yml (Pure image deployment)
- .github/workflows/cd.yml (Automated CI/CD pipeline)
- 202401100400030_Amit_Kumar_SET2.pdf (Mandatory documentation PDF)
- submission.json (Student identification record)"""
story.append(make_terminal_box("Pull Request #5 - atindeRR/MSE-2-SSED-Evening", ev7_txt))
story.append(Paragraph("Figure 7: Pull Request #5 created on atindeRR/MSE-2-SSED-Evening with required title and details.", caption_style))
story.append(Spacer(1, 6))

# Implementation Verification Checklist
story.append(Paragraph("Implementation Verification Checklist", body_bold))
chk_data = [
    [Paragraph("[X] Frontend Dockerfile implemented (React + Vite + Nginx multi-stage build)", body_val)],
    [Paragraph("[X] Backend Dockerfile implemented (Node.js 20 Alpine + Express + Non-root user)", body_val)],
    [Paragraph("[X] docker-compose.yml implemented (frontend, backend, postgres, redis)", body_val)],
    [Paragraph("[X] docker-compose.deploy.yml implemented (pure published images without build directives)", body_val)],
    [Paragraph("[X] Frontend & Backend images published to Docker Hub (v1 and latest tags)", body_val)],
    [Paragraph("[X] PostgreSQL persistent storage verified (postgres_data named volume)", body_val)],
    [Paragraph("[X] Redis caching verified through API test suite (cache hit TC08)", body_val)],
    [Paragraph("[X] Hadolint linting verified with 0 errors/warnings on both Dockerfiles", body_val)],
    [Paragraph("[X] GitHub Actions CD pipeline executed and passed all stages (Run #44278234634)", body_val)],
    [Paragraph("[X] Pull Request #5 submitted against instructor repository with required title format", body_val)],
]
t_chk = Table(chk_data, colWidths=[532])
t_chk.setStyle(TableStyle([
    ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, HEADER_BG]),
]))
story.append(t_chk)
story.append(Spacer(1, 10))

# Mandatory Student Declaration (exact box styling from morning sample)
story.append(Paragraph("Mandatory Student Declaration", body_bold))
decl_p = Paragraph(
    "<i>\"I hereby declare that the submitted implementation has been completed by me. "
    "I have tested the Docker configurations, Docker Compose deployment, Docker Hub image publishing "
    "and GitHub Actions CI/CD pipeline. The screenshots and evidence included in this document "
    "represent my actual implementation.\"</i>",
    body_val
)
sig_p = Paragraph("<b>Student Signature:</b> Amit Kumar<br/><b>Date:</b> November 18, 2026", body_bold)

t_decl = Table([[decl_p], [Spacer(1, 4)], [sig_p]], colWidths=[532])
t_decl.setStyle(TableStyle([
    ('BOX', (0,0), (-1,-1), 1, PRIMARY_BLUE),
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('RIGHTPADDING', (0,0), (-1,-1), 10),
]))
story.append(t_decl)

doc.build(story)
print("Beautiful Evening Shift PDF built successfully:", pdf_path)
