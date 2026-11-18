from pathlib import Path
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted, Table, TableStyle, Flowable, Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'SUBMISSION_DOCUMENTATION.md'
OUTPUT = ROOT / '2400291530214_Vishal_Prajapati_SET2.pdf'
PAGE_W, PAGE_H = A4
NAVY = colors.HexColor('#17324D')
BLUE = colors.HexColor('#2C6E9B')
PALE = colors.HexColor('#EAF1F6')
INK = colors.HexColor('#202A33')
MUTED = colors.HexColor('#5B6873')
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='CoverTitleX', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=25, leading=31, textColor=NAVY, alignment=1, spaceAfter=8*mm))
styles.add(ParagraphStyle(name='CoverSubX', parent=styles['Normal'], fontName='Helvetica', fontSize=13, leading=18, textColor=BLUE, alignment=1, spaceAfter=3*mm))
styles.add(ParagraphStyle(name='H1X', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=NAVY, spaceBefore=8, spaceAfter=8, keepWithNext=True))
styles.add(ParagraphStyle(name='H2X', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=BLUE, spaceBefore=7, spaceAfter=5, keepWithNext=True))
styles.add(ParagraphStyle(name='BodyX', parent=styles['BodyText'], fontName='Helvetica', fontSize=8.7, leading=12.2, textColor=INK, spaceAfter=5))
styles.add(ParagraphStyle(name='SmallX', parent=styles['BodyText'], fontName='Helvetica', fontSize=7.6, leading=10.2, textColor=INK, spaceAfter=3))
styles.add(ParagraphStyle(name='CodeX', parent=styles['Code'], fontName='Courier', fontSize=6.6, leading=8.2, textColor=NAVY, backColor=colors.HexColor('#F1F4F7'), borderColor=colors.HexColor('#D6DEE6'), borderWidth=.5, borderPadding=5, leftIndent=5, rightIndent=5, spaceBefore=3, spaceAfter=7))
styles.add(ParagraphStyle(name='CalloutX', parent=styles['BodyText'], fontName='Helvetica-Oblique', fontSize=8.4, leading=11.5, textColor=INK, backColor=PALE, borderColor=BLUE, borderWidth=1, borderPadding=7, spaceBefore=5, spaceAfter=8))
styles.add(ParagraphStyle(name='CellX', parent=styles['BodyText'], fontName='Helvetica', fontSize=6.8, leading=8.6, textColor=INK, spaceAfter=0))
styles.add(ParagraphStyle(name='CellHeadX', parent=styles['BodyText'], fontName='Helvetica-Bold', fontSize=6.8, leading=8.6, textColor=colors.white, spaceAfter=0))

def clean(s):
    return s.replace('→', '->').replace('–', '-').replace('—', '-').replace('’', "'").replace('“', '"').replace('”', '"').replace('…', '...')

def inline(s):
    s = escape(clean(s))
    s = re.sub(r'`([^`]+)`', r'<font name="Courier" size="7">\1</font>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', s)
    s = re.sub(r'\[([^]]+)\]\(([^)]+)\)', r'<u>\1</u> (\2)', s)
    return s

