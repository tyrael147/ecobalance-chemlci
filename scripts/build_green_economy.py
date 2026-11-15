"""Build figures/fig-green-economy.svg: sectors of the green economy x AI tasks, with the
specific tasks and the LIST projects placed in the grid (revealed on click in slides.md).

    python3 -I scripts/build_green_economy.py \
        _private_source_docs/green_economy.svg \
        _private_source_docs/specific_tasks_mapping.py \
        _private_source_docs/projects_sector_mapping.py

The mapping files are read with ast.literal_eval (never executed).

Top-level groups / classes used by the deck (SvgFigure accepts ids and ".class" keys):
  grid            column bars, row bars and headers of the six AI-for-sustainability sectors
  col-sai         "Sustainable AI" column (dimmed: not the topic of the talk)
  proj-band       extra row "LIST projects"
  task-<slug>     one group per specific task          class "task" (+ project classes)
  proj-<slug>     one group per project chip            class "proj" (+ project class)
Highlighted projects: class "calimero", "pink", "meco" (see OUR_PROJECTS / TASK_OWNER).
"""
import ast
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "figures" / "fig-green-economy.svg"

SECTORS = ["Green manufacturing", "Sustainable mobility", "Green construction",
           "Green energy", "Sustainable cities", "Sustainable food systems"]
ROWS = ["Automation", "Data-gap filling", "Forecasting", "Decision support"]
COL_X = [156 + 146 * i for i in range(7)]          # left edge of each column bar (width 130)
ROW_H, ROW_GAP = 82, 14
ROW_Y = [124 + (ROW_H + ROW_GAP) * i for i in range(4)]   # top of each row bar
OLD_ROW_CENTER = [190, 314, 438, 562]                # row centres in the source SVG (height 100)
PROJ_Y = ROW_Y[-1] + ROW_H + 18                      # top of the extra "LIST projects" row
BOTTOM = PROJ_Y + 96
BAR_TOP = 110

# projects presented in this talk > css class
OUR_PROJECTS = {"CALIMERO": "calimero", "PINK": "pink", "MECO-EPD": "meco"}
# specific task > project class that owns it (only the tasks discussed in the talk)
TASK_OWNER = {
    "in-silico chemical characterization": "calimero",
    "in-silico chemical environmental data": "pink",
    "Sustainability assessment agents": "pink",
    "Automatic environmental data parsing": "meco",
}

ORANGE = "#f46524"
DARK = "#353535"


