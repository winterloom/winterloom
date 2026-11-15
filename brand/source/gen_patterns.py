"""Winterloom op-art blackwork pattern generator.

Every pattern is a one-bit bitmap on the brand dot grid: each cell is either
ink or ground, with no greys, no anti-aliasing and no gradients. Shading comes
from line spacing or ordered (Bayer) dither, never from tone. Run:

    pip install numpy pillow
    python3 gen_patterns.py <out dir> [scale]

It writes <name>-on-dark.svg / -on-light.svg (crisp, one rect run per span)
and matching PNGs at `scale` pixels per dot (default 8).
"""
import os, sys
import numpy as np
from PIL import Image

INK = {"on-dark": ("#cfe8f2", "#05080b"), "on-light": ("#0d1a20", "#eef2f3")}
N = 128   # tile side in dots


def grid(w=N, h=N):
    """Centred coordinates in dots, y pointing up."""
    y, x = np.mgrid[0:h, 0:w].astype(float)
    return x - (w - 1) / 2, (h - 1) / 2 - y


def bands(d, w):
    """Echoed contours: alternate ink and ground every w dots of distance."""
    return (np.floor(d / w).astype(int) % 2) == 0


def smin(a, b, k):
    """Smooth minimum, so echoed contours of two shapes merge into chevrons."""
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)


def capsule(x, y, ax, ay, bx, by, r):
    px, py, vx, vy = x - ax, y - ay, bx - ax, by - ay
    t = np.clip((px * vx + py * vy) / (vx * vx + vy * vy), 0, 1)
    return np.hypot(px - vx * t, py - vy * t) - r


def vesica_eye(x, y, s):
    """Signed distance to an almond (two-circle vesica) of half-width s, lying flat."""
    R = s * 1.25
    off = R - s * 0.62
    return np.maximum(np.hypot(x, y - off), np.hypot(x, y + off)) - R


