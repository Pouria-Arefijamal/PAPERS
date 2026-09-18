import re, html, sys, urllib.request
for u in ["https://arxiv.org/abs/2608.21874","https://arxiv.org/abs/2603.03667"]:
    print("===", u)
    try:
        req=urllib.request.Request(u, headers={"User-Agent":"Mozilla/5.0"})
        t=urllib.request.urlopen(req, timeout=45).read().decode("utf-8","ignore")
    except Exception as e:
        print("ERR", e); continue
    m=re.search(r'<blockquote class="abstract[^>]*>(.*?)</blockquote>', t, re.S)
    print("ABSTRACT:", html.unescape(re.sub(r"<[^>]+>","",m.group(1))).strip()[:1400] if m else "n/a")
    m=re.search(r'<h1 class="title[^>]*>(.*?)</h1>', t, re.S)
    print("TITLE:", html.unescape(re.sub(r"<[^>]+>","",m.group(1))).strip() if m else "n/a")
    m=re.search(r'<div class="authors">(.*?)</div>', t, re.S)
    print("AUTHORS:", html.unescape(re.sub(r"<[^>]+>","",m.group(1))).strip()[:300] if m else "n/a")
    m=re.search(r'Comments:</td>\s*<td[^>]*>(.*?)</td>', t, re.S)
    print("COMMENTS:", html.unescape(re.sub(r"<[^>]+>","",m.group(1))).strip()[:300] if m else "n/a")
    print()
