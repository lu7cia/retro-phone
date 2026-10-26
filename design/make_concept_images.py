#!/usr/bin/env python3
"""Render the concept PNGs in design/concept/ from design/art.py (needs Playwright + Chromium).

    python design/make_concept_images.py

If Playwright cannot find its own browser, point CHROMIUM_PATH at any Chromium binary.
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import art  # noqa: E402

CSS = open(os.path.join(HERE, "art.css"), encoding="utf-8").read()
FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unbounded:wght@600;700;800'
         '&family=DM+Mono:wght@400;500&display=swap">')
NAMES = [("ice", "ICE POP"), ("grape", "GRAPE SODA"), ("kiwi", "KIWI"), ("gum", "BUBBLEGUM"), ("ghost", "GHOST")]


def page(body: str, w: int, h: int) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{CSS}
:root{{--font-display:"Unbounded","Arial Black",sans-serif;--font-mono:"DM Mono",ui-monospace,monospace}}
html,body{{margin:0;background:#E4DEFA;color:#17123B}}
.stage{{width:{w}px;height:{h}px;box-sizing:border-box;padding:46px 56px 40px;display:flex;flex-direction:column;justify-content:space-between}}
.head{{display:flex;justify-content:space-between;align-items:baseline}}
.brand{{font:800 30px/1 var(--font-display);letter-spacing:.16em}}
.tag{{font:500 17px/1 var(--font-mono);letter-spacing:.08em;opacity:.7}}
.row{{display:flex;justify-content:space-between;align-items:flex-end;gap:10px}}
.cell{{display:grid;gap:10px;justify-items:center}}
.cell svg{{width:100%;height:auto;display:block;overflow:visible}}
.cap{{font:700 17px/1 var(--font-display);letter-spacing:.06em}}
</style></head><body>{body}</body></html>"""


def lineup() -> str:
    cells = "".join(
        f'<div class="cell" style="width:19%">{art.front_view("L" + cw, cw=cw)}<span class="cap">{label}</span></div>'
        for cw, label in NAMES)
    return page(f'<div class="stage"><div class="head"><span class="brand">SHEER</span>'
                f'<span class="tag">A PHONE WITH NOTHING TO HIDE · CONCEPT V0.1</span></div><div class="row">{cells}</div></div>', 1900, 740)


def frontback() -> str:
    body = (f'<div class="stage" data-cw="ice"><div class="head"><span class="brand">SHEER</span>'
            f'<span class="tag">FRONT + BACK · ICE POP</span></div>'
            f'<div class="row" style="justify-content:center;gap:0"><div class="cell" style="width:36%;transform:rotate(-3deg);margin-right:-3%">{art.front_view("F")}</div>'
            f'<div class="cell" style="width:36%;transform:rotate(3.5deg) translateY(2%)">{art.back_view("B")}</div></div></div>')
    return page(body, 1500, 1020)


def shoot(html: str, out: str, w: int, h: int, scale: float):
    from playwright.sync_api import sync_playwright
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
        path = f.name
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None)
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
        pg.goto("file://" + path, wait_until="networkidle")
        pg.wait_for_timeout(600)
        pg.screenshot(path=out)
        b.close()
    os.unlink(path)
    print("wrote", out, f"{os.path.getsize(out) / 1024:.0f} KB")


if __name__ == "__main__":
    out = os.path.join(HERE, "concept")
    os.makedirs(out, exist_ok=True)
    shoot(lineup(), os.path.join(out, "colorways.png"), 1900, 740, 1.5)
    shoot(frontback(), os.path.join(out, "front_back_ice.png"), 1500, 1020, 1.5)
