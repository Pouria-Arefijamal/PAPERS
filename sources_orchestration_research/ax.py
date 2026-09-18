import sys, urllib.parse, urllib.request, xml.etree.ElementTree as ET
ns={'a':'http://www.w3.org/2005/Atom'}
def q(term, n=4):
    url="https://export.arxiv.org/api/query?search_query="+urllib.parse.quote(term)+f"&max_results={n}"
    try:
        d=urllib.request.urlopen(url, timeout=30).read()
    except Exception as e:
        print("ERR",e); return
    r=ET.fromstring(d)
    for e in r.findall('a:entry',ns):
        print("ID   :", e.find('a:id',ns).text)
        print("TITLE:", ' '.join(e.find('a:title',ns).text.split()))
        print("DATE :", e.find('a:published',ns).text[:10], "| UPD:", e.find('a:updated',ns).text[:10])
        print("AUTH :", ', '.join(a.find('a:name',ns).text for a in e.findall('a:author',ns))[:220])
        c=e.find('a:comment',ns); j=e.find('a:journal_ref',ns); doi=e.find('a:doi',ns)
        if c is not None: print("CMT  :", ' '.join(c.text.split())[:200])
        if j is not None: print("JREF :", ' '.join(j.text.split())[:200])
        if doi is not None: print("DOI  :", doi.text)
        print("-"*70)
for t in sys.argv[1:]:
    print("="*70); print("QUERY:",t); q(t)
