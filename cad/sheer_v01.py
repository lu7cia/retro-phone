#!/usr/bin/env python3
"""
SHEER v0.1 - "looks-like" model of the see-through phone.

What this is
------------
A printable blockout: front shell, back shell, and dummy internals (screen,
mainboard, battery, keyboard board) so you can hold the thing, check the size
and see how the guts look through tinted clear plastic.

What this is NOT
----------------
A final design. It is sized around PLACEHOLDER parts. Once you pick a real
screen / board / battery, change the numbers below and re-run.

How to use
----------
    pip install cadquery trimesh
    python cad/sheer_v01.py            # writes cad/out/step/*.step and cad/out/stl/*.stl

Units are millimetres.
    X = left/right, Y = bottom -> top edge of the phone, Z = back face -> screen side.
    Z = 0 is the BACK face of the phone, Z = T is the FRONT (screen) face.
"""
import os
import sys

import cadquery as cq

# --------------------------------------------------------------------------
# 1. THE NUMBERS (edit these, re-run, get new files)
# --------------------------------------------------------------------------
W, H, T = 70.0, 120.0, 15.0     # body width, height, thickness
R = 10.0                        # corner radius seen from the front
ER = 3.5                        # round-over on the front and back edges
WALL = 2.6                      # shell wall thickness (SLA printers want >= 1.2)
SPLIT = 8.5                     # seam height above the back face

# Screen "glass seat" (a shallow recess on the front). Set SCREEN_THROUGH=True
# to cut a real opening when you have an actual display module.
SCREEN_W, SCREEN_H, SCREEN_CY, SCREEN_R = 56.0, 56.0, 21.5, 3.5
SCREEN_DEPTH = 0.8
SCREEN_THROUGH = False

# Keyboard (4 rows of keys, BlackBerry-Q10-ish proportions)
KEY_W, KEY_H, KEY_UP = 5.3, 6.2, 1.4      # key footprint + how far it sticks out
KEY_PITCH_X, KEY_PITCH_Y = 6.1, 7.6
KB_TOP_Y = -19.5                          # y of the top edge of row 1

# Screws: M2 x 12 from the back into the front bosses
POST_XY = [(27.0, 51.0), (-27.0, 51.0), (27.0, -51.0), (-27.0, -51.0)]
POST_R = 3.0
SCREW_HOLE_D, SCREW_CBORE_D, SCREW_CBORE_DEPTH, PILOT_D = 2.4, 4.4, 1.4, 1.8

# Ports (all on the seam-height centre line)
PORT_Z = 7.5
JACK_X, JACK_D = 16.0, 6.2                # 3.5 mm headphone jack, top edge
USBC_W, USBC_H = 9.4, 3.6                 # USB-C, bottom edge
SIM_Y, SIM_Z = 8.0, 5.0                   # SIM + microSD tray, right edge

# --------------------------------------------------------------------------
# 2. SMALL HELPERS
# --------------------------------------------------------------------------


def rr(w, h, r, z0, z1, cx=0.0, cy=0.0):
    """Rounded rectangle, extruded from z0 to z1."""
    r = min(r, w / 2 - 1e-3, h / 2 - 1e-3)
    return (cq.Workplane("XY").workplane(offset=z0).center(cx, cy)
            .rect(w, h).extrude(z1 - z0).edges("|Z").fillet(r))


def body(w, h, t, r, er, z0=0.0):
    """The chunky 'pillow' body: rounded corners + rounded front/back edges."""
    return (cq.Workplane("XY").workplane(offset=z0)
            .rect(w, h).extrude(t)
            .edges("|Z").fillet(r)
            .faces(">Z or <Z").edges().fillet(er))


def zslab(z0, z1):
    return (cq.Workplane("XY")
            .box(W + 40, H + 40, z1 - z0, centered=(True, True, False))
            .translate((0, 0, z0)))


