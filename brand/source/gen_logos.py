"""Winterloom logo generator.

Every Winterloom logo is VT323 glyph outlines plus the block cursor, laid on
VT323's own dot grid (1 dot = 40 font units = 1/25 em). Run:

    pip install fonttools brotli
    python3 gen_logos.py <VT323 font file> <out dir> [text ...]

With no text it writes the standard set. With text it writes one wordmark per
argument, so a product lockup is `python3 gen_logos.py font out "winterloom/oracle"`.
"""
import sys, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

DOT = 40            # one pixel row of VT323, in font units
ADV = 400           # every VT323 glyph advances 10 dots
CUR_W, CUR_LO, CUR_HI = 8 * DOT, -2 * DOT, 14 * DOT   # cursor: 8 x 16 dots, baseline - 2 dots to cap height
PAD = 2 * DOT       # tight bounding pad; clear space is set in the README, not baked in
INK = {"on-dark": {"ink": "#cfe8f2", "dim": "#6b8794", "ground": "#05080b"},
       "on-light": {"ink": "#0d1a20", "dim": "#4d626c", "ground": "#eef2f3"}}

def glyph_paths(font, text):
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    out, x = [], 0
    for ch in text:
        g = gs[cmap[ord(ch)]]
        pen = SVGPathPen(gs)
        g.draw(TransformPen(pen, (1, 0, 0, -1, x, 0)))   # flip y: font up, svg down
        out.append((ch, pen.getCommands()))
        x += ADV
    return out, x

def lockup(font, parts, cursor=True, tile=None, theme="on-dark"):
    """parts: list of (text, role) where role is 'ink' or 'dim'."""
    c = INK[theme]
    paths, x = [], 0
    for text, role in parts:
        gp, w = glyph_paths(font, text)
        for ch, d in gp:
            if d: paths.append(f'<path transform="translate({x} 0)" fill="{c[role]}" d="{d}"/>')
        x += w
    right = x
    if cursor:
        cx = x + DOT
        paths.append(f'<rect x="{cx}" y="{-CUR_HI}" width="{CUR_W}" height="{CUR_HI - CUR_LO}" fill="{c["ink"]}"/>')
        right = cx + CUR_W
    top, bottom = -CUR_HI - PAD, -CUR_LO + PAD + (2 * DOT if any(ch in "gjpqy" for t, _ in parts for ch in t) else 0)
    left = -PAD
    w, h = right + PAD - left, bottom - top
    if tile:   # square app tile, content centred, 17% margin
        side = round(max(w, h) / 0.66)
        ox, oy = (side - w) / 2 - left, (side - h) / 2 - top
        body = f'<rect width="{side}" height="{side}" fill="{c["ground"]}"/><g transform="translate({ox:.0f} {oy:.0f})">' + "".join(paths) + "</g>"
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {side} {side}">{body}</svg>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{left} {top} {w} {h}">' + "".join(paths) + "</svg>"

def standard(font, out):
    sets = {
        "wordmark": dict(parts=[("winterloom", "ink")]),
        "wordmark-plain": dict(parts=[("winterloom", "ink")], cursor=False),
        "prompt": dict(parts=[("~ $ ", "dim"), ("winterloom", "ink")]),
        "mark": dict(parts=[("w", "ink")]),
        "icon": dict(parts=[("w", "ink")], tile=True),
    }
    for name, kw in sets.items():
        for theme in INK:
            open(os.path.join(out, f"{name}-{theme}.svg"), "w").write(lockup(font, theme=theme, **kw))

if __name__ == "__main__":
    font = TTFont(sys.argv[1]); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    if len(sys.argv) > 3:
        for t in sys.argv[3:]:
            parts = [(t.split("/", 1)[0], "ink"), ("/" + t.split("/", 1)[1], "dim")] if "/" in t else [(t, "ink")]
            for theme in INK:
                open(os.path.join(out, f"{t.replace('/', '-')}-{theme}.svg"), "w").write(lockup(font, parts, theme=theme))
    else:
        standard(font, out)
