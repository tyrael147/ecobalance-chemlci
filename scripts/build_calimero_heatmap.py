"""Build figures/fig-calimero-performance.svg from data/calimero/heatmap.json (stdlib only)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = json.loads((ROOT / "data/calimero/heatmap.json").read_text())
OUT = ROOT / "figures/fig-calimero-performance.svg"

S = 1570 / 3939  # source px -> viewBox units
GX0, GX1, GY0, GY1 = 754 * S, 3468 * S, 82 * S, 2975 * S
rows, cols = D["rows"], D["cols"]
CW, CH = (GX1 - GX0) / len(cols), (GY1 - GY0) / len(rows)
FONT = 'font-family="Raleway, Arial, sans-serif"'
W, H = 1570, 1245


def lum(hexc):
    v = []
    for i in (1, 3, 5):
        c = int(hexc[i:i + 2], 16) / 255
        v.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]


o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">']
o.append(f'<g id="title"><text x="{(GX0 + GX1) / 2:.1f}" y="{21:.1f}" text-anchor="middle" '
         f'font-size="21" fill="#222" {FONT}>Best algorithm and data combination per cluster</text></g>')

# axes
a = ['<g id="axes">']
for r, name in enumerate(rows):
    y = GY0 + (r + 0.5) * CH
    a.append(f'<text x="{GX0 - 12:.1f}" y="{y + 5:.1f}" text-anchor="end" font-size="14.5" fill="#222" {FONT}>{name}</text>')
    a.append(f'<line x1="{GX0 - 6:.1f}" y1="{y:.1f}" x2="{GX0:.1f}" y2="{y:.1f}" stroke="#222" stroke-width="1"/>')
for c, name in enumerate(cols):
    x = GX0 + (c + 0.5) * CW
    a.append(f'<text x="{x:.1f}" y="{GY1 + 28:.1f}" text-anchor="middle" font-size="14.5" fill="#222" {FONT}>{name}</text>')
    a.append(f'<line x1="{x:.1f}" y1="{GY1:.1f}" x2="{x:.1f}" y2="{GY1 + 6:.1f}" stroke="#222" stroke-width="1"/>')
a.append(f'<text x="{GX0 + (GX1 - GX0) / 2:.1f}" y="{GY1 + 50:.1f}" text-anchor="middle" font-size="15" fill="#222" {FONT}>Chemical Cluster</text>')
a.append(f'<text transform="translate(14 {(GY0 + GY1) / 2:.1f}) rotate(-90)" text-anchor="middle" font-size="15" fill="#222" {FONT}>Target</text>')
a.append('</g>')
o += a

# colorbar
BX0, BX1 = 3640 * S, 3785 * S
vmin, vmax = D["vmin"], D["vmax"]
by0, by1 = 81 * S, 2975 * S
c = ['<g id="colorbar">', '<defs><linearGradient id="calimero-cb" x1="0" y1="0" x2="0" y2="1">']
for off, col in D["colorbar"]:
    c.append(f'<stop offset="{off}" stop-color="{col}"/>')
c.append('</linearGradient></defs>')
c.append(f'<rect x="{BX0:.1f}" y="{by0:.1f}" width="{BX1 - BX0:.1f}" height="{by1 - by0:.1f}" fill="url(#calimero-cb)"/>')
for t in (0.2, 0.3, 0.4, 0.5, 0.6, 0.7):
    y = by0 + (vmax - t) / (vmax - vmin) * (by1 - by0)
    c.append(f'<line x1="{BX1:.1f}" y1="{y:.1f}" x2="{BX1 + 5:.1f}" y2="{y:.1f}" stroke="#222" stroke-width="1"/>')
    c.append(f'<text x="{BX1 + 9:.1f}" y="{y + 5:.1f}" font-size="14.5" fill="#222" {FONT}>{t}</text>')
c.append(f'<text transform="translate({BX1 + 52:.1f} {(by0 + by1) / 2:.1f}) rotate(-90)" text-anchor="middle" font-size="15" fill="#222" {FONT}>Max R2</text>')
c.append('</g>')
o += c

for cell in D["cells"]:
    r, cc = cell["r"], cell["c"]
    x, y = GX0 + cc * CW, GY0 + r * CH
    tc = "#222222" if lum(cell["color"]) > 0.408 else "#ffffff"
    cx = x + CW / 2
    o.append(f'<g id="cell-r{r}-c{cc}">'
             f'<rect x="{x:.2f}" y="{y:.2f}" width="{CW:.2f}" height="{CH:.2f}" fill="{cell["color"]}" stroke="#ffffff" stroke-width="1"/>'
             f'<text x="{cx:.1f}" y="{y + CH / 2 - 2:.1f}" text-anchor="middle" font-size="11" fill="{tc}" {FONT}>{cell["algo"]}</text>'
             f'<text x="{cx:.1f}" y="{y + CH / 2 + 11:.1f}" text-anchor="middle" font-size="11" fill="{tc}" {FONT}>({cell["rep"]})</text></g>')
o.append('</svg>')
OUT.write_text("\n".join(o) + "\n")