def cyl(x, y, z, r, h, axis="Z"):
    d = {"X": (1, 0, 0), "Y": (0, 1, 0), "Z": (0, 0, 1)}[axis]
    return cq.Workplane("XY").add(
        cq.Solid.makeCylinder(r, h, cq.Vector(x, y, z), cq.Vector(*d)))


def box(cx, cy, cz, sx, sy, sz):
    return cq.Workplane("XY").box(sx, sy, sz).translate((cx, cy, cz))


def with_notches(part, z0, z1, r=3.4):
    """Punch round notches where the screw posts live."""
    for (x, y) in POST_XY:
        part = part.cut(cyl(x, y, z0 - 1, r, z1 - z0 + 2))
    return part


def fuse_all(solids):
    out = solids[0]
    for s in solids[1:]:
        out = out.union(s)
    return out


# --------------------------------------------------------------------------
# 3. THE SHELL
# --------------------------------------------------------------------------


def make_shells():
    outer = body(W, H, T, R, ER)
    inner = body(W - 2 * WALL, H - 2 * WALL, T - 2 * WALL, R - WALL, 0.8, z0=WALL)
    shell = outer.cut(inner)

    front = shell.intersect(zslab(SPLIT, T + 5))
    back = shell.intersect(zslab(-5, SPLIT))

    # seam: tongue on the back half, matching rabbet on the front half
    tongue = (rr(W - 3.0, H - 3.0, R - 1.5, SPLIT, SPLIT + 1.2)
              .cut(rr(W - 2 * WALL, H - 2 * WALL, R - WALL, SPLIT - 0.2, SPLIT + 1.4)))
    back = back.union(tongue)
    front = front.cut(rr(W - 2.8, H - 2.8, R - 1.4, SPLIT - 0.1, SPLIT + 1.4))

    # screw posts (back) and bosses (front)
    for (x, y) in POST_XY:
        back = back.union(cyl(x, y, WALL - 0.2, POST_R, SPLIT - WALL + 0.2))
        front = front.union(cyl(x, y, SPLIT, POST_R, (T - WALL) - SPLIT + 0.2))
    for (x, y) in POST_XY:
        # clearance hole through back wall + post, counterbore for the screw head
        back = back.cut(cyl(x, y, -1, SCREW_HOLE_D / 2, SPLIT + 2))
        back = back.cut(cyl(x, y, -1, SCREW_CBORE_D / 2, SCREW_CBORE_DEPTH + 1))
        # pilot hole in the front boss
        front = front.cut(cyl(x, y, SPLIT - 0.5, PILOT_D / 2, 4.3))

    # ports: cut through the whole wall of both halves
    cuts = []
    # 3.5 mm headphone jack (top edge)
    cuts.append(cyl(JACK_X, H / 2 - WALL - 2, PORT_Z, JACK_D / 2, WALL + 6, "Y"))
    # USB-C (bottom edge)
    cuts.append(cq.Workplane("XZ", origin=(0, -(H / 2 - WALL - 2), 0))
                .center(0, PORT_Z).slot2D(USBC_W, USBC_H).extrude(WALL + 6))
    # speaker holes + mic hole (bottom edge)
    bot_y0 = -(H / 2) - 4.0                   # start outside the phone, cut inward
    bot_len = 4.0 + WALL + 2.0
    for i in range(6):
        cuts.append(cyl(13.0 + i * 2.2, bot_y0, PORT_Z, 0.6, bot_len, "Y"))
    cuts.append(cyl(-14.0, bot_y0, PORT_Z, 0.55, bot_len, "Y"))
    # SIM + microSD tray slot and pin-eject hole (right edge)
    cuts.append(cq.Workplane("YZ", origin=(W / 2 - WALL - 2, 0, 0))
                .center(SIM_Y, SIM_Z).slot2D(12.0, 1.6).extrude(WALL + 6))
    cuts.append(cyl(W / 2 - WALL - 2, SIM_Y + 8.5, SIM_Z, 0.6, WALL + 6, "X"))
    for c in cuts:
        front = front.cut(c)
        back = back.cut(c)

    # screen glass seat + earpiece recess (front face)
    if SCREEN_THROUGH:
        front = front.cut(rr(SCREEN_W, SCREEN_H, SCREEN_R, T - WALL - 1, T + 1, 0, SCREEN_CY))
    else:
        front = front.cut(rr(SCREEN_W, SCREEN_H, SCREEN_R, T - SCREEN_DEPTH, T + 1, 0, SCREEN_CY))
    front = front.cut(
        cq.Workplane("XY").workplane(offset=T - 0.8).center(0, H / 2 - 5.2)
        .slot2D(14.0, 1.6).extrude(2.0))

    # side nubs: volume rocker (left) and power (right), on the back half
    def nub(sign, cy, length):
        # sunk 1 mm into the wall, 1 mm proud, rounded only on the outside face
        n = box(sign * (W / 2 - 1.0 + 1.0), cy, 6.0, 2.0, length, 2.6)
        return n.faces(">X" if sign > 0 else "<X").edges().fillet(0.5)

    back = back.union(nub(-1, 27.0, 16.0)).union(nub(+1, 27.0, 9.0))

    # keys: raised key bumps on the front face
    keys = []
    for r in range(3):
        cy = KB_TOP_Y - KEY_H / 2 - r * KEY_PITCH_Y
        for c in range(10):
            keys.append((((c - 4.5) * KEY_PITCH_X), cy, KEY_W, KEY_H))
    cy = KB_TOP_Y - KEY_H / 2 - 3 * KEY_PITCH_Y
    for c in (0, 1, 8, 9):
        keys.append((((c - 4.5) * KEY_PITCH_X), cy, KEY_W, KEY_H))
    keys.append((0.0, cy, 5 * KEY_PITCH_X + KEY_W, KEY_H))          # space bar
    # nav row: call, back, menu, end + round d-pad
    ny = -12.5
    keys += [(-25.5, ny, 9.0, 5.5), (-14.5, ny, 8.0, 5.5),
             (14.5, ny, 8.0, 5.5), (25.5, ny, 9.0, 5.5)]

    key_solids = []
    for (kx, ky, kw, kh) in keys:
        z0, z1 = T - 0.5, T + KEY_UP
        k = (cq.Workplane("XY").workplane(offset=z0).center(kx, ky)
             .rect(kw, kh).extrude(z1 - z0)
             .edges("|Z").fillet(0.8)
             .faces(">Z").edges().fillet(0.5))
        key_solids.append(k)
    # d-pad ring + centre button
    dpad = (cq.Workplane("XY").workplane(offset=T - 0.5).center(0, ny)
            .circle(6.5).extrude(0.5 + 1.0).faces(">Z").edges().fillet(0.4))
    dpad = dpad.cut(cq.Workplane("XY").workplane(offset=T + 0.2).center(0, ny)
                    .circle(5.6).circle(5.0).extrude(1.2))  # groove ring
    centre = (cq.Workplane("XY").workplane(offset=T - 0.5).center(0, ny)
              .circle(3.0).extrude(0.5 + 1.5).faces(">Z").edges().fillet(0.5))
    key_solids += [dpad, centre]
    for ks in key_solids:
        front = front.union(ks)

    return front, back


