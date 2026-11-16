#!/usr/bin/env python3
"""Draw the annotated copies of the photos.

Reads photos/labels.json and writes photos/<name>-annotated.jpg for each photo listed there:
the original with a numbered box round each labelled chip, and a legend underneath.

    python3 tools/annotate.py

Needs Pillow. The originals are never changed.
"""

import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTOS = os.path.join(ROOT, "photos")

KNOWN = (255, 214, 0)       # yellow: identified
UNKNOWN = (255, 128, 0)     # orange: marking read, part not identified
INK = (20, 20, 20)
PAPER = (245, 245, 245)
BAND = (24, 24, 24)

FONTS = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def font(size):
    for path in FONTS:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    sys.exit("annotate.py: no TrueType font found; add one to FONTS")


def annotate(name, spec):
    src = os.path.join(PHOTOS, name)
    im = Image.open(src).convert("RGB")
    w, h = im.size
    unit = w / 4000.0                      # sizes below are for a 4000-pixel-wide photo
    line = max(3, round(5 * unit))
    tag_font = font(round(44 * unit))
    text_font = font(round(40 * unit))
    title_font = font(round(48 * unit))
    pad = round(10 * unit)

    labels = spec["labels"]

    # Legend: a title, then the labels in two columns.
    row_h = round(62 * unit)
    margin = round(40 * unit)
    half = (len(labels) + 1) // 2
    band_h = margin + round(70 * unit) + half * row_h + margin
    out = Image.new("RGB", (w, h + band_h), BAND)
    out.paste(im, (0, 0))
    d = ImageDraw.Draw(out)

    for n, label in enumerate(labels, 1):
        colour = KNOWN if label.get("known", True) else UNKNOWN
        x0, y0, x1, y1 = label["box"]
        x0, y0, x1, y1 = x0 - pad, y0 - pad, x1 + pad, y1 + pad
        d.rectangle((x0, y0, x1, y1), outline=INK, width=line + 4)
        d.rectangle((x0 + 2, y0 + 2, x1 - 2, y1 - 2), outline=colour, width=line)

        # Number tag: on the box's top-left corner, moved inside the photo if it would leave it.
        tag = str(n)
        tw = d.textlength(tag, font=tag_font)
        th = round(50 * unit)
        if x1 - x0 > 300 * unit:           # a big chip: put the tag inside its corner
            tx0, ty0 = x0 + line, y0 + line
        else:
            tx0 = max(0, min(x0, w - tw - 2 * pad))
            ty0 = y0 - th - pad if y0 - th - pad >= 0 else y1
        d.rectangle((tx0, ty0, tx0 + tw + 2 * pad, ty0 + th + pad), fill=colour, outline=INK, width=2)
        d.text((tx0 + pad, ty0 + pad // 2), tag, font=tag_font, fill=INK)

    d.text((margin, h + margin // 2), spec["title"], font=title_font, fill=PAPER)
    top = h + margin + round(70 * unit)
    col_w = (w - 2 * margin) // 2
    for n, label in enumerate(labels, 1):
        colour = KNOWN if label.get("known", True) else UNKNOWN
        col, row = divmod(n - 1, half)
        x = margin + col * col_w
        y = top + row * row_h
        tag = str(n)
        tw = d.textlength("00", font=tag_font)
        d.rectangle((x, y, x + tw + 2 * pad, y + round(52 * unit)), fill=colour)
        d.text((x + pad, y + pad // 3), tag, font=tag_font, fill=INK)
        d.text((x + tw + 4 * pad, y + pad // 2), label["text"], font=text_font, fill=PAPER)

    dst = os.path.join(PHOTOS, os.path.splitext(name)[0] + "-annotated.jpg")
    out.save(dst, quality=90)
    print(os.path.relpath(dst, ROOT), out.size)


def main():
    with open(os.path.join(PHOTOS, "labels.json")) as f:
        specs = json.load(f)
    for name, spec in specs.items():
        if not name.startswith("_"):
            annotate(name, spec)


if __name__ == "__main__":
    main()
