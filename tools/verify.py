#!/usr/bin/env python3
"""Verify paper candidates by title against OpenAlex (primary) and Crossref (fallback).

Input: JSON list of {key, title, hint (optional: expected venue/year)}
Output: JSON + human-readable table
"""
import json
import sys
import difflib
from concurrent.futures import ThreadPoolExecutor
from litlib import openalex_title, crossref_title, alex_rows, crossref_rows


def sim(a, b):
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()


def verify(cand):
    q = cand["title"]
    rows = alex_rows(openalex_title(q, 6))
    best, bs = None, 0.0
    for r in rows:
        s = sim(q, r.get("title"))
        if s > bs:
            best, bs = r, s
    src = "openalex"
    if bs < 0.82:
        crows = crossref_rows(crossref_title(q, 5))
        for r in crows:
            s = sim(q, r.get("title"))
            if s > bs:
                best, bs, src = r, s, "crossref"
    return {"cand": cand, "match": best, "score": round(bs, 3), "source": src,
            "alternatives": [r.get("title") for r in rows[:4]]}


if __name__ == "__main__":
    cands = json.load(open(sys.argv[1]))
    out = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        for res in ex.map(verify, cands):
            out.append(res)
    json.dump(out, open(sys.argv[2], "w"), indent=1)
    for r in out:
        m = r["match"] or {}
        flag = "OK " if r["score"] >= 0.88 else ("?? " if r["score"] >= 0.70 else "XX ")
        print("%s %.2f | %s" % (flag, r["score"], r["cand"]["title"][:78]))
        print("        -> %s" % (m.get("title") or "NOT FOUND")[:100])
        print("           %s | %s | %s | doi=%s | %s" % (
            m.get("year"), (m.get("venue") or "?")[:60], ",".join((m.get("authors") or [])[:3]),
            m.get("doi"), r["source"]))
        if flag == "XX ":
            print("           ALT: %s" % ("; ".join(x or "" for x in r["alternatives"])[:160]))
