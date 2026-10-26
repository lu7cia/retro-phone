# retro-phone (working title: SHEER)

A see-through, 90s-style phone. Jelly-tinted clear shell, physical QWERTY keyboard, 3.5 mm headphone jack, SIM tray. Linux first, Android later.

**The page** (concept art, how the tech fits together, 3D model, plan with a checklist that remembers your progress):
https://claude.ai/artifact/WYrH7391twCHidHB4a7YYb

It is private. Only the owner can open it until it is shared from the page's Share menu.

## Start here

1. Open the page. The bar at the top always shows your one next step.
2. Want to print the model? Read [`cad/README.md`](cad/README.md).
3. Want the plan as plain text? Read [`docs/PLAN.md`](docs/PLAN.md).

## What's in here

| Path | What |
|---|---|
| `cad/` | Printable v0.1 model (STL + STEP) and the Python script that generates it |
| `design/` | Concept art generator (`art.py`), all page text (`content.py`), page builder |
| `design/concept/` | PNGs: all five colorways, and front + back |
| `docs/PLAN.md` | The five-stage plan, generated from `design/content.py` |

## Status

Concept v0.1. A looks-like model exists. Nothing electronic has been built or tested yet. Stage 0 and Stage 1 of the plan are next.

## Rebuild everything

```
pip install cadquery trimesh pillow playwright

python cad/sheer_v01.py                 # model  -> cad/out/stl, cad/out/step
python design/build_page.py             # page   -> design/site/index.html, docs/PLAN.md
python design/make_concept_images.py    # PNGs   -> design/concept/
```

The turntable and CAD preview images in `design/site/img/` come from a 3D render of the STL files (three.js in headless Chromium). They only need regenerating if the model changes.
