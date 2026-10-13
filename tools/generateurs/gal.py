import os
import re, sys, html
from bs4 import BeautifulSoup
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HEAD, TAIL

R = '/home/claude/portfolio/'
SRC = os.environ.get('SRC_OLD', 'old/')  # anciennes pages à convertir (sauvegarde)

PAGES = [
    dict(f='cas01-realisations', cls='t1', n='01', h1='Réalisations · organisation et fichiers',
         eyebrow='Cas d’étude 01 · SNCF Gares & Connexions'),
    dict(f='cas01-produits', cls='t1', n='01', h1='Réalisations · Les produits',
         eyebrow='Cas d’étude 01 · SNCF Gares & Connexions'),
    dict(f='cas02-realisations', cls='t2', n='02', h1='Réalisations',
         eyebrow='Cas d’étude 02 · Île-de-France Mobilités'),
    dict(f='cas03-realisations', cls='t3', n='03', h1='Réalisations',
         eyebrow='Cas d’étude 03 · Conseil d’État'),
]

def esc(t): return html.escape(t, quote=True)

def clean(node):
    """Copie l'élément sans styles inline ni attributs de mise en page."""
    for t in node.find_all(True):
        for a in list(t.attrs):
            if a not in ('href', 'target', 'rel'):
                del t.attrs[a]
    return node

def body_html(card, title_tag):
    out = []
    for el in card.find_all(recursive=False):
        if el is title_tag or el.name == 'h3':
            continue
        if el.name == 'div' and el.find('span') and not el.find('p'):  # ligne kicker/num
            continue
        if el.name == 'div' and el.find('p'):
            for c in el.find_all(recursive=False):
                clean(c); out.append(str(c))
            continue
        if el.name == 'p' and 'italic' in (el.get('style') or ''):
            out.append('<p class="note">%s</p>' % el.decode_contents())
            continue
        if el.name == 'ul' and el.find('li') and 'border-radius: 999px' in (el.find('li').get('style') or ''):
            clean(el); el['class'] = 'pills'
        else:
            clean(el)
        out.append(str(el))
    return '\n'.join(out)

def dims(src):
    try:
        with Image.open(R + src) as im:
            return im.size
    except Exception:
        return (None, None)

def img_tag(img, first):
    src = img['src']
    w, h = dims(src)
    m = re.search(r'max-width:\s*(\d+)px', img.get('style', ''))
    cls = ' class="narrow" style="--mw:%spx"' % m.group(1) if m else ''
    size = ' width="%d" height="%d"' % (w, h) if w else ''
    lazy = '' if first else ' loading="lazy" decoding="async"'
    return '<img src="%s" alt="%s"%s%s%s>' % (src, esc(img['alt']), size, lazy, cls)

def item(a, idx, first):
    cards = [c for c in a.find_all(recursive=False)]
    head = cards[0]
    kick = head.find('span').get_text(strip=True)
    num = head.find('span').find_next('span').get_text(strip=True)
    h3 = head.find('h3')
    title = h3.decode_contents().strip()
    body = body_html(head, h3)
    media = cards[1] if len(cards) > 1 else None
    id_ = 'r%s' % num
    kcls = ''
    mhtml = ''
    if media is None:
        kcls = ' solo'
    elif media.find('figure'):
        kcls = ' wide'
        figs = []
        for fg in media.find_all('figure'):
            cap = fg.find('figcaption')
            n = cap.find('span').get_text(strip=True)
            txt = cap.get_text(' ', strip=True)
            txt = re.sub(r'^\s*%s\s*·\s*' % re.escape(n), '', txt)
            figs.append('<figure>%s<figcaption><b>%s</b>%s</figcaption></figure>' % (img_tag(fg.find('img'), False), n, esc(txt)))
        mhtml = '<div class="gi-media grid">\n%s\n</div>' % '\n'.join(figs)
    elif media.find('svg'):
        tiles = []
        for t in media.find_all('div', recursive=True):
            svg = t.find('svg', recursive=False) or None
            if len(t.find_all('span', recursive=False)) == 2 and t.find('div', recursive=False) and t.find('div', recursive=False).find('svg'):
                s = t.find('svg')
                spans = t.find_all('span', recursive=False)
                svg_s = re.sub(r'viewbox', 'viewBox', str(s))
                svg_s = re.sub(r' (fill|stroke-linecap|stroke-linejoin|stroke-width|stroke)="[^"]*"', '', svg_s)
                svg_s = svg_s.replace('<svg ', '<svg fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" ', 1)
                tiles.append('<div class="tile"><span class="ic">%s</span><b>%s</b><span class="d">%s</span></div>' % (svg_s, spans[0].get_text(strip=True), spans[1].get_text(strip=True)))
        mhtml = '<div class="gi-media"><div class="tiles">\n%s\n</div></div>' % '\n'.join(tiles)
    else:
        imgs = media.find_all('img')
        mhtml = '<div class="gi-media">\n%s\n</div>' % '\n'.join(img_tag(im, first and i == 0) for i, im in enumerate(imgs))
    if kcls == ' wide':
        text = '<div class="gi-text"><div class="gi-head"><span class="gi-n">%s</span><p class="gi-k">%s</p><h2 class="gi-t">%s</h2></div><div class="gi-b">%s</div></div>' % (num, esc(kick), title, body)
    else:
        text = '<div class="gi-text"><span class="gi-n">%s</span><p class="gi-k">%s</p><h2 class="gi-t">%s</h2><div class="gi-b">%s</div></div>' % (num, esc(kick), title, body)
    return id_, kick, num, '<article class="gi%s reveal" id="%s">\n%s\n%s\n</article>' % (kcls, id_, text, mhtml)

