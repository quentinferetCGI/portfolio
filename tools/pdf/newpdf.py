"""Génère les PDF depuis le nouveau design. Usage : newpdf.py full|short|cgi"""
import re, os, sys, io, shutil, asyncio
from bs4 import BeautifulSoup
from PIL import Image
from playwright.async_api import async_playwright

MODE = sys.argv[1]
R = '/home/claude/portfolio/'
SP = os.path.dirname(os.path.abspath(__file__)) + '/'
O = SP + 'np_' + MODE + '/'
SITE = 'https://quentinferetcgi.github.io/portfolio/'
shutil.rmtree(O, ignore_errors=True)
os.makedirs(O + 'assets/fonts')
for f in os.listdir(R + 'assets/fonts'):
    shutil.copy(R + 'assets/fonts/' + f, O + 'assets/fonts/' + f)
if MODE == 'cgi':
    for f in ('cgi-logo.png', 'cgi-gradient.jpg'):
        shutil.copy(SP + 'cgi_out/assets/' + f, O + 'assets/' + f)

MAXW = int(os.environ.get('MAXW', 1300 if MODE == 'full' else 1200))
Q = int(os.environ.get('Q', 60 if MODE == 'full' else 66))
CGI = MODE == 'cgi'
CASES = {'cas01': ('01', 'SNCF Gares & Connexions', 't1'), 'cas02': ('02', 'Île-de-France Mobilités', 't2'), 'cas03': ('03', "Conseil d'État", 't3')}

css = ''
for f in ('tokens', 'home', 'case', 'gallery', 'about'):
    css += open(R + 'assets/%s.css' % f).read() + '\n'
css = re.sub(r'body\.(t[123])', r'.\1', css)
css = re.sub(r'url\((fonts/)', 'url(assets/fonts/', css)

def soup(p): return BeautifulSoup(open(R + p + '.html').read(), 'html.parser')

def prep(html, pid=None):
    """liens internes, ids, attributs web."""
    html = re.sub(r' target="_blank" rel="noopener"| loading="lazy" decoding="async"| loading="lazy"', '', html)
    html = re.sub(r'<script.*?</script>', '', html, flags=re.S)
    if pid:
        html = re.sub(r'\bid="([^"]+)"', lambda m: 'id="%s-%s"' % (pid, m.group(1)), html)
        html = re.sub(r'href="#([^"]+)"', lambda m: 'href="#%s-%s"' % (pid, m.group(1)), html)
    if MODE == 'full':
        html = re.sub(r'href="([a-z0-9-]+)\.html(?:#[^"]*)?"', r'href="#pg-\1"', html)
    else:
        html = re.sub(r'href="(cas0\d)-resume\.html"', r'href="#\1"', html)
        html = re.sub(r'href="(?!https?:|#)([^"]+)"', lambda m: 'href="%s%s"' % (SITE, m.group(1)), html)
    html = html.replace('href="index.html"', 'href="%s"' % SITE) if MODE != 'full' else html
    return html

BASE = '''
@page{size:A4 landscape;margin:0}
*{-webkit-print-color-adjust:exact;print-color-adjust:exact}
html,body{margin:0;background:#fff}
.reveal{opacity:1!important;transform:none!important;transition:none!important}
.site-header,.site-footer,.snav,.skip,.next,.gal-back,.crumb,.idx,.cta-row{display:none!important}
.gi-text{position:static!important}
a{text-decoration:none}
.hero .sys *{animation-duration:0s!important}
'''
CGI_CSS = '''
:root{--accent:#5236AB;--accent-ink:#200A58;--accent-soft:#EFEDF8;--ink:#151515;--ink-2:#333;--ink-3:#5A5F6B;--line:#E6E6E6;--c1:#5236AB;--c1-soft:#EFEDF8;--c2:#5236AB;--c2-soft:#EFEDF8;--c3:#5236AB;--c3-soft:#EFEDF8;--r-sm:0;--r-md:0;--r-lg:0}
.t1,.t2,.t3{--t:#5236AB;--ts:#EFEDF8}
*{font-family:Arial,'Liberation Sans',Helvetica,sans-serif!important}
h1,h2,h3,.display,.title{font-weight:400!important;letter-spacing:-.01em}
.btn,.badge,.tags li,.idx a{border-radius:999px}
img,figure,.shot,.cover{border-radius:0!important;box-shadow:none!important}
'''
FULL_CSS = '''
:root{--section:64px}
.pg{break-before:page}
.pg:first-child{break-before:auto}
.cover,.vol,.learn,.ba,.deltas,.benef,.stats3,.decs,.dec,.pb,.cta-row,.poster,.gi,.pc,.fig,.shot,.dec,.pb,.step,.tile,.scope,.kpi-hero,.tldr,.callout,.lvl,.stats3>*,.vol>*,.benef>*,.learn>*,.arch,.princ>*,.job,.sk,.edu>*,figure{break-inside:avoid}
h1,h2,h3,.eyebrow,.sec-head,.sub{break-after:avoid}
.gi{padding:22px 0}.gi-media{padding:16px}.gi-n{font-size:40px}
.gi-media{break-inside:auto}
.hero{padding:32px 0 40px}
.sec{padding-top:48px}.sec-head,.sub,.sec>.eyebrow{break-after:avoid}
'''

