"""Build a source-grounded English Markdown report and a paginated PDF."""
from pathlib import Path
from xml.sax.saxutils import escape
import re
import math
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted, Image, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports'
OUT.mkdir(exist_ok=True)
FIG=OUT/'figures';FIG.mkdir(exist_ok=True)
C=35;R=C/3;A=C-R
def fmt(x, digits=2):return f'{x:.{digits}f}'
def raw_x(t,er=.05,ep=.85,es=.05):return (C*t-R*er-A*es)/(ep-es)
def table(headers,rows):
    return '| '+' | '.join(headers)+' |\n| '+' | '.join('---' for _ in headers)+' |\n'+'\n'.join('| '+' | '.join(str(v) for v in row)+' |' for row in rows)

ratio_rows=[]
for t in [.10,.20,.30,.40,.50,.60]:
    x=raw_x(t)
    if x>A:
        ratio_rows.append([f'E{int(t*100)}', 'Exceeds available volume', '-', '-', f'Maximum : E{fmt((R*.05+A*.85)/C*100)}'])
    else:
        ratio_rows.append([f'E{int(t*100)}',fmt(x)+' L',fmt(A-x)+' L',fmt(100*x/A)+' %','Simulation only'])
residual_rows=[]
for er in [.05,.10,.20,.30,.50,.70,.85]:
    minimum=(R*er+A*.05)/C
    x=raw_x(.3,er)
    residual_rows.append([f'E{int(er*100)}',fmt(minimum*100)+' %',fmt(x)+' L' if x>=0 else 'Impossible',fmt(A-x)+' L' if x>=0 else 'Impossible'])
pump_rows=[]
for ep in [.60,.70,.75,.85]:
    x=raw_x(.30,ep=ep)
    pump_rows.append([f'{int(ep*100)} %',fmt(x)+' L',fmt(A-x)+' L',fmt(x/A*100)+' %'])

rho_g=.741;rho_e=.790;afr_g=14.7;afr_e=9.0
def air(e):return (1-e)*rho_g*afr_g+e*rho_e*afr_e
def energy(e):return (1-e)*rho_g*42.7+e*rho_e*26.8
physics_rows=[]
for e in [.05,.10,.20,.30,.50,.85]:
    physics_rows.append([f'E{int(e*100)}',fmt(air(e),3),fmt(100*(air(.05)/air(e)-1))+' %',fmt(energy(e),2)])

from report_pages import build_pages
pages = build_pages(table, fmt, (ratio_rows, residual_rows, pump_rows, physics_rows), air, energy)

markdown='\n\n<!-- pagebreak -->\n\n'.join(p.strip() for p in pages)+'\n'
(OUT/'Report_Toyota_Aygo_E85_SP98.md').write_text(markdown,encoding='utf-8')

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(8.0,2.65))
es=[.05,.10,.20,.30,.50,.85]
ys=[100*(air(.05)/air(e)-1) for e in es]
ax.bar([f'E{int(e*100)}' for e in es],ys,color=['#00685c']*5+['#d49b48'],width=.55)
for i,y in enumerate(ys):ax.text(i,y+1,f'{fmt(y,1)} %',ha='center',fontsize=9)
ax.set_ylabel('Extra fuel flow (%)')
ax.set_ylim(0,max(ys)+7);ax.grid(axis='y',alpha=.13);ax.set_axisbelow(True)
fig.text(.12,.01,'Stoichiometric model relative to E5; no ECU limit shown.',fontsize=9,color='#52655e')
fig.tight_layout(rect=(0,.05,1,1));fig.savefig(FIG/'injection.png',dpi=240);plt.close(fig)
fig,ax=plt.subplots(figsize=(8.0,2.65))
ys=[energy(e) for e in es]
ax.bar([f'E{int(e*100)}' for e in es],ys,color='#526f91',width=.55)
for i,y in enumerate(ys):ax.text(i,y+.5,f'{fmt(y,1)}',ha='center',fontsize=9)
ax.set_ylabel('Modelled energy (MJ/L)');ax.set_ylim(0,max(ys)+5)
ax.grid(axis='y',alpha=.13);ax.set_axisbelow(True)
fig.text(.12,.01,'Binary petrol/ethanol model; unchanged engine efficiency assumed.',fontsize=9,color='#52655e')
fig.tight_layout(rect=(0,.05,1,1));fig.savefig(FIG/'energy.png',dpi=240);plt.close(fig)