# --------------------------------------------------------------------------
# 4. DUMMY INTERNALS (print these in opaque plastic to see the "guts")
# --------------------------------------------------------------------------


def make_dummies():
    parts = {}

    # screen module sits right behind the front wall
    d = rr(60.0, 60.0, 2.0, T - WALL - 2.8, T - WALL, 0, SCREEN_CY)
    parts["dummy_display"] = with_notches(d, T - WALL - 2.8, T - WALL)

    # mainboard behind the screen, components on the back-facing side
    pz1 = T - WALL - 2.8            # top of the board
    pz0 = pz1 - 1.6
    pcb = rr(62.0, 64.0, 4.0, pz0, pz1, 0, 23.0)
    pcb = with_notches(pcb, pz0, pz1)
    comps = [                              # x, y, width, height, thickness
        (-9.0, 39.0, 14.0, 14.0, 1.2),     # SoC
        (14.0, 36.0, 20.0, 16.0, 2.2),     # cellular modem + can
        (-17.0, 18.0, 16.0, 13.0, 1.6),    # shield can
        (12.0, 12.0, 14.0, 9.0, 1.4),      # wifi / bt module
        (-4.0, 1.5, 10.0, 4.0, 1.5),       # battery connector
        (19.0, 48.5, 7.0, 7.0, 1.3),       # audio codec
        (-18.0, 49.5, 9.0, 5.0, 1.0),      # PMIC
    ]
    for (cx, cy, sx, sy, sh) in comps:
        pcb = pcb.union(box(cx, cy, pz0 - sh / 2 + 0.05, sx, sy, sh + 0.1).edges("|Z").fillet(0.3))
    parts["dummy_mainboard"] = pcb

    # battery in the lower half, visible from the back
    b0, b1 = WALL + 0.1, WALL + 0.1 + 5.5
    batt = rr(56.0, 40.0, 3.0, b0, b1, 0, -31.5).faces(">Z or <Z").edges().fillet(0.6)
    parts["dummy_battery"] = with_notches(batt, b0, b1)

    # keyboard board behind the keys (also covers the nav-key row)
    k1 = T - WALL
    k0 = k1 - 1.6
    kb = rr(62.0, 42.5, 2.0, k0, k1, 0, -30.25)
    parts["dummy_keyboard_board"] = with_notches(kb, k0, k1)
    return parts


