import sys, json
raw = sys.stdin.read()
try:
    d = json.loads(raw)
except Exception as e:
    print("  PARSE-ERROR", e); sys.exit()
for it in d["message"]["items"]:
    au = it.get("author", [])
    names = ", ".join((a.get("given", "") + " " + a.get("family", "")).strip() for a in au[:10])
    ct = it.get("container-title", [""]) or [""]
    sc = it.get("short-container-title", [""]) or [""]
    yr = it.get("issued", {}).get("date-parts", [[None]])[0]
    ev = (it.get("event") or {}).get("name", "")
    print("  DOI:", it.get("DOI"))
    print("  TITLE:", (it.get("title") or [""])[0])
    print("  AUTHORS:", names)
    print("  YEAR:", yr)
    print("  VENUE:", ct[0], "| short:", sc[0], "| event:", ev)
    print("  TYPE:", it.get("type"), "| PUB:", it.get("publisher"))
    print("  ---")
