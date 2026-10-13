import asyncio, json
from playwright.async_api import async_playwright
pages=['index','apropos','cas01-resume','cas01','cas01-realisations','cas01-produits','cas02-resume','cas02','cas02-realisations','cas03-resume','cas03','cas03-realisations','accessibilite','plan-du-site']
JS=r"""()=>{
 function parse(c){const q=c.match(/color\(srgb ([^)]+)\)/);if(q){const p=q[1].split(/[ \/]+/).filter(Boolean).map(Number);return[p[0]*255,p[1]*255,p[2]*255,p.length>3?p[3]:1]}const m=c.match(/rgba?\(([^)]+)\)/);if(!m)return[0,0,0,0];const p=m[1].split(/[ ,\/]+/).filter(Boolean).map(Number);return[p[0],p[1],p[2],p.length>3?p[3]:1]}
 function over(f,b){const a=f[3];return[f[0]*a+b[0]*(1-a),f[1]*a+b[1]*(1-a),f[2]*a+b[2]*(1-a),1]}
 function lum(c){const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(c[0])+.7152*f(c[1])+.0722*f(c[2])}
 function ratio(a,b){const l1=lum(a),l2=lum(b);return (Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05)}
 function bgOf(e){let layers=[];let img=false;for(let x=e;x;x=x.parentElement){const cs=getComputedStyle(x);if(cs.backgroundImage&&cs.backgroundImage!=='none')img=true;const c=parse(cs.backgroundColor);if(c[3]>0){layers.push(c);if(c[3]===1)break}}
  let base=[255,255,255,1];for(let i=layers.length-1;i>=0;i--)base=over(layers[i],base);return {c:base,img}}
 const out=[];const seen=new Set();
 document.querySelectorAll('body *').forEach(e=>{
  if(!([...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())))return;
  const cs=getComputedStyle(e);if(cs.visibility==='hidden'||cs.display==='none')return;const r=e.getBoundingClientRect();if(r.width===0)return;
  if(e.closest('[aria-hidden=true]'))return;
  let op=1;for(let x=e;x;x=x.parentElement){op*=parseFloat(getComputedStyle(x).opacity)}
  const bg=bgOf(e);let fg=parse(cs.color);fg=over([fg[0],fg[1],fg[2],fg[3]*op],bg.c);
  const ratioV=ratio(fg,bg.c);const fs=parseFloat(cs.fontSize),bold=parseInt(cs.fontWeight)>=700;const large=fs>=24||(fs>=18.66&&bold);
  const need=large?3:4.5;
  if(ratioV<need){const key=cs.color+'|'+bg.c.map(Math.round)+'|'+fs;if(seen.has(key))return;seen.add(key);
   out.push({txt:e.textContent.trim().replace(/\s+/g,' ').slice(0,40),cls:e.tagName+'.'+e.className,color:cs.color,bg:bg.c.map(Math.round).join(','),fs,ratio:+ratioV.toFixed(2),need,img:bg.img})}
 });
 return out}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={'width':1440,'height':900},reduced_motion='reduce'); pg=await ctx.new_page()
        allr={}
        for n in pages:
            await pg.goto('http://localhost:8765/%s.html'%n); await pg.wait_for_timeout(300)
            await pg.add_style_tag(content='.reveal{opacity:1!important;transform:none!important}')
            allr[n]=await pg.evaluate(JS)
            print('==',n,len(allr[n]))
            for x in allr[n]: print('  ',x['ratio'],'/',x['need'],x['fs'],x['color'],'on',x['bg'],'img' if x['img'] else '','|',x['cls'][:28],'|',x['txt'])
        await b.close()
asyncio.run(main())
