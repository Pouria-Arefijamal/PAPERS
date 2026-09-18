#!/usr/bin/env python3
"""Curated master paper database for the PhD literature review.

Provenance rules used throughout:
  * Bibliographic fields (title, authors, year, venue, doi, peer_reviewed) come from
    Crossref/OpenAlex verification performed in this session (data/seed_verified.json,
    data/crossref_meta.json) or from subagent reports that state the Crossref record.
  * Technical fields are populated from (i) the Crossref abstract where retrieved,
    (ii) open-access full text located in this session, or (iii) the paper's own
    well-known published description. Where a field could not be verified from a
    retrievable source the exact string "NA" is used and `evidence` records the level.
  * evidence levels:  BIB = bibliographic only; ABS = abstract read;
    FULL = open-access full text read; SUB = subagent report with stated source URL.
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "master.json")

# ---------------------------------------------------------------------------
# helper
# ---------------------------------------------------------------------------

def P(**kw):
    base = dict(
        paper_id=None, title=None, authors=None, year=None, venue=None, doi=None,
        peer_reviewed=None, arxiv=None, github=None, source_url=None, evidence="BIB",
        area=None, subcategory=None, calls=None,   # calls = which CSV files it goes into
    )
    base.update(kw)
    return base


PAPERS = []
A = PAPERS.append
