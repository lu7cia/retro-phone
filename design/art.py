"""SHEER concept art, generated as SVG.

Every coordinate is millimetres in "front view" space, matching cad/sheer_v01.py:
    svg_x = 35 + cad_x        (0..70, left -> right)
    svg_y = 60 - cad_y        (0..120, top -> bottom)

Colours come from CSS variables (see art.css), so one drawing serves every colorway.
"""
from __future__ import annotations

import random

W, H = 70.0, 120.0
VIEWBOX = "-9 -8 92 141"          # phone views: leaves room for the coloured shadow + side buttons

# keyboard grid (same numbers as the CAD)
KW, KH = 5.3, 6.2
PX, PY = 6.1, 7.6
ROW_TOP = 79.5                      # svg y of the first row's top edge
NAV_Y = 72.5


def n(v: float) -> str:
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


def rrp(x, y, w, h, r) -> str:
    """Rounded-rect path."""
    x2, y2 = x + w, y + h
    return (f"M{n(x + r)},{n(y)}H{n(x2 - r)}A{n(r)},{n(r)} 0 0 1 {n(x2)},{n(y + r)}"
            f"V{n(y2 - r)}A{n(r)},{n(r)} 0 0 1 {n(x2 - r)},{n(y2)}H{n(x + r)}"
            f"A{n(r)},{n(r)} 0 0 1 {n(x)},{n(y2 - r)}V{n(y + r)}A{n(r)},{n(r)} 0 0 1 {n(x + r)},{n(y)}Z")


def kx(c: int) -> float:
    return 35 + (c - 4.5) * PX


# ---------------------------------------------------------------------------
# shared defs
# ---------------------------------------------------------------------------

def defs(u: str) -> str:
    return f'''<defs>
<clipPath id="{u}-body"><rect width="70" height="120" rx="10"/></clipPath>
<clipPath id="{u}-scr"><rect x="7" y="10.5" width="56" height="56" rx="3.5"/></clipPath>
<linearGradient id="{u}-sh" x1="0" y1="0" x2="1" y2="1"><stop offset="0" class="s-sh0"/><stop offset=".5" class="s-sh1"/><stop offset="1" class="s-sh2"/></linearGradient>
<linearGradient id="{u}-key" x1="0" y1="0" x2="0" y2="1"><stop offset="0" class="s-key0"/><stop offset="1" class="s-key1"/></linearGradient>
<linearGradient id="{u}-pcb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" class="s-pcb0"/><stop offset="1" class="s-pcb1"/></linearGradient>
<linearGradient id="{u}-hl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".62"/><stop offset=".7" stop-color="#fff" stop-opacity=".08"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="{u}-hl2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".0"/><stop offset=".5" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="{u}-scrg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2a1d6b"/><stop offset=".55" stop-color="#150f3d"/><stop offset="1" stop-color="#0b0828"/></linearGradient>
<linearGradient id="{u}-metal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6f8fb"/><stop offset=".5" stop-color="#b4bcc9"/><stop offset="1" stop-color="#8a94a6"/></linearGradient>
<linearGradient id="{u}-gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe9a8"/><stop offset="1" stop-color="#c4902b"/></linearGradient>
<linearGradient id="{u}-batt" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe066"/><stop offset="1" stop-color="#f0a61a"/></linearGradient>
<linearGradient id="{u}-chip" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a3c4c"/><stop offset="1" stop-color="#14151d"/></linearGradient>
<linearGradient id="{u}-kb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#27384d"/><stop offset="1" stop-color="#16212f"/></linearGradient>
<radialGradient id="{u}-led"><stop offset="0" class="f-led" stop-color="var(--led)" stop-opacity="1"/><stop offset="1" stop-color="var(--led)" stop-opacity="0"/></radialGradient>
<filter id="{u}-b1" x="-15%" y="-15%" width="130%" height="130%"><feGaussianBlur stdDeviation=".6"/></filter>
<filter id="{u}-b2" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="1.6"/></filter>
<filter id="{u}-b4" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="4"/></filter>
<mask id="{u}-pcbm"><rect x="-1" y="-1" width="72" height="122" fill="#fff"/>{"".join(f'<circle cx="{x}" cy="{y}" r="3.4" fill="#000"/>' for x, y in POSTS)}</mask>
<symbol id="{u}-k" overflow="visible">
  <rect x="-2.65" y="-2.6" width="5.3" height="6.2" rx="1" fill="#000" opacity=".16"/>
  <rect x="-2.65" y="-3.1" width="5.3" height="6.2" rx="1" fill="url(#{u}-key)" class="k-deep" stroke-width=".25" stroke-opacity=".55"/>
  <rect x="-2.15" y="-2.75" width="4.3" height="2.3" rx=".7" fill="#fff" opacity=".42"/>
</symbol>
</defs>'''


POSTS = [(62, 9), (8, 9), (62, 111), (8, 111)]


