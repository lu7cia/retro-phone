#!/usr/bin/env python3
"""Build design/site/index.html from page_template.html + art.py + content.py.

    python design/build_page.py

Needs only the standard library. Images in design/site/img/ come from design/make_images.py.
"""
from __future__ import annotations

import os
import re
import sys
from html import escape, unescape

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import art          # noqa: E402
import content as C  # noqa: E402

FLAG = ('<svg viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M3 1.5h1.6v13H3zM5.2 2.4c2.1-1.3 3.7 1.1 6.2-.1l1.6-.8v6.2l-1.6.8c-2.5 1.2-4.1-1.2-6.2.1z"/></svg>')
N_TURN = 24


def stage_html(s: dict) -> str:
    items = []
    for tid, title, desc, help_html in s["tasks"]:
        items.append(
            f'<li><label class="task"><input class="task-box" type="checkbox" data-id="{tid}">'
            f'<span><span class="t">{escape(title)}</span><span class="d">{escape(desc)}</span></span></label>'
            f'<details class="task-more"><summary>How</summary><div class="task-help">{help_html}</div></details></li>')
    meta = "".join(f"<span>{escape(m)}</span>" for m in s["meta"])
    return (
        f'<details class="stage-card" data-short="{s["short"]}"{" open" if s["open"] else ""}>'
        f'<summary><div class="stage-sum"><span class="num">{s["n"]}</span>'
        f'<span><h3>{escape(s["title"])}</h3><span class="meta">{meta}</span></span>'
        f'<span class="stage-end"><span class="prog">0/{len(s["tasks"])}</span><span class="chev"></span></span></div></summary>'
        f'<div class="stage-body"><p class="done-when"><b>Done when</b>{escape(s["done"])}</p>'
        f'<ul class="tasks">{"".join(items)}</ul></div></details>')


def shop_html() -> str:
    rows = []
    for part, why, price, buy in C.SHOP:
        link = (f'<a href="{escape(buy[0], quote=True)}" target="_blank" rel="noopener noreferrer">{escape(buy[1])}</a>'
                if buy else '<span class="w">any shop</span>')
        rows.append(f'<div class="shop-row"><span class="p">{escape(part)}</span><span class="w">{escape(why)}</span>'
                    f'<span class="c">{escape(price)}</span><span>{link}</span></div>')
    return "\n".join(rows)


def links_html() -> str:
    cards = []
    for title, items in C.LINKS:
        lis = "".join(
            f'<li><a href="{escape(h, quote=True)}" target="_blank" rel="noopener noreferrer">{escape(t)}</a><span>{escape(d)}</span></li>'
            for h, t, d in items)
        cards.append(f'<div class="linkcard"><h3>{escape(title)}</h3><ul>{lis}</ul></div>')
    return "\n".join(cards)


def alerts_html() -> str:
    out = []
    for i, (title, body) in enumerate(C.ALERTS, 1):
        out.append(f'<div class="alert"><span class="flag">{FLAG}Alert {i}</span><h3>{escape(title)}</h3><p>{body}</p></div>')
    return "\n".join(out)


def notes_html() -> str:
    return "\n".join(f'<div class="note"><h3>{escape(t)}</h3><p>{escape(d)}</p></div>' for t, d in C.NOTES)


def sources_html() -> str:
    return "\n".join(f'<li><a href="{escape(h, quote=True)}" target="_blank" rel="noopener noreferrer">{escape(t)}</a></li>' for h, t in C.SOURCES)


def turn_html() -> str:
    return "".join(f'<img src="img/turn_{i:02d}.jpg" width="560" height="760" alt="" decoding="async">' for i in range(N_TURN))