def collect_imgs(html):
    return set(re.findall(r'src="(assets/[^"]+)"', html))

def compress(html, bgcol=(255, 255, 255)):
    for s in sorted(collect_imgs(html)):
        if 'cgi-' in s and CGI:
            continue
        im = Image.open(R + s)
        if im.mode in ('RGBA', 'LA', 'P'):
            im = im.convert('RGBA'); base = Image.new('RGB', im.size, bgcol); base.paste(im, mask=im.split()[-1]); im = base
        im = im.convert('RGB')
        if im.width > MAXW:
            im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
        new = 'assets/' + os.path.splitext(os.path.basename(s))[0] + '.jpg'
        im.save(O + new, quality=Q, optimize=True)
        html = html.replace('src="%s"' % s, 'src="%s"' % new)
    return html

# ---------------- FULL ----------------
def build_full():
    order = ['index', 'cas01-resume', 'cas01', 'cas01-realisations', 'cas01-produits', 'cas02-resume', 'cas02', 'cas02-realisations',
             'cas03-resume', 'cas03', 'cas03-realisations', 'apropos']
    chunks = []
    for p in order:
        s = soup(p)
        cls = s.body.get('class', [''])[0] if s.body.get('class') else ''
        main = s.find('main')
        for x in main.select('.snav'): x.decompose()
        chunks.append('<section class="pg %s" id="pg-%s">%s</section>' % (cls, p, prep(main.decode_contents(), p)))
    return '\n'.join(chunks)

# ---------------- SLIDES (short / cgi) ----------------
W, H = 1403, 992
def sel_html(p, sels):
    s = soup(p); out = []
    for sl in sels:
        for el in s.select(sl):
            for x in el.select('.snav,.cta-row' + (',.more,.fig,figure' if sl == '#decisions' else '') + (',.others' if 'h-par' in sl else '')): x.decompose()
            out.append(str(el))
    return '\n'.join(out)

COVER_CGI = '''<div class="cvr">
 <div class="cl">
  <div class="kick">Portfolio · Designer UX/UI</div>
  <h1>Concevoir des services numériques utiles, avec des design systems partagés</h1>
  <p class="subt">Trois cas d'étude : SNCF Gares &amp; Connexions, Île-de-France Mobilités et Conseil d'État.</p>
  <div class="who"><p><b>Quentin Féret</b>, Designer UX/UI</p><p class="date">Octobre 2026</p></div>
  <div class="links"><p>Portfolio complet en ligne : <a href="%(S)s">quentinferetcgi.github.io/portfolio</a></p><p>Contact : <a href="https://www.linkedin.com/in/quentin-feret">linkedin.com/in/quentin-feret</a></p></div>
  <img class="logo" src="assets/cgi-logo.png" alt="CGI">
 </div>
 <div class="cr"><div class="crbox"><div class="g1"></div><div class="ph"><img src="assets/index-01.jpg" alt="Aperçu du design system SNCF Gares &amp; Connexions"></div><div class="g2"></div></div></div>
</div>''' % {'S': SITE}

