#!/usr/bin/env python3
"""Small helper library for bibliographic verification via OpenAlex + Crossref.

No API keys required. Rate limited politely.
"""
import json
import threading
import time
import urllib.parse
import urllib.request

_LOCK = threading.Lock()

MAILTO = "phd.litreview@example.org"
UA = "Mozilla/5.0 (compatible; litreview/1.0; mailto:%s)" % MAILTO

_last = [0.0]


def _get(url, min_interval=1.0, retries=3):
    for attempt in range(retries):
        with _LOCK:
            dt = time.time() - _last[0]
            if dt < min_interval:
                time.sleep(min_interval - dt)
            _last[0] = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except Exception as e:
            if attempt == retries - 1:
                return {"__error__": str(e)}
            time.sleep(2.0 * (attempt + 1))
    return {"__error__": "unknown"}


def openalex_search(query, per_page=10, extra=""):
    url = ("https://api.openalex.org/works?search=%s&per-page=%d&mailto=%s%s"
           % (urllib.parse.quote(query), per_page, MAILTO, extra))
    return _get(url)


def openalex_title(title, per_page=5):
    url = ("https://api.openalex.org/works?filter=title.search:%s&per-page=%d&mailto=%s"
           % (urllib.parse.quote(title), per_page, MAILTO))
    return _get(url)


def crossref_title(title, rows=3):
    url = ("https://api.crossref.org/works?query.bibliographic=%s&rows=%d"
           "&select=title,author,issued,container-title,DOI,type,publisher,event,page,volume,issue"
           % (urllib.parse.quote(title), rows))
    return _get(url, min_interval=1.0)


def crossref_doi(doi):
    url = "https://api.crossref.org/works/%s" % urllib.parse.quote(doi)
    return _get(url, min_interval=1.0)


def norm_alex(w):
    """Flatten an OpenAlex work into a compact dict."""
    src = None
    pl = w.get("primary_location") or {}
    if pl.get("source"):
        src = pl["source"].get("display_name")
    auths = []
    for a in (w.get("authorships") or [])[:12]:
        n = (a.get("author") or {}).get("display_name")
        if n:
            auths.append(n)
    return {
        "title": w.get("display_name"),
        "year": w.get("publication_year"),
        "venue": src,
        "type": w.get("type"),
        "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
        "cited_by": w.get("cited_by_count"),
        "authors": auths,
        "is_oa": (w.get("open_access") or {}).get("is_oa"),
        "oa_url": (w.get("best_oa_location") or {}).get("pdf_url") if w.get("best_oa_location") else None,
        "ids": w.get("ids"),
    }


def alex_rows(resp):
    if "__error__" in resp:
        return []
    return [norm_alex(w) for w in resp.get("results", [])]


def crossref_rows(resp):
    if "__error__" in resp:
        return []
    out = []
    for it in resp.get("message", {}).get("items", []):
        auths = []
        for a in (it.get("author") or [])[:12]:
            nm = " ".join(x for x in [a.get("given"), a.get("family")] if x).strip()
            if nm:
                auths.append(nm)
        yr = None
        dp = (it.get("issued") or {}).get("date-parts") or [[None]]
        if dp and dp[0]:
            yr = dp[0][0]
        out.append({
            "title": (it.get("title") or [None])[0],
            "year": yr,
            "venue": (it.get("container-title") or [None])[0],
            "doi": it.get("DOI"),
            "type": it.get("type"),
            "publisher": it.get("publisher"),
            "authors": auths,
            "event": ((it.get("event") or {}).get("name")),
        })
    return out


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) or "LLM network management"
    print(json.dumps(alex_rows(openalex_search(q, 5)), indent=1)[:4000])
