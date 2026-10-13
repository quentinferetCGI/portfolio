import asyncio, json
from playwright.async_api import async_playwright
pages=['index','apropos','cas01-resume','cas01','cas01-realisations','cas01-produits','cas02-resume','cas02','cas02-realisations','cas03-resume','cas03','cas03-realisations']
JS = r"""()=>{
 const o={};
 o.title=document.title; o.lang=document.documentElement.lang;
 o.viewport=(document.querySelector('meta[name=viewport]')||{}).content;
 o.desc=!!document.querySelector('meta[name=description]'); o.og=[...document.querySelectorAll('meta[property^="og:"]')].map(m=>m.getAttribute('property'));
 o.canonical=!!document.querySelector('link[rel=canonical]');
 o.h=[...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h=>h.tagName[1]+':'+h.textContent.trim().replace(/\s+/g,' ').slice(0,50));
 o.landmarks=[...document.querySelectorAll('header,nav,main,footer,aside,section[aria-label],section[aria-labelledby],[role=region],[role=banner],[role=contentinfo]')].map(e=>e.tagName.toLowerCase()+(e.getAttribute('aria-label')?'['+e.getAttribute('aria-label')+']':'')+(e.closest('main')&&e.tagName!=='MAIN'?'(in main)':''));
 o.navs=[...document.querySelectorAll('nav')].map(n=>n.getAttribute('aria-label'));
 const imgs=[...document.images]; o.imgs=imgs.length; o.noalt=imgs.filter(i=>!i.hasAttribute('alt')).length; o.emptyalt=imgs.filter(i=>i.getAttribute('alt')==='').length;
 o.altlen=imgs.map(i=>(i.getAttribute('alt')||'').length).sort((a,b)=>b-a).slice(0,3);
 o.nodim=imgs.filter(i=>!i.getAttribute('width')).length;
 o.longalt=imgs.filter(i=>(i.getAttribute('alt')||'').length>150).map(i=>i.getAttribute('src'));
 const as=[...document.querySelectorAll('a')];
 o.links=as.length; o.blank=as.filter(a=>a.target==='_blank').map(a=>(a.textContent.trim().slice(0,40))+'|'+(a.title||'')+'|'+(a.getAttribute('aria-label')||''));
 o.arrow=as.filter(a=>/[→←↗]/.test(a.textContent)).length;
 const names={}; as.forEach(a=>{const n=(a.getAttribute('aria-label')||a.textContent).trim().replace(/\s+/g,' ');(names[n]=names[n]||new Set()).add(a.getAttribute('href'))});
 o.dupnames=Object.entries(names).filter(([n,s])=>s.size>1).map(([n,s])=>n+' => '+[...s].join(','));
 o.emptylinks=as.filter(a=>!(a.textContent.trim()||a.getAttribute('aria-label')||a.querySelector('img[alt]'))).length;
 o.aria=[...document.querySelectorAll('[role],[aria-label],[aria-hidden],[aria-labelledby],[aria-current]')].map(e=>e.tagName.toLowerCase()+'.'+(e.className||'')+' '+['role','aria-label','aria-hidden','aria-current'].filter(a=>e.hasAttribute(a)).map(a=>a+'='+String(e.getAttribute(a)).slice(0,40)).join(' ')).slice(0,40);
 const lsty=getComputedStyle(document.querySelector('main a, a'));
 const inl=[...document.querySelectorAll('main p a, main li a, .srcs a, .lead a')];
 o.inlineLinks=inl.slice(0,6).map(a=>a.textContent.trim().slice(0,30)+' => deco:'+getComputedStyle(a).textDecorationLine+' color:'+getComputedStyle(a).color+' parent:'+getComputedStyle(a.parentElement).color);
 // tailles cibles
 const small=[...document.querySelectorAll('a,button,input,summary')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.width<24||r.height<24)&&getComputedStyle(e).display!=='inline'}).map(e=>e.tagName+'.'+e.className+' '+Math.round(e.getBoundingClientRect().width)+'x'+Math.round(e.getBoundingClientRect().height));
 o.smallTargets=small.slice(0,8);
 o.inlineSmall=[...document.querySelectorAll('a')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height<24&&getComputedStyle(e).display==='inline'}).length;
 // fontes
 const fs={}; document.querySelectorAll('body *').forEach(e=>{if([...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())){const s=parseFloat(getComputedStyle(e).fontSize);fs[s]=(fs[s]||0)+1}});
 o.fontsizes=fs;
 o.scripts=[...document.scripts].map(s=>s.src||'inline');
 o.skip=(document.querySelector('.skip')||{}).outerHTML; o.mainid=!!document.querySelector('main#contenu');
 o.text=document.body.innerText.length;
 return o;}"""
async def main():
    out={}
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={'width':1440,'height':900},reduced_motion='reduce'); pg=await ctx.new_page()
        for n in pages:
            await pg.goto('http://localhost:8765/%s.html'%n); await pg.wait_for_timeout(300)
            out[n]=await pg.evaluate(JS)
        await b.close()
    json.dump(out,open('probe.json','w'),ensure_ascii=False,indent=1)
asyncio.run(main())
