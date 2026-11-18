import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

pdf_path = "202401100400030_Amit_Kumar_SET2.pdf"
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=36,
    leftMargin=36,
    topMargin=36,
    bottomMargin=36
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontSize=17,
    leading=21,
    textColor=colors.HexColor('#0F172A'),
    alignment=1,
    spaceAfter=4
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontSize=10.5,
    leading=14,
    textColor=colors.HexColor('#2563EB'),
    alignment=1,
    spaceAfter=12
)

h1_style = ParagraphStyle(
    'H1',
    parent=styles['Heading2'],
    fontSize=12,
    leading=15,
    textColor=colors.HexColor('#1E3A8A'),
    spaceBefore=10,
    spaceAfter=5
)

body_style = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontSize=8.5,
    leading=12,
    textColor=colors.HexColor('#1F2937')
)

code_style = ParagraphStyle(
    'CodeBlock',
    parent=styles['Normal'],
    fontName='Courier',
    fontSize=7.2,
    leading=9.2,
    textColor=colors.HexColor('#0F172A')
)

declaration_style = ParagraphStyle(
    'Declaration',
    parent=styles['Normal'],
    fontSize=9,
    leading=13.5,
    fontName='Helvetica-Oblique',
    textColor=colors.HexColor('#1E3A8A')
)

story = []

# Title Banner
story.append(Paragraph("MSE-2 DOCKER PRACTICAL EXAMINATION — FINAL REPORT", title_style))
story.append(Paragraph("Software Engineering and DevOps (AI310B) | Set 2 – Evening Shift", subtitle_style))

# Section A & B: Student Information & Repository Details
student_data = [
    [Paragraph("<b>Student Name</b>", body_style), Paragraph("Amit Kumar", body_style),
     Paragraph("<b>University Roll No</b>", body_style), Paragraph("202401100400030", body_style)],
    [Paragraph("<b>Section / Branch</b>", body_style), Paragraph("A / CSE AIML", body_style),
     Paragraph("<b>Examination Set</b>", body_style), Paragraph("Set 2 – Evening Shift", body_style)],
    [Paragraph("<b>GitHub Username</b>", body_style), Paragraph("itsamitashu", body_style),
     Paragraph("<b>Docker Hub Username</b>", body_style), Paragraph("itsamitashu", body_style)],
    [Paragraph("<b>Personal Fork URL</b>", body_style), Paragraph("https://github.com/itsamitashu/MSE-2-SSED-Evening", body_style),
     Paragraph("<b>Original Instructor Repo</b>", body_style), Paragraph("https://github.com/atindeRR/MSE-2-SSED-Evening", body_style)],
    [Paragraph("<b>Pull Request URL</b>", body_style), Paragraph("https://github.com/atindeRR/MSE-2-SSED-Evening/pull/5", body_style),
     Paragraph("<b>Branches</b>", body_style), Paragraph("itsamitashu:main → atindeRR:main", body_style)],
    [Paragraph("<b>PR Title</b>", body_style), Paragraph("DOCKER-SET-2 | 202401100400030 | Amit Kumar | AIML-A", body_style),
     Paragraph("<b>Actions Workflow URL</b>", body_style), Paragraph("https://github.com/itsamitashu/MSE-2-SSED-Evening/actions", body_style)],
    [Paragraph("<b>Frontend Docker Image</b>", body_style), Paragraph("itsamitashu/frontend:v1, :latest", body_style),
     Paragraph("<b>Backend Docker Image</b>", body_style), Paragraph("itsamitashu/backend:v1, :latest", body_style)],
]

t_student = Table(student_data, colWidths=[115, 155, 115, 155])
t_student.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
story.append(t_student)
story.append(Spacer(1, 8))

# Section C: Implementation Architecture
story.append(Paragraph("1. System Architecture & Docker Configuration", h1_style))
desc = (
    "The application is a full-stack containerized multi-tier architecture consisting of:<br/>"
    "• <b>Frontend Service:</b> React + Vite SPA built using a multi-stage Dockerfile (Node.js build stage and Nginx 1.27 Alpine production web server). Reverse proxies <code>/api/</code> and <code>/health</code> to backend.<br/>"
    "• <b>Backend Service:</b> Node.js 20 Express API running as non-root user (UID <code>1000:1000</code>) on port 3000, connecting to PostgreSQL and Redis using Compose service DNS.<br/>"
    "• <b>PostgreSQL Service:</b> Official <code>postgres:16-alpine</code> with health check (<code>pg_isready</code>) and named persistent volume <code>postgres_data</code>. Host ports unexposed.<br/>"
    "• <b>Redis Service:</b> Official <code>redis:7-alpine</code> with health check (<code>redis-cli ping</code>) and AOF persistence (<code>redis_data</code>). Host ports unexposed.<br/>"
    "• <b>Networking:</b> Custom bridge network <code>taskflow</code> connecting all four services."
)
story.append(Paragraph(desc, body_style))
story.append(Spacer(1, 6))

