"""Génère la version anglaise du site dans en/ et relie les deux langues.

Usage (depuis la racine du dépôt) : python3 tools/i18n/apply.py

- Lit les traductions de tools/i18n/en/*.json (clé = identifiant de segment,
  voir tools/i18n/src/_index.json). Un segment absent garde le texte source
  (noms propres, outils, chiffres).
- Écrit en/<page>.html avec lang="en", chemins ../assets/, canonical et og:*
  propres à la version anglaise.
- Ajoute dans les deux langues les liens hreflang et le sélecteur de langue.
Le script est idempotent : on peut le relancer après chaque modification
d'une page française ou d'une traduction.
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from segment import segments  # noqa: E402

BASE = 'https://quentinferetcgi.github.io/portfolio/'
I18N = os.path.join(ROOT, 'tools', 'i18n')
index = json.load(open(os.path.join(I18N, 'src', '_index.json')))
tr = {}
for f in glob.glob(os.path.join(I18N, 'en', '*.json')):
    tr.update(json.load(open(f)))

PAGES = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, '*.html')))
MARK = '<!-- i18n -->'


def url(page, lang):
    path = '' if page == 'index.html' else page
    return BASE + ('en/' if lang == 'en' else '') + path


def alternates(page):
    return (f'{MARK}\n<link rel="alternate" hreflang="fr" href="{url(page, "fr")}">\n'
            f'<link rel="alternate" hreflang="en" href="{url(page, "en")}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{url(page, "fr")}">\n')


def strip_i18n(src):
    src = re.sub(re.escape(MARK) + r'\n(?:<link rel="alternate" hreflang[^>]*>\n)+', '', src)
    src = re.sub(r'<meta property="og:locale:alternate"[^>]*>\n', '', src)
    src = re.sub(r'\n<a class="lang"[^>]*>[^<]*</a>', '', src)
    return src


def add_links(src, page, lang):
    src = strip_i18n(src)
    src = re.sub(r'(<link rel="canonical"[^>]*>\n)', lambda m: m.group(1) + alternates(page), src, count=1)
    alt_locale = 'fr_FR' if lang == 'en' else 'en_US'
    src = re.sub(r'(<meta property="og:locale"[^>]*>\n)',
                 lambda m: m.group(1) + f'<meta property="og:locale:alternate" content="{alt_locale}">\n', src, count=1)
    if lang == 'fr':
        switch = (f'<a class="lang" href="en/{page}" hreflang="en" lang="en" '
                  f'data-umami-event="langue-en">English</a>')
    else:
        switch = (f'<a class="lang" href="../{page}" hreflang="fr" lang="fr" '
                  f'data-umami-event="langue-fr">Français</a>')
    src = re.sub(r'(<nav class="nav"[^>]*>.*?)(\n</nav>)', lambda m: m.group(1) + '\n' + switch + m.group(2),
                 src, count=1, flags=re.S)
    return src


def translate(src):
    out, last, missing = [], 0, []
    for a, b, t in segments(src):
        sid = index.get(t)
        if sid is None:
            continue
        if sid in tr:
            out.append(src[last:a]); out.append(tr[sid]); last = b
    out.append(src[last:])
    return ''.join(out)


def to_en(src, page):
    src = strip_i18n(src)
    src = translate(src)
    src = src.replace('<html lang="fr">', '<html lang="en">', 1)
    src = src.replace('content="fr_FR"', 'content="en_US"')
    src = re.sub(r'(rel="canonical" href=")[^"]*', lambda m: m.group(1) + url(page, 'en'), src, count=1)
    src = re.sub(r'(property="og:url" content=")[^"]*', lambda m: m.group(1) + url(page, 'en'), src, count=1)
    src = re.sub(r'(?<=["\'(\s,])assets/', '../assets/', src)
    src = re.sub(r'(\d)(?:&nbsp;| | | )%', r'\1%', src)
    return add_links(src, page, 'en')


def main():
    os.makedirs(os.path.join(ROOT, 'en'), exist_ok=True)
    for page in PAGES:
        p = os.path.join(ROOT, page)
        fr = open(p, encoding='utf-8').read()
        en = to_en(fr, page)
        open(os.path.join(ROOT, 'en', page), 'w', encoding='utf-8').write(en)
        open(p, 'w', encoding='utf-8').write(add_links(fr, page, 'fr'))
        print('en/' + page)


if __name__ == '__main__':
    main()