# --------------------------------------------------------------------------
# 5. EXPORT
# --------------------------------------------------------------------------


def main(out_dir=None):
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = out_dir or os.path.join(here, "out")
    step_dir = os.path.join(out_dir, "step")
    stl_dir = os.path.join(out_dir, "stl")
    os.makedirs(step_dir, exist_ok=True)
    os.makedirs(stl_dir, exist_ok=True)

    front, back = make_shells()
    parts = {"sheer_front_shell": front, "sheer_back_shell": back}
    parts.update({"sheer_" + k: v for k, v in make_dummies().items()})

    for name, wp in parts.items():
        cq.exporters.export(wp, os.path.join(step_dir, name + ".step"))
        cq.exporters.export(wp, os.path.join(stl_dir, name + ".stl"),
                            tolerance=0.02, angularTolerance=0.15)
        bb = wp.val().BoundingBox()
        print(f"{name:28s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:5.1f} mm   "
              f"volume {wp.val().Volume() / 1000:7.2f} cm3   solids {len(wp.solids().vals())}")

    # one STEP with every part in place, coloured, for opening in Fusion / Onshape / FreeCAD
    colours = {"front_shell": (0.45, 0.75, 1.0, 0.45), "back_shell": (0.45, 0.75, 1.0, 0.45),
               "dummy_display": (0.05, 0.05, 0.15, 1.0), "dummy_mainboard": (0.2, 0.4, 0.9, 1.0),
               "dummy_battery": (1.0, 0.78, 0.1, 1.0), "dummy_keyboard_board": (0.1, 0.15, 0.22, 1.0)}
    assy = cq.Assembly(name="SHEER_v0.1")
    for name, wp in parts.items():
        assy.add(wp, name=name, color=cq.Color(*colours[name.replace("sheer_", "")]))
    assy.save(os.path.join(step_dir, "sheer_v01_assembly.step"))

    # does anything collide with anything it shouldn't? (volumes in mm3)
    names = list(parts)
    clashes = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            try:
                vol = sum(s.Volume() for s in parts[a].intersect(parts[b]).solids().vals())
            except Exception:
                vol = 0.0
            if vol > 0.5:
                clashes.append((a, b, vol))
    print("interference check:", "clean" if not clashes else "")
    for a, b, v in clashes:
        print(f"  {a} <-> {b}: {v:.1f} mm3")
    return parts


if __name__ == "__main__":
    sys.exit(0 if main(*(sys.argv[1:2])) else 1)