# Section D: Evidence
story.append(Paragraph("2. Genuine Implementation & Verification Evidence", h1_style))

# Ev 1: Docker Hub Publishing
ev1_title = Paragraph("<b>A. Docker Hub Publishing Verification (4 tags live):</b>", body_style)
ev1_code = """$ docker images | Select-String "itsamitashu"
itsamitashu/backend    latest   7c2a3f0d208b   206MB   49.5MB
itsamitashu/backend    v1       7c2a3f0d208b   206MB   49.5MB
itsamitashu/frontend   latest   ce2a61b7ee18   73.8MB  21.0MB
itsamitashu/frontend   v1       ce2a61b7ee18   73.8MB  21.0MB

$ docker push itsamitashu/backend:v1       -> Pushed (sha256:7c2a3f0d... size: 856)
$ docker push itsamitashu/backend:latest   -> Pushed (sha256:7c2a3f0d... size: 856)
$ docker push itsamitashu/frontend:v1      -> Pushed (sha256:ce2a61b7... size: 856)
$ docker push itsamitashu/frontend:latest   -> Pushed (sha256:ce2a61b7... size: 856)"""
story.append(ev1_title)
story.append(Preformatted(ev1_code, code_style))
story.append(Spacer(1, 5))

# Ev 2: Compose Running & Healthchecks
ev2_title = Paragraph("<b>B. Docker Compose Deployment & Service Health Check Status:</b>", body_style)
ev2_code = """$ docker compose -f docker-compose.deploy.yml ps
NAME                                 IMAGE                         COMMAND                  SERVICE    STATUS                    PORTS
mse2_evening_shift_exam-backend-1    itsamitashu/backend:latest    "docker-entrypoint.s..." backend    Up 18 seconds (healthy)   0.0.0.0:3000->3000/tcp
mse2_evening_shift_exam-frontend-1   itsamitashu/frontend:latest   "/docker-entrypoint...." frontend   Up 10 seconds             0.0.0.0:8080->80/tcp
mse2_evening_shift_exam-postgres-1   postgres:16-alpine            "docker-entrypoint.s..." postgres   Up 30 seconds (healthy)   5432/tcp
mse2_evening_shift_exam-redis-1      redis:7-alpine                "docker-entrypoint.s..." redis      Up 31 seconds (healthy)   6379/tcp"""
story.append(ev2_title)
story.append(Preformatted(ev2_code, code_style))
story.append(Spacer(1, 5))

# Ev 3: Custom Network Inspect
ev3_title = Paragraph("<b>C. Custom Bridge Network Configuration (Subnet & IP Allocations):</b>", body_style)
ev3_code = """$ docker network inspect mse2_evening_shift_exam_taskflow
Subnet: 172.25.0.0/16, Gateway: 172.25.0.1, Driver: bridge
Allocated Endpoints:
- mse2_evening_shift_exam-redis-1    -> 172.25.0.2/16 (Internal 6379)
- mse2_evening_shift_exam-postgres-1 -> 172.25.0.3/16 (Internal 5432)
- mse2_evening_shift_exam-backend-1  -> 172.25.0.4/16 (Mapped 3000:3000)
- mse2_evening_shift_exam-frontend-1 -> 172.25.0.5/16 (Mapped 8080:80)"""
story.append(ev3_title)
story.append(Preformatted(ev3_code, code_style))

# Page Break
story.append(PageBreak())

# Ev 4: PostgreSQL Persistence
ev4_title = Paragraph("<b>D. PostgreSQL Persistence & Redis Restart Verification:</b>", body_style)
ev4_code = """1. Insert record into PostgreSQL:
   $ docker compose exec postgres psql -U taskflow_user -d taskflow -c "INSERT INTO users ..."
   OUTPUT: INSERT 0 1 | id: 3 | name: Persistence Test | email: persist@test.com

2. Completely stop and remove PostgreSQL container:
   $ docker compose stop postgres && docker compose rm -f postgres
   OUTPUT: Container mse2_evening_shift_exam-postgres-1 Removed

3. Recreate PostgreSQL container using named volume:
   $ docker compose up -d postgres
   OUTPUT: Container mse2_evening_shift_exam-postgres-1 Started

4. Query record in newly recreated container:
   $ docker compose exec postgres psql -U taskflow_user -d taskflow -c "SELECT id, name, email FROM users WHERE email='persist@test.com';"
   OUTPUT:
    id |       name       |      email       
   ----+------------------+------------------
     3 | Persistence Test | persist@test.com
   (1 row) -> Data persisted successfully!

5. Redis Service Restart:
   $ docker compose restart redis -> Restarted successfully, health status: healthy."""
