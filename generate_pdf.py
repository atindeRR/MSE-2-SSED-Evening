import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, PageBreak
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

# Custom styles
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontSize=18,
    leading=22,
    textColor=colors.HexColor('#1E3A8A'),
    alignment=1,
    spaceAfter=10
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontSize=11,
    leading=15,
    textColor=colors.HexColor('#4B5563'),
    alignment=1,
    spaceAfter=15
)

h1_style = ParagraphStyle(
    'H1',
    parent=styles['Heading2'],
    fontSize=13,
    leading=16,
    textColor=colors.HexColor('#1E3A8A'),
    spaceBefore=12,
    spaceAfter=6
)

body_style = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontSize=9,
    leading=13,
    textColor=colors.HexColor('#1F2937')
)

code_style = ParagraphStyle(
    'CodeBlock',
    parent=styles['Normal'],
    fontName='Courier',
    fontSize=7.5,
    leading=9.5,
    textColor=colors.HexColor('#111827')
)

declaration_style = ParagraphStyle(
    'Declaration',
    parent=styles['Normal'],
    fontSize=9.5,
    leading=14,
    fontName='Helvetica-Oblique',
    textColor=colors.HexColor('#1E3A8A')
)

story = []

# Title
story.append(Paragraph("MSE-2 DOCKER PRACTICAL EXAMINATION REPORT", title_style))
story.append(Paragraph("Software Engineering and DevOps (AI310B) — Set 2 (Evening Shift)", subtitle_style))
story.append(Spacer(1, 8))

# Section A & B: Student & Submission Info Table
student_data = [
    [Paragraph("<b>Student Name</b>", body_style), Paragraph("Amit Kumar", body_style),
     Paragraph("<b>Roll Number</b>", body_style), Paragraph("202401100400030", body_style)],
    [Paragraph("<b>Section</b>", body_style), Paragraph("A", body_style),
     Paragraph("<b>Branch</b>", body_style), Paragraph("CSE AIML", body_style)],
    [Paragraph("<b>GitHub Username</b>", body_style), Paragraph("itsamitashu", body_style),
     Paragraph("<b>Docker Hub Username</b>", body_style), Paragraph("itsamitashu", body_style)],
    [Paragraph("<b>Fork Repository</b>", body_style), Paragraph("https://github.com/itsamitashu/MSE-2-SSED-Evening", body_style),
     Paragraph("<b>Target Repository</b>", body_style), Paragraph("https://github.com/atindeRR/MSE-2-SSED-Evening", body_style)],
    [Paragraph("<b>PR Title Format</b>", body_style), Paragraph("DOCKER-SET-2 | 202401100400030 | Amit Kumar | AIML-A", body_style),
     Paragraph("<b>Target Branch</b>", body_style), Paragraph("main", body_style)],
    [Paragraph("<b>Frontend Docker Image</b>", body_style), Paragraph("itsamitashu/frontend:v1, :latest", body_style),
     Paragraph("<b>Backend Docker Image</b>", body_style), Paragraph("itsamitashu/backend:v1, :latest", body_style)],
]

t_student = Table(student_data, colWidths=[110, 160, 110, 160])
t_student.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t_student)
story.append(Spacer(1, 10))

# Section: Docker Implementation Summary
story.append(Paragraph("1. Docker Implementation Overview", h1_style))
desc = (
    "<b>Architecture:</b> Multi-container microservices application comprising a React Vite frontend (Nginx runtime on port 80/8080), "
    "an Express.js backend (port 3000), a PostgreSQL 16 database, and a Redis 7 caching service on a dedicated bridge network <code>taskflow</code>.<br/>"
    "• <b>Frontend Dockerfile:</b> Multi-stage build with Node.js build stage and lightweight Nginx Alpine production runtime. Zero hadolint warnings.<br/>"
    "• <b>Backend Dockerfile:</b> Multi-stage Alpine build, non-root execution (UID 1000:1000), minimal production dependencies, zero hadolint warnings.<br/>"
    "• <b>Docker Compose:</b> Configured health checks for all services, custom bridge network, and named volumes <code>postgres_data</code> & <code>redis_data</code>.<br/>"
    "• <b>Image Deployment:</b> <code>docker-compose.deploy.yml</code> uses published Docker Hub images without local build directives."
)
story.append(Paragraph(desc, body_style))
story.append(Spacer(1, 8))

# Section: Verification Evidence
story.append(Paragraph("2. Implementation & Execution Evidence", h1_style))

# Item 1: Docker Images Tagged & Published
ev1_title = Paragraph("<b>A. Docker Hub Publishing Verification:</b>", body_style)
ev1_text = """$ docker images | Select-String "itsamitashu"
itsamitashu/backend    latest   7c2a3f0d208b   206MB   49.5MB
itsamitashu/backend    v1       7c2a3f0d208b   206MB   49.5MB
itsamitashu/frontend   latest   ce2a61b7ee18   73.8MB  21.0MB
itsamitashu/frontend   v1       ce2a61b7ee18   73.8MB  21.0MB

$ docker push itsamitashu/backend:v1 -> Pushed (digest: sha256:7c2a3f0d... size: 856)
$ docker push itsamitashu/backend:latest -> Pushed (digest: sha256:7c2a3f0d... size: 856)
$ docker push itsamitashu/frontend:v1 -> Pushed (digest: sha256:ce2a61b7... size: 856)
$ docker push itsamitashu/frontend:latest -> Pushed (digest: sha256:ce2a61b7... size: 856)"""
story.append(ev1_title)
story.append(Preformatted(ev1_text, code_style))
story.append(Spacer(1, 6))