# ---------------------------------------------------------------------------
# layers (each returns a <g> in front-view space)
# ---------------------------------------------------------------------------

def glyph(kind: str, cx: float, cy: float, fill="var(--ink)", op=.8) -> str:
    t = f'transform="translate({n(cx)} {n(cy)})"'
    if kind == "SHIFT":
        return f'<path {t} d="M0,-1.3L1.5,.4H.55V1.4H-.55V.4H-1.5Z" fill="{fill}" fill-opacity="{op}"/>'
    if kind == "DEL":
        return (f'<g {t} fill="none" stroke="{fill}" stroke-opacity="{op}" stroke-width=".38" stroke-linejoin="round" stroke-linecap="round">'
                f'<path d="M-1.8,0L-.6,-1.3H1.8V1.3H-.6Z"/><path d="M.1,-.6L1,.6M1,-.6L.1,.6"/></g>')
    if kind == "ENTER":
        return (f'<path {t} d="M1.6,-1.4V.4H-1.3M-.3,-.6L-1.3,.4L-.3,1.4" fill="none" stroke="{fill}" stroke-opacity="{op}" '
                f'stroke-width=".42" stroke-linecap="round" stroke-linejoin="round"/>')
    return ""


def keys_markup(u: str, legends: bool = True) -> str:
    rows = [list("QWERTYUIOP"),
            list("ASDFGHJKL") + ["DEL"],
            ["SHIFT"] + list("ZXCVBNM") + [".", "ENTER"],
            None]
    out = []
    for r in range(4):
        y = ROW_TOP + KH / 2 + r * PY
        cols = range(10) if r < 3 else (0, 1, 8, 9)
        for c in cols:
            x = kx(c)
            out.append(f'<use href="#{u}-k" x="{n(x)}" y="{n(y)}"/>')
            if not legends:
                continue
            if r < 3:
                lg = rows[r][c]
            else:
                lg = {0: "ALT", 1: "SYM", 8: "@", 9: "?"}[c]
            if lg in ("SHIFT", "DEL", "ENTER"):
                out.append(glyph(lg, x, y - .2))
            elif lg in ("ALT", "SYM"):
                out.append(f'<text class="legend" x="{n(x)}" y="{n(y - .2)}" style="font-size:1.95px;letter-spacing:.05px">{lg}</text>')
            else:
                out.append(f'<text class="legend" x="{n(x)}" y="{n(y - .2)}">{lg}</text>')
    # space bar
    y = ROW_TOP + KH / 2 + 3 * PY
    sw = 5 * PX + KW
    out.append(f'<rect x="{n(35 - sw / 2)}" y="{n(y - 2.6)}" width="{n(sw)}" height="{n(KH)}" rx="1" fill="#000" opacity=".16"/>')
    out.append(f'<rect x="{n(35 - sw / 2)}" y="{n(y - 3.1)}" width="{n(sw)}" height="{n(KH)}" rx="1" fill="url(#{u}-key)" class="k-deep" stroke-width=".25" stroke-opacity=".55"/>')
    out.append(f'<rect x="{n(35 - sw / 2 + .5)}" y="{n(y - 2.75)}" width="{n(sw - 1)}" height="2.3" rx=".7" fill="#fff" opacity=".42"/>')
    out.append(f'<rect x="{n(31)}" y="{n(y - .15)}" width="8" height=".7" rx=".35" class="f-ink" opacity=".22"/>')
    return "\n".join(out)


