# CLAUDE.md — Portfolio de designer (site statique, accessible, mesuré)

Ce fichier décrit tout ce qui a été construit sur ce projet, pour le refaire à l'identique sur un autre portfolio. Les valeurs propres à Quentin Féret (noms, chiffres, clients, identifiants) sont à remplacer ; la méthode, le design system, la structure et les règles sont à conserver.

## 1. Le projet en une phrase

Site statique (HTML + CSS + un peu de JS, sans build, sans framework) publié sur GitHub Pages : une page d'accueil, une page À propos, 3 cas d'étude (chacun avec résumé et galeries), une déclaration d'accessibilité et un plan du site. 14 pages en français, et leur version anglaise dans `en/` (voir §13).

- Dépôt : `/home/claude/portfolio`, branche `main`, publié sur `https://quentinferetcgi.github.io/portfolio/`.
- Langue de travail et de tous les livrables : **français**. Typographie française (espaces insécables avant `:`, `%`, guillemets « »).
- Rôle attendu de Claude : **directeur artistique + auditeur accessibilité**. Il propose, justifie, puis applique ; il n'invente aucun fait.

## 2. Règles de conduite (valides pour tout projet de ce type)

1. **N'invente rien.** Chiffres, clients, dates, liens de presse, taux de conformité : uniquement ce que l'utilisateur a fourni ou ce qui est vérifié. En cas de doute, demander (`AskUserQuestion`).
2. **Corrections validées à conserver** (à adapter) : « 6 design systems » ; ne pas remettre la définition « 410 composants » ; « Dans la presse » vit dans les pages **Résumé**, pas dans les galeries.
3. **Travailler sur une branche** (`refonte-da`, `accessibilite`), tester, puis fusionner dans `main` et pousser. Trailer de commit : `Co-Authored-By` + `Claude-Session` donnés par le système.
4. **Valider par page** : proposer une page, faire valider, puis passer à la suivante. Ne pas migrer tout d'un coup.
5. **Vérifier avant d'affirmer** : captures Playwright (bureau 1280 px et mobile 390 px), outils d'audit, puis conclure. Ne jamais déclarer « conforme » sans audit.
6. Pour les tableaux de bord ou documents longs : créer le squelette tôt, remplir section par section, relire ses propres chiffres.

## 3. Structure des fichiers

```
index.html                  Accueil : hero + illustration animée, chiffres clés, 3 affiches de cas
apropos.html                À propos : citation, chiffres, convictions, parcours, compétences, formation, contact
cas0N.html                  Cas d'étude complet (sections 01 à 09, sommaire collant)
cas0N-resume.html           Résumé (+ « Dans la presse »)
cas0N-realisations.html     Galerie réalisations
cas01-produits.html         Galerie produits (cas 1 uniquement)
accessibilite.html          Déclaration d'accessibilité (modèle officiel)
plan-du-site.html           Plan du site
assets/tokens.css           Jetons + composants de base (en-tête, pied de page, boutons, focus, sr-only)
assets/home.css             Accueil
assets/about.css            À propos
assets/case.css             Cas d'étude et résumés (teinte par cas)
assets/gallery.css          Galeries et bloc presse
assets/legal.css            Accessibilité et plan du site
assets/fonts/               Inter 400/500/600/700, woff2, auto-hébergée (aucun appel à Google Fonts)
assets/*.jpg|png            Visuels : images optimisées, `width`/`height` renseignés
tools/                      Scripts (voir §10)
.nojekyll                   Obligatoire pour GitHub Pages
```

Chaque page charge `tokens.css` + sa feuille dédiée, ajoute `<script>document.documentElement.classList.add('js')</script>` dans le `<head>` et le script Umami (voir §7).

## 4. Design system (`assets/tokens.css`)

Direction artistique : éditoriale, sobre, base neutre chaude, un accent bleu, une teinte par cas.

