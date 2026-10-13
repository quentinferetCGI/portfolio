import asyncio, json
from playwright.async_api import async_playwright
pages=['index','apropos','cas01-resume','cas01','cas01-realisations','cas01-produits','cas02-resume','cas02','cas02-realisations','cas03-resume','cas03','cas03-realisations','accessibilite','plan-du-site']
AXE=open('node_modules/axe-core/axe.min.js').read()
async def main():
    res={}
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for w,h,tag in ((1440,900,'d'),(390,800,'m')):
            ctx=await b.new_context(viewport={'width':w,'height':h},reduced_motion='reduce')
            pg=await ctx.new_page()
            for n in pages:
                await pg.goto('http://localhost:8765/%s.html'%n); await pg.wait_for_timeout(500)
                await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
                await pg.add_script_tag(content=AXE)
                r=await pg.evaluate("""async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice']},resultTypes:['violations','incomplete']})""")
                res[n+'-'+tag]={'v':[{'id':v['id'],'impact':v['impact'],'help':v['help'],'n':len(v['nodes']),'ex':[(x['target'],x['html'][:140],(x.get('any') or x.get('all') or x.get('none') or [{}])[0].get('message','')) for x in v['nodes'][:3]]} for v in r['violations']],
                                'inc':[{'id':v['id'],'n':len(v['nodes']),'ex':[x['target'] for x in v['nodes'][:2]]} for v in r['incomplete']]}
        await b.close()
    json.dump(res,open('axe.json','w'),ensure_ascii=False,indent=1)
    agg={}
    for k,v in res.items():
        for x in v['v']: agg.setdefault(x['id'],[x['impact'],x['help'],0,set()]); agg[x['id']][2]+=x['n']; agg[x['id']][3].add(k)
    for i,(imp,h,n,ks) in sorted(agg.items(),key=lambda a:-a[1][2]): print(i,imp,n,len(ks),'pages |',h)
    print('--- incomplete')
    inc={}
    for k,v in res.items():
        for x in v['inc']: inc.setdefault(x['id'],0); inc[x['id']]+=x['n']
    print(inc)
asyncio.run(main())
