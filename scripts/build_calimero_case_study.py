#!/usr/bin/env python3
"""Build figures/fig-calimero-case-study.svg from data/calimero/case_study.json.

Stdlib only. Run as: python3 -I scripts/build_calimero_case_study.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "calimero", "case_study.json")
OUT = os.path.join(ROOT, "figures", "fig-calimero-case-study.svg")

W, H = 1000, 620
X0, X1 = 120, 860              # plot left / right edges
Y_TOP, Y_BASE = 70, 450        # top of plot and zero line
L_MAX, L_STEP = 120.0, 20.0    # left axis: EcoTox (CTUe)
R_MAX, R_STEP = 7e-8, 1e-8     # right axis: HTox (CTUh)
SLOT_W = (X1 - X0) / 4.0       # four product slots (2 groups x 2 products)
BAR_W, BAR_GAP = 56, 6
BLUE, GREEN = "#3a6182", "#62ae55"
GRID, FRAME, TEXT = "#e3e3e3", "#cfcfcf", "#404040"
FONT = "Raleway, Arial, sans-serif"

SCENARIOS = ["without predicted CFs", "with predicted CFs"]
PRODUCTS = ["pumice stone", "synthetic stone"]
GROUP_IDS = {"without predicted CFs": "bars-without", "with predicted CFs": "bars-with"}


def ly(v):
    return Y_BASE - v * (Y_BASE - Y_TOP) / L_MAX


def ry(v):
    return Y_BASE - v * (Y_BASE - Y_TOP) / R_MAX


def num(x):
    s = f"{x:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


def line(x1, y1, x2, y2, stroke, width=1):
    return (f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" '
            f'stroke="{stroke}" stroke-width="{width}"/>')


def text(x, y, s, size, anchor="middle", weight=None, fill=TEXT):
    w = f' font-weight="{weight}"' if weight else ""
    return (f'<text x="{num(x)}" y="{num(y)}" font-size="{size}" text-anchor="{anchor}"'
            f'{w} fill="{fill}">{s}</text>')


def rect(x, y, w, h, fill, rid):
    return (f'<rect id="{rid}" x="{num(x)}" y="{num(y)}" width="{num(w)}" '
            f'height="{num(h)}" fill="{fill}"/>')


def sci(v):
    """Right-axis tick label in the source's style, e.g. 3.00E-08 or 0.00E+00."""
    if v == 0:
        return "0.00E+00"
    return f"{v * 1e8:.2f}E-08"


def axes_group():
    out = ['<g id="axes" font-size="16">']
    # gridlines and left-axis ticks (EcoTox)
    v = 0.0
    while v <= L_MAX + 1e-9:
        y = ly(v)
        if v == 0:
            out.append(line(X0, y, X1, y, FRAME, 1.2))
        else:
            out.append(line(X0, y, X1, y, GRID, 1))
        out.append(line(X0 - 6, y, X0, y, FRAME, 1))
        out.append(text(X0 - 10, y + 5.5, num(v), 16, anchor="end"))
        v += L_STEP
    # right-axis ticks (HTox)
    k = 0
    while k * R_STEP <= R_MAX + 1e-15:
        y = ry(k * R_STEP)
        out.append(line(X1, y, X1 + 6, y, FRAME, 1))
        out.append(text(X1 + 10, y + 5.5, sci(k * R_STEP), 15, anchor="start"))
        k += 1
    # plot frame sides and group dividers
    out.append(line(X0, Y_TOP, X0, Y_BASE, FRAME, 1))
    out.append(line(X1, Y_TOP, X1, Y_BASE, FRAME, 1))
    for gi in range(3):
        x = X0 + gi * 2 * SLOT_W
        out.append(line(x, Y_BASE, x, Y_BASE + 92, FRAME, 1))
    # axis titles
    out.append(f'<text x="30" y="{num((Y_TOP + Y_BASE) / 2)}" font-size="20" '
               f'text-anchor="middle" fill="{TEXT}" '
               f'transform="rotate(-90 30 {num((Y_TOP + Y_BASE) / 2)})">EcoTox (CTUe)</text>')
    cx_r = 968
    out.append(f'<text x="{cx_r}" y="{num((Y_TOP + Y_BASE) / 2)}" font-size="20" '
               f'text-anchor="middle" fill="{TEXT}" '
               f'transform="rotate(-90 {cx_r} {num((Y_TOP + Y_BASE) / 2)})">HTox (CTUh)</text>')
    # x labels: products (row 1) and scenarios (row 2)
    for gi, scen in enumerate(SCENARIOS):
        for pi, prod in enumerate(PRODUCTS):
            cx = X0 + (gi * 2 + pi) * SLOT_W + SLOT_W / 2
            out.append(text(cx, Y_BASE + 30, prod, 18, weight="bold", fill="#111"))
        gc = X0 + gi * 2 * SLOT_W + SLOT_W
        out.append(text(gc, Y_BASE + 78, scen, 20, weight="bold", fill="#111"))
    out.append("</g>")
    return "\n".join(out)


def legend_group():
    out = ['<g id="legend" font-size="20">']
    out.append(rect(290, 12, 18, 18, BLUE, "legend-swatch-ecotox"))
    out.append(text(316, 27, "Ecotoxicity, freshwater", 20, anchor="start"))
    out.append(rect(580, 12, 18, 18, GREEN, "legend-swatch-htox"))
    out.append(text(606, 27, "Human toxicity, total", 20, anchor="start"))
    out.append("</g>")
    return "\n".join(out)


def bars_group(scen, items):
    gid = GROUP_IDS[scen]
    gi = SCENARIOS.index(scen)
    out = [f'<g id="{gid}">']
    for pi, prod in enumerate(PRODUCTS):
        item = items[(scen, prod)]
        slot = gi * 2 + pi
        cx = X0 + slot * SLOT_W + SLOT_W / 2
        bx = cx - (2 * BAR_W + BAR_GAP) / 2
        gx = bx + BAR_W + BAR_GAP
        tag = f"{'wo' if gi == 0 else 'w'}-{prod.split()[0]}"
        yb = ly(item["ecotox_ctue"])
        out.append(rect(bx, yb, BAR_W, Y_BASE - yb, BLUE, f"{tag}-ecotox"))
        yg = ry(item["htox_ctuh"])
        out.append(rect(gx, yg, BAR_W, Y_BASE - yg, GREEN, f"{tag}-htox"))
    out.append("</g>")
    return "\n".join(out)


def main():
    with open(DATA, encoding="utf-8") as fh:
        data = json.load(fh)
    items = {(it["scenario"], it["product"]): it for it in data["items"]}
    for scen in SCENARIOS:
        for prod in PRODUCTS:
            if (scen, prod) not in items:
                raise SystemExit(f"missing item: {scen} / {prod}")

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'font-family="{FONT}">',
        axes_group(),
        legend_group(),
    ]
    for scen in SCENARIOS:
        parts.append(bars_group(scen, items))
    parts.append("</svg>")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