def press(sec):
    head = sec.find('div')
    k = head.find('span').get_text(strip=True)
    h2 = head.find('h2').get_text(strip=True)
    intro = head.find('p').decode_contents() if head.find('p') else ''
    out = ['<section class="press" id="presse" aria-labelledby="h-presse">',
           '<div class="press-head"><p class="k">%s</p><h2 class="title" id="h-presse">%s</h2><p>%s</p></div>' % (k, h2, intro)]
    cards = []
    ul = sec.find('ul', recursive=False)
    if ul:
        for li in ul.find_all('li', recursive=False):
            top = li.find('div')
            spans = top.find_all('span')
            src = spans[1].get_text(strip=True); badge = spans[2].get_text(strip=True); date = spans[3].get_text(strip=True)
            h3 = li.find('h3').decode_contents()
            p = li.find('p').decode_contents()
            a = li.find('a')
            cards.append('<li class="pc reveal"><div class="pc-top"><span class="pc-src">%s<span class="badge">%s</span></span><span class="date">%s</span></div><h3>%s</h3><p>%s</p><a class="ext" href="%s" target="_blank" rel="noopener">%s</a></li>' % (src, badge, date, h3, p, esc(a['href']), a.get_text(strip=True)))
    art = sec.find('article', recursive=False)
    if art:
        img = art.find('img')
        w, h = dims(img['src'])
        pb = art.find_all('div', recursive=False)[1]
        top = pb.find('div')
        src = top.find('span').get_text(strip=True)
        date = top.find('span').find_next('span').get_text(strip=True)
        chips = ''.join('<li>%s</li>' % li.get_text(strip=True) for li in top.find_all('li'))
        h3 = pb.find('h3').decode_contents(); p = pb.find('p').decode_contents(); a = pb.find('a')
        cards.append('<li class="pc feat reveal"><div class="ph"><img src="%s" alt="%s" width="%d" height="%d" loading="lazy" decoding="async"></div><div class="pb"><div class="pc-top"><span class="pc-src">%s</span><span class="date">%s</span></div><ul>%s</ul><h3>%s</h3><p>%s</p><a class="ext" href="%s" target="_blank" rel="noopener">%s</a></div></li>' % (img['src'], esc(img['alt']), w, h, src, date, chips, h3, p, esc(a['href']), a.get_text(strip=True)))
    out.append('<ul class="press-list">\n%s\n</ul>' % '\n'.join(cards))
    out.append('</section>')
    return '\n'.join(out)

def build(P):
    s = BeautifulSoup(open(SRC + P['f'] + '.html').read(), 'html.parser')
    title = s.title.get_text(strip=True)
    desc = s.find('meta', attrs={'name': 'description'})['content']
    crumb_a = s.find('div', style=re.compile('padding: 40px 24px 0')).find('a')
    crumb_href, crumb_txt = crumb_a['href'], crumb_a.get_text(strip=True).lstrip('← ').strip()
    secs = s.find('main').find_all('section', recursive=False)
    items = []; first = True
    for a in secs[0].find_all('article', recursive=False):
        items.append(item(a, len(items), first)); first = False
    pr = press(secs[1]) if len(secs) > 1 else ''
    ft = s.find('footer').find_all('a')
    back_href, back_txt = ft[0]['href'], ft[0].get_text(strip=True)
    sp = ft[1].find_all('span')
    nxt_k, nxt_t = sp[0].get_text(strip=True), sp[1].get_text(strip=True)
    nxt_cta = nxt_t if '→' in nxt_t else nxt_t + ' →'
    nxt_h2 = nxt_k if nxt_k else ''

    back_lbl = esc(back_txt if back_txt.startswith('←') else '← ' + back_txt)
    idx = ''.join('<li><a href="#%s"><b>%s</b>%s</a></li>' % (i, n, esc(k)) for i, k, n, _ in items)
    if pr:
        idx += '<li><a href="#presse"><b>↗</b>Dans la presse</a></li>'
    head = HEAD.replace("{title} — Cas d'étude · Quentin Féret", "{title} · Quentin Féret").replace('case.css">', 'case.css">\n<link rel="stylesheet" href="assets/gallery.css">') \
        .replace('{title}', esc(title).replace('&amp;amp;', '&amp;')).replace('{desc}', esc(desc)).replace('{cls}', P['cls'])
    head = head.replace('<a href="index.html" aria-current="page">Projets</a>', '<a href="index.html" aria-current="page">Projets</a>')
    top = '''<section class="gal-head" aria-labelledby="h1">
<div class="wrap">
<p class="crumb"><a href="%s">← %s</a></p>
<p class="eyebrow" style="margin-bottom:16px">%s</p>
<h1 class="display" id="h1">%s</h1>
<ol class="idx" aria-label="Sommaire de la page">%s</ol>
</div>
</section>
<div class="wrap">
<div class="gal">
%s
</div>
%s
<p class="gal-back"><a href="%s">%s</a></p>''' % (crumb_href, esc(crumb_txt), esc(P['eyebrow']), esc(P['h1']), idx,
                                                        '\n'.join(x[3] for x in items), pr,
                                                        back_href,
                                                        back_lbl)
    tail = TAIL.replace('{next_title}', esc(nxt_k)) \
        .replace('{next_href}', ft[1]['href']).replace('{next_cta}', esc(nxt_cta))
    # CTA : les titres d'origine sont conservés
    open(R + P['f'] + '.html', 'w').write(head + top + tail)
    return len(items)

if __name__ == '__main__':
    for P in PAGES:
        print(P['f'], build(P))