- **Neutres** : `--bg #FAFAF8`, `--surface #FFF`, `--ink #0E0F12`, `--ink-2 #3A3F4A`, `--ink-3 #5A5F6B` (AA sur `--bg`, 6,3:1), `--line #E7E6E1`.
- **Accent** : `--accent #2340FF`, `--accent-ink #1A2FC4` (texte/survol), `--accent-soft #E9ECFF`.
- **Teinte par cas** : `--c1 #0B1F4B` bleu nuit, `--c2 #0E5F63` vert-pétrole, `--c3 #6E1F3A` bordeaux sourd, chacune avec `-soft`. Sur les pages de cas, `body.t1/.t2/.t3` définit `--t` et `--ts`.
- **Typographie** : Inter, 5 tailles seulement : `--fs-display clamp(40,5.2vw,64)`, `--fs-title clamp(28,3.4vw,40)`, `--fs-lead clamp(18,1.6vw,22)`, `--fs-body 17px`, `--fs-small 13px`. Aucun texte porteur d'information sous 13 px.
- **Espace** : unité 8 px ; `--section clamp(96px,12vw,160px)`, `--gutter clamp(16px,4vw,32px)`, `--maxw 1200px`.
- **Formes** : rayons 10/16/24/pill ; deux ombres douces. **Mouvement** : `--ease cubic-bezier(.2,.7,.2,1)`, 300 ms.
- **Focus** : `:focus-visible{outline:3px solid var(--accent);outline-offset:3px}`.
- Composants : en-tête collant (`.site-header`, `--hh:66px`), sommaire collant (`.snav`), `.reveal` (apparition au scroll via IntersectionObserver, désactivée en `prefers-reduced-motion`), `.kpi-hero`, `.vol`, `.arch`, `.ba` (avant/après), `.deltas`, `.fig`, `.card`, `.steps`, `.poster`, `.pc` (carte presse), `.gi` (galerie : texte collant 4fr / média 8fr), `.tiles`, `.idx` (sommaire de galerie), `.sr-only`, `.skip`.
- Gabarit de page : lien d'évitement → `header.site-header` → `<main id="contenu">` → `footer.site-footer`.

## 5. Contenu et structure éditoriale

- **Accueil** : un `<h1>` promesse, une illustration `role="img"` décrite, un bandeau de 4 chiffres, 3 affiches de cas (lien `data-umami-event="ouvrir-cas"`).
- **Cas d'étude** : bloc « résultat clé » (`.kpi-hero`), métadonnées (`dl.meta` : client, rôle, période, équipe, outils), 9 sections numérotées (TL;DR, contexte, démarche, décisions, réalisations, résultats…), carte « cas suivant » (`aside.next`).
- **Résumé** : version courte + section « Dans la presse » avant « cas suivant ».
- **Galeries** : en-tête, sommaire `nav.idx-nav > ol.idx`, items `.gi` (variantes `.wide`, `.solo`), retour au cas.
- Chaque image a un `alt` descriptif (48 à 92 caractères), les décoratives sont `aria-hidden`.

## 6. Accessibilité (RGAA 4.1.2 / WCAG 2.2 AA) — règles à respecter dès la conception

