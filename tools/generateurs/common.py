HEAD = '''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Cas d'étude · Quentin Féret</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#FAFAF8">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 64 64%22%3E%3Crect width=%2264%22 height=%2264%22 rx=%2214%22 fill=%22%230E0F12%22/%3E%3Ctext x=%2232%22 y=%2242%22 font-family=%22Helvetica,Arial%22 font-size=%2226%22 font-weight=%22700%22 fill=%22white%22 text-anchor=%22middle%22%3EQF%3C/text%3E%3C/svg%3E">
<link rel="preload" href="assets/fonts/inter-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/tokens.css">
<link rel="stylesheet" href="assets/case.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body class="{cls}">
<a class="skip" href="#contenu">Aller au contenu</a>

<header class="site-header">
<div class="wrap">
<a class="brand" href="index.html"><span class="mono" aria-hidden="true">QF</span><span>Quentin Féret <small>— Designer UX/UI</small></span></a>
<nav class="nav" aria-label="Navigation principale">
<a href="index.html" aria-current="page">Projets</a>
<a href="apropos.html">À propos</a>
<a href="https://www.linkedin.com/in/quentin-feret" target="_blank" rel="noopener">Contact</a>
</nav>
</div>
</header>

<main id="contenu">
'''
TAIL = '''
<aside class="next reveal">
<h2>{next_title}</h2>
<a class="btn" href="{next_href}">{next_cta}</a>
</aside>

</div>
</main>

<footer class="site-footer">
<div class="wrap"><span>Quentin Féret · Portfolio</span><a href="https://www.linkedin.com/in/quentin-feret" target="_blank" rel="noopener">Me contacter sur LinkedIn →</a></div>
</footer>

<script>
(function(){
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var els=document.querySelectorAll('.reveal');
  if('IntersectionObserver' in window&&!reduce){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});
    els.forEach(function(e){io.observe(e)});
    var links=[].slice.call(document.querySelectorAll('.snav a'));
    var map={};links.forEach(function(a){map[a.getAttribute('href').slice(1)]=a});
    var so=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(a){a.classList.remove('on')});map[e.target.id].classList.add('on')}})},{rootMargin:'-30% 0px -60% 0px'});
    Object.keys(map).forEach(function(id){var s=document.getElementById(id);if(s)so.observe(s)});
  }else{els.forEach(function(e){e.classList.add('in')})}
})();
</script>
</body>
</html>
'''
SNAV = '''<nav class="snav" aria-label="Sommaire du cas">
<ul>
<li><a href="#tldr"><b>01</b>En bref</a></li>
<li><a href="#contexte"><b>02</b>Contexte &amp; enjeu</a></li>
<li><a href="#demarche"><b>03</b>Démarche</a></li>
<li><a href="#decisions"><b>04</b>Décisions clés</a></li>
<li><a href="#realisations"><b>05</b>Réalisations</a></li>
<li><a href="#resultats"><b>06</b>{res}</a></li>
</ul>
</nav>
'''
