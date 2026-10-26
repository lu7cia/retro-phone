#!/usr/bin/env python3
"""Turn raw 3D renders (PNG) into the web images the page uses.

    python design/make_images.py <renders_dir>

<renders_dir> holds static_front.png, static_back.png, static_exploded.png and turn_00..23.png.
Needs Pillow.
"""
import os
import sys

from PIL import Image, ImageChops

BG = (0xE4, 0xDE, 0xFA)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "site", "img")


def content_box(im, thresh=14):
    diff = ImageChops.difference(im.convert("RGB"), Image.new("RGB", im.size, BG)).convert("L")
    return diff.point(lambda v: 255 if v > thresh else 0).getbbox()


def card(src, dst, size=(800, 1000), pad=40):
    im = Image.open(src).convert("RGB")
    box = content_box(im)
    crop = im.crop(box)
    scale = min((size[0] - 2 * pad) / crop.width, (size[1] - 2 * pad) / crop.height)
    crop = crop.resize((round(crop.width * scale), round(crop.height * scale)), Image.LANCZOS)
    canvas = Image.new("RGB", size, BG)
    canvas.paste(crop, ((size[0] - crop.width) // 2, (size[1] - crop.height) // 2))
    canvas.save(dst, "JPEG", quality=86, optimize=True, progressive=True)


def main(src_dir):
    os.makedirs(OUT, exist_ok=True)
    for name in ("front", "back", "exploded"):
        card(os.path.join(src_dir, f"static_{name}.png"), os.path.join(OUT, f"cad_{name}.jpg"))
    for i in range(24):
        im = Image.open(os.path.join(src_dir, f"turn_{i:02d}.png")).convert("RGB")
        im.save(os.path.join(OUT, f"turn_{i:02d}.jpg"), "JPEG", quality=84, optimize=True, progressive=True)
    total = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
    print(f"wrote {len(os.listdir(OUT))} images, {total / 1024:.0f} KB total")


if __name__ == "__main__":
    main(sys.argv[1])