class Architecture(Flowable):
    def __init__(self):
        super().__init__(); self.width = 500; self.height = 120
    def draw(self):
        c = self.canv
        boxes = [(4,66,88,34,'Browser','localhost:8080'), (130,66,112,34,'Frontend / Nginx',':80'), (290,66,112,34,'Backend / Express',':3000'), (204,5,108,34,'PostgreSQL','postgres:5432'), (354,5,100,34,'Redis','redis:6379')]
        for x,y,w,h,title,sub in boxes:
            c.setFillColor(PALE if title != 'PostgreSQL' else colors.HexColor('#E7F2EA')); c.setStrokeColor(BLUE); c.roundRect(x,y,w,h,5,fill=1,stroke=1)
            c.setFillColor(NAVY); c.setFont('Helvetica-Bold',8); c.drawCentredString(x+w/2,y+21,title); c.setFont('Helvetica',7); c.drawCentredString(x+w/2,y+9,sub)
        c.setStrokeColor(MUTED); c.setFillColor(MUTED); c.setFont('Helvetica',7)
        self.arrow(c,92,83,130,83); c.drawCentredString(110,91,'HTTP'); self.arrow(c,242,83,290,83); c.drawCentredString(266,91,'/api, /health')
        self.arrow(c,330,66,275,39); self.arrow(c,365,66,403,39)
        c.setDash(2,2); c.setStrokeColor(BLUE); c.roundRect(192,0,272,45,7,fill=0,stroke=1); c.setDash(); c.setFillColor(MUTED); c.setFont('Helvetica-Oblique',6.5); c.drawCentredString(328,1,'taskflow network; PostgreSQL files stored in postgres_data volume')
    @staticmethod
    def arrow(c,x1,y1,x2,y2):
        from math import atan2,cos,sin,pi
        c.line(x1,y1,x2,y2); a=atan2(y2-y1,x2-x1); size=5
        c.line(x2,y2,x2-size*cos(a-pi/6),y2-size*sin(a-pi/6)); c.line(x2,y2,x2-size*cos(a+pi/6),y2-size*sin(a+pi/6))

def footer(canvas,doc):
    canvas.saveState()
    if doc.page>1:
        canvas.setStrokeColor(colors.HexColor('#D4DEE7')); canvas.line(18*mm,15*mm,PAGE_W-18*mm,15*mm); canvas.setFont('Helvetica',7); canvas.setFillColor(MUTED)
        canvas.drawString(18*mm,10*mm,'MSE-2 Software Engineering and DevOps | Set 2'); canvas.drawRightString(PAGE_W-18*mm,10*mm,f'Page {doc.page}')
    canvas.restoreState()

def cover():
    story=[Spacer(1,27*mm),Paragraph('MSE-2 SOFTWARE ENGINEERING<br/>AND DEVOPS',styles['CoverTitleX']),Paragraph('ASSIGNMENT DOCUMENTATION',styles['CoverSubX']),Paragraph('SET 2 - EVENING SHIFT',styles['CoverSubX']),Spacer(1,14*mm)]
    rows=[['STUDENT NAME','Vishal Prajapati'],['ROLL NUMBER','2400291530214'],['SECTION','AIML-C'],['BRANCH','AIML'],['GITHUB USERNAME','VishalPrajapati3112'],['DOCKER HUB USERNAME','vishalprajapati214'],['SUBMISSION DATE','18 November 2026']]
    t=Table(rows,colWidths=[52*mm,92*mm],rowHeights=[13*mm]*len(rows),hAlign='CENTER')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),PALE),('TEXTCOLOR',(0,0),(0,-1),NAVY),('FONTNAME',(0,0),(0,-1),'Helvetica-Bold'),('FONTNAME',(1,0),(1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),9),('GRID',(0,0),(-1,-1),.5,colors.HexColor('#CAD6E0')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),9)]))
    story += [t,Spacer(1,16*mm),Paragraph('FULL-STACK CONTAINERIZATION<br/>DOCKER • COMPOSE • POSTGRESQL • REDIS • CI/CD',styles['CoverSubX']),Spacer(1,10*mm),Paragraph('Editable source: SUBMISSION_DOCUMENTATION.md',styles['SmallX']),Paragraph('Verification results and evidence status are summarized in Sections J and K.',styles['CalloutX']),PageBreak()]
    return story

def parse_table(lines):
    rows=[[inline(c.strip()) for c in line.strip().strip('|').split('|')] for line in lines]
    if len(rows)>1 and all(re.fullmatch(r'\s*:?-{3,}:?\s*',c) for c in lines[1].strip().strip('|').split('|')): rows.pop(1)
    data=[]
    for ri,row in enumerate(rows): data.append([Paragraph(c,styles['CellHeadX'] if ri==0 else styles['CellX']) for c in row])
    n=max(len(r) for r in data); widths=[25*mm,50*mm,48*mm,51*mm] if n==4 else ([42*mm,132*mm] if n==2 else [174*mm/n]*n)
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#C8D2DC')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F5F8FA')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    return t

