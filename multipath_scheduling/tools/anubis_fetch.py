#!/usr/bin/env python3
"""Fetch a URL through an Anubis proof-of-work challenge (HAL/DiVA/DBLP style)."""
import hashlib, json, re, sys, time
import requests

UA = "Mozilla/5.0 (X11; Linux x86_64) Chrome/120"


def solve(random_data: str, difficulty: int, threads: int = 4) -> tuple[str, int]:
    target = "0" * difficulty
    nonce = 0
    while True:
        h = hashlib.sha256((random_data + str(nonce)).encode()).hexdigest()
        if h.startswith(target):
            return h, nonce
        nonce += 1


def fetch(url: str, outfile: str | None = None, tries: int = 3):
    s = requests.Session()
    s.headers["User-Agent"] = UA
    for attempt in range(tries):
        r = s.get(url, timeout=60, allow_redirects=True)
        body = r.text if "text" in r.headers.get("content-type", "") or r.content[:5] == b"<!doc" else None
        if r.content[:5] == b"%PDF-":
            if outfile:
                open(outfile, "wb").write(r.content)
            return r
        m = re.search(r'id="anubis_challenge"[^>]*>(\{.*?\})</script>', r.text, re.S)
        if not m:
            m = re.search(r'<script[^>]*id="anubis_challenge"[^>]*>(.*?)</script>', r.text, re.S)
        if not m:
            print(f"no challenge found (status {r.status_code}); first 200 bytes: {r.content[:200]!r}")
            return r
        ch = json.loads(m.group(1))
        c, rules = ch["challenge"], ch["rules"]
        t0 = time.time()
        h, nonce = solve(c["randomData"], rules["difficulty"])
        dt = int((time.time() - t0) * 1000)
        print(f"solved difficulty={rules['difficulty']} nonce={nonce} in {dt}ms")
        p = {
            "id": c["id"],
            "response": h,
            "nonce": str(nonce),
            "redir": url,
            "elapsedTime": str(dt),
        }
        pr = s.get("https://hal.science/.within.website/x/cmd/anubis/api/pass-challenge",
                   params=p, timeout=60, allow_redirects=True)
        print("pass-challenge:", pr.status_code, pr.headers.get("content-type"))
        if pr.content[:5] == b"%PDF-":
            if outfile:
                open(outfile, "wb").write(pr.content)
            return pr
    return None


if __name__ == "__main__":
    url = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    r = fetch(url, out)
    if r is None:
        print("FAILED")
        sys.exit(1)
    if r.content[:5] == b"%PDF-":
        print("GOT PDF", len(r.content), "bytes ->", out)
    else:
        print("final status", r.status_code, "len", len(r.content))
        if out:
            open(out, "wb").write(r.content)
