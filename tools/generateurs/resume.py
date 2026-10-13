import sys; sys.path.insert(0,'.')
from common import HEAD, TAIL
D = {
 'cas01': dict(cls='t1', n='01', name='SNCF Gares &amp; Connexions', plain='SNCF Gares & Connexions',
   tags=['Dette graphique','Transversalité','Multiplateforme'],
   role="Piloter 16 projets avec une équipe de 6 designers, grâce à un outil de pilotage que j'ai conçu, pour assurer le delivery des évolutions sur 5 design systems.",
   kpi=('Résultat clé','50 → 10&nbsp;%','big','du temps consacré à la conception : il est réinvesti dans le cadrage, la recherche, les tests et la maintenance.'),
   img='index-01.jpg', alt="Aperçu du design system SNCF Gares & Connexions.",
   vol=[('5','Design systems à gérer'),('~80','Composants atomes par design system'),('~40','Composants molécules par design system'),('~80','Modèles de pages par design system'),('Oui','Design tokens · couleurs, mockups, langues et responsive')],
   learn=["Structurer plusieurs design systems avec une architecture de tokens réaliste.","Améliorer les process de travail entre toutes les parties prenantes.","Diffuser la recherche utilisateur en amont de la conception."],
   next=('cas02-resume.html','Cas suivant : Île-de-France Mobilités')),
 'cas02': dict(cls='t2', n='02', name='Île-de-France Mobilités', plain='Île-de-France Mobilités',
   tags=['Billettique','Design system','Multiplateforme'],
   role="Piloter 12 chantiers de conception en parallèle et construire un design system multiplateforme partagé par 3 équipes design et 3 équipes de développement.",
   kpi=('Résultat clé','80 → 20&nbsp;%','big','du temps consacré à la conception : il est réinvesti dans le cadrage, les tests, la livraison et la maintenance.'),
   img='index-02.jpg', alt="Aperçu du design system Île-de-France Mobilités.",
   vol=[('1','Design system à gérer'),('63','Composants atomes'),('75','Composants molécules'),('180','Composants pages'),('Oui','Design tokens · couleurs, responsive et mockups')],
   learn=["Concevoir pour Android et iOS en plus du Web.","Coordonner le travail sur 12 fonctionnalités en parallèle.","Développer un design system multiplateforme."],
   next=('cas03-resume.html',"Cas suivant : Conseil d'État")),
 'cas03': dict(cls='t3', n='03', name="Conseil d'État", plain="Conseil d'État",
   tags=['Refonte graphique','Design system','Service public'],
   role="Synchroniser 5 designers autour d'un design system commun, et intégrer l'accessibilité (RGAA) dans la conception.",
   kpi=('Périmètre','5&nbsp;outils<br>5&nbsp;designers','big sm',"Les designers des outils de Télérecours, synchronisés autour d'un design system commun."),
   img='index-03.jpg', alt="Design system UI Kit V2.0 des services de Télérecours du Conseil d'État.",
   vol=[('1','Design system à gérer'),('21','Composants atomes'),('26','Composants molécules'),('Oui','Design tokens · sur la colorimétrie')],
   learn=["Gérer un design system partagé entre 5 designers.","Intégrer l'accessibilité numérique (RGAA) dans la conception.","Tester en amont de la production."],
   next=('index.html','Retour aux trois cas')),
}
for k,d in D.items():
    tags=''.join(f'<li>{t}</li>' for t in d['tags'])
    vcls='vol' if len(d['vol'])==5 else 'vol n4'
    vol=''.join(f'<div><span class="num">{a}</span><p>{b}</p></div>' for a,b in d['vol'])
    learn=''.join(f'<div class="card"><b>0{i+1}</b><p>{t}</p></div>' for i,t in enumerate(d['learn']))
    lab,big,bcls,txt=d['kpi']
    body=f'''
<section class="ch" aria-labelledby="h1">
<div class="wrap">
<p class="crumb"><a href="index.html">Projets</a> / Cas d'étude {d['n']} · Résumé</p>
<div class="ch-top">
<div>
<p class="eyebrow" style="margin-bottom:16px">Cas d'étude {d['n']} · Résumé</p>
<h1 class="display" id="h1">{d['name']}</h1>
<ul class="tags">{tags}</ul>
<p class="eyebrow" style="margin:28px 0 8px;color:var(--ink-3)">Mon rôle</p>
<p class="lead">{d['role']}</p>
</div>
<aside class="kpi-hero" aria-label="{lab}">
<span class="label">{lab}</span>
<span class="{bcls.replace('big','big num',1) if False else 'big num'+(' sm' if 'sm' in bcls else '')}">{big}</span>
<p>{txt}</p>
</aside>
</div>
<div class="cover"><img src="assets/{d['img']}" alt="{d['alt']}" width="2400" height="1350"></div>
</div>
</section>

<div class="wrap">

<section class="sec" aria-labelledby="h-vol" style="padding-top:clamp(64px,8vw,104px)">
<div class="sec-head"><p class="k">Volumétrie</p><h2 class="title" id="h-vol">Le design system en chiffres.</h2></div>
<div class="{vcls} reveal" role="group" aria-label="Volumétrie du design system">{vol}</div>
</section>

<section class="sec" aria-labelledby="h-learn" style="padding-top:clamp(64px,8vw,104px)">
<div class="sec-head"><p class="k">Ce que j'ai appris</p><h2 class="title" id="h-learn">Trois enseignements.</h2></div>
<div class="learn reveal">{learn}</div>
</section>

<aside class="next reveal">
<h2>Lire le cas complet</h2>
<a class="btn" href="{k}.html">Commencer par le contexte →</a>
</aside>
<p class="srcs" style="margin-top:24px"><a href="{d['next'][0]}">{d['next'][1]} →</a></p>
'''
    out=HEAD.format(title=d['plain']+' — Résumé', desc=f"Résumé du cas d'étude {d['n']} : {d['plain']}. "+d['role'], cls=d['cls'])+body+TAIL.replace('{next_title}','').replace('{next_href}','').replace('{next_cta}','')
    # le TAIL ajoute un second bloc .next vide : on le retire
    import re
    out=re.sub(r'\n<aside class="next reveal">\n<h2></h2>\n<a class="btn" href=""></a>\n</aside>\n','\n',out)
    open(f'/home/claude/portfolio/{k}-resume.html','w').write(out)
    print(k,len(out),'next-vide' if '<h2></h2>' in out else 'ok')
