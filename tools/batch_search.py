#!/usr/bin/env python3
"""Run a batch of OpenAlex searches and dump results to JSON."""
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from litlib import openalex_search, alex_rows

QUERIES = json.load(open(sys.argv[1]))
OUT = sys.argv[2]
PER_PAGE = int(sys.argv[3]) if len(sys.argv) > 3 else 12


def run(q):
    r = openalex_search(q, per_page=PER_PAGE)
    return q, alex_rows(r)


rows = {}
with ThreadPoolExecutor(max_workers=4) as ex:
    for q, res in ex.map(run, QUERIES):
        rows[q] = res
        print("done: %-70s -> %d" % (q[:70], len(res)), flush=True)

json.dump(rows, open(OUT, "w"), indent=1)
print("WROTE", OUT)
