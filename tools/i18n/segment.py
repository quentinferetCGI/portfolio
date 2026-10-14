"""Découpe une page HTML en segments traduisibles, sans réécrire le code.

Un segment = le contenu interne (inline compris) du plus haut élément « pur »
(qui ne contient que du texte et des balises de phrasé), ou un attribut
textuel (alt, aria-label, title, placeholder, meta description / og).
Chaque segment est repéré par ses positions dans le fichier source, ce qui
permet de réinjecter la traduction à l'identique (voir apply.py).
"""
from html.parser import HTMLParser
import re

PHRASING = {'a', 'abbr', 'b', 'bdi', 'bdo', 'br', 'cite', 'code', 'data', 'dfn', 'em', 'i',
            'kbd', 'mark', 'q', 's', 'samp', 'small', 'span', 'strong', 'sub', 'sup', 'time',
            'u', 'var', 'wbr', 'img', 'svg', 'path', 'circle', 'rect', 'g', 'line', 'polyline'}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
SKIP = {'script', 'style'}
TEXT_ATTRS = {'alt', 'aria-label', 'title', 'placeholder'}
META_NAMES = {'description', 'og:title', 'og:description', 'og:site_name'}


class Node:
    def __init__(self, tag, parent, inner_start):
        self.tag, self.parent, self.inner_start = tag, parent, inner_start
        self.inner_end = None
        self.children, self.texts = [], []  # texts: (start, end)

    @property
    def pure(self):
        return all(c.tag in PHRASING and c.pure for c in self.children)


class P(HTMLParser):
    def __init__(self, src):
        super().__init__(convert_charrefs=False)
        self.src = src
        self.lines = [0]
        for m in re.finditer('\n', src):
            self.lines.append(m.end())
        self.root = Node('#root', None, 0)
        self.cur = self.root
        self.attrs = []  # (start, end, text)
        self.skip = 0

    def off(self):
        l, c = self.getpos()
        return self.lines[l - 1] + c

    def handle_starttag(self, tag, attrs):
        start = self.off()
        raw = self.get_starttag_text()
        end = start + len(raw)
        self._attrs(tag, attrs, start, raw)
        if tag in SKIP:
            self.skip += 1
        if tag in VOID:
            n = Node(tag, self.cur, end); n.inner_end = end
            self.cur.children.append(n)
            return
        n = Node(tag, self.cur, end)
        self.cur.children.append(n)
        self.cur = n

    def handle_startendtag(self, tag, attrs):
        start = self.off(); raw = self.get_starttag_text()
        self._attrs(tag, attrs, start, raw)
        n = Node(tag, self.cur, start + len(raw)); n.inner_end = n.inner_start
        self.cur.children.append(n)

    def handle_endtag(self, tag):
        start = self.off()
        if tag in SKIP:
            self.skip -= 1
        n = self.cur
        while n is not self.root and n.tag != tag:
            n.inner_end = start; n = n.parent
        if n is self.root:
            return
        n.inner_end = start
        self.cur = n.parent

    def handle_data(self, data):
        if self.skip or not data.strip():
            return
        s = self.off()
        self.cur.texts.append((s, s + len(data)))

    def handle_entityref(self, name):
        s = self.off(); self.cur.texts.append((s, s + len(name) + 2))

    def handle_charref(self, name):
        s = self.off(); self.cur.texts.append((s, s + len(name) + 3))

    def _attrs(self, tag, attrs, start, raw):
        d = dict(attrs)
        names = set(TEXT_ATTRS)
        if tag == 'meta' and (d.get('name') in META_NAMES or d.get('property') in META_NAMES):
            names = {'content'}
        for name in names:
            if name not in d or not (d[name] or '').strip():
                continue
            m = re.search(r'\s%s\s*=\s*(["\'])(.*?)\1' % re.escape(name), raw, re.S)
            if m:
                self.attrs.append((start + m.start(2), start + m.end(2), m.group(2)))


def has_text(n):
    return bool(n.texts) or any(has_text(c) for c in n.children)


def segments(src):
    p = P(src); p.feed(src); p.close()
    segs = []

    def walk(n, parent_pure):
        if n.tag in SKIP:
            return
        if n is not p.root and n.pure and not parent_pure and n.inner_end is not None and has_text(n):
            segs.append((n.inner_start, n.inner_end, src[n.inner_start:n.inner_end]))
            return
        for (s, e) in n.texts:  # texte orphelin dans un conteneur mixte
            segs.append((s, e, src[s:e]))
        for c in n.children:
            walk(c, n.pure and n is not p.root)

    walk(p.root, False)
    segs += p.attrs
    segs.sort()
    return segs
