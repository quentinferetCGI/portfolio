# Prompt de reproduction — portfolio de designer, accessible et mesuré

À coller dans une nouvelle session, avec le dépôt de référence (ce projet, contenant `CLAUDE.md` et `tools/`) et les contenus du nouveau projet en pièces jointes. Remplacer les éléments entre [crochets].

---

Agis comme directeur artistique, développeur front-end et auditeur accessibilité (RGAA 4.1.2, WCAG 2.2 AA). Tu travailles en français.

## Mission

Crée le portfolio de [Prénom Nom], [métier], en reprenant **à l'identique** la méthode, le design system, la structure et les règles du dépôt de référence `[chemin ou URL du dépôt]`. Lis d'abord son `CLAUDE.md` en entier : il fait foi. Réutilise `assets/*.css`, les polices Inter auto-hébergées et les scripts de `tools/`.

## Livrables (site statique HTML/CSS, sans build, publié sur GitHub Pages)

1. Accueil, À propos, [N] cas d'étude, chacun avec une page complète, un résumé (avec « Dans la presse ») et, si besoin, des galeries Réalisations / Produits.
2. Page Accessibilité (déclaration au modèle officiel de https://accessibilite.numerique.gouv.fr/) et page Plan du site, liées depuis le pied de page de chaque page.
3. Mesure d'audience Umami Cloud sans cookie, avec les événements `contact-linkedin`, `cas-complet`, `presse-lien`, `ouvrir-cas`.
4. Un audit d'accessibilité rédigé (score indicatif, 16 écarts type, plan d'action) puis les correctifs appliqués.
5. Si je le demande : PDF complet, court et version [entreprise], liens avec UTM.
6. Un `CLAUDE.md` à jour à la fin.

## Données du projet (ne rien inventer, demande ce qui manque)

- Identité et métier : [ ]
- Cas d'étude (client, rôle, période, équipe, outils, chiffres validés, visuels, liens de presse) : [ ]
- Nombres à ne pas dire ou à corriger : [ ]
- URL de publication : [ ]
- ID du site Umami : [ ]
- Contact autorisé pour la déclaration d'accessibilité : [LinkedIn / e-mail]
- Teinte de chaque cas (3 couleurs sourdes, contraste AA vérifié) : [ ]

## Méthode imposée

1. Crée une branche. Annonce ton plan en une phrase, puis travaille avec une liste de tâches.
2. Montre une page, fais-la valider, puis passe à la suivante. Fournis des captures bureau (1280 px) et mobile (390 px).
3. Design system : mêmes jetons, mêmes 5 tailles de texte, mêmes composants que le dépôt de référence. Aucun texte porteur d'information sous 13 px.
4. Accessibilité dès la conception : un seul `h1`, aucun saut de titre, landmarks nommés de façon unique, pas d'`aside` imbriqué, `aria-label` seulement sur un élément qui le supporte, alternatives d'images pertinentes, `canonical` et Open Graph sur chaque page, liens externes annonçant « nouvel onglet », cibles d'au moins 24 px, mouvement réduit respecté.
5. Reflow : aucun défilement horizontal à 320 px ; grilles en `minmax(0,1fr)` ; pas de hauteur fixe sur le texte ; décor débordant coupé avec `overflow:clip`.
6. Audit avec `tools/audit` : axe-core, html-validate, contrastes réels (y compris `color-mix`), zoom 200 % et 400 %, espacement du texte WCAG 1.4.12, parcours clavier. Objectif : 0 violation et 0 erreur. Bloque `cloud.umami.is` pendant les tests.
7. Déclaration d'accessibilité : applique les 13 rubriques du modèle officiel avec **l'état réel**. Sans audit RGAA complet, l'état est « non évalué », sans taux. Précise que la démarche est volontaire si le site n'est pas légalement assujetti. N'écris jamais « conforme » sans audit.
8. Ne rédige ni chiffre, ni client, ni citation, ni lien de presse que je n'ai pas fournis.

## Quand m'interroger (une seule fois, par `AskUserQuestion`)

Contact public, état de conformité affiché, statut légal, tout chiffre ambigu, toute décision irréversible.

## Fin de mission

Fusionne dans `main`, pousse, vérifie la page en ligne. Réponds en quelques lignes : ce qui est fait, ce qui reste à valider, ce que tu n'as pas pu vérifier (lecteur d'écran, site en ligne, audit RGAA complet).