def literal(path, name):
    tree = ast.parse(Path(path).read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit(f"{name} not found in {path}")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def wrap(text, width):
    lines, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return lines + [cur]


def chip(cx, cy, text, cls, gid, own, font=14, width=126, maxch=16, weight=600, pad=11):
    lines = wrap(text, maxch)
    lh = font * 1.22
    h = len(lines) * lh + pad
    stroke = ORANGE if own else "#9a9a9a"
    sw = 2.2 if own else 1
    out = [f'<g id="{gid}" class="{cls}">',
           f'<rect x="{cx - width / 2:.1f}" y="{cy - h / 2:.1f}" width="{width}" height="{h:.1f}" rx="6" '
           f'fill="#ffffff" stroke="{stroke}" stroke-width="{sw}"/>']
    y0 = cy - (len(lines) - 1) * lh / 2 + font * 0.36
    for i, ln in enumerate(lines):
        out.append(f'<text x="{cx:.1f}" y="{y0 + i * lh:.1f}" text-anchor="middle" style="font-size:{font}px" '
                   f'font-weight="{weight}" fill="{ORANGE if own else DARK}" '
                   f'font-family="Raleway, Arial, sans-serif">{escape(ln)}</text>')
    out.append("</g>")
    return "\n".join(out)


def main(src, tasks_py, projects_py):
    svg = Path(src).read_text()
    tasks = literal(tasks_py, "sector_ai_intersections")
    projects = literal(projects_py, "sector_projects")

    defs = re.search(r"<defs>.*?</defs>", svg, re.S).group(0).replace("font-size: 14px", "font-size: 16px")
    headers = svg[svg.index("<!-- 1. Green manufacturing -->"):svg.index("<!-- 7. Sustainable AI -->")]
    sai = svg[svg.index("<!-- 7. Sustainable AI -->"):svg.index("<!-- ==================== ROW HEADERS")]
    row_block = svg[svg.index("<!-- ==================== ROW HEADERS"):svg.rindex("</svg>")]
    chunks = re.split(r"(?=<!-- Row \d)", row_block)[1:]
    row_headers = "\n".join(f'<g transform="translate(0,{ROW_Y[i] + ROW_H / 2 - OLD_ROW_CENTER[i]})">{c}</g>'
                             for i, c in enumerate(chunks))

    grey, green = "#e6e6e6", 'fill="#6ea880" fill-opacity="0.55"'
    xr = COL_X[5] + 130 + 8   # row bars end after the last AI-for-sustainability column
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {BOTTOM + 6}">', defs]

    # grid ---------------------------------------------------------------
    g = ['<g id="grid">', f'<g fill="{grey}">']
    g += [f'<rect x="{x}" y="{BAR_TOP}" width="130" height="{PROJ_Y - 12 - BAR_TOP}"/>' for x in COL_X[:6]]
    g += ["</g>", f"<g {green}>"]
    g += [f'<rect x="130" y="{y}" width="{xr - 130}" height="{ROW_H}"/>' for y in ROW_Y]
    g += ["</g>", headers, row_headers, "</g>"]
    parts.append("\n".join(g))

    # Sustainable AI column ------------------------------------------------
    x7 = COL_X[6]
    c = ['<g id="col-sai">', f'<rect x="{x7}" y="{BAR_TOP}" width="130" height="{PROJ_Y - 12 - BAR_TOP}" fill="{grey}"/>',
         f"<g {green}>"]
    c += [f'<rect x="{xr}" y="{y}" width="{1190 - xr}" height="{ROW_H}"/>' for y in ROW_Y]
    c += ["</g>", sai, "</g>"]
    parts.append("\n".join(c))

    # LIST projects band -----------------------------------------------------
    b = ['<g id="proj-band">',
         f'<rect x="130" y="{PROJ_Y}" width="{xr - 130}" height="{BOTTOM - PROJ_Y}" fill="{ORANGE}" fill-opacity="0.16"/>',
         f'<g fill="{grey}" fill-opacity="0.9">']
    b += [f'<rect x="{x}" y="{PROJ_Y}" width="130" height="{BOTTOM - PROJ_Y}"/>' for x in COL_X[:6]]
    b += ["</g>",
          f'<text x="56" y="{PROJ_Y + 44}" class="header-text">LIST</text>',
          f'<text x="56" y="{PROJ_Y + 63}" class="header-text">projects</text>', "</g>"]
    parts.append("\n".join(b))

    # specific tasks -----------------------------------------------------------
    for si, sector in enumerate(SECTORS):
        rows_of = {}
        for ri, row in enumerate(ROWS):
            for t in tasks.get(sector, {}).get(row, []):
                rows_of.setdefault(t, []).append(ri)
        cx = COL_X[si] + 65
        for t, ris in rows_of.items():
            cy = sum(ROW_Y[r] + ROW_H / 2 for r in ris) / len(ris)
            owner = TASK_OWNER.get(t)
            cls = "task" + (f" {owner}" if owner else "")
            parts.append(chip(cx, cy, t, cls, f"task-{slug(t)}", bool(owner)))

    # projects -----------------------------------------------------------------
    for si, sector in enumerate(SECTORS):
        names = projects.get(sector, [])
        cx = COL_X[si] + 65
        step = 22.5
        y0 = PROJ_Y + (BOTTOM - PROJ_Y) / 2 - (len(names) - 1) * step / 2
        for i, p in enumerate(names):
            own = OUR_PROJECTS.get(p)
            cls = "proj" + (f" {own}" if own else "")
            parts.append(chip(cx, y0 + i * step, p, cls, f"proj-{slug(sector)}-{slug(p)}", bool(own),
                              font=12 if len(p) <= 14 else 10.5, width=124, maxch=40, weight=700, pad=6))

    parts.append("</svg>\n")
    out = "\n".join(parts)
    assert "&amp;" not in out and "<image" not in out
    OUT.write_text(out)
    print("wrote", OUT)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    main(*sys.argv[1:])
