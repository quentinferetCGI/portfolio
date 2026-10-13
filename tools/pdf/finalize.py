import subprocess,glob,os
from PIL import Image
from pypdf import PdfReader,PdfWriter
import sys
src=sys.argv[1]; out=sys.argv[2]; TITLE=sys.argv[3]
for f in glob.glob(os.path.dirname(src)+'/b-*.png'): os.remove(f)
subprocess.run(['pdftoppm','-r','20','-gray','-png',src,os.path.dirname(src)+'/b'],stderr=subprocess.DEVNULL)
fs=sorted(glob.glob(os.path.dirname(src)+'/b-*.png'))
blank=[]
for i,f in enumerate(fs):
    im=Image.open(f).convert('L'); w,h=im.size
    body=im.crop((0,int(h*0.04),w,int(h*0.90)))  # exclude footer
    import numpy as np
    a=np.array(body); 
    if (a<200).mean()<0.002: blank.append(i)
print('blank pages',[b+1 for b in blank])
wr=PdfWriter(clone_from=src)
for i in sorted(blank,reverse=True): del wr.pages[i]
# keep outline? rebuild not needed; set metadata
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import io
N=len(wr.pages)
for i,p in enumerate(wr.pages):
    W=float(p.mediabox.width); H=float(p.mediabox.height)
    buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=(W,H)); c.setFont('Helvetica',7); c.setFillColor(HexColor('#5A5F6B'))
    m=12/25.4*72; y=7/25.4*72
    c.drawString(m,y,'Quentin Féret — Designer UX/UI · Portfolio'); c.drawRightString(W-m,y,f'{i+1} / {N}')
    c.save(); buf.seek(0)
    p.merge_page(PdfReader(buf).pages[0])
wr.add_metadata({'/Title':TITLE,'/Author':'Quentin Féret','/Subject':"Trois cas d'étude autour du design system : SNCF Gares & Connexions, Île-de-France Mobilités, Conseil d'État",'/Keywords':'Designer UX/UI, design system, portfolio, accessibilité'})
wr.compress_identical_objects(remove_identicals=True, remove_orphans=True)
wr.write(os.path.dirname(src)+'/tmp.pdf')
subprocess.run(['qpdf','--object-streams=generate','--recompress-flate',os.path.dirname(src)+'/tmp.pdf',out])
print(len(PdfReader(out).pages),'pages',round(os.path.getsize(out)/1e6,2),'MB')
