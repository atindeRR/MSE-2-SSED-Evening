import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

pdf_path = "202401100400030_Amit_Kumar_SET2.pdf"
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=40,
    leftMargin=40,
    topMargin=32,
    bottomMargin=32
)

styles = getSampleStyleSheet()

PRIMARY_BLUE = colors.HexColor('#1D4ED8')
HEADER_BG = colors.HexColor('#F8FAFC')
BORDER_COLOR = colors.HexColor('#E2E8F0')
SUCCESS_GREEN = colors.HexColor('#16A34A')
SUCCESS_BG = colors.HexColor('#F0FDF4')

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
    spaceBefore=7,
    spaceAfter=4
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
    spaceBefore=2,
    spaceAfter=6
)

ev_title_style = ParagraphStyle(
    'EvTitle',
    parent=styles['Normal'],
    fontName='Helvetica-BoldOblique',
    fontSize=9,
    leading=12,
    textColor=colors.HexColor('#0F172A'),
    spaceBefore=2,
    spaceAfter=3
)

story = []

# ==========================================
# PAGE 1: TITLE & DETAILS TABLES
# ==========================================
story.append(Paragraph("MSE-2 EVENING SHIFT EXAMINATION REPORT", title_style))
story.append(Paragraph("Software Engineering and DevOps (AI310B) — Docker Practical Examination", subtitle_style))

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
    [Paragraph("Frontend Image (General):", body_bold), Paragraph("https://hub.docker.com/r/itsamitashu/frontend", body_val_mono)],
    [Paragraph("Backend Image (General):", body_bold), Paragraph("https://hub.docker.com/r/itsamitashu/backend", body_val_mono)],
    [Paragraph("Frontend Image (TaskFlow):", body_bold), Paragraph("https://hub.docker.com/r/itsamitashu/taskflow-frontend", body_val_mono)],
    [Paragraph("Backend Image (TaskFlow):", body_bold), Paragraph("https://hub.docker.com/r/itsamitashu/taskflow-backend", body_val_mono)],
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
    "Deploy Compose Validation, Pull Images, Deploy Containers, Verify Health (HTTP 200), Jest "
    "API Tests (12/12 Passed)"
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
story.append(Image("screenshots/fig1_github_actions.png", width=360, height=230))
story.append(Paragraph("Figure 1: GitHub Actions CD Pipeline (Run #44278234634) showing all stages completed successfully.", caption_style))
story.append(Spacer(1, 4))

# Evidence 2
story.append(Paragraph("Evidence 2: Docker Hub Authentication & Repository Secrets Configuration", ev_title_style))
story.append(Image("screenshots/fig2_github_secrets.png", width=420, height=202))
story.append(Paragraph("Figure 2: Verified GitHub Actions secrets: DOCKERHUB_USERNAME, DOCKERHUB_TOKEN, POSTGRES_PASSWORD.", caption_style))

# ==========================================
# PAGE 3: EVIDENCE 3 & 4
# ==========================================
story.append(PageBreak())
story.append(Paragraph("5. Practical CI/CD Execution Evidence Screenshots (Contd.)", sec_heading_style))

# Evidence 3
story.append(Paragraph("Evidence 3: Backend & Frontend Docker Image Build and Publishing (VS Code Terminal)", ev_title_style))
story.append(Image("screenshots/fig3_docker_push.png", width=330, height=237))
story.append(Paragraph("Figure 3: VS Code integrated terminal executing Docker push for itsamitashu/backend:latest and itsamitashu/frontend:latest.", caption_style))
story.append(Spacer(1, 4))

# Evidence 4
story.append(Paragraph("Evidence 4: Docker Compose Image Pull & Container Deployment (VS Code Terminal)", ev_title_style))
story.append(Image("screenshots/fig4_deploy_compose.png", width=360, height=230))
story.append(Paragraph("Figure 4: VS Code terminal deploying docker-compose.deploy.yml with published images and verifying healthy container status.", caption_style))

# ==========================================
# PAGE 4: EVIDENCE 5 & 6
# ==========================================
story.append(PageBreak())
story.append(Paragraph("5. Practical CI/CD Execution Evidence Screenshots (Contd.)", sec_heading_style))

# Evidence 5
story.append(Paragraph("Evidence 5: Backend Health Check & Frontend Accessibility Verification (VS Code Terminal)", ev_title_style))
story.append(Image("screenshots/fig5_curl_verification.png", width=335, height=232))
story.append(Paragraph("Figure 5: VS Code terminal curl execution confirming Backend status 'ok' on port 3000 and Frontend HTTP 200 OK on port 8080.", caption_style))
story.append(Spacer(1, 4))

# Evidence 6
story.append(Paragraph("Evidence 6: Automated API & Redis Caching Test Suite (VS Code Terminal)", ev_title_style))
story.append(Image("screenshots/fig6_jest_tests.png", width=335, height=232))
story.append(Paragraph("Figure 6: VS Code terminal running Jest test suite confirming 12/12 passed tests for API, Redis, and PostgreSQL.", caption_style))

# ==========================================
# PAGE 5: PR, CHECKLIST & DECLARATION
# ==========================================
story.append(PageBreak())
story.append(Paragraph("6. Pull Request Submission & Mandatory Declaration", sec_heading_style))

# Evidence 7
story.append(Paragraph("Evidence 7: Submitted Pull Request on Instructor Repository (#5)", ev_title_style))
story.append(Image("screenshots/fig7_github_pr.png", width=400, height=192))
story.append(Paragraph("Figure 7: Pull Request #5 created on atindeRR/MSE-2-SSED-Evening with required title and details.", caption_style))
story.append(Spacer(1, 4))

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
    ('TOPPADDING', (0,0), (-1,-1), 1.8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
    ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, HEADER_BG]),
]))
story.append(t_chk)
story.append(Spacer(1, 8))

# Mandatory Student Declaration
story.append(Paragraph("Mandatory Student Declaration", body_bold))
decl_p = Paragraph(
    "<i>\"I hereby declare that the submitted implementation has been completed by me. "
    "I have tested the Docker configurations, Docker Compose deployment, Docker Hub image publishing "
    "and GitHub Actions CI/CD pipeline. The screenshots and evidence included in this document "
    "represent my actual implementation.\"</i>",
    body_val
)
sig_p = Paragraph("<b>Student Signature:</b> Amit Kumar<br/><b>Date:</b> November 18, 2026", body_bold)

t_decl = Table([[decl_p], [Spacer(1, 3)], [sig_p]], colWidths=[532])
t_decl.setStyle(TableStyle([
    ('BOX', (0,0), (-1,-1), 1, PRIMARY_BLUE),
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('RIGHTPADDING', (0,0), (-1,-1), 10),
]))
story.append(t_decl)

doc.build(story)
print("Pixel-perfect Evening Shift PDF with genuine screenshots generated successfully:", pdf_path)