def nav_markup(u: str) -> str:
    y = NAV_Y

    def pill(cx, w, fill, glyph_svg):
        return (f'<g transform="translate({n(cx)} {n(y)})">'
                f'<rect x="{n(-w / 2)}" y="-2.2" width="{n(w)}" height="5.5" rx="2.75" fill="#000" opacity=".16"/>'
                f'<rect x="{n(-w / 2)}" y="-2.75" width="{n(w)}" height="5.5" rx="2.75" fill="{fill}" class="k-deep" stroke-width=".25" stroke-opacity=".55"/>'
                f'<rect x="{n(-w / 2 + .7)}" y="-2.4" width="{n(w - 1.4)}" height="2.1" rx="1.05" fill="#fff" opacity=".45"/>'
                f'{glyph_svg}</g>')

    handset = ('<path d="M-1.9,.9C-2.2,-.5 -1.1,-1.6 1.7,-1.9" fill="none" stroke="#fff" stroke-width=".95" stroke-linecap="round"/>'
               '<circle cx="-1.9" cy=".95" r=".7" fill="#fff"/><circle cx="1.7" cy="-1.9" r=".7" fill="#fff"/>')
    handset_end = f'<g transform="rotate(135)">{handset}</g>'
    back = '<path d="M-1.6,-.2H1 a1.3,1.3 0 0 1 0,2.6H-.4 M-1.6,-.2L-.6,-1.2M-1.6,-.2L-.6,.8" fill="none" stroke="var(--ink)" stroke-opacity=".75" stroke-width=".42" stroke-linecap="round" stroke-linejoin="round" transform="translate(0 -.6)"/>'
    menu = '<path d="M-1.6,-1H1.6M-1.6,.3H1.6M-1.6,1.6H1.6" stroke="var(--ink)" stroke-opacity=".75" stroke-width=".45" stroke-linecap="round" transform="translate(0 -.55)"/>'
    out = [
        pill(9.5, 9, "#2fd27c", handset),
        pill(20.5, 8, f"url(#{u}-key)", back),
        pill(49.5, 8, f"url(#{u}-key)", menu),
        pill(60.5, 9, "#ff4a6b", handset_end),
    ]
    # d-pad
    out.append(f'''<g transform="translate(35 {n(y)})">
<circle r="6.6" cy=".5" fill="#000" opacity=".16"/>
<circle r="6.5" fill="url(#{u}-key)" class="k-deep" stroke-width=".28" stroke-opacity=".6"/>
<circle r="5.5" fill="none" stroke="#fff" stroke-width=".25" opacity=".55"/>
<path d="M0,-5.1L1,-3.8H-1Z M0,5.1L1,3.8H-1Z M-5.1,0L-3.8,-1V1Z M5.1,0L3.8,-1V1Z" class="f-ink" opacity=".6"/>
<circle r="3" cy=".3" fill="#000" opacity=".14"/>
<circle r="3" fill="url(#{u}-key)" class="k-deep" stroke-width=".25" stroke-opacity=".6"/>
<ellipse cy="-1.1" rx="1.9" ry="1.1" fill="#fff" opacity=".5"/>
</g>''')
    return "\n".join(out)


def front_shell(u: str, legends: bool = True, keys: bool = True) -> str:
    window = rrp(7, 10.5, 56, 56, 3.5)
    body = rrp(0, 0, 70, 120, 10)
    s = [f'<g class="L-front">',
         f'<path d="{body}{window}" fill-rule="evenodd" fill="url(#{u}-sh)"/>',
         f'<rect x="7" y="10.5" width="56" height="56" rx="3.5" class="f-shell" opacity=".12"/>',
         # saturated rim: thick plastic looks deeper at the edges
         f'<g clip-path="url(#{u}-body)"><rect width="70" height="120" rx="10" fill="none" class="k-deep" stroke-width="6.5" opacity=".42" filter="url(#{u}-b1)"/></g>',
         # where the flat face ends and the round-over begins
         f'<rect x="3.5" y="3.5" width="63" height="113" rx="6.5" fill="none" stroke="#fff" stroke-width=".22" opacity=".5"/>',
         # glass seat
         f'<rect x="6.6" y="10.1" width="56.8" height="56.8" rx="3.8" fill="none" stroke="#fff" stroke-width=".32" opacity=".75"/>',
         f'<rect x="7" y="10.5" width="56" height="56" rx="3.5" fill="none" class="k-deep" stroke-width=".55" opacity=".5"/>',
         # earpiece + notification LED (glows through the plastic)
         f'<rect x="28" y="4.3" width="14" height="1.7" rx=".85" fill="#0d0a22" opacity=".8"/>',
         f'<rect x="28.3" y="5.6" width="13.4" height=".5" rx=".25" fill="#fff" opacity=".35"/>',
         # printed headphones glyph next to the jack (90s walkman-style marking)
         '<g fill="none" stroke="#fff" stroke-opacity=".8" stroke-width=".4" stroke-linecap="round" transform="translate(44 5.2)"><path d="M-1.9,.9V-.2A1.9,1.9 0 0 1 1.9,-.2V.9"/><rect x="-2.5" y=".2" width="1.1" height="2" rx=".4" fill="#fff" fill-opacity=".8"/><rect x="1.4" y=".2" width="1.1" height="2" rx=".4" fill="#fff" fill-opacity=".8"/></g>',
         f'<circle cx="19.5" cy="5.2" r="3.2" fill="url(#{u}-led)" opacity=".7"/>',
         f'<circle cx="19.5" cy="5.2" r=".6" class="f-led"/>',
         ]
    if keys:
        s.append(nav_markup(u))
        s.append(keys_markup(u, legends))
    s.append('</g>')
    return "\n".join(s)


def display(u: str, ui: bool = True) -> str:
    s = [f'<g class="L-display">',
         # module body + amber flex tail
         f'<rect x="32" y="66" width="6" height="5" fill="var(--flex)"/>',
         f'<rect x="5" y="8.5" width="60" height="60" rx="2.5" fill="#0a0820"/>',
         f'<rect x="7" y="10.5" width="56" height="56" rx="3.5" fill="url(#{u}-scrg)"/>']
    if ui:
        s.append(f'<g clip-path="url(#{u}-scr)">{screen_ui(u)}</g>')
    # glass sheen
    s.append(f'<path d="M7,10.5H43L7,50Z" fill="#fff" opacity=".10" clip-path="url(#{u}-scr)"/>')
    s.append('</g>')
    return "\n".join(s)


