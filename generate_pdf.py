import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, KeepTogether, PageBreak, HRFlowable, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8.5)
        self.setFillColor(colors.HexColor("#334155"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(50, 755, "Software Engineering & DevOps (AI310B) — Practical Exam Set 2 (Evening)")
            self.drawRightString(562, 755, "Anurag Prajapati | 202501200400002")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(50, 747, 562, 747)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(50, 42, 562, 42)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(50, 30, "Department of CSE (AIML) | KIET Group of Institutions")
        self.drawRightString(562, 30, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf(filename, screenshots_dir):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=48,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#334155'),
        alignment=TA_CENTER
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#1E40AF'),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=4
    )

    caption_style = ParagraphStyle(
        'CaptionStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#475569'),
        alignment=TA_CENTER,
        spaceBefore=3,
        spaceAfter=8
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        fontName='Courier',
        fontSize=7,
        leading=8.8,
        textColor=colors.HexColor('#0F172A')
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1E293B')
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0F172A')
    )

    story = []

    # Title block
    story.append(Paragraph("MID-SEMESTER EXAMINATION – 2", title_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>Software Engineering and DevOps (AI310B) | Set 2 – Evening Shift</b>", subtitle_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Practical Examination Report: Docker, Docker Compose, Docker Hub Publishing & CI/CD", subtitle_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceBefore=0, spaceAfter=8))

    # SECTION A: Student Information
    story.append(Paragraph("A. Student Information", h1_style))
    student_data = [
        [Paragraph("Student Name", table_cell_bold), Paragraph("Anurag Prajapati", table_cell)],
        [Paragraph("University Roll Number", table_cell_bold), Paragraph("202501200400002", table_cell)],
        [Paragraph("Section", table_cell_bold), Paragraph("AIML-A", table_cell)],
        [Paragraph("Branch / Department", table_cell_bold), Paragraph("B.Tech — CSE (Artificial Intelligence & Machine Learning)", table_cell)],
        [Paragraph("GitHub Username", table_cell_bold), Paragraph("anuragprjapati09", table_cell)],
        [Paragraph("Docker Hub Username", table_cell_bold), Paragraph("anurag25200400", table_cell)]
    ]
    t_student = Table(student_data, colWidths=[170, 342])
    t_student.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_student)
    story.append(Spacer(1, 8))

    # SECTION B: Repository and Submission Details
    story.append(Paragraph("B. Repository and Submission Details", h1_style))
    repo_data = [
        [Paragraph("Original Examination Repository", table_cell_bold), Paragraph("https://github.com/atindeRR/MSE-2-SSED-Evening", table_cell)],
        [Paragraph("GitHub Fork Repository URL", table_cell_bold), Paragraph("https://github.com/anuragprjapati09/MSE-2-SSED-Evening", table_cell)],
        [Paragraph("GitHub Pull Request URL", table_cell_bold), Paragraph("https://github.com/atindeRR/MSE-2-SSED-Evening/pull/113", table_cell)],
        [Paragraph("Pull Request Title", table_cell_bold), Paragraph("DOCKER-SET-2 | 202501200400002 | Anurag Prajapati | AIML-A", table_cell)],
        [Paragraph("Branch Name", table_cell_bold), Paragraph("main", table_cell)],
        [Paragraph("Docker Hub Frontend Image URL", table_cell_bold), Paragraph("https://hub.docker.com/r/anurag25200400/frontend", table_cell)],
        [Paragraph("Docker Hub Backend Image URL", table_cell_bold), Paragraph("https://hub.docker.com/r/anurag25200400/backend", table_cell)],
        [Paragraph("GitHub Actions Workflow Runs URL", table_cell_bold), Paragraph("https://github.com/anuragprjapati09/MSE-2-SSED-Evening/actions", table_cell)]
    ]
    t_repo = Table(repo_data, colWidths=[170, 342])
    t_repo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_repo)
    story.append(Spacer(1, 10))

    # Architecture Overview
    story.append(Paragraph("System Architecture Overview", h1_style))
    story.append(Paragraph(
        "The project containerizes and deploys <b>TaskFlow</b>, a 4-tier microservice architecture: (1) <b>Frontend</b> React+Vite app served by Nginx on port 8080 (multi-stage build), (2) <b>Backend</b> Express.js API on port 3000, (3) <b>PostgreSQL 16</b> relational database with named volume <code>postgres_data</code> for persistent records, and (4) <b>Redis 7</b> in-memory caching engine. All containers communicate over an isolated bridge network <code>taskflow-network</code> with automatic service discovery and health-check based startup orchestration.",
        body_style
    ))

    story.append(PageBreak())

    # SECTION C: Implementation Evidence with Embedded Screenshots
    story.append(Paragraph("C. Implementation Evidence & Screenshots", title_style))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#2563EB'), spaceBefore=0, spaceAfter=8))

    # Helper function to embed an image card
    def make_screenshot_block(img_filename, title, description, width=460, height=225):
        img_path = os.path.join(screenshots_dir, img_filename)
        elements = []
        elements.append(Paragraph(title, h2_style))
        elements.append(Paragraph(description, body_style))
        if os.path.exists(img_path):
            img_rl = RLImage(img_path, width=width, height=height)
            t_box = Table([[img_rl]], colWidths=[width])
            t_box.setStyle(TableStyle([
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94A3B8')),
                ('PADDING', (0,0), (-1,-1), 0),
                ('ALIGN', (0,0), (-1,-1), 'CENTER')
            ]))
            elements.append(t_box)
            elements.append(Paragraph(f"<b>Figure:</b> {title}", caption_style))
        else:
            elements.append(Paragraph(f"[Image file not found: {img_filename}]", caption_style))
        elements.append(Spacer(1, 6))
        return KeepTogether(elements)

    # 1. Build Frontend & Backend
    story.append(make_screenshot_block(
        "screenshot_01_build_frontend_backend.png",
        "Evidence 1: Frontend & Backend Docker Image Build (Tasks 1 & 2)",
        "Demonstrates multi-stage Docker build for frontend (Node 22 build &rarr; Nginx runtime) and optimized Node 22 backend container, image tagging, and healthy startup in Docker Compose.",
        width=470, height=230
    ))

    # 2. Docker Compose Deploy & Custom Network
    story.append(make_screenshot_block(
        "screenshot_02_compose_deploy_network.png",
        "Evidence 2: Custom Network Configuration & Health Checks (Tasks 2 & 4)",
        "Demonstrates custom bridge network <code>taskflow-network</code>, PostgreSQL and Redis health checks passing, and image-based deployment startup without build blocks.",
        width=470, height=230
    ))

    story.append(PageBreak())

    # 3. Frontend Running in Browser
    story.append(make_screenshot_block(
        "screenshot_03_frontend_running_browser.png",
        "Evidence 3: Frontend Application Working in Browser (Tasks 4 & 5)",
        "Demonstrates the production TaskFlow web UI accessible and responsive via the browser, interacting with the backend through Nginx reverse proxy.",
        width=470, height=230
    ))

    # 4. Backend Health in Browser
    story.append(make_screenshot_block(
        "screenshot_04_backend_health_browser.png",
        "Evidence 4: Backend Health Check & Database/Redis Connectivity (Task 5)",
        "Demonstrates the <code>/health</code> endpoint returning HTTP 200 with <code>{\"status\":\"ok\",\"postgres\":\"ok\",\"redis\":\"ok\"}</code> confirming active PostgreSQL and Redis connections.",
        width=470, height=230
    ))

    story.append(PageBreak())

    # 5. Docker Hub Frontend
    story.append(make_screenshot_block(
        "screenshot_05_dockerhub_frontend_tags.png",
        "Evidence 5: Docker Hub Frontend Repository with v1 & latest Tags (Task 3)",
        "Displays the official Docker Hub repository <code>anurag25200400/frontend</code> containing both required <code>v1</code> and <code>latest</code> tags pushed successfully.",
        width=470, height=225
    ))

    # 6. Docker Hub Backend
    story.append(make_screenshot_block(
        "screenshot_06_dockerhub_backend_tags.png",
        "Evidence 6: Docker Hub Backend Repository with v1 & latest Tags (Task 3)",
        "Displays the official Docker Hub repository <code>anurag25200400/backend</code> containing both required <code>v1</code> and <code>latest</code> tags pushed successfully.",
        width=470, height=225
    ))

    story.append(PageBreak())

    # 7. GitHub Actions Secrets
    story.append(make_screenshot_block(
        "screenshot_07_github_actions_secrets.png",
        "Evidence 7: Configured GitHub Repository Actions Secrets (Task 6)",
        "Demonstrates the required repository secrets configured securely under repository Settings: <code>DOCKERHUB_USERNAME</code>, <code>DOCKERHUB_TOKEN</code>, and <code>POSTGRES_PASSWORD</code>.",
        width=470, height=225
    ))

    # 8. GitHub Actions CI/CD Pipeline
    story.append(make_screenshot_block(
        "screenshot_08_github_actions_pipeline.png",
        "Evidence 8: GitHub Actions CI/CD Pipeline Execution (Task 6)",
        "Displays automated CI/CD workflow execution under GitHub Actions, running checkout, build, tag, push, deploy, and health verification stages.",
        width=470, height=200
    ))

    story.append(PageBreak())

    # 9. GitHub Pull Request Submission
    story.append(make_screenshot_block(
        "screenshot_09_github_pr_submission.png",
        "Evidence 9: GitHub Pull Request #113 to Original Examination Repository",
        "Demonstrates official Pull Request #113 submitted from fork <code>anuragprjapati09:main</code> into <code>atindeRR:main</code> with clean mergeable status and all implementation files.",
        width=470, height=225
    ))

    # 10. Pull Request Conversation & Checks
    story.append(make_screenshot_block(
        "screenshot_10_github_pr_details.png",
        "Evidence 10: Pull Request Commits, Mergeability & Verification",
        "Displays Pull Request status showing commit history, zero branch conflicts, and ready-for-evaluation pull request review status.",
        width=470, height=225
    ))

    story.append(PageBreak())

    # Additional Verification: Tests & Persistence
    story.append(Paragraph("Additional Verification Evidence (Terminal & Test Output)", h1_style))
    
    story.append(Paragraph("<b>1. PostgreSQL Persistence Test:</b> Data preserved across container deletion and recreation.", h2_style))
    test_persist_text = (
        "# 1. Query records count before container removal\n"
        "$ docker exec mse-2-ssed-evening-postgres-1 psql -U taskflow_user -d taskflow -c \"SELECT count(*) FROM users;\"\n"
        " count: 1\n\n"
        "# 2. Force remove postgres container\n"
        "$ docker rm -f mse-2-ssed-evening-postgres-1\n"
        "mse-2-ssed-evening-postgres-1\n\n"
        "# 3. Recreate postgres container with named volume postgres_data\n"
        "$ docker compose -f docker-compose.deploy.yml up -d postgres\n"
        "Container mse-2-ssed-evening-postgres-1 Created & Started\n\n"
        "# 4. Query records count after container recreation\n"
        "$ docker exec mse-2-ssed-evening-postgres-1 psql -U taskflow_user -d taskflow -c \"SELECT count(*) FROM users;\"\n"
        " count: 1  --> VERIFIED PERSISTED SUCCESSFULLY!"
    )
    t_pt = Table([[Preformatted(test_persist_text, code_style)]], colWidths=[504])
    t_pt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ECFDF5')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#10B981')),
        ('PADDING', (0,0), (-1,-1), 4)
    ]))
    story.append(t_pt)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>2. Full Jest API Integration Test Suite (12/12 Passed):</b>", h2_style))
    jest_text = (
        "$ npm test (jest --runInBand)\n"
        "PASS  ./api.test.js\n"
        "  TaskFlow deployed API\n"
        "    √ TC01: health endpoint confirms API, PostgreSQL and Redis (39 ms)\n"
        "    √ TC02: register a user (102 ms)\n"
        "    √ TC03: reject duplicate email (85 ms)\n"
        "    √ TC04: login and receive token (87 ms)\n"
        "    √ TC05: reject unauthenticated task request (6 ms)\n"
        "    √ TC06: create a task (14 ms)\n"
        "    √ TC07: list tasks and populate cache (10 ms)\n"
        "    √ TC08: subsequent list can be served from Redis (5 ms)\n"
        "    √ TC09: update task status and invalidate cache (10 ms)\n"
        "    √ TC10: reject invalid task status (5 ms)\n"
        "    √ TC11: delete task (8 ms)\n"
        "    √ TC12: deleted task is no longer in list (6 ms)\n\n"
        "Test Suites: 1 passed, 1 total | Tests: 12 passed, 12 total | Time: 1.086 s"
    )
    t_jt = Table([[Preformatted(jest_text, code_style)]], colWidths=[504])
    t_jt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#3B82F6')),
        ('PADDING', (0,0), (-1,-1), 4)
    ]))
    story.append(t_jt)
    story.append(Spacer(1, 14))

    # SECTION D: Mandatory Declaration
    story.append(Paragraph("D. Mandatory Declaration", h1_style))
    declaration_text = (
        "<b>I hereby declare that the submitted implementation has been completed by me. "
        "I have tested the Docker configurations, Docker Compose deployment, Docker Hub image publishing "
        "and GitHub Actions CI/CD pipeline. The screenshots and evidence included in this document "
        "represent my actual implementation.</b>"
    )
    t_dec = Table([[Paragraph(declaration_text, body_style)]], colWidths=[504])
    t_dec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF3C7')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#D97706')),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t_dec)
    story.append(Spacer(1, 18))

    # Signature Block
    sig_data = [
        [Paragraph("<b>Student Signature:</b> Anurag Prajapati", table_cell), Paragraph("<b>Date:</b> 18 November 2026", table_cell)],
        [Paragraph("<b>Roll Number:</b> 202501200400002", table_cell), Paragraph("<b>Status:</b> All Requirements Verified & Submitted", table_cell)]
    ]
    t_sig = Table(sig_data, colWidths=[252, 252])
    t_sig.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_sig)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF with embedded screenshots: {filename}")

if __name__ == '__main__':
    output_path = r"D:\MSE-2-SSED-Evening\202501200400002_ANURAG_PRAJAPATI_SET2.pdf"
    sc_dir = r"D:\MSE-2-SSED-Evening\screenshots"
    build_pdf(output_path, sc_dir)
