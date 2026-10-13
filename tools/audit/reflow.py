import asyncio
from playwright.async_api import async_playwright
pages=['index','apropos','cas01-resume','cas01','cas01-realisations','cas01-produits','cas02-resume','cas02','cas02-realisations','cas03-resume','cas03','cas03-realisations','accessibilite','plan-du-site']
SP="*{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important}p{margin-bottom:2em!important}"
CLIP=r"""()=>{const o=[];document.querySelectorAll('body *').forEach(e=>{const cs=getComputedStyle(e);if((cs.overflow!=='visible'||cs.overflowY!=='visible')&&e.scrollHeight>e.clientHeight+2&&e.clientHeight>0&&!['HTML','BODY'].includes(e.tagName)&&!(cs.overflowX==='auto'&&cs.overflowY==='visible'))o.push(e.tagName+'.'+e.className+' '+e.scrollHeight+'>'+e.clientHeight)});return o.slice(0,5)}"""
OVF=r"""()=>{const w=document.documentElement.clientWidth;const o=[];document.querySelectorAll('body *').forEach(e=>{const r=e.getBoundingClientRect();if(r.width>0&&r.right>w+1&&!e.closest('.snav ul'))o.push(e.tagName+'.'+e.className+' '+Math.round(r.right))});return [document.documentElement.scrollWidth,w,o.slice(0,4)]}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for w,lab in ((640,'200%'),(320,'400%')):
            ctx=await b.new_context(viewport={'width':w,'height':800},reduced_motion='reduce'); pg=await ctx.new_page(); await pg.route('**/cloud.umami.is/**',lambda r:r.abort())
            for n in pages:
                await pg.goto('http://localhost:8765/%s.html'%n); await pg.wait_for_timeout(250)
                a=await pg.evaluate(OVF)
                await pg.add_style_tag(content=SP); await pg.wait_for_timeout(150)
                c=await pg.evaluate(CLIP); a2=await pg.evaluate(OVF)
                print(lab,n,'scrollW',a[0],'/',a[1],a[2],'| spacing:',a2[0],a2[2][:2],'clip',c[:3])
            await ctx.close()
        await b.close()
asyncio.run(main())
