#!/usr/bin/env python3
"""Fetch metadata + abstract for a list of DOIs via Crossref (fast, high rate limit)."""
import json
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from litlib import crossref_doi


def one(doi):
    r = crossref_doi(doi)
    if "__error__" in r:
        return doi, {"__error__": r["__error__"]}
    m = r.get("message", {})
    auths = []
    for a in (m.get("author") or [])[:20]:
        nm = " ".join(x for x in [a.get("given"), a.get("family")] if x).strip()
        if nm:
            auths.append(nm)
    yr = None
    dp = (m.get("issued") or {}).get("date-parts") or [[None]]
    if dp and dp[0]:
        yr = dp[0][0]
    return doi, {
        "title": (m.get("title") or [None])[0],
        "authors": auths,
        "year": yr,
        "venue": (m.get("container-title") or [None])[0],
        "short_venue": (m.get("short-container-title") or [None])[0],
        "type": m.get("type"),
        "publisher": m.get("publisher"),
        "event": ((m.get("event") or {}).get("name")),
        "volume": m.get("volume"),
        "issue": m.get("issue"),
        "page": m.get("page"),
        "abstract": m.get("abstract"),
        "references_count": m.get("reference-count"),
        "is_referenced_by_count": m.get("is-referenced-by-count"),
        "url": m.get("URL"),
        "license": [l.get("URL") for l in (m.get("license") or [])][:3],
        "subject": m.get("subject"),
    }


if __name__ == "__main__":
    dois = json.load(open(sys.argv[1]))
    seen = set()
    uniq = []
    for d in dois:
        if d and d.lower() not in seen:
            seen.add(d.lower())
            uniq.append(d)
    out = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(one, d) for d in uniq]
        n = 0
        for f in as_completed(futs):
            doi, meta = f.result()
            out[doi] = meta
            n += 1
            if n % 20 == 0:
                print("fetched %d/%d" % (n, len(uniq)), flush=True)
    json.dump(out, open(sys.argv[2], "w"), indent=1)
    print("WROTE", sys.argv[2], "with", len(out), "records;",
          sum(1 for v in out.values() if v.get("abstract")), "have abstracts")
