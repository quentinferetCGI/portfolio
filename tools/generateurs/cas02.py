import sys; sys.path.insert(0,'.')
from common import *
body = '''
<!-- 1. EN-TÊTE -->
<section class="ch" aria-labelledby="h1">
<div class="wrap">
<p class="crumb"><a href="index.html">Projets</a> / Cas d'étude 02</p>
<div class="ch-top">
<div>
<p class="eyebrow" style="margin-bottom:16px">UX/UI × Design system</p>
<h1 class="display" id="h1">Île-de-France Mobilités</h1>
<p class="lead">Piloter 12 chantiers de conception en parallèle et construire un design system multiplateforme partagé par 3 équipes design et 3 équipes de développement.</p>
<ul class="tags"><li>Billettique</li><li>Design system</li><li>Multiplateforme</li></ul>
</div>
<aside class="kpi-hero" aria-label="Résultat clé">
<span class="label">Résultat clé</span>
<span class="big num">80 → 20&nbsp;%</span>
<p>du temps consacré à la conception : il est réinvesti dans le cadrage, les tests, la livraison et la maintenance.</p>
</aside>
</div>
<dl class="meta m4">
<div><dt>Client</dt><dd>Île-de-France Mobilités</dd></div>
<div><dt>Rôle</dt><dd>Designer UX/UI</dd></div>
<div><dt>Période</dt><dd>Sept. 2023 – mai 2025</dd></div>
<div><dt>Outils</dt><dd>Figma</dd></div>
</dl>
<p class="team"><b>Équipe</b> · Programme de modernisation de la billettique, avec la Direction du Numérique et les entreprises PwC, CGI, MC2i, Ingé-Stif, Monetech, Apple et Google</p>
<div class="cover"><img src="assets/index-02.jpg" alt="Aperçu du design system Île-de-France Mobilités." width="2400" height="1350"></div>
</div>
</section>

''' + SNAV.format(res="Résultats &amp; impact") + '''
<div class="wrap">

<!-- 2. TL;DR -->
<section class="sec" id="tldr" aria-labelledby="h-tldr" style="padding-top:64px">
<div class="sec-head"><p class="k">En bref</p><h2 class="title" id="h-tldr">Le problème, ma décision, l'effet.</h2></div>
<div class="tldr reveal">
<div><h3>Problème</h3><p>12 fonctionnalités interdépendantes conçues sans charte ni design system, sur des fichiers séparés, livrées en PNG.</p></div>
<div><h3>Décision</h3><p>Un design system relié de bout en bout, des fondamentaux aux modèles de page, et une nouvelle organisation des fichiers.</p></div>
<div><h3>Effet</h3><p>La conception passe de 80&nbsp;% à 20&nbsp;% du temps, et un design system commun à tous les produits IDFM est lancé.</p></div>
</div>
</section>

<!-- 3. CONTEXTE & ENJEU -->
<section class="sec" id="contexte" aria-labelledby="h-ctx">
<div class="sec-head"><p class="k">Contexte &amp; enjeu</p><h2 class="title" id="h-ctx">Des acteurs indépendants, avant l'arrivée d'une équipe design.</h2></div>
<div class="prose reveal">
<p>Designer sur le programme de modernisation de la billettique (PMB), je suis intervenu sur la conception des parcours de 12 fonctionnalités interdépendantes, avec différentes équipes travaillant chacune sur leurs propres fichiers, initiés depuis 2019.</p>
<p>Côté IDFM, le projet a été lancé avec plusieurs acteurs indépendants, avant l'arrivée d'une équipe design. Les chefs de projet et les parties prenantes avaient commencé à concevoir les maquettes sans s'appuyer sur la charte graphique IDFM, inexistante à l'époque, ni sur les fondements de chaque environnement technologique.</p>
</div>

<h3 class="sub">Périmètre — Android · iOS · Web · 7 fonctionnalités</h3>
<div class="scope reveal">
<div class="card"><h4>Titre de transport</h4><ul><li>Navigo Liberté + — nouveau titre de transport</li></ul></div>
<div class="card"><h4>Service</h4><ul><li>Navigo Annuel sur smartphone — nouveau service</li></ul></div>
<div class="card"><h4>Achat</h4><ul><li>L'achat d'un titre dématérialisé</li></ul></div>
<div class="card"><h4>Après-vente</h4><ul><li>Le service après-vente</li></ul></div>
<div class="card"><h4>Compte</h4><ul><li>L'espace personnel</li><li>La création et la gestion d'un compte</li></ul></div>
<div class="card"><h4>Mobilités</h4><ul><li>Les services de mobilités alternatives</li></ul></div>
</div>
<figure class="fig reveal">
<div class="img"><img src="assets/cas02-01.jpg" alt="Navigo Liberté + : un même parcours décliné sur Android, iOS et le web, en vue ordinateur et en vue mobile." loading="lazy" decoding="async"></div>
<figcaption><h4>Exemple · Navigo Liberté +</h4><p>Un même parcours décliné sur Android, iOS et le web, en vue ordinateur et en vue mobile.</p></figcaption>
</figure>

<h3 class="sub">Constat — trois faits à mon arrivée</h3>
<div class="stats3 reveal">
<div class="stat"><span class="num">01</span><h4>Un produit non aligné avec les maquettes</h4></div>
<div class="stat"><span class="num">02</span><h4>Aucun design system existant</h4></div>
<div class="stat"><span class="num">03</span><h4>Une conception inadaptée au développement</h4></div>
</div>

<h3 class="sub">Problèmes identifiés</h3>
<div class="pb reveal">
<div class="card"><span class="id">P1 · PRODUCTION</span><h4>Une production non alignée avec les maquettes</h4><p>Les maquettes ont été conçues sans tenir compte des spécifications fonctionnelles de chaque environnement technologique, ni de la charte digitale d'IDFM.</p></div>
<div class="card"><span class="id">P2 · FICHIERS</span><h4>Aucune organisation dans les fichiers</h4><p>Le temps était consacré à retrouver une maquette et à comprendre l'enchaînement des écrans.</p></div>
<div class="card"><span class="id">P3 · LIVRAISON</span><h4>Une livraison difficile auprès des développeurs</h4><p>Les maquettes étaient livrées au format PNG : les outils d'inspection des développeurs ne pouvaient pas fonctionner.</p></div>
</div>
</section>

<!-- 4. DÉMARCHE -->
<section class="sec" id="demarche" aria-labelledby="h-dem">
<div class="sec-head"><p class="k">Démarche</p><h2 class="title" id="h-dem">Quatre enjeux, un système relié de bout en bout.</h2>
<p class="lead">Contribuer à structurer un design system multiplateforme, destiné à plusieurs fonctionnalités de l'écosystème Île-de-France Mobilités.</p></div>
<ol class="steps n4 reveal">
<li><h4>Mutualiser l'existant</h4><p>Identifier ce qui peut être partagé et réutilisé d'une fonctionnalité à l'autre.</p></li>
<li><h4>Assurer la cohérence</h4><p>Structurer les évolutions selon les spécificités du Web, d'Android et d'iOS.</p></li>
<li><h4>Faciliter la transmission</h4><p>Rendre les spécifications fonctionnelles compréhensibles par les équipes techniques.</p></li>
<li><h4>Intégrer l'accessibilité</h4><p>Prendre en compte le RGAA, le RAAM et les audits sur les fonctionnalités en cours de développement.</p></li>
</ol>

<h3 class="sub">Architecture — avant, aujourd'hui</h3>
<div class="lvl reveal">
<div class="row"><span>Avant<small>des éléments sans lien entre eux</small></span>
<div class="c off"><b>01 Fondamentaux</b>Déconnectés des composants</div>
<div class="c"><b>02 Atomes</b>Composants existants en production</div>
<div class="c off"><b>03 Molécules</b>Inexistant</div>
<div class="c off"><b>04 Pages</b>Inexistant</div></div>
<div class="row"><span>Aujourd'hui<small>un système relié de bout en bout</small></span>
<div class="c hl"><b>01 Fondamentaux</b>La charte digitale IDFM traduite pour la conception de produit</div>
<div class="c hl"><b>02 Atomes</b>Librairies iOS et Android, refactorisation des composants en production</div>
<div class="c hl"><b>03 Molécules</b>Les fonctionnalités clés rassemblées et documentées<span class="tag">Nouveau</span></div>
<div class="c hl"><b>04 Pages</b>Des modèles de patrons de conception pour chaque environnement<span class="tag">Nouveau</span></div></div>
<p class="gapnote">Fondamentaux reconnectés aux atomes · deux niveaux créés : molécules et pages.</p>
</div>
<div class="vol n4 reveal" role="group" aria-label="Volumétrie du design system">
<div><span class="num">1</span><p>design system à gérer</p></div>
<div><span class="num">63</span><p>composants atomes</p></div>
<div><span class="num">75</span><p>composants molécules</p></div>
<div><span class="num">180</span><p>composants pages</p></div>
</div>
<p class="srcs"><b>Design tokens</b> · couleurs, responsive et mockups.</p>
</section>

<!-- 5. DÉCISIONS CLÉS -->
<section class="sec" id="decisions" aria-labelledby="h-dec">
<div class="sec-head"><p class="k">Décisions clés</p><h2 class="title" id="h-dec">Quatre décisions pour passer de la maquette au système.</h2>
<p class="lead">Chaque décision répond à un constat précis et se traduit par un effet observable.</p></div>
<div class="decs">
<article class="dec reveal"><header><b>D1</b><h3>Relier les fondations aux composants</h3></header>
<dl>
<div><dt>Constat</dt><dd>Aucun design system, et une charte digitale IDFM inexistante au lancement du projet.</dd></div>
<div><dt>Décision</dt><dd>Traduire la charte en fondamentaux, créer les librairies iOS et Android, refactoriser les composants en production et construire les niveaux molécules et pages.</dd></div>
<div><dt>Effet</dt><dd class="eff"><span>+2 niveaux</span>un système relié de bout en bout, des fondamentaux aux modèles de page.</dd></div>
</dl></article>
<article class="dec reveal" data-d="1"><header><b>D2</b><h3>Réorganiser le dossier de fichiers</h3></header>
<dl>
<div><dt>Constat</dt><dd>Aucune organisation : le temps passait à retrouver une maquette.</dd></div>
<div><dt>Décision</dt><dd>Une nouvelle organisation du dossier, autour de fichiers clés pour documenter, tester, partager et construire.</dd></div>
<div><dt>Effet</dt><dd class="eff"><span>Moins de fichiers</span>l'effort de conception est synchronisé sur toutes les fonctionnalités à livrer.</dd></div>
</dl></article>
<article class="dec reveal"><header><b>D3</b><h3>Livrer aux développeurs un format exploitable</h3></header>
<dl>
<div><dt>Constat</dt><dd>Des maquettes livrées en PNG : les outils d'inspection ne fonctionnaient pas.</dd></div>
<div><dt>Décision</dt><dd>Améliorer les livrables et les informations transmises pour une implémentation fidèle, avec des composants analysés selon leurs états et leurs variantes.</dd></div>
<div><dt>Effet</dt><dd class="eff"><span>0 → 30 %</span>du temps consacré à la livraison.</dd></div>
</dl></article>
<article class="dec reveal" data-d="1"><header><b>D4</b><h3>Faire adopter les méthodes, par la démonstration</h3></header>
<dl>
<div><dt>Constat</dt><dd>Des profils de conception hétérogènes, répartis sur plusieurs équipes.</dd></div>
<div><dt>Décision</dt><dd>Un enseignement adapté à chacun, et des démonstrations et prototypes interactifs pour le management, avec une écoute active des besoins.</dd></div>
<div><dt>Effet</dt><dd class="eff"><span>Projet transverse</span>un design system commun à tous les produits de la marque IDFM est lancé.</dd></div>
</dl></article>
</div>
<figure class="fig reveal" style="margin-top:40px">
<div class="img"><img src="assets/cas02-02.png" alt="Nouvelle organisation du dossier Billettique IDFM autour de fichiers clés." loading="lazy" decoding="async"></div>
<figcaption><h4>Organisation · Dossier Billettique IDFM</h4><p>Des fichiers clés pour documenter, tester, partager et construire ont permis de synchroniser l'effort de conception sur toutes les fonctionnalités à livrer, et de réduire le nombre de fichiers à gérer.</p></figcaption>
</figure>

<h3 class="sub">Le travail de fond derrière ces décisions</h3>
<div class="more reveal">
<div class="card"><h4>Fondations &amp; tokens</h4><ul><li>Explication de l'organisation des fondations visuelles</li><li>Démocratisation de la charte digitale du client auprès des équipes</li></ul></div>
<div class="card"><h4>Bibliothèques &amp; handoff</h4><ul><li>Analyse de la logique, des états et des variantes des composants</li><li>Livrables et informations transmises améliorés pour les développeurs</li></ul></div>
<div class="card"><h4>Accessibilité</h4><ul><li>Prise en compte du RGAA, du RAAM et des audits d'accessibilité sur les fonctionnalités en cours de développement</li></ul></div>
</div>
</section>

<!-- 6. RÉALISATIONS -->
<section class="sec" id="realisations" aria-labelledby="h-real">
<div class="sec-head"><p class="k">Réalisations</p><h2 class="title" id="h-real">Du parcours au composant documenté.</h2>
<p class="lead">Un aperçu des livrables : pages produit, documentation des composants et cartographie des parcours.</p></div>
<div class="shots">
<figure class="shot reveal"><img src="assets/cas02-realisations-10.png" alt="Page de présentation de Navigo Liberté + sur mobile et sur ordinateur." loading="lazy" decoding="async"><figcaption>Page de présentation · Navigo Liberté + <span>Mobile et ordinateur</span></figcaption></figure>
<figure class="shot reveal"><img src="assets/cas02-realisations-09.png" alt="Documentation du composant champ de saisie, par environnement." loading="lazy" decoding="async"><figcaption>Documentation d'un composant · Champ de saisie <span>Ordinateur, iOS, Android</span></figcaption></figure>
<figure class="shot reveal"><img src="assets/cas02-realisations-06.jpg" alt="Cartographie des parcours, avant et aujourd'hui." loading="lazy" decoding="async"><figcaption>Cartographie des parcours <span>Avant / Aujourd'hui</span></figcaption></figure>
</div>
<div class="cta-row"><a class="btn btn-primary" href="cas02-realisations.html">Toutes les réalisations →</a></div>
</section>

<!-- 7. RÉSULTATS -->
<section class="sec" id="resultats" aria-labelledby="h-res">
<div class="sec-head"><p class="k">Résultats &amp; impact</p><h2 class="title" id="h-res">La conception passe de 80 % à 20 % du temps.</h2>
<p class="lead">Le temps libéré est réinvesti dans le cadrage, les tests, la livraison et la maintenance.</p></div>
<div class="ba reveal" role="group" aria-label="Répartition du temps par phase, avant et aujourd'hui">
<div class="row"><span>Avant<small>ancienne organisation</small></span>
<div class="bar"><i class="p-rec" style="width:20%">20&nbsp;%</i><i class="p-con" style="width:80%">80&nbsp;%</i></div></div>
<div class="row"><span>Aujourd'hui<small>nouvelle organisation</small></span>
<div class="bar"><i class="p-cad" style="width:10%">10&nbsp;%</i><i class="p-rec" style="width:20%">20&nbsp;%</i><i class="p-con" style="width:20%">20&nbsp;%</i><i class="p-tes" style="width:10%">10&nbsp;%</i><i class="p-liv" style="width:30%">30&nbsp;%</i><i class="p-mai" style="width:10%">10&nbsp;%</i></div></div>
<ul class="legend"><li><i class="p-cad"></i>Cadrer</li><li><i class="p-rec"></i>Rechercher</li><li><i class="p-con"></i>Concevoir</li><li><i class="p-tes"></i>Tester</li><li><i class="p-liv"></i>Livrer</li><li><i class="p-mai"></i>Maintenir</li></ul>
</div>
<div class="deltas reveal" aria-label="Évolution par phase">
<div><span>Cadrer</span><b>0 → 10 %</b></div>
<div><span>Rechercher</span><b>20 → 20 %</b></div>
<div class="hl"><span>Concevoir</span><b>80 → 20 %</b></div>
<div><span>Tester</span><b>0 → 10 %</b></div>
<div><span>Livrer</span><b>0 → 30 %</b></div>
<div><span>Maintenir</span><b>0 → 10 %</b></div>
</div>

<h3 class="sub">Les résultats identifiés</h3>
<ol class="benef n3 reveal">
<li><b>01</b>Accélération de la production des livrables de conception</li>
<li><b>02</b>Mise en place d'un cycle de production itératif</li>
<li><b>03</b>Lancement d'un projet transverse : un design system commun à tous les produits de la marque IDFM</li>
</ol>

<h3 class="sub">Ce que j'ai appris</h3>
<div class="learn reveal">
<div class="card"><b>01</b><p>Concevoir pour Android et iOS en plus du Web.</p></div>
<div class="card"><b>02</b><p>Coordonner le travail sur 12 fonctionnalités en parallèle.</p></div>
<div class="card"><b>03</b><p>Développer un design system multiplateforme.</p></div>
</div>
</section>
'''
out = HEAD.format(title="Île-de-France Mobilités", desc="Cas d'étude : construire un design system multiplateforme pour le programme de modernisation de la billettique d'Île-de-France Mobilités. La conception passe de 80 % à 20 % du temps.", cls="t2") + body + TAIL.replace('{next_title}',"Cas suivant : Conseil d'État").replace('{next_href}','cas03-resume.html').replace('{next_cta}','Découvrir le cas →')
open('/home/claude/portfolio/cas02.html','w').write(out)
print(len(out))
