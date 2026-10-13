#!/usr/bin/env python3
"""Eritrea: the Constitution of Eritrea (ratified 23 May 1997) from WIPO Lex (no official online
source exists), and the two legal texts published in full by the Ministry of Information (shabait.com).

Usage: python3 er_fetch.py [--no-download]"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import er_text as T  # noqa

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(os.path.dirname(REPO), "_raw", "er")
RETRIEVED = os.environ.get("LC_RETRIEVED", "2026-10-13")
WIPO = "https://www.wipo.int/wipolex/en/text/215187"
SHABAIT = {32432: ("act", "proclamations", "Proclamation No. 180/2017"), 27758: ("regulation", "legal-notices", "Legal Notice No. 124/2015")}
DL = "--no-download" not in sys.argv


def lines_of(h):
    h = re.sub(r"(?is)<(script|style).*?</\1>", "", h)
    h = re.sub(r"(?i)<br\s*/?>", "\n", h)
    h = re.sub(r"(?i)</(p|div|li|h\d|tr|dd|dt)>", "\n\n", h)
    t = html.unescape(re.sub(r"<[^>]+>", "", h))
    return [re.sub(r"[ \t\xa0]+", " ", x).strip() for x in t.replace("\r", "").split("\n")]


def constitution():
    p = os.path.join(RAW, "wipolex-215187.html")
    if DL:
        T.fetch(WIPO, p, delay=3)
    t = open(p, encoding="utf-8", errors="replace").read()
    i = t.find("Ratified by the Constituent Assembly")
    seg = t[t.rfind("<p", 0, i):]
    seg = seg[:seg.find("</body>")] if "</body>" in seg else seg
    raw = [x for x in lines_of(seg)]
    lines = []
    pend = None
    for x in raw:
        if re.match(r"^\d{1,2}\.?$", x):
            pend = x.rstrip(".")
            continue
        if pend and x:
            lines.append(pend + ". " + x)
            pend = None
            continue
        lines.append(x)
    out = []
    lvl = {"CHAPTER": "##", "ART": "###"}
    for x in lines:
        if not x:
            out.append("")
            continue
        if re.match(r"^CHAPTER [IVXL]+\b", x):
            out += [lvl["CHAPTER"] + " " + x, ""]
        elif re.match(r"^Article \d+\s*[-–]", x) and len(x) < 120:
            out += [lvl["ART"] + " " + x, ""]
        elif x == "PREAMBLE":
            out += ["## PREAMBLE", ""]
        else:
            out += [re.sub(r"^(\d+)\.(\s)", r"\1\\.\2", x), ""]
    body = []
    for x in out:
        if x == "" and body and body[-1] == "":
            continue
        body.append(x)
    meta = {"title": "The Constitution of Eritrea", "identifier": "Constitution of Eritrea (1997)", "type": "constitution",
            "jurisdiction": "er", "language": "en", "date": "1997-05-23", "status": "unknown", "source": WIPO,
            "retrieved": RETRIEVED,
            "note": "Ratified by the Constituent Assembly on 23 May 1997; it has not been implemented. Text from WIPO Lex (non-official mirror)."}
    T.write_md(os.path.join(REPO, "constitution", "constitution-1997.md"), meta, meta["title"], body)


def shabait():
    for pid, (typ, d, ident) in SHABAIT.items():
        p = os.path.join(RAW, "shabait-%d.json" % pid)
        if DL:
            T.fetch("https://shabait.com/wp-json/wp/v2/posts/%d" % pid, p, delay=3)
        x = json.load(open(p))
        lines = lines_of(x["content"]["rendered"])
        body = ["## " + x if re.match(r"^(ARTICLE|Article) \d+\b", x) and len(x) < 150 else x
                for x in T.structure(lines, "en", art_word="Article")]
        title = html.unescape(x["title"]["rendered"]).strip()
        m = re.search(r"/((?:19|20)\d\d)\b", ident)
        meta = {"title": title, "identifier": ident, "type": typ, "jurisdiction": "er", "language": "en",
                "year": int(m.group(1)), "status": "unknown", "source": x["link"], "retrieved": RETRIEVED,
                "note": "Text as published by the Ministry of Information (shabait.com), not the Gazette of Eritrean Laws."}
        T.write_md(os.path.join(REPO, d, m.group(1), T.slug(ident) + ".md"), meta, title, body)


if __name__ == "__main__":
    os.makedirs(RAW, exist_ok=True)
    constitution()
    shabait()