def app_icon(kind: str, cx: float, cy: float, c1: str, c2: str, u: str) -> str:
    g = {
        "msg": '<rect x="-2.8" y="-1.9" width="5.6" height="3.8" rx=".5" fill="none" stroke="#fff" stroke-width=".55"/><path d="M-2.8,-1.9L0,.4L2.8,-1.9" fill="none" stroke="#fff" stroke-width=".55" stroke-linejoin="round"/>',
        "phone": '<path d="M-2.4,2.2C-3,-.2 -1.4,-2.4 2.3,-2.6" fill="none" stroke="#fff" stroke-width="1.15" stroke-linecap="round"/><circle cx="-2.5" cy="2.3" r=".85" fill="#fff"/><circle cx="2.4" cy="-2.6" r=".85" fill="#fff"/>',
        "disc": f'<circle r="3.1" fill="#fff" opacity=".95"/><circle r="1.05" fill="{c2}"/><circle r="3.1" fill="none" stroke="{c2}" stroke-width=".3" opacity=".6"/><rect x="1.5" y="-1.3" width="2.2" height="2.6" fill="{c2}" opacity=".35"/>',
        "tape": f'<rect x="-3.3" y="-2.2" width="6.6" height="4.4" rx=".6" fill="#fff" opacity=".95"/><circle cx="-1.4" cy="-.4" r=".95" fill="{c2}"/><circle cx="1.4" cy="-.4" r=".95" fill="{c2}"/><rect x="-1.9" y="1.1" width="3.8" height=".75" rx=".35" fill="{c2}" opacity=".6"/>',
        "pet": f'<ellipse rx="2.7" ry="3.3" fill="#fff" opacity=".96"/><rect x="-1.5" y="-1.9" width="3" height="2.4" rx=".4" fill="{c2}"/><circle cx="-1.1" cy="1.7" r=".38" fill="{c2}"/><circle cx="0" cy="1.7" r=".38" fill="{c2}"/><circle cx="1.1" cy="1.7" r=".38" fill="{c2}"/>',
        "pin": f'<path d="M0,3.5C-2.7,.6 -2.7,-3.3 0,-3.3C2.7,-3.3 2.7,.6 0,3.5Z" fill="#fff"/><circle cy="-1" r="1.05" fill="{c2}"/>',
        "note": f'<rect x="-2.4" y="-3" width="4.8" height="6" rx=".6" fill="#fff"/><path d="M-1.4,-1.5H1.4M-1.4,-.1H1.4M-1.4,1.3H.5" stroke="{c2}" stroke-width=".45" stroke-linecap="round"/>',
        "gear": '<circle r="2.55" fill="none" stroke="#fff" stroke-width="1.15" stroke-dasharray=".95 .95"/><circle r="1.2" fill="#fff"/>',
    }[kind]
    return (f'<g transform="translate({n(cx)} {n(cy)})"><rect x="-4.25" y="-4.25" width="8.5" height="8.5" rx="2.3" fill="{c1}"/>'
            f'<rect x="-4.25" y="-4.25" width="8.5" height="3.9" rx="2.3" fill="#fff" opacity=".28"/>{g}</g>')