- `lang="fr"`, `<title>` unique, un seul `<h1>`, **pas de saut de niveau de titre** (h2 → h3 → h4), jamais de titre ou de `<p>` dans un `<span>`.
- Landmarks : `header`, `nav`, `main`, `footer`. Chaque `nav`/`aside`/`section` répété a un **nom unique** (`aria-label` ou `aria-labelledby`). Pas d'`aside` imbriqué dans un autre landmark : utiliser `<div role="group" aria-label>` pour un encart.
- `aria-label` seulement sur un élément qui le supporte (landmark, ou `role` explicite : `group`, `img`).
- Contrastes : texte ≥ 4,5:1, éléments graphiques ≥ 3:1, **mesurés aussi sur les `color-mix` et dégradés** (axe ne les calcule pas ; utiliser `tools/audit/contrast.py`). Teintes de barres de cas : `.p-rec` = `color-mix(var(--t) 86%, #fff)` + texte blanc ; `.p-con` = `color-mix(var(--t) 20%, #fff)` + texte `--t`.
- Reflow : à 320 px (zoom 400 %) aucun défilement horizontal ; grilles en `minmax(0,1fr)`, `overflow-wrap:anywhere` sur les gros chiffres et les liens longs ; jamais de hauteur fixe sur un conteneur de texte ; décor débordant coupé avec `overflow:clip` (pas `hidden`, pas `clip-path`).
- Espacement du texte (WCAG 1.4.12) : tester avec `line-height:1.5`, `letter-spacing:.12em`, `word-spacing:.16em`, `p{margin-bottom:2em}`.
- Cibles ≥ 24 × 24 px (liens du pied de page : `padding-block:6px`).
- Liens `target="_blank"` : `rel="noopener"` + `<span class="sr-only"> (nouvel onglet)</span>`.
- Mouvement : tout est visible sans JS ; animations coupées en `prefers-reduced-motion`.
- Métadonnées sur chaque page : `canonical`, `og:type`, `og:locale`, `og:site_name`, `og:title`, `og:description`, `og:url` (pas d'`og:image` tant qu'un visuel n'est pas choisi).
- État obtenu sur ce projet : 0 violation axe-core, 0 erreur html-validate, zoom 200 % et 400 % sans perte, sur 14 pages. Un test lecteur d'écran (NVDA / VoiceOver) **n'a pas** été fait.

## 7. Mesure d'audience (Umami Cloud, sans cookie)

- Script, avant `</head>` de chaque page : `<script defer src="https://cloud.umami.is/script.js" data-website-id="<ID DU SITE>"></script>` (l'ID actuel est propre à ce projet : à remplacer).
- Pas de bandeau de consentement ; mention dans le pied de page : « Statistiques de visite anonymes, sans cookie ».
- Événements : `contact-linkedin`, `cas-complet`, `presse-lien`, `ouvrir-cas` (attribut `data-umami-event`).
- Suivre l'origine des visites : liens avec `?utm_source=…&utm_medium=…&utm_campaign=…` (jamais `utmsource`, qui n'est pas valide). Exemple CV : `?utm_source=cv&utm_medium=pdf&utm_campaign=candidature`.
- Exclure ses propres visites : `localStorage.setItem('umami.disabled','1')` dans le navigateur concerné.

## 8. Pages légales (accessibilite.html, plan-du-site.html)

Source officielle : https://accessibilite.numerique.gouv.fr/ (modèle de déclaration d'accessibilité, 13 rubriques dans cet ordre) : engagement, périmètre, état de conformité, résultats des tests, contenus non accessibles (3 catégories), établissement de la déclaration (dates), technologies, environnement de test, outils, pages vérifiées, retour d'information et contact, voies de recours (Défenseur des droits), validité (mise à jour après modification importante ou 3 ans).

Décisions prises sur ce projet (à reconfirmer à chaque nouveau projet) :
- Portfolio personnel : présenté comme **démarche volontaire** (« à ma connaissance » non assujetti à l'article 47 de la loi 2005-102).
- **État : « non évalué »**, aucun taux, tant qu'il n'y a pas d'audit RGAA complet (106 critères, échantillon). Ne jamais écrire « partiellement conforme » ou un pourcentage sans audit.
- Contact : LinkedIn uniquement (choix de l'utilisateur). Aucune adresse e-mail publiée sans accord.
- Aucun schéma pluriannuel ni plan d'actions publié : le dire, ne pas l'inventer.
- Pied de page de **chaque page** : « Accessibilité : non évaluée » (→ déclaration), « Plan du site », contact. Le libellé suit l'état réel (« non conforme », « partiellement conforme », « totalement conforme ») dès qu'un audit existe.
- Mettre à jour la date de la déclaration et la liste des défauts après chaque correction.

## 9. Journal du travail réalisé (ordre chronologique)

1. Direction artistique et système de design (`tokens.css`), accueil, puis chaque page migrée et validée une à une.
2. Trois cas d'étude, trois résumés, page À propos, quatre galeries (Réalisations ×3, Produits ×1).
3. Fusion de `refonte-da` dans `main`.
4. Trois PDF dans le nouveau design : complet (75 p, 4,2 Mo), court (15 p, 0,76 Mo), court CGI (15 p, 0,51 Mo).
5. Déplacement de « Dans la presse » dans les pages Résumé.
6. Ajout d'Umami Cloud et des événements ; conseils UTM pour le CV.
7. Audit d'accessibilité (score indicatif 78/100, 16 écarts dont 3 majeurs), rapport rédigé dans un document Claude Docs.
8. Correctifs des 16 écarts, déclaration d'accessibilité, plan du site, pied de page commun, métadonnées. Résultat : 0 violation axe, HTML valide.

## 10. Outils (`tools/`)

- `tools/audit/` : `axe_run.py` (axe-core 4.10.2 via Playwright), `probe.py` (titres, landmarks, liens, images, tailles de police), `contrast.py` (contrastes réels, gère `color(srgb …)`), `reflow.py` (200 %/400 % + espacement du texte), `kbd3.py` (parcours Tab avec 450 ms d'attente), `hv.json` (config html-validate). Installation : `npm i` dans `tools/audit` (axe-core, html-validate) ; Playwright pour Python avec Chromium (déjà présent dans l'environnement). Serveur local : `python3 -m http.server 8765` depuis la racine. **Bloquer `cloud.umami.is`** dans les scripts Playwright (`page.route`), sinon les tests ralentissent.
- `tools/generateurs/` : `common.py` (en-tête/pied de page des cas), `cas02.py`, `cas03.py`, `gal.py` (galeries), `resume.py`. Historiques : ils ont servi à générer les pages, mais **les fichiers HTML font foi**, et leurs modèles d'en-tête/pied ne contiennent pas les derniers changements (nouveau pied de page, métadonnées, `sr-only`). À mettre à jour avant de les réutiliser. `gal.py` lit les anciennes pages dans `SRC_OLD`.
- `tools/pdf/` : `newpdf.py` (modes `full`, `short`, `cgi`, Chromium → PDF, images allégées par `MAXW`/`Q`), `finalize.py` (détecte et retire les pages blanches, fixe le titre du PDF ; usage : `finalize.py source.pdf sortie.pdf "Titre"`). Règles d'impression : `break-inside:avoid` sur les blocs (`.cover,.vol,.learn,.ba…`) ; couverture CGI avec classes `.cvr`/`.subt` (éviter les conflits avec `case.css`). Les liens du PDF doivent pointer vers l'URL réelle du site et porter des UTM.

## 11. Pièges rencontrés et solutions

- Item de galerie large avec grand vide : un `div` en `flex:2 1 420px` fuyait dans `.gi-b` → aplatir les div imbriqués.
- Conflit de fusion sur `cas03-resume.html` : garder la version de la refonte (`git checkout --theirs`).
- Anciens liens `monkeybusinessman.github.io` morts (404) : remplacés partout par l'URL actuelle.
- Une grille à `1fr` déborde dès qu'un enfant a un mot long insécable : toujours `minmax(0,1fr)`.
- `overflow:hidden` + décor `::after` débordant = fausse alerte de rognage ; `clip-path` fait déborder le défilement : utiliser `overflow:clip`.
- `grep` ne suffit pas pour vérifier le HTML : lancer html-validate (a repéré une balise `</ul<h3>` malformée).
- Le dépôt a été renommé (`quentinferetCGI/portfolio`) : le push passe, avec un avertissement.

## 12. Procédure pour reproduire sur un autre projet

1. Cloner ce dépôt, créer une branche, **conserver** `assets/*.css`, `fonts/`, la structure de pages et `tools/`.
2. Demander à l'utilisateur : identité, clients/missions, chiffres validés, visuels, liens de presse, URL de publication, ID Umami, contact autorisé, état d'audit réel.
3. Remplacer : teintes de cas (`--c1..c3`), textes, images (avec `alt`), métadonnées (`canonical`, `og:*`), liens, ID Umami, domaine dans la déclaration d'accessibilité.
4. Valider page par page avec l'utilisateur (captures bureau + mobile).
5. Lancer l'audit (`tools/audit`), corriger jusqu'à 0 violation axe et 0 erreur html-validate, vérifier 200 %/400 % et l'espacement du texte.
6. Rédiger la déclaration selon le modèle officiel avec **l'état réel** ; proposer un vrai audit RGAA et un test lecteur d'écran avant toute mention de conformité.
7. Générer les PDF si demandés (liens avec UTM), fusionner dans `main`, pousser, vérifier la page en ligne.

## 13. Version anglaise (`en/`)

- `en/` contient les 14 pages en anglais, mêmes noms de fichiers. **Ne pas les modifier à la main** : elles sont générées depuis les pages françaises.
- Chaîne : `tools/i18n/segment.py` découpe chaque page en segments (contenu des éléments de texte + attributs `alt`, `aria-label`, `title`, meta description/og) repérés par position ; `tools/i18n/src/_index.json` associe chaque texte source à un identifiant ; `tools/i18n/en/<page>.json` contient les traductions (identifiant → HTML anglais, balises internes conservées). Un identifiant absent garde le texte source (noms propres, outils).
- Régénérer après toute modification : `python3 tools/i18n/apply.py` (idempotent). Le script écrit `en/*.html` (`lang="en"`, `../assets/`, `canonical` et `og:url` en `/en/`, `og:locale` en_US) et ajoute aux deux langues les liens `hreflang` fr/en/x-default (bloc `<!-- i18n -->`), `og:locale:alternate` et le sélecteur de langue FR | EN (`div.lang-sw role="group"` en fin de `nav.nav`, langue active en `span[aria-current]`, nom accessible « FR – Français » / « EN – English », événements Umami `langue-en` / `langue-fr`).
- Modifier un texte français : mettre à jour la clé correspondante dans `_index.json` (ou réexporter) et sa traduction, sinon le segment reste en français dans `en/`. Vérifier avec une recherche de mots français dans `en/`.
- Choix de traduction : anglais américain, ton consulting ; « Projets » → Work, « Réalisations » → Deliverables, « cas d'étude » → case study ; organismes français explicités à la première mention (Conseil d'État = France's supreme administrative court, RGAA = France's official accessibility standard based on WCAG) ; liens vers des contenus français signalés « (in French) ».
- Les visuels (captures Figma, écrans) restent en français ; leur `alt` est traduit.
