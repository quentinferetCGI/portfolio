import asyncio
from playwright.async_api import async_playwright
pages=['cas01','cas02','cas03','cas01-realisations','index']
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for w,h in ((1440,900),(390,800)):
            ctx=await b.new_context(viewport={'width':w,'height':h}); pg=await ctx.new_page()
            for n in pages:
                await pg.goto('http://localhost:8765/%s.html'%n); await pg.wait_for_timeout(300)
                total=await pg.evaluate("document.querySelectorAll('a[href]').length")
                bad=[]
                for i in range(total+2):
                    await pg.keyboard.press('Tab'); await pg.wait_for_timeout(450)
                    d=await pg.evaluate("""()=>{const e=document.activeElement;const r=e.getBoundingClientRect();
                     const out=[];for(const s of ['.site-header','.snav']){const x=document.querySelector(s);if(!x)continue;const q=x.getBoundingClientRect();const st=getComputedStyle(x).position;
                       if(st==='sticky'||st==='fixed'){ if(r.top<q.bottom-1&&r.bottom>q.top+1&&!x.contains(e)) out.push(s)}}
                     return {t:(e.textContent||'').trim().replace(/\\s+/g,' ').slice(0,28),top:Math.round(r.top),out,sy:Math.round(scrollY)}}""")
                    if d['out']: bad.append((d['t'],d['top'],d['out'],d['sy']))
                print(w,n,'obscured by sticky:',bad[:6])
            await ctx.close()
        await b.close()
asyncio.run(main())
