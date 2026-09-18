import sys, json, urllib.request, urllib.parse, time
def s(t, rows=3):
    u="https://api.crossref.org/works?rows=%d&query.bibliographic=%s"%(rows,urllib.parse.quote(t))
    try:
        d=json.load(urllib.request.urlopen(u,timeout=40))['message']['items']
    except Exception as e:
        print("ERR",t,e); return
    print("### QUERY:",t)
    for d in d:
        au=d.get('author',[])
        print("  DOI  :",d.get('DOI'))
        print("  TITLE:",(d.get('title') or ['?'])[0][:150])
        print("  AUTH :",'; '.join((a.get('given','')+' '+a.get('family','')).strip() for a in au)[:200])
        print("  VENUE:",(d.get('container-title') or ['?'])[0][:90],"| vol",d.get('volume'),"| iss",d.get('issue'),"| pp",d.get('page'),"| art",d.get('article-number'))
        for k in ('published-print','published-online','issued'):
            if k in d: print("  DATE :",k,d[k]['date-parts'][0]); break
        print("  TYPE :",d.get('type'),"|",d.get('publisher'))
        print("  ---")
    print("="*74)
for t in sys.argv[1:]:
    s(t); time.sleep(3)