def slides():
    sheets = []
    def add(sid, band, html, cls=''):
        sheets.append((sid, band, html, cls))
    if CGI:
        add('cover', '', COVER_CGI, 'coversheet')
    else:
        hero = sel_html('index', ['.hero'])
        add('cover', '', hero + '<div style="margin-top:32px;font-size:16px;color:#3A3F4A;line-height:1.7;padding:0 32px"><p style="margin:0">Quentin Féret — Designer UX/UI · Paris</p><p style="margin:0">Portfolio complet en ligne : <a href="%s">quentinferetcgi.github.io/portfolio</a></p><p style="margin:0">Contact : <a href="https://www.linkedin.com/in/quentin-feret">linkedin.com/in/quentin-feret</a></p><p style="margin:16px 0 0;font-size:14px;color:#5A5F6B">Version courte : trois cas d\'étude en résumé. Chaque page renvoie vers le cas complet en ligne.</p></div>' % SITE, 'coversheet2')
    add('sommaire', '', ('<h1 class="ptitle">Sommaire</h1>' if CGI else '') + sel_html('index', ['.proof', '.cases']), 'toc')
    for c, (n, name, tc) in CASES.items():
        def band(label, page): return '<div class="band"><span><b>Cas d\'étude %s</b> · %s — %s</span><a class="cta" href="%s%s.html">Voir le cas complet en ligne →</a></div>' % (n, name.replace('&', '&amp;'), label, SITE, page)
        add(c, band('Présentation', c), '<div class="%s">%s</div>' % (tc, sel_html(c, ['.ch'])))
        add(c + '-r', band('Résumé', c + '-resume'), '<div class="%s">%s</div>' % (tc, sel_html(c + '-resume', ['main > div.wrap'])))
        add(c + '-s', band('Décisions clés', c), '<div class="%s">%s</div>' % (tc, sel_html(c, ['#decisions'])))
        add(c + '-x', band('Résultats', c), '<div class="%s">%s</div>' % (tc, sel_html(c, ['#resultats'])))
    add('apropos', '', sel_html('apropos', ['.ab-hero', '.figs', '.ab-sec[aria-labelledby=h-par]']), 'about')
    return sheets

