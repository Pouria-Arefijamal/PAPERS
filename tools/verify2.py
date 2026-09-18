#!/usr/bin/env python3
"""Parallel title verification: OpenAlex primary, Crossref fallback. Streams output."""
import json
import sys
import difflib
import threading
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from litlib import openalex_title, crossref_title, alex_rows, crossref_rows


def sim(a, b):
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()


def verify(cand):
    q = cand["title"]
    best, bs, src = None, 0.0, "openalex"
    rows = alex_rows(openalex_title(q, 6))
    for r in rows:
        s = sim(q, r.get("title"))
        if s > bs:
            best, bs = r, s
    if bs < 0.82:
        for r in crossref_rows(crossref_title(q, 5)):
            s = sim(q, r.get("title"))
            if s > bs:
                best, bs, src = r, s, "crossref"
    return {"cand": cand, "match": best, "score": round(bs, 3), "source": src,
            "alts": [r.get("title") for r in rows[:3]]}


if __name__ == "__main__":
    cands = json.load(open(sys.argv[1]))
    out = [None] * len(cands)
    lock = threading.Lock()
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(verify, c): i for i, c in enumerate(cands)}
        for f in as_completed(futs):
            i = futs[f]
            try:
                res = f.result()
            except Exception as e:
                res = {"cand": cands[i], "match": None, "score": 0, "source": "error", "alts": [str(e)]}
            out[i] = res
            m = res["match"] or {}
            flag = "OK " if res["score"] >= 0.88 else ("?? " if res["score"] >= 0.70 else "XX ")
            with lock:
                print("%s %s %.2f | %s" % (cands[i].get("key", ""), flag, res["score"], cands[i]["title"][:70]), flush=True)
                print("      -> %s | %s | %s | %s | doi=%s" % (
                    (m.get("title") or "NOT FOUND")[:88], m.get("year"),
                    (m.get("venue") or "?")[:55], ",".join((m.get("authors") or [])[:3])[:60], m.get("doi")), flush=True)
                if flag == "XX ":
                    print("      ALT: %s" % (" ;; ".join(x or "" for x in res["alts"])[:150]), flush=True)
    json.dump(out, open(sys.argv[2], "w"), indent=1)
    print("WROTE", sys.argv[2])
