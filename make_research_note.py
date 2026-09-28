"""Generate a compact research note from verified project outputs."""
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from matplotlib.font_manager import FontProperties, findfont

pdfmetrics.registerFont(TTFont('DejaVu', findfont(FontProperties(family='DejaVu Sans'))))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', findfont(FontProperties(family='DejaVu Sans', weight='bold'))))
pdfmetrics.registerFontFamily('DejaVu', normal='DejaVu', bold='DejaVu-Bold', italic='DejaVu', boldItalic='DejaVu-Bold')
root=Path(__file__).parent
output=root/'results/RESEARCH_NOTE.pdf'
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleCustom',parent=styles['Title'],fontName='DejaVu-Bold',fontSize=17,leading=21,textColor=colors.HexColor('#162a47'),spaceAfter=12))
styles.add(ParagraphStyle(name='SubtitleCustom',parent=styles['Normal'],fontName='DejaVu',fontSize=9,leading=13,textColor=colors.HexColor('#53647b'),spaceAfter=13))
styles.add(ParagraphStyle(name='BodyCustom',parent=styles['BodyText'],fontName='DejaVu',fontSize=8.3,leading=11.5,spaceAfter=6))
styles.add(ParagraphStyle(name='HeadCustom',parent=styles['Heading2'],fontName='DejaVu-Bold',fontSize=10.5,leading=13,textColor=colors.HexColor('#194f69'),spaceBefore=9,spaceAfter=4))
styles.add(ParagraphStyle(name='SmallCustom',parent=styles['BodyText'],fontName='DejaVu',fontSize=7.8,leading=11,spaceAfter=5))
P=lambda text,style='BodyCustom':Paragraph(text,styles[style])

def make_table(data,widths):
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dce8ef')),
       ('TEXTCOLOR',(0,0),(-1,0),colors.HexColor('#162a47')),
       ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8),
       ('BOTTOMPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),
       ('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#93aab8')),
       ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f5f8fa')])]))
    return t

story=[P('Spatial overlap of emotion regulation, reward, and depression maps','TitleCustom'),
 P('Exploratory research note | 28 September 2026 | Reproducible computational analysis; not peer reviewed','SubtitleCustom'),
 P('<b>Abstract.</b> We compared Neurosynth association-test maps for three psychological terms using descriptive voxel overlap, anatomical annotation, and a cross-method check with NeuroQuery. Emotion regulation and reward shared 1,296 positive voxels at z &ge; 3 (Jaccard 0.067). The two largest overlap components were near bilateral medial temporal structures in the AAL atlas, but region labels varied within each component. NeuroQuery and Neurosynth showed stronger rank-based agreement for reward (Spearman rho 0.502) than for emotion regulation (0.272). These observations generate hypotheses about the literature; they do not identify unique neural mechanisms or support clinical inference.'),
 P('Research question','HeadCustom'),
 P('How stable is the spatial overlap of term-associated neuroimaging maps across thresholds, and how similar are maps produced by a second automated synthesis method?'),
 P('Data and methods','HeadCustom'),
 P('Neurosynth unthresholded association-test z maps were obtained for emotion regulation (247 listed studies), reward (922), and depression (502). We confirmed identical 91 x 109 x 91 voxel grids and affine transforms. For positive z cutoffs 2, 3, 4, and 5, we computed voxel counts, intersection, Jaccard, and Dice on pairwise finite voxels. Six-neighbor connected components at z &ge; 3 were annotated with AAL SPM12 only after exact atlas-grid verification. Study IDs were compared to quantify shared literature.'),
 P('NeuroQuery 1.1.0 predicted maps were generated with the same phrases. Neurosynth maps were interpolated from 2 mm to NeuroQuery\'s 4 mm grid. We compared Spearman ranks over 28,542 common nonzero voxels and overlap among each map\'s top-ranked 1%, 5%, and 10%. These are descriptive ranks, not matched inferential statistics.'),
 P('Primary overlap','HeadCustom'),
 make_table([['Positive z cutoff','Shared voxels','Jaccard','Dice'],['2','4,725','0.120','0.214'],['3','1,296','0.067','0.126'],['4','420','0.040','0.078'],['5','169','0.028','0.054']],[125,115,105,105]),
 Spacer(1,8),
 P('The decrease with stricter thresholds shows that the extent of overlap depends on the cutoff. Among the 247 emotion-regulation studies, 20 also appeared in the reward set (8.1%); shared voxels cannot be attributed specifically to those 20 studies.'),
 PageBreak(),
 P('Spatial characterization','HeadCustom'),
 P('At z &ge; 3 the two largest six-neighbor components contained 395 and 296 voxels. The first peak was MNI (24, 2, -16), labeled Amygdala_R by AAL SPM12. The second peak, (-18, 2, -14), was outside an AAL label, although 127 component voxels were labeled Amygdala_L. At z &ge; 5, 22.3% and 25.7% of the original z &ge; 3 voxels persisted in these components. A peak label does not describe the full spatial extent.'),
 Image(str(root/'results/orthogonal_overlap_z3.png'),width=6.7*inch,height=2.25*inch),
 P('Figure 1. Orthogonal views through the first overlap peak. Blue: emotion regulation only; orange: reward only; purple: overlap. The silhouette is a data footprint, not an anatomical MRI.','SmallCustom'),
 P('Cross-method pattern agreement','HeadCustom'),
 make_table([['Phrase','Spearman rho','Top 1% Jaccard','Top 5%','Top 10%'],['Emotion regulation','0.272','0.244','0.126','0.156'],['Reward','0.502','0.546','0.391','0.399'],['Depression','0.399','0.034','0.115','0.146']],[112,82,95,78,78]),
 Spacer(1,8),
 P('Reward showed the greatest focal overlap at all three rank cutoffs. Depression exceeded emotion regulation in whole-mask Spearman correlation, illustrating that global and focal agreement answer different questions.'),
 P('Interpretation and limitations','HeadCustom'),
 P('Automated text selection does not establish that every included study investigates the named process. Source papers differ in samples, tasks, coordinate reporting, and statistical practices. Spatial autocorrelation and shared literature invalidate a naive significance test on voxel overlap. NeuroQuery predicts report locations and Neurosynth tests term-coordinate associations; their scales are not directly comparable. The two tools are methodologically distinct but draw on related literature, so this check is not independent replication. Atlas boundaries and resampling introduce further uncertainty. No subject-level outcomes or diagnoses were studied.'),
 P('Next testable question','HeadCustom'),
 P('Would the bilateral medial temporal overlap persist in a manually curated set of nonoverlapping emotion-regulation and reward studies, using one preregistered coordinate-based meta-analysis pipeline and a justified spatial null model?'),
 P('References and reproducibility','HeadCustom'),
 P('Yarkoni T et al. Large-scale automated synthesis of human functional neuroimaging data. <i>Nature Methods</i> 2011;8:665-670. DOI: 10.1038/nmeth.1635.','SmallCustom'),
 P('Dockes J et al. NeuroQuery, comprehensive meta-analysis of human brain mapping. <i>eLife</i> 2020;9:e53385. DOI: 10.7554/eLife.53385.','SmallCustom')]

def footer(canvas,doc):
    canvas.setFont('Helvetica',8); canvas.setFillColor(colors.HexColor('#64748b'))
    canvas.drawString(45,30,'Neurosynth Map Explorer | Exploratory research note')
    canvas.drawRightString(565,30,str(doc.page))

doc=SimpleDocTemplate(str(output),pagesize=(612,792),leftMargin=45,rightMargin=45,topMargin=42,bottomMargin=48)
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(output)
