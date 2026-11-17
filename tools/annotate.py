#!/usr/bin/env python3
"""Draw the annotated copies of the photos.

Reads photos/labels.json and writes photos/<name>-annotated.jpg for each photo listed there:
the original with a numbered box round each labelled chip, a circle round each listed test pad,
and a legend underneath.

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
PAD = (0, 229, 255)         # cyan: test pad
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


def overlaps(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def draw_pads(d, pads, radius, size, unit, pad_font):
    """Circle each test pad and write its id beside it, on whichever side is clear."""
    w, h = size
    line = max(2, round(4 * unit))
    gap = round(8 * unit)
    th = round(36 * unit)
    taken = [(x - radius, y - radius, x + radius, y + radius) for x, y in (p["at"] for p in pads)]
    for p in pads:
        x, y = p["at"]
        d.ellipse((x - radius, y - radius, x + radius, y + radius), outline=INK, width=line + 3)
        d.ellipse((x - radius, y - radius, x + radius, y + radius), outline=PAD, width=line)
    for p in pads:
        x, y = p["at"]
        tw = round(d.textlength(p["id"], font=pad_font)) + 2 * gap
        spots = [
            (x + radius + gap, y - th // 2),            # right
            (x - radius - gap - tw, y - th // 2),       # left
            (x - tw // 2, y - radius - gap - th),       # above
            (x - tw // 2, y + radius + gap),            # below
        ]
        boxes = [(sx, sy, sx + tw, sy + th) for sx, sy in spots]
        inside = [b for b in boxes if b[0] >= 0 and b[1] >= 0 and b[2] <= w and b[3] <= h]
        clear = [b for b in inside if not any(overlaps(b, t) for t in taken)]
        box = (clear or inside or boxes)[0]
        taken.append(box)
        d.rectangle(box, fill=INK)
        d.text((box[0] + gap, box[1] + round(2 * unit)), p["id"], font=pad_font, fill=PAD)


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
    pads = spec.get("pads", [])

    # Legend: a title, then the labels in two columns.
    row_h = round(62 * unit)
    margin = round(40 * unit)
    half = (len(labels) + 1) // 2
    band_h = margin + round(70 * unit) + (half + bool(pads)) * row_h + margin
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

    if pads:
        draw_pads(d, pads, spec.get("pad_radius", round(34 * unit)), (w, h), unit, font(round(30 * unit)))

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

    if pads:
        y = top + half * row_h
        r = round(22 * unit)
        d.ellipse((margin + pad, y + pad // 2, margin + pad + 2 * r, y + pad // 2 + 2 * r), outline=PAD, width=line)
        note = "%s to %s: test pads, not yet identified (boards/test-points.md)" % (pads[0]["id"], pads[-1]["id"])
        d.text((margin + d.textlength("00", font=tag_font) + 4 * pad, y + pad // 2), note, font=text_font, fill=PAPER)

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
