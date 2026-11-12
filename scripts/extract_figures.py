#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Crop journal figures from a PDF by Fig. N. caption anchors.

Usage:
  python extract_figures.py <input.pdf> <outdir> [--zoom 2.4] [--manual-json clips.json]

Notes:
- Handles typical Elsevier-style two-column pages (left/right/full bands).
- Always inspect a few PNGs afterward; multi-panel figures may need manual clips.
- Avoid clipping body text above the figure (tighten top toward drawings bbox).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

import fitz  # PyMuPDF


def find_caption_anchors(doc):
    """Return {fig_num: (page_index, caption_rect)} for first 'Fig. N.' hit."""
    found = {}
    for pno in range(len(doc)):
        page = doc[pno]
        for n in range(1, 80):
            for inst in page.search_for(f"Fig. {n}."):
                if n not in found or pno < found[n][0]:
                    found[n] = (pno, inst)
    return found


def content_bbox(page, x0, y0, x1, y1):
    bb = None
    for d in page.get_drawings():
        r = fitz.Rect(d["rect"])
        if r.x1 < x0 or r.x0 > x1 or r.y1 <= y0 or r.y0 >= y1:
            continue
        if r.width < 1.5 and r.height < 1.5:
            continue
        r = fitz.Rect(max(r.x0, x0), max(r.y0, y0), min(r.x1, x1), min(r.y1, y1))
        if r.is_empty:
            continue
        bb = r if bb is None else (bb | r)
    for im in page.get_image_info():
        r = fitz.Rect(im["bbox"])
        if r.x1 < x0 or r.x0 > x1 or r.y1 <= y0 or r.y0 >= y1:
            continue
        r = fitz.Rect(max(r.x0, x0), max(r.y0, y0), min(r.x1, x1), min(r.y1, y1))
        if r.is_empty:
            continue
        bb = r if bb is None else (bb | r)
    return bb


def guess_clip(page, cap, pad=1.0):
    left = (35.0, 295.0)
    right = (298.0, 560.0)
    full = (35.0, 560.0)
    if cap.x0 > 300:
        x0, x1 = right
        band = "R"
    elif cap.x1 < 300:
        x0, x1 = left
        band = "L"
    else:
        x0, x1 = full
        band = "F"

    bb = content_bbox(page, x0, 50.0, x1, cap.y0 - 2)
    bb_full = content_bbox(page, full[0], 50.0, full[1], cap.y0 - 2)
    if bb_full and (bb is None or bb_full.get_area() > bb.get_area() * 1.8):
        bb = bb_full
        band = "F"
    if bb is None or bb.height < 25:
        bb = content_bbox(page, x0, cap.y1 + 2, x1, 780.0)
    if bb is None or bb.height < 20:
        bb = fitz.Rect(x0, 55.0, x1, cap.y0 - 2)

    clip = fitz.Rect(bb.x0 - pad, bb.y0 - pad, bb.x1 + pad, bb.y1 + pad) & page.rect
    return clip, band


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("outdir")
    ap.add_argument("--zoom", type=float, default=2.4)
    ap.add_argument("--manual-json", default=None, help='{"1": [x0,y0,x1,y1], ...} in PDF pts')
    args = ap.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")
    os.makedirs(args.outdir, exist_ok=True)
    manual = json.load(open(args.manual_json, encoding="utf-8")) if args.manual_json else {}

    doc = fitz.open(args.pdf)
    anchors = find_caption_anchors(doc)
    if not anchors:
        print("No 'Fig. N.' captions found", file=sys.stderr)
        sys.exit(2)

    for n in sorted(anchors):
        pno, cap = anchors[n]
        page = doc[pno]
        if str(n) in manual:
            clip = fitz.Rect(*manual[str(n)]) & page.rect
            tag = "manual"
        else:
            clip, tag = guess_clip(page, cap)
        pix = page.get_pixmap(matrix=fitz.Matrix(args.zoom, args.zoom), clip=clip, alpha=False)
        out = os.path.join(args.outdir, f"fig{n:02d}.png")
        pix.save(out)
        print(f"fig{n:02d} p{pno+1} {tag} clip=({clip.x0:.0f},{clip.y0:.0f},{clip.x1:.0f},{clip.y1:.0f}) {pix.width}x{pix.height}")
    doc.close()
    print("done:", len(anchors), "figures ->", args.outdir)


if __name__ == "__main__":
    main()