SLIDE_CSS = '''
.sheet{width:%dpx;height:%dpx;padding:44px 56px 64px;display:flex;flex-direction:column;gap:12px;overflow:hidden;break-after:page;position:relative}
.band{display:flex;justify-content:space-between;align-items:center;font-size:14px;color:#5A5F6B;border-bottom:1px solid var(--line);padding-bottom:10px}
.band b{color:var(--t,var(--accent));font-weight:700} .band a{font-weight:600;color:var(--t,var(--accent))}
.fit{flex:1;min-height:0;display:flex;align-items:flex-start;justify-content:center}
.inner{width:1290px;max-width:none}
.inner .sec,.inner .ch{padding-top:8px!important}
.inner .wrap{max-width:none;padding:0 24px}
.inner .ab-sec{padding-top:24px}.inner .ab-hero{padding:8px 0 24px}.inner .quote{min-height:0}.inner .ab-head{margin-bottom:20px}.inner .job{padding:14px 24px}.inner .tl{gap:10px}
.inner .hero{padding:16px 0 24px}.inner .cases{padding-top:24px}
.inner .cover{margin-top:24px}
.inner .meta{margin-top:24px}
.inner .reveal{opacity:1!important;transform:none!important}
.coversheet,.coversheet2,.toc,.about{padding-top:44px}
.coversheet2 .fit{align-items:center}
''' % (W, H)
CGI_SLIDE_CSS = '''
.band{color:#333;border-bottom:none}.band b{color:#5236AB}
.cta{background:#5236AB;color:#fff!important;padding:7px 18px;border-radius:999px;font-weight:700;font-size:13px}
.ptitle{margin:8px 24px 28px;font-size:44px;line-height:1.1;color:#000}
.coversheet{padding:0!important}.coversheet .fit,.coversheet .inner{width:100%%;height:100%%}
.cvr{display:grid;grid-template-columns:1fr 620px;height:%dpx}
.cl{padding:72px 40px 56px 64px;display:flex;flex-direction:column;gap:22px;position:relative}
.kick{color:#5236AB;font-weight:700;font-size:16px}
.cvr h1{margin:0;font-size:58px;line-height:1.08;color:#000}
.subt{margin:0;font-size:21px;line-height:1.45;color:#333;max-width:600px}
.who{margin-top:14px}.who p,.links p{margin:0}.who p{font-size:20px}.date{color:#5A5F6B;font-size:17px!important}
.links{font-size:15px;color:#333;line-height:1.8}
.logo{position:absolute;left:64px;bottom:64px;width:120px}
.cr{position:relative}.crbox{position:absolute;right:72px;top:%dpx;width:600px;height:600px}
.g1{position:absolute;left:300px;top:0;width:300px;height:300px;background:url(assets/cgi-gradient.jpg) center/cover;clip-path:polygon(0 0,100%% 0,100%% 100%%,50%% 100%%,50%% 50%%,0 50%%)}
.ph{position:absolute;left:150px;top:150px;width:300px;height:300px;overflow:hidden;background:#EFEDF8}.ph img{width:100%%;height:100%%;object-fit:cover;object-position:left center}
.g2{position:absolute;left:0;top:300px;width:300px;height:300px;background:linear-gradient(135deg,#200A58 0%%,#5236AB 55%%,#E31937 100%%);clip-path:polygon(0 0,50%% 0,50%% 50%%,100%% 50%%,100%% 100%%,0 100%%)}
''' % (H, (H - 600) // 2)

async def main():
    extra = (CGI_CSS if CGI else '')
    if MODE == 'full':
        body = build_full(); body = compress(body)
        doc = '<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Quentin Féret — Designer UX/UI · Portfolio</title><style>%s\n%s\n%s\n%s</style></head><body>%s</body></html>' % (css, BASE, FULL_CSS, extra, body)
        vp = (1290, 900)
    else:
        out = []
        sh = slides()
        for sid, band, html, cls in sh:
            html = prep(html)
            out.append('<div class="sheet %s" id="%s">%s<div class="fit"><div class="inner">%s</div></div></div>' % (cls, sid, band, html))
        body = compress('\n'.join(out), (255, 255, 255))
        doc = '<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Quentin Féret — Designer UX/UI · Portfolio (version courte)</title><style>%s\n%s\n%s\n%s</style></head><body>%s</body></html>' % (css, BASE, SLIDE_CSS, extra + (CGI_SLIDE_CSS if CGI else ''), body)
        vp = (W, H)
    open(O + 'doc.html', 'w').write(doc)
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        ctx = await b.new_context(viewport={'width': vp[0], 'height': vp[1]}, reduced_motion='reduce')
        pg = await ctx.new_page()
        await pg.goto('file://' + O + 'doc.html'); await pg.wait_for_load_state('networkidle')
        await pg.emulate_media(media='print', reduced_motion='reduce')
        await pg.evaluate('document.fonts.ready.then(()=>1)'); await pg.wait_for_timeout(600)
        if MODE != 'full':
            z = await pg.evaluate("""()=>[...document.querySelectorAll('.sheet')].map(s=>{const f=s.querySelector('.fit'),i=s.querySelector('.inner');if(s.classList.contains('coversheet'))return [s.id,1];const fh=f.clientHeight,fw=f.clientWidth;i.style.zoom=1;const ih=i.scrollHeight;let z=Math.min(1,fh/ih,fw/1290);i.style.zoom=z;return [s.id,Math.round(ih),fh,+z.toFixed(2)]})""")
            for x in z: print(x)
            await pg.pdf(path=O + 'raw.pdf', width='297mm', height='210mm', print_background=True, scale=0.8, margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'}, outline=True, tagged=True)
        else:
            await pg.pdf(path=O + 'raw.pdf', format='A4', landscape=True, print_background=True, scale=0.8,
                         margin={'top': '12mm', 'bottom': '14mm', 'left': '12mm', 'right': '12mm'}, outline=True, tagged=True)
        await b.close()
asyncio.run(main())
print(os.path.getsize(O + 'raw.pdf') / 1e6, 'MB raw')
