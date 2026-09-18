#!/bin/bash
while IFS= read -r d; do
  [ -z "$d" ] && continue
  echo "=== DOI: $d"
  curl -s --max-time 35 -H "User-Agent: survey-bot/1.0 (mailto:research@example.org)" \
    "https://api.crossref.org/works/$d" | python3 -c '
import sys,json
try: d=json.load(sys.stdin)["message"]
except Exception as e:
    print("  FAILED:",e); sys.exit()
au=d.get("author",[])
names=", ".join((a.get("given","")+" "+a.get("family","")).strip() for a in au[:10])
ct=(d.get("container-title") or [""])[0]
print("  TITLE:",(d.get("title") or [""])[0])
print("  AUTHORS:",names)
print("  YEAR:",d.get("issued",{}).get("date-parts"))
print("  VENUE:",ct)
print("  EVENT:",(d.get("event") or {}).get("name",""))
print("  TYPE:",d.get("type"),"| PAGES:",d.get("page"),"| VOL:",d.get("volume"))
'
  sleep 2
done