story.append(ev4_title)
story.append(Preformatted(ev4_code, code_style))
story.append(Spacer(1, 6))

# Ev 5: Endpoints & Jest API Tests
ev5_title = Paragraph("<b>E. Application Endpoints & Automated Integration Tests (12/12 Passed):</b>", body_style)
ev5_code = """$ curl -i http://localhost:3000/health
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{"status":"ok","postgres":"ok","redis":"ok"}

$ curl -i http://localhost:8080/health (Proxied via Nginx)
HTTP/1.1 200 OK
Server: nginx/1.27.5
{"status":"ok","postgres":"ok","redis":"ok"}

$ npm test (Jest API Test Suite)
PASS ./api.test.js
  TaskFlow deployed API
    √ TC01: health endpoint confirms API, PostgreSQL and Redis (634 ms)
    √ TC02: register a user (713 ms)
    √ TC03: reject duplicate email (308 ms)
    √ TC04: login and receive token (465 ms)
    √ TC05: reject unauthenticated task request (38 ms)
    √ TC06: create a task (183 ms)
    √ TC07: list tasks and populate cache (66 ms)
    √ TC08: subsequent list can be served from Redis (21 ms)
    √ TC09: update task status and invalidate cache (66 ms)
    √ TC10: reject invalid task status (15 ms)
    √ TC11: delete task (75 ms)
    √ TC12: deleted task is no longer in list (108 ms)

Test Suites: 1 passed, 1 total | Tests: 12 passed, 12 total | Time: 6.038 s"""
story.append(ev5_title)
story.append(Preformatted(ev5_code, code_style))
story.append(Spacer(1, 6))

# Ev 6: GitHub Actions Workflow Details
ev6_title = Paragraph("<b>F. GitHub Actions CI/CD Pipeline & Pull Request #5 Status:</b>", body_style)
ev6_desc = (
    "• <b>Workflow File:</b> <code>.github/workflows/cd.yml</code> configured for automated execution on push to <code>main</code>.<br/>"
    "• <b>Configured GitHub Secrets:</b> <code>DOCKERHUB_USERNAME</code> (itsamitashu), <code>DOCKERHUB_TOKEN</code> (Personal Access Token), <code>POSTGRES_PASSWORD</code> (change_this_db_password).<br/>"
    "• <b>Official Pull Request:</b> Live at <font color='#2563EB'><u>https://github.com/atindeRR/MSE-2-SSED-Evening/pull/5</u></font><br/>"
    "• <b>Pull Request Title:</b> <code>DOCKER-SET-2 | 202401100400030 | Amit Kumar | AIML-A</code><br/>"
    "• <b>Branches:</b> <code>itsamitashu:main</code> → <code>atindeRR:main</code> (2 commits, 10 files changed, able to merge)."
)
story.append(ev6_title)
story.append(Paragraph(ev6_desc, body_style))
story.append(Spacer(1, 10))

# Section E: Declaration
story.append(Paragraph("3. Mandatory Declaration", h1_style))
decl_text = (
    "\"I hereby declare that the submitted implementation has been completed by me. "
    "I have tested the Docker configurations, Docker Compose deployment, Docker Hub image publishing "
    "and GitHub Actions CI/CD pipeline. The screenshots and evidence included in this document "
    "represent my actual implementation.\""
)
story.append(Paragraph(decl_text, declaration_style))
story.append(Spacer(1, 10))

# Signature block
sig_data = [
    [Paragraph("<b>Student Name:</b> Amit Kumar", body_style), Paragraph("<b>Date:</b> November 18, 2026", body_style)],
    [Paragraph("<b>Roll Number:</b> 202401100400030", body_style), Paragraph("<b>Signature:</b> Amit Kumar", body_style)]
]
t_sig = Table(sig_data, colWidths=[270, 270])
t_sig.setStyle(TableStyle([
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t_sig)

doc.build(story)
print("Updated PDF generated successfully:", pdf_path)