def build():
    lines=SOURCE.read_text(encoding='utf-8-sig').splitlines(); story=cover()+[Paragraph('Contents',styles['H1X'])]
    toc=['Introduction','Application architecture','Dockerfile implementation','Docker Compose','Docker Hub publishing','Image-based deployment','Networking and persistence','GitHub Actions CI/CD','Testing and verification','Screenshot evidence checklist','GitHub submission information','Conclusion','Declaration']
    for i,name in enumerate(toc,1): story.append(Paragraph(f'<font color="#2C6E9B">{i:02d}</font>  {escape(name)}',styles['BodyX']))
    story += [Spacer(1,8),Paragraph('Evidence status: local runtime checks and Docker Hub publishing are complete; GitHub Actions is not verified. See Section J.',styles['CalloutX']),PageBreak()]
    started=False; skip=False; code_mode=False; code=[]; active_section=''; i=0
    while i<len(lines):
        line=lines[i]
        if line.startswith('## A. Cover page'): skip=True
        if line.startswith('## B. Introduction'): skip=False; started=True
        if skip or not started or line.startswith('# MSE-2'): i+=1; continue
        if line.startswith('```'):
            if code_mode:
                raw='\n'.join(clean(s) for s in code); wrapped=[]
                for source_line in raw.splitlines(): wrapped.extend([source_line] if len(source_line)<=112 else [source_line[j:j+112] for j in range(0,len(source_line),112)])
                story.append(Preformatted('\n'.join(wrapped),styles['CodeX'],maxLineLength=112)); code_mode=False; code=[]
            else: code_mode=True; code=[]
            i+=1; continue
        if code_mode: code.append(line); i+=1; continue
        if not line.strip() or line.strip()=='---': i+=1; continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'): rows.append(lines[i]); i+=1
            story += [parse_table(rows),Spacer(1,5)]; continue
        if line.startswith('## '):
            active_section = line[3:4]
            story.append(Paragraph(inline(line[3:]),styles['H1X']))
            if line.startswith('## C.'): story += [Architecture(),Spacer(1,9)]
            i+=1; continue
        if line.startswith('### '): story.append(Paragraph(inline(line[4:]),styles['H2X'])); i+=1; continue
        if line.startswith('> '): story.append(Paragraph(inline(line[2:]),styles['CalloutX'])); i+=1; continue
        if line.startswith('- ') or re.match(r'^\d+\. ',line):
            item=re.sub(r'^- |^\d+\. ','',line); story.append(Paragraph('&bull;&nbsp;&nbsp;'+inline(item),styles['BodyX']))
            match=re.match(r'^(\d+)\. ',line)
            if active_section == 'K' and match:
                evidence_dir=ROOT / 'submission-evidence'
                images=sorted(evidence_dir.glob(f'{int(match.group(1)):02d}-*.png')) if evidence_dir.exists() else []
                for image_path in images:
                    story.append(Image(str(image_path),width=174*mm,height=105*mm,kind='proportional'))
                    story.append(Spacer(1,6))
            i+=1; continue
        if line.startswith('**') and line.endswith('**'): story.append(Paragraph(inline(line),styles['CalloutX'])); i+=1; continue
        para=[line.strip()]; j=i+1
        while j<len(lines) and lines[j].strip() and not lines[j].startswith(('#','```','|','> ','- ')) and not re.match(r'^\d+\. ',lines[j]): para.append(lines[j].strip()); j+=1
        story.append(Paragraph(inline(' '.join(para)),styles['BodyX'])); i=j
    return story

doc=SimpleDocTemplate(str(OUTPUT),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=21*mm,title='MSE-2 Software Engineering and DevOps - Set 2',author='VishalPrajapati3112')
doc.build(build(),onFirstPage=footer,onLaterPages=footer)
print(f'Created {OUTPUT} ({OUTPUT.stat().st_size} bytes)')