fontroot=Path('/usr/share/fonts/truetype/dejavu')
for name,file in [('DejaVu','DejaVuSans.ttf'),('DejaVu-Bold','DejaVuSans-Bold.ttf'),('DejaVu-Oblique','DejaVuSans-Oblique.ttf'),('DejaVuMono','DejaVuSansMono.ttf')]:
    path=fontroot/file
    if not path.is_file():path=Path(matplotlib.get_data_path())/'fonts/ttf'/file
    pdfmetrics.registerFont(TTFont(name,str(path)))
pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVu-Bold',italic='DejaVu-Oblique',boldItalic='DejaVu-Bold')
navy=colors.HexColor('#102B34');green=colors.HexColor('#00685C');muted=colors.HexColor('#52655E');light=colors.HexColor('#EFF5F2')
styles={
 'body':ParagraphStyle('Body',fontName='DejaVu',fontSize=9.4,leading=14.2,textColor=navy,spaceAfter=9),
 'h1':ParagraphStyle('H1',fontName='DejaVu-Bold',fontSize=21,leading=27,textColor=green,spaceAfter=20),
 'h2':ParagraphStyle('H2',fontName='DejaVu-Bold',fontSize=13,leading=18,textColor=navy,spaceAfter=10),
 'table':ParagraphStyle('Table',fontName='DejaVu',fontSize=8.15,leading=11.3,textColor=navy),
 'tablehead':ParagraphStyle('TableHead',fontName='DejaVu-Bold',fontSize=8.3,leading=11.8,textColor=colors.white),
 'quote':ParagraphStyle('Quote',fontName='DejaVu',fontSize=10.2,leading=15.8,textColor=navy),
 'cover':ParagraphStyle('Cover',fontName='DejaVu-Bold',fontSize=37,leading=46,textColor=colors.white,spaceAfter=14),
 'coversub':ParagraphStyle('CoverSub',fontName='DejaVu',fontSize=20,leading=28,textColor=colors.HexColor('#86D8BE'),spaceAfter=29),
 'coverbody':ParagraphStyle('CoverBody',fontName='DejaVu',fontSize=11,leading=18,textColor=colors.HexColor('#DEEBE9'),spaceAfter=19),
 'code':ParagraphStyle('Code',fontName='DejaVuMono',fontSize=8.1,leading=12,textColor=navy,backColor=light,borderPadding=10,spaceBefore=4,spaceAfter=12),
}
def inline(text):
    s=escape(text)
    s=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',lambda m:f'<a href="{m[2]}" color="#00685C">{m[1]}</a>',s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'`([^`]+)`',r'<font name="DejaVuMono">\1</font>',s)
    return s

WIDTH=A4[0]-96
story=[]
for page_index,page in enumerate(pages):
    if page_index:story.append(PageBreak())
    else:story.extend([Spacer(1,62),Paragraph('TECHNICAL REPORT / VERSION 0.1.0',styles['coverbody']),Spacer(1,20)])
    lines=page.strip().splitlines();i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:i+=1;continue
        if line.startswith('<!-- figure:'):
            filename=line.split(':',1)[1].split('-->')[0].strip()
            story.extend([Image(str(FIG/filename),width=WIDTH,height=WIDTH*2.65/8),Spacer(1,9)]);i+=1;continue
        if line.startswith('# '):
            story.append(Paragraph(inline(line[2:]),styles['cover' if page_index==0 else 'h1']));i+=1;continue
        if line.startswith('## '):
            story.append(Paragraph(inline(line[3:]),styles['coversub' if page_index==0 else 'h2']));i+=1;continue
        if line.startswith('```'):
            code=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
            story.append(Preformatted('\n'.join(code),styles['code']));i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[:\- ]+',c) for c in cells):rows.append(cells)
                i+=1
            n=len(rows[0]);widths=[WIDTH/n]*n
            if n==2:widths=[WIDTH*.28,WIDTH*.72]
            if n==3:widths=[WIDTH*.30,WIDTH*.25,WIDTH*.45]
            if n==5:widths=[WIDTH*.12,WIDTH*.20,WIDTH*.20,WIDTH*.17,WIDTH*.31]
            data=[[Paragraph(inline(c),styles['tablehead' if j==0 else 'table']) for c in row] for j,row in enumerate(rows)]
            tbl=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
            tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),green),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,light]),
                ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
                ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,-1),(-1,-1),.4,colors.HexColor('#D0DDD7'))]))
            story.extend([tbl,Spacer(1,13)]);continue
        if line.startswith('>'):
            quote=[]
            while i<len(lines) and lines[i].strip().startswith('>'):quote.append(lines[i].strip()[1:].strip());i+=1
            box=Table([[Paragraph(inline(' '.join(quote)),styles['quote'])]],colWidths=[WIDTH])
            box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),light),('LINEBEFORE',(0,0),(0,-1),3,green),('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),13),('TOPPADDING',(0,0),(-1,-1),13),('BOTTOMPADDING',(0,0),(-1,-1),13)]))
            story.extend([box,Spacer(1,14)]);continue
        para=[line];i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].strip().startswith(('#','|','```','>','<!--')):
            para.append(lines[i].strip());i+=1
        story.append(Paragraph(inline(' '.join(para)),styles['coverbody' if page_index==0 else 'body']))

