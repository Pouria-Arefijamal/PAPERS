import sys, json, urllib.request, urllib.parse
def cr(doi):
    try:
        d=json.load(urllib.request.urlopen("https://api.crossref.org/works/"+urllib.parse.quote(doi), timeout=30))['message']
    except Exception as e:
        print("ERR",doi,e); return
    print("DOI   :", d.get('DOI'))
    print("TITLE :", (d.get('title') or ['?'])[0])
    au=d.get('author',[])
    print("AUTH  :", '; '.join((a.get('given','')+' '+a.get('family','')).strip() for a in au))
    ct=d.get('container-title') or ['?']
    print("VENUE :", ct[0], "| vol", d.get('volume'), "| iss", d.get('issue'), "| art", d.get('article-number'))
    print("PAGES :", d.get('page'))
    for k in ('published-print','published-online','issued','created'):
        if k in d: print(f"{k:16}:", d[k]['date-parts'][0]); break
    print("TYPE  :", d.get('type'), "| publisher:", d.get('publisher'))
    print("-"*72)
for x in sys.argv[1:]: cr(x)