BAYER = np.array([[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26],
                  [12, 44, 4, 36, 14, 46, 6, 38], [60, 28, 52, 20, 62, 30, 54, 22],
                  [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
                  [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]]) / 64.0


def dither(v):
    """One-bit ordered dither of a 0..1 tone field (dotwork / stipple)."""
    h, w = v.shape
    t = np.tile(BAYER, (h // 8 + 1, w // 8 + 1))[:h, :w]
    return v > t


# ---------------------------------------------------------------- patterns

def contour():
    """Echoed contour bands around three seeds; where they meet, chevrons."""
    x, y = grid()
    d = capsule(x, y, -40, 30, 10, 44, 6)
    d = smin(d, capsule(x, y, 30, -10, 46, -46, 5), 18)
    d = smin(d, np.hypot(x + 30, y + 34) - 4, 18)
    return bands(d, 3)


def warp():
    """A square grid pulled into a lens: lines thicken and bulge toward the centre."""
    x, y = grid()
    r = np.hypot(x, y) / (N / 2)
    k = 1 + 1.6 * np.exp(-(r / 0.55) ** 2)          # local magnification
    u, v = x / k, y / k
    cell = 8
    line = lambda t: (np.mod(t, cell) < 1.6)
    return line(u) | line(v)


def rays():
    """Rays fanning from a lattice diamond; the diamond holds a fine grid."""
    x, y = grid()
    diam = np.abs(x) + np.abs(y)
    R = 30
    th = np.arctan2(y, x)
    out = (np.floor(th / (2 * np.pi) * 64) % 2 == 0) & (diam > R + 6)
    frame = bands(diam - R, 2) & (diam > R) & (diam <= R + 6)
    # inner lattice: diagonal grid plus rings around each node
    u, v = (x + y) / 2, (x - y) / 2
    gu, gv = np.mod(u, 6) - 3, np.mod(v, 6) - 3
    lattice = (np.abs(gu) < 0.5) | (np.abs(gv) < 0.5) | (np.abs(np.hypot(gu, gv) - 2.2) < 0.45)
    inner = lattice & (diam <= R - 1)
    return out | frame | inner


def eye():
    """The watching eye: a vesica almond, echoed outward, iris and pupil inside."""
    x, y = grid()
    d = vesica_eye(x, y, 26)
    outside = bands(d, 3) & (d > 2) & (d < 26)
    lid = (d > -1.5) & (d <= 0.5)
    r = np.hypot(x, y)
    iris = (np.abs(r - 11) < 1.2) | ((r < 6.5) & ~((np.hypot(x + 2.5, y - 2.5) < 1.6)))
    rays_in = (np.floor(np.arctan2(y, x) / (2 * np.pi) * 24) % 2 == 0) & (r > 6.5) & (r < 9.5)
    return outside | lid | ((iris | rays_in) & (d < -1.5))


def dotwork():
    """Stippled orb: a lit sphere and its ring, shaded only by ordered dither."""
    x, y = grid()
    R = 38
    r2 = (x * x + y * y) / (R * R)
    z = np.sqrt(np.clip(1 - r2, 0, 1))
    nx, ny, nz = x / R, y / R, z
    L = np.array([-0.5, 0.6, 0.62]); L /= np.linalg.norm(L)
    lit = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1) ** 1.4
    sphere = (r2 < 1) & dither(0.06 + 0.9 * lit)
    rim = np.abs(np.sqrt(r2) - 1) * R < 0.6
    rr = np.hypot(x, y * 3.4)                         # flat orbital ring
    rd = (rr - 54) * rr / np.maximum(np.hypot(x, y * 3.4 ** 2), 1e-6)   # distance in dots
    front = y < 0                                     # ring passes in front of the lower half
    ring = (np.abs(rd) < 0.7) & (front | (r2 >= 1))
    gap = (np.abs(rd) < 2.2) & front              # clear ground either side of the ring
    halo = (r2 >= 1) & dither(np.clip(0.12 - 0.12 * (np.sqrt(r2) - 1), 0, 1))
    return ((sphere | rim | halo) & ~gap) | ring


def field():
    """The composition rule: busy echoed contours with one quiet eye at rest."""
    x, y = grid()
    d = capsule(x, y, -64, -20, 64, 20, 0)
    d = smin(d, capsule(x, y, -40, 64, 40, -64, 0), 14)
    busy = bands(d, 2.5)
    e = vesica_eye(x, y, 18)
    plate = e < 5                                     # clear ground around the eye
    lid = (e > -1.2) & (e <= 0.4)
    r = np.hypot(x, y)
    pupil = (r < 5) & ~(np.hypot(x + 1.8, y - 1.8) < 1.2)
    return (busy & ~plate) | lid | (pupil & (e < -1.2)) | ((np.abs(e - 3) < 0.5))


def rule():
    """A divider: an echoed zigzag, 256 x 16 dots, for section breaks in notes."""
    x, y = grid(256, 16)
    zig = np.abs(np.mod(x, 16) - 8) - 4               # triangle wave, amplitude 4
    d = np.abs(y - zig * 0.9)
    return bands(d, 2) & (d < 8)


PATTERNS = {"contour": contour, "warp": warp, "rays": rays, "eye": eye,
            "dotwork": dotwork, "field": field, "rule": rule}


# ---------------------------------------------------------------- output

def to_svg(bits, ink, ground):
    h, w = bits.shape
    d = []
    for j in range(h):
        row = bits[j]
        i = 0
        while i < w:
            if row[i]:
                k = i
                while k < w and row[k]:
                    k += 1
                d.append(f"M{i} {j}h{k - i}v1h-{k - i}z")
                i = k
            else:
                i += 1
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" shape-rendering="crispEdges">'
            f'<rect width="{w}" height="{h}" fill="{ground}"/><path fill="{ink}" d="{"".join(d)}"/></svg>')


def hexrgb(c):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "patterns"
    scale = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    os.makedirs(os.path.join(out, "png"), exist_ok=True)
    for name, fn in PATTERNS.items():
        bits = fn()
        for theme, (ink, ground) in INK.items():
            with open(os.path.join(out, f"{name}-{theme}.svg"), "w") as f:
                f.write(to_svg(bits, ink, ground))
            img = np.where(bits[..., None], hexrgb(ink), hexrgb(ground)).astype(np.uint8)
            Image.fromarray(img).resize((bits.shape[1] * scale, bits.shape[0] * scale), Image.NEAREST) \
                .save(os.path.join(out, "png", f"{name}-{theme}.png"), optimize=True)
        print(name, bits.shape, f"{bits.mean():.0%} ink")


if __name__ == "__main__":
    main()
