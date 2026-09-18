import re, html, urllib.request
for u in ["https://arxiv.org/abs/2506.00062","https://arxiv.org/abs/2412.15891","https://arxiv.org/abs/2608.26126","https://arxiv.org/abs/2501.00790"]:
    print("===", u)
    try:
        req=urllib.request.Request(u, headers={"User-Agent":"Mozilla/5.0"})
        t=urllib.request.urlopen(req, timeout=45).read().decode("utf-8","ignore")
    except Exception as e:
        print("ERR", e); continue
    for pat,name in [(r'<h1 class="title[^>]*>(.*?)</h1>','TITLE'),(r'<div class="authors">(.*?)</div>','AUTHORS'),(r'<blockquote class="abstract[^>]*>(.*?)</blockquote>','ABSTRACT')]:
        m=re.search(pat,t,re.S)
        v=html.unescape(re.sub(r"<[^>]+>","",m.group(1))).strip() if m else "n/a"
        print(name+":", v[:1100])
    m=re.search(r'Comments:</td>\s*<td[^>]*>(.*?)</td>', t, re.S)
    print("COMMENTS:", html.unescape(re.sub(r"<[^>]+>","",m.group(1))).strip()[:200] if m else "n/a")
    print()