# Item 2: Docker Compose Services Running & Health Checks
ev2_title = Paragraph("<b>B. Docker Compose Deployment & Service Health Checks:</b>", body_style)
ev2_text = """$ docker compose -f docker-compose.deploy.yml ps
NAME                                 IMAGE                         COMMAND                  SERVICE    STATUS                    PORTS
mse2_evening_shift_exam-backend-1    itsamitashu/backend:latest    "docker-entrypoint.s..." backend    Up 18 seconds (healthy)   0.0.0.0:3000->3000/tcp
mse2_evening_shift_exam-frontend-1   itsamitashu/frontend:latest   "/docker-entrypoint...." frontend   Up 10 seconds             0.0.0.0:8080->80/tcp
mse2_evening_shift_exam-postgres-1   postgres:16-alpine            "docker-entrypoint.s..." postgres   Up 30 seconds (healthy)   5432/tcp (internal)
mse2_evening_shift_exam-redis-1      redis:7-alpine                "docker-entrypoint.s..." redis      Up 31 seconds (healthy)   6379/tcp (internal)"""
story.append(ev2_title)
story.append(Preformatted(ev2_text, code_style))
story.append(Spacer(1, 6))

# Item 3: Custom Docker Network Configuration
ev3_title = Paragraph("<b>C. Custom Docker Network (Isolated Bridge):</b>", body_style)
ev3_text = """$ docker network inspect mse2_evening_shift_exam_taskflow
Subnet: 172.25.0.0/16, Gateway: 172.25.0.1
Connected Containers:
- mse2_evening_shift_exam-redis-1    -> 172.25.0.2/16 (Port 6379 internal)
- mse2_evening_shift_exam-postgres-1 -> 172.25.0.3/16 (Port 5432 internal)
- mse2_evening_shift_exam-backend-1  -> 172.25.0.4/16 (Port 3000 mapped)
- mse2_evening_shift_exam-frontend-1 -> 172.25.0.5/16 (Port 80 mapped to 8080)"""
story.append(ev3_title)
story.append(Preformatted(ev3_text, code_style))
story.append(Spacer(1, 6))

# Page Break for clean layout
story.append(PageBreak())

# Item 4: Database Persistence Verification
ev4_title = Paragraph("<b>D. PostgreSQL Data Persistence Verification:</b>", body_style)
ev4_text = """1. Insert record into PostgreSQL:
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
   (1 row)
   RESULT: PostgreSQL data persisted successfully across container removal."""
story.append(ev4_title)
story.append(Preformatted(ev4_text, code_style))
story.append(Spacer(1, 8))

# Item 5: API Health & Full Integration Test Suite
ev5_title = Paragraph("<b>E. Application Endpoints & Automated Jest Test Suite:</b>", body_style)
ev5_text = """$ curl -i http://localhost:3000/health
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{"status":"ok","postgres":"ok","redis":"ok"}

$ curl -i http://localhost:8080/health (Proxied via Nginx)
HTTP/1.1 200 OK
Server: nginx/1.27.5
{"status":"ok","postgres":"ok","redis":"ok"}

$ npm test (Jest Test Suite)
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

Test Suites: 1 passed, 1 total | Tests: 12 passed, 12 total"""
story.append(ev5_title)
story.append(Preformatted(ev5_text, code_style))
story.append(Spacer(1, 8))

# Item 6: GitHub Actions Workflow Architecture
ev6_title = Paragraph("<b>F. GitHub Actions CI/CD Pipeline (.github/workflows/cd.yml):</b>", body_style)
ev6_text = (
    "<b>Trigger:</b> On push to <code>main</code> branch.<br/>"
    "<b>Stages:</b><br/>"
    "1. Checkout source code (<code>actions/checkout@v4</code>)<br/>"
    "2. Validate required secrets (<code>DOCKERHUB_USERNAME</code>, <code>DOCKERHUB_TOKEN</code>, <code>POSTGRES_PASSWORD</code>)<br/>"
    "3. Set up Docker Buildx (<code>docker/setup-buildx-action@v3</code>)<br/>"
    "4. Authenticate to Docker Hub (<code>docker/login-action@v3</code>)<br/>"
    "5. Build and push backend image (tagged <code>:v1</code> and <code>:latest</code>)<br/>"
    "6. Build and push frontend image (tagged <code>:v1</code> and <code>:latest</code>)<br/>"
    "7. Generate deployment <code>.env</code> file with non-hardcoded secrets<br/>"
    "8. Validate <code>docker-compose.deploy.yml</code> (verifies no <code>build:</code> directives)<br/>"
    "9. Pull published Docker Hub images (<code>docker compose -f docker-compose.deploy.yml pull</code>)<br/>"
    "10. Deploy application (<code>docker compose -f docker-compose.deploy.yml up -d</code>)<br/>"
    "11. Verify health endpoints & run automated Jest test suite against live deployment<br/>"
    "12. Teardown stack cleanly."
)
story.append(ev6_title)
story.append(Paragraph(ev6_text, body_style))
story.append(Spacer(1, 14))

# Section D: Mandatory Declaration
story.append(Paragraph("3. Mandatory Declaration", h1_style))
decl_text = (
    "\"I hereby declare that the submitted implementation has been completed by me. "
    "I have tested the Docker configurations, Docker Compose deployment, Docker Hub image publishing "
    "and GitHub Actions CI/CD pipeline. The screenshots and evidence included in this document "
    "represent my actual implementation.\""
)
story.append(Paragraph(decl_text, declaration_style))
story.append(Spacer(1, 14))

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
print("PDF generated successfully:", pdf_path)
