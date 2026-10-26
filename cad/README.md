# SHEER v0.1 printable model

A **looks-like** model of the see-through phone: right size, right shape, fake guts. It is sized around placeholder parts, so treat it as a fit-check, not a final design.

Size: **70 × 120 × 15 mm**, 2.6 mm walls, 10 mm corners. Four M2 × 12 screws close it.

## What's in `out/`

| File | What it is | Print it? |
|---|---|---|
| `stl/sheer_front_shell.stl` | Front half: raised keys, D-pad, glass seat, earpiece slot, ports | **Yes, in clear resin** |
| `stl/sheer_back_shell.stl` | Back half: four screw posts, side buttons, ports | **Yes, in clear resin** |
| `stl/sheer_dummy_display.stl` | Fake screen module | Optional, opaque |
| `stl/sheer_dummy_mainboard.stl` | Fake board with chips on the back side | Optional, opaque |
| `stl/sheer_dummy_battery.stl` | Fake battery (paint it yellow) | Optional, opaque |
| `stl/sheer_dummy_keyboard_board.stl` | Fake keyboard board | Optional, opaque |
| `step/*.step` | Same parts as STEP, for Fusion, Onshape or FreeCAD | For editing |
| `step/sheer_v01_assembly.step` | Everything in place, coloured | For viewing |

Every STL is watertight and no two parts collide (the script checks this each time it runs).

## Get a price (20 minutes, no buying)

1. Open an instant-quote page: [JLC3DP](https://jlc3dp.com/), [PCBWay SLA printing](https://www.pcbway.com/rapid-prototyping/3d-printing/3d-printing-SLA.html) or [Xometry](https://www.xometry.com/).
2. Upload `sheer_front_shell.stl`. Choose **SLA resin** and the **transparent / clear** material. Quantity 1.
3. Repeat for `sheer_back_shell.stl`. Write down both prices.

Notes for clear parts:

- Clear resin comes out slightly hazy unless it is polished. Ask for polishing or a clear coat, or wet-sand through 400 → 2000 grit and clear-coat it yourself.
- Clear resin can yellow over time without a UV-resistant coat.
- The 2.6 mm walls pass the usual 1.2 mm minimum. Files are well under the 50 MB upload limit PCBWay lists.
- If a service offers tinted clear resin, pick your colour. If not, order clear and tint it later.

## Change a number

Everything is a named number at the top of `sheer_v01.py`. Edit one and re-run:

```
pip install cadquery trimesh
python cad/sheer_v01.py
```

| Name | Meaning |
|---|---|
| `W, H, T` | Body width, height, thickness |
| `R`, `ER` | Corner radius, edge round-over |
| `WALL` | Shell wall thickness |
| `SPLIT` | Where the two halves meet (height above the back face) |
| `SCREEN_*` | Screen window size and position. `SCREEN_THROUGH = True` cuts a real opening |
| `KEY_*`, `KB_TOP_Y` | Key size, spacing and where the keyboard starts |
| `POST_XY` | Screw post positions |
| `JACK_X`, `USBC_*`, `SIM_*` | Port positions and sizes |

Axes: X is left/right, Y is bottom to top of the phone, Z is back face (0) to screen face.

## Not in v0.1

- A strap loop (ball chain).
- A real screen opening (turn on `SCREEN_THROUGH` once you have a display).
- Snap-on swappable back covers.
- Anything sized from real measured parts. Measure the display, board and battery you buy and update the numbers.
