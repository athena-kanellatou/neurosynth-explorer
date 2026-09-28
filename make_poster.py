"""Create a single-page, portfolio-ready exploratory research poster."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from matplotlib.font_manager import FontProperties, findfont

root=Path(__file__).parent
out=root/'results/RESEARCH_POSTER.pdf'
pdfmetrics.registerFont(TTFont('DV',findfont(FontProperties(family='DejaVu Sans'))))
pdfmetrics.registerFont(TTFont('DVB',findfont(FontProperties(family='DejaVu Sans', weight='bold'))))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
W,H=landscape(A3)
c=canvas.Canvas(str(out),pagesize=(W,H))
navy=colors.HexColor('#132c46'); teal=colors.HexColor('#087f8c'); ink=colors.HexColor('#23384a'); pale=colors.HexColor('#eef5f7')
c.setFillColor(colors.white);c.rect(0,0,W,H,fill=1,stroke=0)
c.setFillColor(navy);c.rect(0,H-110,W,110,fill=1,stroke=0)
c.setFillColor(colors.white);c.setFont('DVB',24)
c.drawString(34,H-48,'Where do emotion regulation and reward maps overlap?')
c.setFont('DV',11);c.drawString(35,H-75,'Neurosynth + NeuroQuery | exploratory computational research poster | 28 September 2026')
c.setFont('DVB',8);c.drawRightString(W-35,H-75,'NOT PEER REVIEWED')

style=ParagraphStyle('body',fontName='DV',fontSize=9.2,leading=14,textColor=ink)
small=ParagraphStyle('small',fontName='DV',fontSize=8.2,leading=12,textColor=ink)

def section(x,top,width,title,body,fontsize=None):
    c.setFillColor(teal);c.setFont('DVB',12);c.drawString(x,top,title)
    c.setStrokeColor(colors.HexColor('#bad3d9'));c.line(x,top-7,x+width,top-7)
    paragraph=Paragraph(body,style if fontsize is None else small)
    _,h=paragraph.wrap(width,500);paragraph.drawOn(c,x,top-20-h)
    return top-20-h-24

margin=34; gap=24; cw=(W-2*margin-2*gap)/3
x1=margin;x2=x1+cw+gap;x3=x2+cw+gap
y=H-140
c.setFillColor(pale);c.roundRect(x1,y-82,cw,80,8,fill=1,stroke=0)
c.setFillColor(navy);c.setFont('DVB',12);c.drawString(x1+14,y-24,'Research question')
p=Paragraph('How stable is the spatial overlap across thresholds, and does a second synthesis method show a related pattern?',style)
_,h=p.wrap(cw-28,70);p.drawOn(c,x1+14,y-32-h)
y-=112
y=section(x1,y,cw,'Data and method','Three Neurosynth association maps: emotion regulation (247 studies), reward (922), and depression (502). We compared positive z maps at thresholds 2, 3, 4, and 5, then checked six-neighbor components against the AAL SPM12 atlas.')
y=section(x1,y,cw,'Primary result','At z &ge; 3, emotion regulation and reward share <b>1,296 voxels</b> (Jaccard <b>0.067</b>). Jaccard decreases from 0.120 at z &ge; 2 to 0.028 at z &ge; 5. Twenty studies are assigned to both terms (8.1% of the emotion-regulation set).')
c.drawImage(str(root/'results/overlap.png'),x1,y-205,width=cw,height=195,preserveAspectRatio=True,anchor='c')
c.setFillColor(ink);c.setFont('DV',8);c.drawString(x1,y-220,'Figure 1. Descriptive threshold sensitivity across term pairs.')

y2=H-140
y2=section(x2,y2,cw,'Where is the overlap?','The two largest z &ge; 3 components contain 395 and 296 voxels. Their peaks are MNI (24, 2, -16) and (-18, 2, -14). AAL labels the first peak Amygdala_R; the second peak lies outside an AAL label, although much of its component is labeled Amygdala_L.')
c.drawImage(str(root/'results/orthogonal_overlap_z3.png'),x2,y2-230,width=cw,height=220,preserveAspectRatio=True,anchor='c')
p=Paragraph('Figure 2. Blue: emotion regulation only. Orange: reward only. Purple: overlap. Gray silhouette: data footprint, not structural MRI.',small)
_,h=p.wrap(cw,90);p.drawOn(c,x2,y2-236-h)
y2-=258+h
y2=section(x2,y2,cw,'Threshold stability','At z &ge; 5, 88/395 (22.3%) and 76/296 (25.7%) of the original z &ge; 3 component voxels remain. Smaller contiguous high-z cores persist; this is not a significance test.')

y3=H-140
y3=section(x3,y3,cw,'Cross-method check','We generated NeuroQuery predicted maps for the same phrases and compared their spatial ranks with Neurosynth after resampling to a 4 mm grid. The top 1%, 5%, and 10% cutoffs are descriptive, not matched p-value thresholds.')
for label,rho,jac in [('Emotion regulation','0.272','0.126'),('Reward','0.502','0.391'),('Depression','0.399','0.115')]:
    c.setFillColor(pale);c.roundRect(x3,y3-27,cw,31,4,fill=1,stroke=0)
    c.setFillColor(ink);c.setFont('DVB',9);c.drawString(x3+8,y3-16,label)
    c.setFont('DV',8);c.drawRightString(x3+cw-8,y3-16,f'rho {rho} | top-5% Jaccard {jac}')
    y3-=40
y3-=12
y3=section(x3,y3,cw,'Interpretation','Reward has the highest focal cross-method agreement at all tested fractions. NeuroQuery predicts report locations; Neurosynth tests term-coordinate associations. Their literature overlaps, so this is methodological triangulation rather than independent replication.')
y3=section(x3,y3,cw,'Limits and next test','Keyword selection, publication and coordinate-reporting biases, atlas boundaries, study dependence, and spatial autocorrelation constrain interpretation. A follow-up should curate nonoverlapping studies and prespecify a coordinate meta-analysis and justified spatial null model.',fontsize='small')

c.setFillColor(navy);c.rect(0,0,W,62,fill=1,stroke=0)
c.setFillColor(colors.white);c.setFont('DV',8)
c.drawString(34,37,'Sources: Yarkoni et al., Nature Methods 2011, DOI 10.1038/nmeth.1635; Dockes et al., eLife 2020, DOI 10.7554/eLife.53385.')
c.drawString(34,20,'Reproducible maps, hashes, code and detailed report are supplied with Neurosynth Map Explorer. No subject-level or clinical inference.')
c.showPage();c.save();print(out)