def decorate(c,doc):
    w,h=A4;c.saveState()
    if doc.page==1:
        c.setFillColor(navy);c.rect(0,0,w,h,fill=1,stroke=0)
        c.setFillColor(green);c.rect(0,h-12,w,12,fill=1,stroke=0)
        c.setStrokeColor(colors.HexColor('#2C5860'));c.setLineWidth(1)
        c.line(48,128,w-48,128)
        c.setFillColor(colors.HexColor('#86D8BE'));c.setFont('DejaVu-Bold',10)
        c.drawString(48,99,'CALCULATED COMPOSITION / ENGINE VALIDATION REQUIRED')
        c.setFont('DejaVu',9);c.setFillColor(colors.HexColor('#DEEBE9'));c.drawString(48,78,'France • primary sources • native applications')
    else:
        c.setFillColor(green);c.rect(48,h-42,27,3,fill=1,stroke=0)
        c.setFont('DejaVu-Bold',8);c.setFillColor(muted);c.drawString(84,h-43,'AYGO 2014 / E85 AND SP98')
        c.setFont('DejaVu',8);c.drawRightString(w-48,h-43,'04.10.2026')
        c.setStrokeColor(colors.HexColor('#D0DDD7'));c.line(48,41,w-48,41)
        c.setFont('DejaVu',7.4);c.drawString(48,26,'Modelled composition • no guarantee against an engine warning light')
        c.drawRightString(w-48,26,f'{doc.page:02d}')
    c.restoreState()

pdf=OUT/'Report_Toyota_Aygo_E85_SP98.pdf'
doc=SimpleDocTemplate(str(pdf),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=68,bottomMargin=58,
    title='Toyota Aygo 2014 - E85 / SP98 calculations and engine limits',author='Alexandre / Cylae',
    subject='Volume balance, primary sources and Android / iOS prototypes',pageCompression=1)
doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
print(json.dumps({'markdown':str(OUT/'Report_Toyota_Aygo_E85_SP98.md'),'pdf':str(pdf),'plannedPages':len(pages)},ensure_ascii=False))