def screen_ui(u: str) -> str:
    bars = "".join(f'<rect x="{n(9.6 + i * 1.25)}" y="{n(15.3 - (i + 1) * .75)}" width=".85" height="{n((i + 1) * .75)}" fill="#d9fff1"/>' for i in range(4))
    icons = [("msg", "#ff6fb5", "#c4378a"), ("phone", "#38d985", "#13935a"), ("disc", "#4fc8ff", "#1b86c9"), ("tape", "#ffae42", "#c26d10"),
             ("pet", "#a58bff", "#6a45df"), ("pin", "#bfee3d", "#6f9a0b"), ("note", "#ffe066", "#b99410"), ("gear", "#8fa5d6", "#52669a")]
    ic = []
    for i, (k, c1, c2) in enumerate(icons):
        cx = 17 + (i % 4) * 12
        cy = 44.5 + (i // 4) * 11.2
        ic.append(app_icon(k, cx, cy, c1, c2, u))
    # keyboard-driven cursor on the pet icon
    cx, cy = 17, 55.7
    cursor = (f'<rect x="{n(cx - 5.2)}" y="{n(cy - 5.2)}" width="10.4" height="10.4" rx="3" fill="none" stroke="#fff" stroke-width=".55"/>'
              f'<rect x="{n(cx - 5.2)}" y="{n(cy - 5.2)}" width="10.4" height="10.4" rx="3" fill="none" stroke="#ffffff" stroke-width="1.4" opacity=".25" filter="url(#{u}-b1)"/>')
    battery = ('<rect x="55.2" y="12.3" width="5.2" height="2.7" rx=".5" fill="none" stroke="#d9fff1" stroke-width=".35"/>'
               '<rect x="55.7" y="12.8" width="3.8" height="1.7" rx=".25" fill="#d9fff1"/><rect x="60.5" y="13.1" width=".5" height="1.1" rx=".2" fill="#d9fff1"/>')
    # little pet living in the status bar
    pet = ('<g transform="translate(35 13.1)"><ellipse rx="1.35" ry="1.65" fill="#ffe27a"/><circle cx="-.45" cy="-.2" r=".22" fill="#2a1d6b"/>'
           '<circle cx=".45" cy="-.2" r=".22" fill="#2a1d6b"/><path d="M-.5,.55Q0,1 .5,.55" fill="none" stroke="#2a1d6b" stroke-width=".2" stroke-linecap="round"/></g>')
    return f'''
<rect x="7" y="10.5" width="56" height="5.4" fill="#000" opacity=".28"/>
{bars}<text class="t-mono" x="15.3" y="15.1" font-size="2.3" fill="#d9fff1">4G</text>
{pet}{battery}
<text class="t-disp" x="35.55" y="30.55" text-anchor="middle" font-size="9.6" fill="#ff4fd8" opacity=".8">12:07</text>
<text class="t-disp" x="35" y="30" text-anchor="middle" font-size="9.6" fill="#c8fff0">12:07</text>
<text class="t-mono" x="35" y="35.4" text-anchor="middle" font-size="2.5" fill="#b9b0ff" letter-spacing=".3">MON 26 OCT</text>
{"".join(ic)}
{cursor}
<text class="t-mono" x="10" y="64.9" font-size="2.2" fill="#d9fff1" opacity=".85">MENU</text>
<text class="t-mono" x="60" y="64.9" font-size="2.2" fill="#d9fff1" opacity=".85" text-anchor="end">BACK</text>
'''


def kbd_board(u: str) -> str:
    s = [f'<g class="L-kbd">',
         f'<rect x="4" y="69" width="62" height="42.5" rx="2" fill="url(#{u}-kb)" stroke="#0b1119" stroke-width=".3"/>',
         f'<rect x="4" y="69" width="62" height="42.5" rx="2" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width=".3"/>']
    pts = [(x, NAV_Y) for x in (9.5, 20.5, 35, 49.5, 60.5)]
    for r in range(4):
        y = ROW_TOP + KH / 2 + r * PY
        for c in (range(10) if r < 3 else (0, 1, 8, 9)):
            pts.append((kx(c), y))
    pts.append((35, ROW_TOP + KH / 2 + 3 * PY))
    for x, y in pts:
        s.append(f'<circle cx="{n(x)}" cy="{n(y)}" r="3.4" class="f-light" opacity=".16" filter="url(#{u}-b2)"/>')   # backlight bleed
    for x, y in pts:
        s.append(f'<circle cx="{n(x)}" cy="{n(y)}" r="1.7" fill="none" stroke="url(#{u}-gold)" stroke-width=".32"/>')
    s.append(f'<rect x="31" y="69.8" width="8" height="1.6" fill="url(#{u}-gold)" opacity=".9"/>')
    s.append('</g>')
    return "\n".join(s)


def chip(x, y, w, h, u, label=None, r=.5):
    return (f'<g><rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" rx="{r}" fill="url(#{u}-chip)" stroke="#000" stroke-opacity=".5" stroke-width=".2"/>'
            f'<rect x="{n(x + .4)}" y="{n(y + .35)}" width="{n(w - .8)}" height="{n(min(1.6, h * .3))}" rx=".4" fill="#fff" opacity=".12"/>'
            f'<circle cx="{n(x + 1.0)}" cy="{n(y + h - 1.0)}" r=".32" fill="#fff" opacity=".55"/></g>')


def can(x, y, w, h, u):
    ridges = "".join(f'<path d="M{n(x + 1)},{n(y + 1.5 + i * 1.8)}H{n(x + w - 1)}" stroke="#7d8798" stroke-opacity=".5" stroke-width=".18"/>' for i in range(int((h - 2) / 1.8)))
    return (f'<g><rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" rx=".7" fill="url(#{u}-metal)" stroke="#6c7686" stroke-width=".2"/>'
            f'{ridges}<rect x="{n(x + .5)}" y="{n(y + .4)}" width="{n(w - 1)}" height="1" rx=".4" fill="#fff" opacity=".55"/></g>')


def mainboard(u: str, jack: bool = True, lte: bool = True) -> str:
    random.seed(7)
    s = ['<g class="L-main">',
         f'<g mask="url(#{u}-pcbm)">',
         f'<rect x="4" y="5" width="62" height="64" rx="4" fill="url(#{u}-pcb)" stroke="#000" stroke-opacity=".35" stroke-width=".3"/>',
         f'<rect x="4.4" y="5.4" width="61.2" height="63.2" rx="3.7" fill="none" stroke="#fff" stroke-opacity=".18" stroke-width=".3"/>']
    traces = ["M33,18H39", "M33,22.5H36V28H39", "M19,17H13V13", "M24,28V35.5", "M28,28V33H22V35.5", "M49,32V43.5",
              "M52,32V40H44V43.5", "M50.5,12H46V16", "M47,52.5V56H36", "M18,48.5V54H26V56.5", "M14,35.5V30H9V40",
              "M56,32V38H62V50", "M40,23H36", "M21.5,10.5H27V14", "M57.5,12H62V20", "M30,35.5V44H40", "M14,50V60H20"]
    for t in traces:
        s.append(f'<path d="{t}" fill="none" stroke="#fff" stroke-opacity=".24" stroke-width=".32" stroke-linejoin="round"/>')
    for _ in range(46):
        x, y = random.uniform(7, 63), random.uniform(7, 66)
        if any(a < x < b and c < y < d for a, b, c, d in [(8, 61, 6, 62)] if False):
            continue
        s.append(f'<circle cx="{n(x)}" cy="{n(y)}" r=".3" fill="url(#{u}-gold)" opacity=".55"/>')
    # decoupling caps
    for y in [15.5, 17.9, 20.3, 22.7, 25.1, 27.5]:
        s.append(f'<rect x="16.9" y="{n(y)}" width=".9" height=".55" fill="#d9c9a1"/><rect x="34.2" y="{n(y)}" width=".9" height=".55" fill="#d9c9a1"/>')
    s.append(chip(19, 14, 14, 14, u))                      # SoC
    s.append(can(39, 16, 20, 16, u))                       # modem + can
    if lte:
        s.append(f'<text class="t-mono" x="49" y="24.9" text-anchor="middle" font-size="2.6" fill="#4a5568" opacity=".85">LTE</text>')
    s.append(can(10, 35.5, 16, 13, u))                     # shield can
    s.append(f'<rect x="40" y="43.5" width="14" height="9" rx=".6" fill="url(#{u}-gold)" stroke="#8a6414" stroke-width=".2" opacity=".95"/>'
             f'<rect x="41" y="44.3" width="12" height="2.2" rx=".4" fill="#fff" opacity=".4"/>')   # wifi/bt module
    s.append(chip(50.5, 9, 7, 7, u, r=.4))                 # codec
    s.append(chip(12.5, 8, 9, 5, u, r=.4))                 # PMIC
    s.append('<rect x="26" y="56.5" width="10" height="4" rx=".5" fill="#f4f1e8" stroke="#a8a290" stroke-width=".2"/>'
             '<path d="M27.2,57.6H34.8M27.2,59.4H34.8" stroke="#bcb6a0" stroke-width=".3"/>')      # battery connector
    s.append('</g>')   # end mask
    if jack:
        s.append(f'<g><rect x="47.8" y="1.2" width="6.4" height="6.2" rx="1.2" fill="url(#{u}-metal)" stroke="#5f6878" stroke-width=".25"/>'
                 f'<rect x="48.6" y="1.9" width="4.8" height="1.1" rx=".5" fill="#fff" opacity=".6"/>'
                 f'<circle cx="51" cy="4.7" r="1.35" fill="#1a1c26"/><circle cx="51" cy="4.7" r=".55" fill="#4a5262"/></g>')
    s.append('</g>')
    return "\n".join(s)


def chin(u: str) -> str:
    zig = "M9,112.4" + "".join(f"l1.8,{'-1.6' if i % 2 == 0 else '1.6'}" for i in range(12))
    return f'''<g class="L-chin">
<rect x="7" y="112" width="56" height="6.4" rx="1.8" fill="url(#{u}-kb)" opacity=".92" stroke="#0b1119" stroke-width=".25"/>
<path d="{zig}" fill="none" stroke="url(#{u}-gold)" stroke-width=".38" stroke-linejoin="round" transform="translate(0 1.8)"/>
<rect x="30.3" y="113.2" width="9.4" height="4.9" rx="1.7" fill="url(#{u}-metal)" stroke="#6c7686" stroke-width=".2"/>
<rect x="31.6" y="114.7" width="6.8" height="1.7" rx=".85" fill="#12131a"/>
<rect x="46.5" y="113.4" width="14.5" height="4.6" rx="1" fill="url(#{u}-chip)" stroke="#000" stroke-opacity=".5" stroke-width=".2"/>
{"".join(f'<circle cx="{n(48 + i * 2.2)}" cy="115.7" r=".55" fill="#9aa3b2" opacity=".75"/>' for i in range(6))}
<circle cx="21" cy="115.7" r=".9" fill="#12131a"/><circle cx="21" cy="115.7" r=".9" fill="none" stroke="url(#{u}-metal)" stroke-width=".25"/>
</g>'''


def battery(u: str, label: bool = True) -> str:
    s = ['<g class="L-batt">',
         # wires out of the protection board
         '<path d="M17,72C17,66 27,65 29.6,61" fill="none" stroke="#e5484d" stroke-width=".55" stroke-linecap="round"/>',
         '<path d="M21.5,72C21.5,67 29.5,66.5 32,61" fill="none" stroke="#1a1a22" stroke-width=".55" stroke-linecap="round"/>',
         f'<rect x="7" y="71.5" width="56" height="40" rx="3.2" fill="url(#{u}-batt)" stroke="#a46a07" stroke-width=".35"/>',
         '<rect x="8.4" y="72.9" width="53.2" height="37.2" rx="2.4" fill="none" stroke="#fff" stroke-width=".25" opacity=".45"/>',
         '<rect x="12" y="71.5" width="18" height="3.4" fill="#b9732a"/><rect x="13" y="72.2" width="5" height="1.6" rx=".3" fill="#ffd9a0" opacity=".7"/>',
         '<rect x="8" y="73" width="54" height="9" rx="2" fill="#fff" opacity=".18"/>']
    if label:
        s.append('<rect x="14" y="84" width="42" height="20" rx="1.2" fill="var(--label)" opacity=".94"/>'
                 '<rect x="14" y="84" width="42" height="20" rx="1.2" fill="none" stroke="#c9b27a" stroke-width=".25"/>')
    s.append('</g>')
    return "\n".join(s)


def battery_text() -> str:
    return '''<g class="battery-text" fill="#2a2113">
<text class="t-disp" x="35" y="90" text-anchor="middle" font-size="4.3" letter-spacing=".5">SHEER</text>
<text class="t-mono" x="35" y="94.3" text-anchor="middle" font-size="2.15" letter-spacing=".1">LI-ION POLYMER · 3.7V</text>
<text class="t-disp" x="35" y="99.6" text-anchor="middle" font-size="4.1">3000mAh</text>
<text class="t-mono" x="35" y="102.8" text-anchor="middle" font-size="1.85" opacity=".75">11.1Wh · DO NOT PUNCTURE · PROTOTYPE</text>
</g>'''


def silkscreen() -> str:
    return '''<text class="t-mono" x="21" y="24.9" text-anchor="middle" font-size="2.6" fill="#4a5568" opacity=".85">LTE</text>
<g fill="#fff" fill-opacity=".62" class="t-mono">
<text x="35" y="66.4" text-anchor="middle" font-size="2" letter-spacing=".5">SHEER S-1 · REV A · PROTOTYPE</text>
<text x="35" y="64" text-anchor="middle" font-size="1.55" fill-opacity=".4">NOT FCC CERTIFIED · DO NOT SELL</text>
</g>'''


def back_shell(u: str, screws: bool = True) -> str:
    s = ['<g class="L-back">',
         f'<rect width="70" height="120" rx="10" fill="url(#{u}-sh)"/>',
         f'<g clip-path="url(#{u}-body)"><rect width="70" height="120" rx="10" fill="none" class="k-deep" stroke-width="6.5" opacity=".42" filter="url(#{u}-b1)"/></g>',
         '<rect x="3.5" y="3.5" width="63" height="113" rx="6.5" fill="none" stroke="#fff" stroke-width=".22" opacity=".5"/>']
    for x, y in POSTS:
        s.append(f'<circle cx="{x}" cy="{y}" r="3.1" class="f-light" opacity=".38"/><circle cx="{x}" cy="{y}" r="3.1" fill="none" class="k-deep" stroke-width=".3" opacity=".6"/>')
        if screws:
            s.append(f'<circle cx="{x}" cy="{y}" r="2.25" fill="url(#{u}-metal)" stroke="#5b6475" stroke-width=".25"/>'
                     f'<path d="M{x - 1.4},{y}H{x + 1.4}M{x},{y - 1.4}V{y + 1.4}" stroke="#4a5262" stroke-width=".5" stroke-linecap="round"/>'
                     f'<path d="M{x - 1.7},{y - .9}A2 2 0 0 1 {x - .5},{y - 1.9}" fill="none" stroke="#fff" stroke-width=".35" stroke-linecap="round"/>')
    s.append('</g>')
    return "\n".join(s)


def sheen(u: str) -> str:
    """Specular highlights: drawn last so they sit on the outside surface."""
    return f'''<g class="sheen" clip-path="url(#{u}-body)" pointer-events="none">
<path d="M0,0H52L0,74Z" fill="url(#{u}-hl)" opacity=".5"/>
<path d="M9,0H19L0,34V22Z" fill="url(#{u}-hl2)" opacity=".55"/>
<path d="M60,120H70V108L52,120Z" class="f-light" opacity=".35"/>
</g>
<g pointer-events="none" fill="none" stroke-linecap="round">
<path d="M10.5,.5H59.5" stroke="#fff" stroke-width=".55" opacity=".85"/>
<path d="M.5,10.5V70" stroke="#fff" stroke-width=".45" opacity=".55"/>
<path d="M2.2,4.6Q3,2.8 5.2,1.9" stroke="#fff" stroke-width=".7" opacity=".95"/>
<path d="M69.4,40V110" class="k-light" stroke-width=".7" opacity=".55"/>
<path d="M12,119.5H58" class="k-light" stroke-width=".7" opacity=".6"/>
</g>'''


def side_buttons(u: str) -> str:
    return (f'<rect x="-1.05" y="25" width="1.6" height="16" rx=".7" fill="url(#{u}-sh)" class="k-deep" stroke-width=".25" stroke-opacity=".6"/>'
            f'<rect x="69.45" y="28.5" width="1.6" height="9" rx=".7" fill="url(#{u}-sh)" class="k-deep" stroke-width=".25" stroke-opacity=".6"/>')


def ground(u: str) -> str:
    """Soft coloured shadow: translucent plastic throws coloured light."""
    return (f'<g pointer-events="none"><rect x="3" y="7" width="70" height="120" rx="10" class="f-glow" opacity=".55" filter="url(#{u}-b4)"/>'
            f'<rect x="2" y="5" width="70" height="120" rx="10" fill="#1b1340" opacity=".16" filter="url(#{u}-b2)"/></g>')


# ---------------------------------------------------------------------------
# views
# ---------------------------------------------------------------------------

def svg_open(u: str, cw: str | None, cls: str, label: str, viewbox: str = VIEWBOX) -> str:
    cwattr = f' data-cw="{cw}"' if cw else ""
    return (f'<svg class="phone {cls}"{cwattr} viewBox="{viewbox}" role="img" aria-label="{label}" '
            f'xmlns="http://www.w3.org/2000/svg">')


def front_view(u: str, cw: str | None = None, cls: str = "", legends: bool = True) -> str:
    return "\n".join([
        svg_open(u, cw, cls, "SHEER, front view: see-through phone with screen, D-pad and QWERTY keyboard"),
        defs(u), ground(u),
        back_shell(u, screws=False), battery(u, label=False), chin(u), mainboard(u), display(u), kbd_board(u),
        front_shell(u, legends=legends), side_buttons(u), sheen(u), "</svg>"])


def back_view(u: str, cw: str | None = None, cls: str = "") -> str:
    inner = "\n".join([front_shell(u, keys=False), kbd_board(u), display(u, ui=False), chin(u), mainboard(u, lte=False), battery(u), back_shell(u)])
    return "\n".join([
        svg_open(u, cw, cls, "SHEER, back view: clear shell showing mainboard, battery and screws"),
        defs(u), ground(u),
        f'<g transform="translate(70 0) scale(-1 1)">{inner}{side_buttons(u)}</g>',
        # text on the battery label and board is drawn un-mirrored, in back-view space
        silkscreen(), battery_text(), sheen(u), "</svg>"])


# exploded stack ------------------------------------------------------------

EXPLODE_LAYERS = [
    # id, title, subtitle, anchor in plan space (x, y), builder
    ("front", "SKIN", "front shell + keys", (70, 20), lambda u: front_shell(u)),
    ("kbd", "FINGERS", "QWERTY board", (66, 75), lambda u: kbd_board(u)),
    ("display", "EYES", "screen module", (65, 50), lambda u: display(u)),
    ("main", "BRAIN", "chip, modem, SIM, jack", (66, 30), lambda u: mainboard(u) + chin(u)),
    ("batt", "HEART", "battery", (63, 80), lambda u: battery(u)),
    ("back", "SKIN", "back shell + screws", (70, 75), lambda u: back_shell(u)),
]
SKEW = (1, 0, -.34, .46, 0, 0)


def exploded_view(u: str, cw: str | None = None, cls: str = "") -> str:
    vb = "-46 -6 200 262"
    a, b, c, d, e, f = SKEW
    parts = [svg_open(u, cw, f"exploded {cls}", "Exploded view of the SHEER phone: front shell, keyboard board, display, mainboard, battery and back shell", vb), defs(u)]
    for i, (lid, title, sub, (ax, ay), builder) in enumerate(EXPLODE_LAYERS):
        px, py = a * ax + c * ay, b * ax + d * ay           # anchor after the skew
        slab = ""
        if lid in ("front", "back"):
            slab = f'<rect x="3" y="7" width="64" height="116" rx="10" class="f-glow" opacity=".30" filter="url(#{u}-b2)" pointer-events="none"/>'
        parts.append(
            f'<g class="xl" data-layer="{lid}" style="--i:{i}" tabindex="0" role="button" aria-label="{title}: {sub}">'
            f'<g transform="matrix({a} {b} {c} {d} {e} {f})">{slab}{builder(u)}</g>'
            f'<path class="xl-lead" d="M{n(px + 1.5)},{n(py)}H{n(88)}" fill="none"/>'
            f'<circle class="xl-dot" cx="{n(px)}" cy="{n(py)}" r="1.5"/>'
            f'<text class="xl-t" x="91" y="{n(py + 1.6)}">{title}</text>'
            f'<text class="xl-s" x="91" y="{n(py + 6.6)}">{sub}</text>'
            f'</g>')
    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    print(len(front_view("t")), len(back_view("b")), len(exploded_view("x")))