def build() -> str:
    tpl = open(os.path.join(HERE, "page_template.html"), encoding="utf-8").read()
    # task-help is shown inside <details> now; make sure the template CSS reflects that
    css = open(os.path.join(HERE, "art.css"), encoding="utf-8").read()
    repl = {
        "{{ART_CSS}}": css,
        "{{ART_HERO_FRONT}}": art.front_view("hf", cls="p-front"),
        "{{ART_HERO_BACK}}": art.back_view("hb", cls="p-back"),
        "{{ART_EXPLODED}}": art.exploded_view("ex"),
        "{{TURN_IMGS}}": turn_html(),
        "{{STAGES}}": "\n".join(stage_html(s) for s in C.STAGES),
        "{{SHOP}}": shop_html(),
        "{{LINKS}}": links_html(),
        "{{ALERTS}}": alerts_html(),
        "{{NOTES}}": notes_html(),
        "{{SOURCES}}": sources_html(),
    }
    for k, v in repl.items():
        if k not in tpl:
            raise SystemExit(f"placeholder missing in template: {k}")
        tpl = tpl.replace(k, v)
    return tpl


# ---------------------------------------------------------------------------
# docs/PLAN.md, generated from the same content so page and doc never drift
# ---------------------------------------------------------------------------

def to_md(h: str) -> str:
    h = re.sub(r"<a [^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", lambda m: f"[{m.group(2)}]({m.group(1)})", h, flags=re.S)
    h = re.sub(r"<span class=['\"]mono['\"]>(.*?)</span>", r"`\1`", h)
    h = re.sub(r"<b>(.*?)</b>", r"**\1**", h)
    h = re.sub(r"<li>", "- ", h)
    h = re.sub(r"</li>", "\n", h)
    h = re.sub(r"</?(ol|ul)>", "\n", h)
    h = re.sub(r"</p>", "\n\n", h)
    h = re.sub(r"<[^>]+>", "", h)
    h = unescape(h)
    h = h.replace("[shopping list](#shopping)", "shopping list below")
    return re.sub(r"\n{3,}", "\n\n", h).strip()


def plan_markdown() -> str:
    out = ["# SHEER: the plan", "",
           "_Generated from `design/content.py` by `design/build_page.py`. Edit the content file, not this one._", "",
           "Five stages. Do one small thing at a time. Money and time are rough ballparks, not quotes.", ""]
    for s in C.STAGES:
        out += [f"## Stage {s['n']}: {s['title']}", "", f"{' · '.join(s['meta'])}", "", f"**Done when:** {s['done']}", ""]
        for tid, title, desc, help_html in s["tasks"]:
            out.append(f"- [ ] **{title}**. {desc}")
            for line in to_md(help_html).splitlines():
                out.append(f"  {line}" if line.strip() else "")
        out.append("")
    out += ["## Stage 1 shopping list", "", "| Part | Why | About | Link |", "|---|---|---|---|"]
    for part, why, price, buy in C.SHOP:
        out.append(f"| {part} | {why} | {price} | {'[' + buy[1] + '](' + buy[0] + ')' if buy else 'any shop'} |")
    out += ["", "Prices are rough guesses. Check the live listing.", "", "## Websites for every stage", ""]
    for title, items in C.LINKS:
        out.append(f"**{title}**")
        out += [f"- [{t}]({h}): {d}" for h, t, d in items]
        out.append("")
    out += ["## Bullshit alerts", ""]
    for i, (title, body) in enumerate(C.ALERTS, 1):
        out.append(f"{i}. **{title}.** {to_md(body)}")
    out += ["", "## Sources", ""] + [f"- [{t}]({h})" for h, t in C.SOURCES] + [""]
    return "\n".join(out)


if __name__ == "__main__":
    out_dir = os.path.join(HERE, "site")
    os.makedirs(os.path.join(out_dir, "img"), exist_ok=True)
    html = build()
    path = os.path.join(out_dir, "index.html")
    open(path, "w", encoding="utf-8").write(html)
    print(f"wrote {path}  ({len(html) / 1024:.0f} KB)")
    docs = os.path.join(os.path.dirname(HERE), "docs")
    os.makedirs(docs, exist_ok=True)
    open(os.path.join(docs, "PLAN.md"), "w", encoding="utf-8").write(plan_markdown())
    print("wrote docs/PLAN.md")
