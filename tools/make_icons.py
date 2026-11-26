"""Draws the home-screen icons (tree-ring mark on deep pine).
Needs numpy + Pillow:  python3 tools/make_icons.py"""
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "icons"
OUT.mkdir(exist_ok=True)

BG = np.array([0x17, 0x3A, 0x31], float)
SOFT = np.array([0xB9, 0xCC, 0xC3], float)
INK = np.array([0xEE, 0xF3, 0xEC], float)
GOLD = np.array([0xE7, 0xA9, 0x3A], float)

def draw(size, extent=0.36, ss=3):
    n = size * ss
    y, x = np.mgrid[0:n, 0:n].astype(float)
    cx = cy = n / 2
    dx, dy = x - cx, y - cy
    d = np.hypot(dx, dy) / n          # distance as a fraction of the icon
    a = np.arctan2(dy, dx)
    img = np.broadcast_to(BG, (n, n, 3)).copy()
    rings = 9
    for i in range(rings):
        base = extent * ((i + 1) / rings) ** 0.92
        wob = 1 + 0.035 * np.sin(3 * a + i * 0.7) + 0.018 * np.sin(7 * a + i * 1.3)
        r = base * wob
        gold = i == rings - 3
        strong = i % 3 == 2
        w = 0.020 if gold else (0.012 if strong else 0.007)
        col, alpha = (GOLD, 1.0) if gold else ((INK, .9) if strong else (SOFT, .55))
        mask = np.abs(d - r) < w / 2
        img[mask] = img[mask] * (1 - alpha) + col * alpha
    img[d < 0.035] = GOLD
    im = Image.fromarray(img.clip(0, 255).astype("uint8"), "RGB")
    return im.resize((size, size), Image.LANCZOS)

draw(180).save(OUT / "apple-touch-icon.png")
draw(192).save(OUT / "icon-192.png")
draw(512).save(OUT / "icon-512.png")
draw(512, extent=0.30).save(OUT / "icon-maskable-512.png")  # stays inside the safe zone when cropped to a circle
print("icons written to", OUT)
