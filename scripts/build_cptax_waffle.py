"""Build figures/fig-cptax-waffle.svg: categories of OpenEPD 7.27.0 vs cptax 0.2.0b11 (MECO-EPD poster).

    python3 -I scripts/build_cptax_waffle.py

Top-level groups (one per change type, each with its legend entry): unchanged, modified, moved, new,
dropped, plus caption.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "figures" / "fig-cptax-waffle.svg"
FONT = 'font-family="Raleway, Arial, sans-serif"'
COLS, CELL, GAP = 19, 18, 3.6
KINDS = [  # id, count, colour, legend label
    ("unchanged", 233, "#d9d9d9", "233 unchanged"),
    ("modified", 77, "#52788f", "77 modified"),
    ("moved", 7, "#4a2545", "7 moved"),
    ("new", 25, "#00afc7", "25 new"),
    ("dropped", 9, None, "9 dropped"),
]


def square(i, colour, kind):
    x = (i % COLS) * (CELL + GAP)
    y = (i // COLS) * (CELL + GAP)
    if kind == "dropped":
        return f'<rect x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="2.5" fill="url(#hatch)"/>'
    s = f'<rect x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="2.5" fill="{colour}"/>'
    if kind == "moved":
        s += f'<circle cx="{x + CELL / 2:.1f}" cy="{y + CELL / 2:.1f}" r="2.6" fill="#ffffff"/>'
    return s


def main():
    pitch = CELL + GAP
    lx = COLS * pitch + 22
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -2 560 442">',
             '<defs><pattern id="hatch" width="5" height="5" patternUnits="userSpaceOnUse" '
             'patternTransform="rotate(45)"><rect width="5" height="5" fill="#ffffff"/>'
             '<rect width="2.4" height="5" fill="#f04f6f"/></pattern></defs>']
    i = 0
    for k, (gid, n, colour, label) in enumerate(KINDS):
        g = [f'<g id="{gid}">']
        if gid == "dropped":   # dropped categories sit on their own row below the grid
            i = ((i + COLS - 1) // COLS) * COLS
        g += [square(i + j, colour, gid) for j in range(n)]
        i += n
        ly = 60 + k * 30
        g.append(square(0, colour, gid).replace('x="0.0" y="0.0"', f'x="{lx}" y="{ly}"', 1)
                 .replace('cx="9.0" cy="9.0"', f'cx="{lx + 9}" cy="{ly + 9}"'))
        g.append(f'<text x="{lx + 26}" y="{ly + 13.5}" font-size="14" fill="#353535" {FONT}>{label}</text>')
        g.append("</g>")
        parts.append("\n".join(g))
    rows = (i + COLS - 1) // COLS
    parts.append(f'<g id="caption"><text x="{COLS * pitch / 2:.1f}" y="{rows * pitch + 22:.1f}" '
                 f'text-anchor="middle" font-size="15" fill="#66645d" {FONT}><tspan font-weight="700">OpenEPD</tspan> 7.27.0 vs '
                 f'<tspan font-weight="700">cptax</tspan> 0.2.0b11</text></g>')
    parts.append("</svg>\n")
    OUT.write_text("\n".join(parts))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
