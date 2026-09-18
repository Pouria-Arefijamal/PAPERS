import sys, json, urllib.request, urllib.parse, time, re
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent":"survey-bot/1.0 (mailto:research@example.org)"})
    last=None
    for _ in range(4):
        try:
            return json.load(urllib.request.urlopen(req, timeout=45))
        except Exception as e:
            last=e; time.sleep(4)
    print("  [fetch failed]", last, file=sys.stderr)
    return None
seed = sys.argv[1].rstrip("/").split("/")[-1]
d = get(f"https://api.openalex.org/works/{seed}?select=id,doi,title,cited_by_count,publication_year")
if not d:
    print("SEED FETCH FAILED"); sys.exit(1)
print("SEED:", d.get("title"), "|", d.get("publication_year"), "| cited_by:", d.get("cited_by_count"))
cursor="*"; total=0; rows=[]
while True:
    u=("https://api.openalex.org/works?filter=cites:"+seed+
       "&per-page=200&cursor="+urllib.parse.quote(cursor)+
       "&select=id,doi,title,publication_year,primary_location,authorships,type")
    r=get(u)
    if not r: break
    for w in r["results"]:
        src=((w.get("primary_location") or {}).get("source") or {}).get("display_name")
        rows.append((w.get("publication_year"), w.get("title"), src, (w.get("doi") or "")))
    total+=len(r["results"])
    cursor=r["meta"].get("next_cursor")
    if not cursor or not r["results"]: break
    time.sleep(0.4)
print("TOTAL CITING WORKS:", total)
kw=re.compile(r"bench|evaluat|dataset|testbed|arena|metric|assess|leaderboard", re.I)
print("\n--- CITING WORKS WITH BENCH/EVAL-LIKE TITLES ---")
for y,t,s,doi in sorted(rows, key=lambda x:-(x[0] or 0)):
    if t and kw.search(t):
        print(f"{y} | {t} | {s} | {doi}")
