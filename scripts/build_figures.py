#!/usr/bin/env python3
"""
Generate the vector figures used in the slides (figures/*.svg).

Same conventions as the ecobalance-abm deck: "flat" SVGs (inline presentation
attributes, Raleway text, explicit arrowheads, no <marker>), one named
<g id="..."> per logical layer. Illustrator imports each group as a named layer,
and the slides use the same ids to reveal / highlight parts of a figure on click
(components/SvgFigure.vue).

Once a figure has been edited in Illustrator, treat the edited SVG as the source
of truth (keep the group ids!) and do not re-run this script for that figure.

  fig-ssbd-design.svg      design freedom vs knowledge along innovation (SSbD, low TRL)
  fig-paths.svg            Path 1 / Path 2 / agentic LCI modelling
  fig-chemlci-arch.svg     ChemLCI pipeline: orchestrator, 8 steps, agents, tools, artefacts
  fig-prov-layers.svg      provenance graph levels (lcont / ssbd / prov classes)
  fig-lca-models-uml.svg   lca_models class diagram (python fields <-> RDF predicates),
                           generated from the live pydantic models
  fig-octocrylene-route.svg  Octocrylene route: retrosynthesis -> balanced -> Brightway mapping
  erd-*.svg                erdantic diagrams (supplementary)

Usage:  python -I scripts/build_figures.py
        (needs lca_models + erdantic importable for the UML / erdantic figures;
         inkscape for the PNG copies in figures/png/)
"""
import math
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "figures"
FONT_DIR = ROOT / "public" / "fonts" / "raleway"
FONT = "Raleway, Arial, sans-serif"

# IE-day palette (same as style.css)
INK = "#353535"
MUTED = "#6b6b6b"
ORANGE = "#f46524"
ORANGE_LT = "#f8bd90"
ORANGE_BG = "#fde3d3"
CREAM = "#fcf6d7"
RULE = "#d9d1a8"
GREY = "#9a9a9a"
GREY_LT = "#d6d3c4"
WHITE = "#ffffff"
RED = "#c0392b"
GREEN = "#3b7d23"
# methodological paths (LCM 2025 deck)
P1 = "#c55a11"
P2 = "#548235"
P3 = "#104862"
# ontology namespaces
NS = {
    "lcont": ORANGE,
    "ssbd": "#2f7fb5",
    "prov": "#3b8a3a",
    "oriont": "#80350e",
    "emmo": "#7a4ea3",
    "dcterms": MUTED,
}


# ---------------------------------------------------------------- primitives
def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w, h, body, title):
    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" style="font-variant-numeric:lining-nums;font-feature-settings:\'lnum\'">\n'
        f'<title>{esc(title)}</title>\n{body}\n</svg>\n'
    )


def g(id_, *children):
    return f'<g id="{id_}">\n' + "\n".join(c for c in children if c) + "\n</g>"


def text(x, y, s, size=12, fill=INK, anchor="start", weight="normal", style="normal", rotate=None, tip=None):
    tr = f' transform="rotate({f(rotate)} {f(x)} {f(y)})"' if rotate is not None else ""
    st = ' font-style="italic"' if style == "italic" else ""
    wt = f' font-weight="{weight}"' if weight != "normal" else ""
    t = f"<title>{esc(tip)}</title>" if tip else ""
    return (f'<text x="{f(x)}" y="{f(y)}" font-family="{FONT}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}"{wt}{st}{tr}>{t}{esc(s)}</text>')


def lines(x, y, rows, size=12, lh=None, **kw):
    lh = lh or size * 1.25
    return "\n".join(text(x, y + i * lh, r, size=size, **kw) for i, r in enumerate(rows))


def circle(c, r, fill="none", stroke="none", sw=1.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="{f(r)}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}/>')


def rect(x, y, w, h, fill="none", stroke="none", sw=1.5, rx=0, dash=None, opacity=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(rx)}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>')


def line(p, q, stroke=INK, sw=1.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{f(p[0])}" y1="{f(p[1])}" x2="{f(q[0])}" y2="{f(q[1])}" '
            f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{d}/>')


def path(d, stroke=INK, sw=1.5, fill="none", dash=None, opacity=None):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{da}{o}/>'


def add(p, q, k=1.0):
    return (p[0] + k * q[0], p[1] + k * q[1])


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def unit(v):
    n = math.hypot(*v) or 1
    return (v[0] / n, v[1] / n)


def head(tip, direction, color=INK, length=8, half=4.2):
    u = unit(direction)
    n = (-u[1], u[0])
    base = add(tip, u, -length)
    a = add(base, n, half)
    b = add(base, n, -half)
    return f'<path d="M{f(tip[0])} {f(tip[1])} L{f(a[0])} {f(a[1])} L{f(b[0])} {f(b[1])} Z" fill="{color}"/>'


def cubic_arrow(p0, c1, c2, p3, color=INK, sw=1.6, length=8, half=4.2, dash=None):
    tang = sub(p3, c2) if math.hypot(*sub(p3, c2)) > 1e-6 else sub(p3, c1)
    u = unit(tang)
    end = add(p3, u, -length * 0.85)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    p = (f'<path d="M{f(p0[0])} {f(p0[1])} C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} '
         f'{f(end[0])} {f(end[1])}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"{d}/>')
    return p + "\n" + head(p3, tang, color, length, half)


def arrow(p, q, color=INK, sw=1.6, length=8, half=4.2, dash=None):
    return cubic_arrow(p, add(p, sub(q, p), 1 / 3), add(p, sub(q, p), 2 / 3), q, color, sw, length, half, dash)


def harrow(p, q, color=INK, sw=1.6, dash=None, k=0.5, **kw):
    """S-shaped arrow leaving p horizontally and entering q horizontally."""
    dx = (q[0] - p[0]) * k
    return cubic_arrow(p, (p[0] + dx, p[1]), (q[0] - dx, q[1]), q, color, sw, dash=dash, **kw)


def varrow(p, q, color=INK, sw=1.6, dash=None, k=0.5, **kw):
    dy = (q[1] - p[1]) * k
    return cubic_arrow(p, (p[0], p[1] + dy), (q[0], q[1] - dy), q, color, sw, dash=dash, **kw)


def block(x, y, w, h, fill=WHITE, stroke="none", sw=1.2, shadow=0.16, off=2.2):
    """Rectangular block with a small hard drop shadow (an offset rect: easy to edit in Illustrator)."""
    return (rect(x + off, y + off, w, h, fill="#000000", rx=1, opacity=shadow)
            + "\n" + rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, rx=1))


def tag(x, y, s, size=9.5, fill=WHITE, color=INK, weight="bold", pad=5, h=None, w=None, tip=None):
    """Small white label with a hard shadow, like .tag in style.css. Returns (svg, width)."""
    w = w or tw(s, size, weight) + 2 * pad
    h = h or size + 6
    return (block(x, y, w, h, fill=fill, shadow=0.13, off=1.5)
            + "\n" + text(x + w / 2, y + h / 2 + size * 0.36, s, size, color, "middle", weight, tip=tip)), w


def tw(s, size, weight="normal"):
    """Rough Raleway text width."""
    k = 0.60 if weight == "bold" else 0.54
    narrow = sum(1 for c in s if c in "iljtfrI.,:;'|()[] ")
    return size * (k * (len(s) - narrow) + 0.30 * narrow)


def person(c, color, scale=1.0):
    x, y = c
    s = scale
    return (f'<g>{circle((x, y - 9 * s), 5.5 * s, fill=color)}'
            f'<path d="M{f(x - 8.5 * s)} {f(y + 10 * s)} Q{f(x - 8.5 * s)} {f(y - 2 * s)} '
            f'{f(x)} {f(y - 2 * s)} Q{f(x + 8.5 * s)} {f(y - 2 * s)} {f(x + 8.5 * s)} '
            f'{f(y + 10 * s)} Z" fill="{color}"/></g>')


def bot(c, color=INK, scale=1.0, face=WHITE):
    """Agent icon: rounded head with two eyes and an antenna."""
    x, y = c
    s = scale
    return "\n".join([
        line((x, y - 11 * s), (x, y - 7 * s), color, 1.6 * s),
        circle((x, y - 12.5 * s), 2 * s, fill=color),
        rect(x - 10 * s, y - 7 * s, 20 * s, 15 * s, fill=color, rx=4 * s),
        circle((x - 4 * s, y), 2.4 * s, fill=face),
        circle((x + 4 * s, y), 2.4 * s, fill=face),
        rect(x - 13 * s, y - 2 * s, 2.5 * s, 6 * s, fill=color, rx=1),
        rect(x + 10.5 * s, y - 2 * s, 2.5 * s, 6 * s, fill=color, rx=1),
    ])


def fileicon(x, y, color=INK, scale=1.0, fill=WHITE):
    s = scale
    w, h, k = 14 * s, 18 * s, 5 * s
    return (path(f"M{f(x)} {f(y)} L{f(x + w - k)} {f(y)} L{f(x + w)} {f(y + k)} L{f(x + w)} {f(y + h)} "
                 f"L{f(x)} {f(y + h)} Z", color, 1.3, fill=fill)
            + path(f"M{f(x + w - k)} {f(y)} L{f(x + w - k)} {f(y + k)} L{f(x + w)} {f(y + k)}", color, 1.1)
            + "".join(line((x + 3 * s, y + (8 + 3 * i) * s), (x + w - 3 * s, y + (8 + 3 * i) * s), color, 0.9)
                      for i in range(3)))


def db(c, color=INK, scale=1.0, fill=WHITE):
    x, y = c
    s = scale
    rx, ry, h = 9 * s, 3.2 * s, 14 * s
    return (path(f"M{f(x - rx)} {f(y)} L{f(x - rx)} {f(y + h)} A{f(rx)} {f(ry)} 0 0 0 {f(x + rx)} {f(y + h)} "
                 f"L{f(x + rx)} {f(y)}", color, 1.3, fill=fill)
            + f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(rx)}" ry="{f(ry)}" fill="{fill}" stroke="{color}" stroke-width="1.3"/>'
            + path(f"M{f(x - rx)} {f(y + h / 2)} A{f(rx)} {f(ry)} 0 0 0 {f(x + rx)} {f(y + h / 2)}", color, 1.0))


def molecule(c, color=INK, scale=1.0, fill=WHITE):
    """Hexagon with a side chain (generic chemical candidate)."""
    x, y = c
    r = 9 * scale
    pts = [(x + r * math.cos(math.radians(a)), y + r * math.sin(math.radians(a))) for a in range(30, 390, 60)]
    d = "M" + " L".join(f"{f(p[0])} {f(p[1])}" for p in pts) + " Z"
    tail = pts[0]
    return (path(d, color, 1.5, fill=fill)
            + path(f"M{f(tail[0])} {f(tail[1])} l{f(7 * scale)} {f(-4 * scale)} l{f(7 * scale)} {f(4 * scale)}", color, 1.5)
            + circle((x, y), r * 0.5, stroke=color, sw=1.0))


def write(name, content):
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(content, encoding="utf-8")
    print("wrote", OUT / name)


def export_png(dpi=300):
    inkscape = shutil.which("inkscape")
    if not inkscape:
        print("inkscape not found: skipping PNG export")
        return
    png_dir = OUT / "png"
    png_dir.mkdir(exist_ok=True)
    conf = Path(tempfile.gettempdir()) / "deck-fonts.conf"
    conf.write_text(
        '<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig>'
        '<include ignore_missing="yes">/etc/fonts/fonts.conf</include>'
        f'<dir>{FONT_DIR}</dir><cachedir>{Path(tempfile.gettempdir()) / "deck-fc-cache"}</cachedir>'
        '</fontconfig>')
    env = dict(os.environ, FONTCONFIG_FILE=str(conf))
    for svg_file in sorted(OUT.glob("*.svg")):
        target = png_dir / (svg_file.stem + ".png")
        subprocess.run([inkscape, str(svg_file), "--export-type=png", f"--export-filename={target}",
                        f"--export-dpi={dpi}", "--export-background-opacity=0"],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)
        print("wrote", target)


# ============================================================== SSbD / design paradox
def fig_ssbd():
    W, H = 560, 330
    x0, x1, y0, y1 = 48, 540, 62, 288     # plot area
    axes = g("axes",
             line((x0, y1), (x1, y1), INK, 1.6), head((x1 + 6, y1), (1, 0), INK),
             line((x0, y1), (x0, y0 - 6), INK, 1.6), head((x0, y0 - 12), (0, -1), INK),
             text((x0 + x1) / 2, y1 + 34, "innovation stage  (TRL 1 to 9)", 12, INK, "middle", "bold"),
             *[text(x0 + 18 + i * (x1 - x0 - 30) / 4, y1 + 17, s, 10, MUTED, "middle")
               for i, s in enumerate(["molecule idea", "lab synthesis", "process design", "pilot", "market"])])
    free = g("curve-freedom",
             path(f"M{x0 + 4} {y0 + 10} C{x0 + 160} {y0 + 20} {x0 + 250} {y1 - 30} {x1 - 8} {y1 - 18}", ORANGE, 3.2),
             text(x0 + 165, y0 + 30, "design freedom", 12.5, ORANGE, weight="bold"),
             text(x0 + 165, y0 + 45, "options open, changes are cheap", 10.5, ORANGE, style="italic"))
    know = g("curve-knowledge",
             path(f"M{x0 + 4} {y1 - 14} C{x0 + 220} {y1 - 20} {x0 + 300} {y0 + 40} {x1 - 8} {y0 + 16}", INK, 3.2),
             text(x1 - 10, y0 + 115, "data and knowledge", 12.5, INK, "end", "bold"),
             text(x1 - 10, y0 + 130, "for a detailed LCI", 10.5, INK, "end", style="italic"))
    zone = g("zone-insilico",
             rect(x0 + 3, y0 - 4, 150, y1 - y0 + 2, fill=ORANGE, opacity=0.13),
             line((x0 + 153, y0 - 4), (x0 + 153, y1), ORANGE, 1.4, dash="4 4"),
             text(x0 + 78, y1 - 60, "in-silico,", 12.5, INK, "middle", "bold"),
             text(x0 + 78, y1 - 44, "explorative LCA", 12.5, INK, "middle", "bold"),
             text(x0 + 78, y1 - 28, "SSbD: by design", 11, ORANGE, "middle", "bold"))
    # candidate funnel along the top
    dots = []
    import random
    rnd = random.Random(4)
    for i, n in enumerate([14, 9, 5, 3, 2, 1]):
        cx = x0 + 22 + i * 90
        for k in range(n):
            dots.append(circle((cx + rnd.uniform(-22, 22) * min(n, 6) / 6, 22 + rnd.uniform(-12, 12) * min(n, 8) / 8),
                               3.6, fill=ORANGE if i < 2 else GREY))
    cands = g("candidates", *dots,
              text(x1, 50, "chemical candidates", 10.5, MUTED, "end", style="italic"))
    write("fig-ssbd-design.svg", svg(W, H, "\n".join([axes, know, free, zone, cands]),
                                    "Design freedom vs knowledge along the innovation process"))


# ============================================================== Path 1 / Path 2 / ours
def fig_paths():
    W, H = 920, 360
    cols = [("chemical", 62), ("prediction / decision", 250), ("life cycle inventory", 470),
            ("impact assessment", 640), ("impact", 800)]
    header = g("header", *[text(x, 16, s, 11, MUTED, "middle", "bold") for s, x in cols],
               line((10, 26), (910, 26), RULE, 1.2))
    BW, BH = 150, 42

    def box(cx, cy, label, color, sub=None, w=BW, ghost=False, fill=WHITE):
        x, y = cx - w / 2, cy - BH / 2
        if ghost:
            return (rect(x, y, w, BH, fill="none", stroke=GREY_LT, sw=1.3, dash="4 3")
                    + text(cx, cy + 4, label, 11.5, GREY, "middle", "bold"))
        out = [block(x, y, w, BH, fill=fill), rect(x, y, 4, BH, fill=color)]
        if sub:
            out += [text(cx + 2, cy - 3, label, 11.5, INK, "middle", "bold"),
                    text(cx + 2, cy + 12, sub, 9.5, MUTED, "middle", style="italic")]
        else:
            out.append(text(cx + 2, cy + 4, label, 11.5, INK, "middle", "bold"))
        return "\n".join(out)

    def lane(id_, y, color, name, items, note, extra=""):
        lbl = [rect(10, y - 34, 112, 16, fill=color), text(16, y - 22, name, 10.5, WHITE, weight="bold")]
        return g(id_, *lbl, *items, text(910, y + 36, note, 10.5, color, "end", style="italic"), extra)

    # Path 1
    y = 82
    p1 = lane("lane-p1", y, P1, "Path 1", [
        molecule((62, y), INK, 1.3),
        arrow((88, y), (172, y), P1, 2),
        box(250, y, "chemical > impact", P1, "ML on descriptors"),
        box(470, y, "LCI", P1, ghost=True, w=110), box(640, y, "LCIA", P1, ghost=True, w=110),
        cubic_arrow((328, y), (420, y - 40), (700, y - 40), (762, y), P1, 2),
        box(800, y, "impact", P1, w=76),
    ], "fast screening, but aggregated: route and assumptions hidden in the training data")
    # Path 2
    y = 186
    p2 = lane("lane-p2", y, P2, "Path 2", [
        molecule((62, y), INK, 1.3),
        arrow((88, y), (172, y), P2, 2),
        box(250, y, "route and stoichiometry", P2, "expert + inventory ML"),
        person((192, y - 34), P2, 0.7), text(204, y - 28, "expert", 9.5, P2, weight="bold"),
        arrow((328, y), (412, y), P2, 2), box(470, y, "LCI", P2, w=110),
        arrow((527, y), (582, y), P2, 2), box(640, y, "LCIA", P2, w=110),
        arrow((697, y), (760, y), P2, 2), box(800, y, "impact", P2, w=76),
    ], "informed and explicit, but laborious for many candidates")
    # ours
    y = 290
    stack = lambda cx, cy, w, label: "\n".join(
        [rect(cx - w / 2 + 6 * k, cy - BH / 2 - 6 * k, w, BH, fill=WHITE, stroke=GREY_LT, sw=1) for k in (2, 1)]
        + [box(cx, cy, label, P3, w=w)])
    ours = lane("lane-ours", y, P3, "Agentic LCI", [
        molecule((48, y + 8), INK, 1.1), molecule((66, y - 10), INK, 1.1), molecule((80, y + 12), INK, 1.1),
        arrow((100, y), (172, y), P3, 2),
        block(175, y - BH / 2 - 4, BW, BH + 8, fill=P3),
        bot((198, y), WHITE, 0.9, face=P3),
        text(262, y - 4, "agentic system", 11.5, WHITE, "middle", "bold"),
        text(262, y + 11, "LLMs + tools", 9.5, CREAM, "middle", style="italic"),
        arrow((328, y), (408, y), P3, 2), stack(470, y, 110, "LCI drafts"),
        arrow((527, y), (582, y), P3, 2), box(640, y, "LCIA", P3, w=110),
        arrow((697, y), (760, y), P3, 2), box(800, y, "impacts", P3, w=76),
    ], "fast and explicit: many candidates in parallel, auditable LCIs")
    hitl = g("hitl",
             cubic_arrow((470, y + 26), (470, y + 60), (262, y + 60), (262, y + 30), ORANGE, 1.8, dash="5 4"),
             person((366, y + 48), ORANGE, 0.65),
             text(388, y + 54, "human in the loop: inspect, edit, re-run from any step", 10, ORANGE, weight="bold"))
    write("fig-paths.svg", svg(W, H, "\n".join([header, p1, p2, ours, hitl]),
                              "Methodological paths for the impact of new chemicals"))


# ============================================================== ChemLCI architecture
STEPS = [
    ("1", "SMILES", "identification", ["orchestrator"], ["PubChem", "CIR resolver"], "Molecule"),
    ("2", "Retrosynthesis", "prediction", ["orchestrator"], ["AiZynthFinder", "ASKCOS", "route chooser"], "RetrosynthesisRoute"),
    ("3", "Synthesis route", "completion", ["SynthesisCompleter", "EquationBalancer"],
     ["split reaction", "RDKit balancer", "missing atoms", "by-products", "co-reactants", "balance validator"], "SynthesisRoute"),
    ("4", "Process", "completion", ["ProcessDescriptor"], ["load / save"], "SynthesisRoute + process"),
    ("5", "Inventory", "draft", ["InventoryDrafter"], ["draft validator"], "Inventory (draft)"),
    ("6", "Brightway", "LCI", ["BW2LCIbuilder", "EcoinventSearch"],
     ["ecoinvent search", "semantic search", "smiles2impact", "process node", "biosphere flow", "BW validator"], "Inventory (bw2)"),
    ("7", "LCIA", "", ["LCIA agent"], ["LCIA methods", "run_lcia (bw2.5)"], "LCIAResult"),
    ("8", "Final", "response", ["orchestrator"], [], "report"),
]
ML_TOOLS = {"AiZynthFinder", "ASKCOS", "semantic search", "smiles2impact"}


def fig_arch():
    W, H = 930, 382
    CW, GAP, X0 = 110, 6, 8
    user = g("user",
             person((24, 40), INK, 1.0),
             text(24, 66, "user", 10.5, INK, "middle", "bold"),
             block(44, 18, 238, 34),
             text(52, 33, "“I want LCI for Octocrylene", 11, INK, style="italic"),
             text(52, 46, "produced in Europe.”", 11, INK, style="italic"),
             harrow((282, 35), (346, 48), INK, 1.6))
    smiles = g("prompt-smiles",
               block(44, 56, 298, 22),
               text(51, 70.5, "or only:", 9, MUTED, style="italic"),
               text(88, 70.5, "CCCCC(CC)COC(=O)C(=C(c1ccccc1)c1ccccc1)C#N", 8.6, INK, weight="bold"))
    orch = g("orchestrator",
             block(350, 22, 572, 50, fill=INK),
             bot((376, 50), CREAM, 1.05, face=INK),
             text(400, 43, "orchestrator agent", 14, CREAM, weight="bold"),
             text(400, 60, "reads current_task from the session state > loads the task prompt > delegates", 10.5, ORANGE_LT,
                  style="italic"),
             line((636, 72), (636, 86), GREY, 1.2),
             line((X0 + CW / 2, 86), (X0 + 7 * (CW + GAP) + CW / 2, 86), GREY, 1.2),
             *[varrow((X0 + i * (CW + GAP) + CW / 2, 86), (X0 + i * (CW + GAP) + CW / 2, 102), GREY, 1.2, length=6, half=3.4)
               for i in range(8)])
    groups = []
    for i, (n, l1, l2, agents, tools, art) in enumerate(STEPS):
        x = X0 + i * (CW + GAP)
        out = [block(x, 104, CW, 40, fill=INK),
               text(x + 8, 129, n, 20, ORANGE, weight="900"),
               text(x + 26, 120, l1, 10.5, CREAM, weight="bold"),
               text(x + 26, 134, l2, 10.5, CREAM, weight="bold")]
        if i < 7:
            out.append(head((x + CW + GAP - 0.5, 124), (1, 0), GREY, 6, 3.5))
        # agents
        ay = 160
        for k, a in enumerate(agents):
            sub_agent = k > 0
            out.append(bot((x + 14 + (8 if sub_agent else 0), ay + 9 + k * 24), ORANGE if a != "orchestrator" else INK,
                           0.62))
            out.append(text(x + 27 + (8 if sub_agent else 0), ay + 13 + k * 24, ("> " if sub_agent else "") + a,
                            9.5 if len(a) > 14 else 10, INK if a == "orchestrator" else ORANGE, weight="bold"))
        # tools
        ty = 214
        for k, t in enumerate(tools):
            ml = t in ML_TOOLS
            s, _ = tag(x + 4, ty + k * 19, t, 9, fill=ORANGE if ml else WHITE, color=WHITE if ml else INK,
                       w=CW - 8, h=15, weight="bold" if ml else "normal")
            out.append(s)
        # artefact
        out.append(fileicon(x + 6, 346, INK, 1.0))
        out += [text(x + 25, 358, a_, 9.5, INK, weight="bold") for a_ in [art.split(" (")[0].split(" + ")[0]]]
        rest = art[len(art.split(" (")[0].split(" + ")[0]):].strip()
        if rest:
            out.append(text(x + 25, 370, rest, 9, MUTED, style="italic"))
        groups.append(g(f"step-{n}", *out))
    labels = g("row-labels",
               text(X0, 157, "agents", 9, MUTED, style="italic"),
               text(X0, 211, "tools", 9, MUTED, style="italic"),
               text(X0, 342, "lca_models objects (validated JSON)", 9, MUTED, style="italic"),
               rect(X0 + 300, 333, 9, 9, fill=ORANGE), text(X0 + 313, 341, "ML model (microservice)", 9, MUTED),
               rect(X0 + 430, 333, 9, 9, fill=WHITE, stroke=GREY_LT, sw=1),
               text(X0 + 443, 341, "deterministic / heuristic tool", 9, MUTED))
    write("fig-chemlci-arch.svg", svg(W, H, "\n".join([user, smiles, orch, labels, *groups]),
                                     "ChemLCI pipeline: agents, tools and data objects"))


# ============================================================== provenance levels
def cls(x, y, ns, name, sub=None, w=None, size=11):
    """Ontology class/instance box: coloured namespace bar + name."""
    label = f"{ns}:{name}"
    w = w or max(tw(label, size, "bold"), tw(sub or "", 9.5)) + 20
    out = [block(x, y, w, 34 if sub else 24), rect(x, y, 4, 34 if sub else 24, fill=NS.get(ns, INK)),
           text(x + 10, y + 16, ns + ":", size, NS.get(ns, INK), weight="bold"),
           text(x + 10 + tw(ns + ":", size, "bold") + 1, y + 16, name, size, INK, weight="bold")]
    if sub:
        out.append(text(x + 10, y + 28, sub, 9.5, MUTED, style="italic"))
    return "\n".join(out), w


def elabel(p, s, color=MUTED, anchor="middle", size=9):
    return text(p[0], p[1], s, size, color, anchor, style="italic")


def fig_prov():
    W, H = 1060, 420
    bands = [("workflow", 8, 92), ("steps", 100, 184), ("agents and tools", 192, 300), ("data", 308, 412)]
    bg = g("bands", *[rect(0, y0, W, y1 - y0, fill=WHITE, opacity=0.35 if i % 2 == 0 else 0.0) for i, (_, y0, y1) in enumerate(bands)],
           *[text(10, (y0 + y1) / 2 + 4, s, 11, MUTED, weight="bold") for s, y0, y1 in bands])
    X = 128
    # --- workflow level
    b_user, wu = cls(X, 32, "lcont", "User")
    b_comp, wc = cls(X + 210, 26, "lcont", "Computation", "“LCA of Octocrylene”, 18.5 min, ⊂ ssbd:Computation")
    b_sw, _ = cls(X + 690, 16, "ssbd", "Software", "chemlcibuilder app")
    b_mat, _ = cls(X + 690, 56, "ssbd", "Matter", "precursors used (8)")
    wf = g("level-workflow", b_user, b_comp, b_sw, b_mat,
           arrow((X + wu, 44), (X + 208, 44), GREY, 1.3), elabel((X + wu + 70, 38), "prov:wasAssociatedWith"),
           harrow((X + 210 + wc, 36), (X + 688, 28), GREY, 1.3), elabel((X + 600, 22), "ssbd:hasSoftware"),
           harrow((X + 210 + wc, 52), (X + 688, 68), GREY, 1.3), elabel((X + 595, 82), "prov:used"))
    # --- step level
    steps = ["SMILES", "retro", "synthesis", "process", "draft", "bw LCI", "LCIA", "final"]
    sw_, gap_, sx = 90, 18, X
    items = []
    for i, s in enumerate(steps):
        x = sx + i * (sw_ + gap_)
        items += [block(x, 120, sw_, 26), rect(x, 120, 4, 26, fill=NS["lcont"]),
                  text(x + sw_ / 2 + 2, 137, f"{i + 1} {s}", 10.5, INK, "middle", "bold")]
        if i < 7:
            items.append(arrow((x + sw_ + 2, 133), (x + sw_ + gap_ - 1, 133), GREY, 1.2, 5, 3))
    items += [elabel((sx + 2, 114), "lcont:WorkflowStep ⊂ ssbd:Process, chained by lcont:isPredecessorOf", INK, "start", 9.5)]
    for k, nm in enumerate(["retros", "completed", "process", "draft", "bw_inventory", "lcia"]):
        x = sx + (k + 1.5) * (sw_ + gap_) + 2
        items += [fileicon(x - 9, 156, MUTED, 0.75), text(x + 6, 168, nm, 9, MUTED)]
    items += [elabel((W - 10, 160), "ssbd:hasInput, ssbd:hasOutput", MUTED, "end"), elabel((W - 10, 173), "lcont:HierarchicalData", MUTED, "end")]
    st = g("level-step", *items,
           varrow((X + 340, 62), (X + 340, 118), GREY, 1.2), elabel((X + 346, 98), "ssbd:hasSubProcess", anchor="start"))
    # --- agents and tools
    b_llm, wl = cls(X, 210, "lcont", "LLMInference", "262: prompt, response, tokens")
    b_tool, wt = cls(X, 254, "lcont", "ToolCall", "242: args, result, status")
    b_ag, wa = cls(X + 290, 210, "lcont", "LLMAgent", "8 agents (⊂ prov:SoftwareAgent)")
    b_lsw, wls = cls(X + 545, 204, "lcont", "LLMSoftware", "agent and system prompt")
    b_lm, _ = cls(X + 760, 204, "ssbd", "LargeLanguageModel", "claude-haiku-4.5")
    b_tsw, _ = cls(X + 290, 258, "ssbd", "Software", "@chemlci_tool: model type, uncertainty")
    calls = g("level-call", b_llm, b_tool, b_ag, b_lsw, b_lm, b_tsw,
              varrow((X + 340, 146), (X + 60, 208), GREY, 1.2), elabel((X + 160, 178), "ssbd:hasSubProcess"),
              arrow((X + wl, 222), (X + 288, 222), GREY, 1.3), elabel((X + wl + 62, 216), "lcont:executedBy"),
              arrow((X + 290 + wa, 222), (X + 543, 218), GREY, 1.3),
              arrow((X + 545 + wls, 218), (X + 758, 218), GREY, 1.3), elabel((X + 756, 251), "ssbd:implementsModel", anchor="end"),
              arrow((X + wt, 268), (X + 288, 272), GREY, 1.3), elabel((X + wt + 70, 285), "prov:wasAssociatedWith"),
              text(W - 10, 296, "every call: prov:startedAtTime, prov:endedAtTime, lcont:executionStatus, token counts", 9.5, MUTED, "end", style="italic"))
    # --- data
    b_data, wd = cls(X, 326, "ssbd", "Data", "836: prompts, arguments, results")
    b_fg, wf_ = cls(X + 290, 326, "oriont", "Activity", "in bw_inventory, ⊂ lcont:BackgroundActivity")
    b_eco, we = cls(X + 660, 326, "lcont", "BackgroundActivity", "ecoinvent 3.12 node (lcont:inDatabase)")
    b_cand, _ = cls(X + 660, 372, "lcont", "returnedCandidate", "143 candidates seen by the agent")
    data = g("level-data", b_data, b_fg, b_eco, b_cand,
             varrow((X + 60, 288), (X + 60, 324), GREY, 1.2), elabel((X + 66, 312), "prov:used, prov:generated", anchor="start"),
             arrow((X + 290 + wf_, 340), (X + 658, 340), ORANGE, 1.6), elabel((X + 290 + wf_ + 55, 334), "prov:wasDerivedFrom", ORANGE),
             cubic_arrow((X + 130, 288), (X + 220, 300), (X + 340, 300), (X + 370, 324), ORANGE, 1.4, dash="4 3"),
             elabel((X + 340, 306), "prov:wasInformedBy (selecting tool call)", ORANGE, "start"),
             varrow((X + 750, 360), (X + 750, 371), GREY, 1.2))
    write("fig-prov-layers.svg", svg(W, H, "\n".join([bg, wf, st, calls, data]),
                                    "Levels of the ChemLCI provenance graph"))


# ============================================================== lca_models UML
UML_FIELDS = {
    "RetrosynthesisRoute": ["target_SMILES", "root_node_id", "nodes"],
    "RetrosynthesisNode": ["reaction_SMILES", "product_SMILES", "precursors_SMILES"],
    "SynthesisRoute": ["root_node_id", "nodes"],
    "ReactionNode": ["reaction_SMILES", "target_molecule", "byproducts", "detailed_equation", "process_description"],
    "Equation": ["reaction_smiles", "reactants", "products"],
    "ReactionParticipant": ["molecule", "stoichiometry"],
    "Molecule": ["smiles", "name", "chemical_formula", "molecular_weight", "inchi"],
    "Inventory": ["name", "comment", "nodes"],
    "LCIActivityNode": ["name", "unit", "location", "database", "code", "reference_flow", "exchanges"],
    "ChemicalObject": ["name", "molecule"],
    "LCIExchange": ["name", "amount", "unit", "type", "from_activity", "to_activity", "flow_object"],
    "FlowObject": ["name", "cas_number", "category"],
    "Location": ["code", "name"],
    "LCIAResult": ["functional_unit", "foreground_db", "scores", "summary"],
    "ImpactCategoryScore": ["method_tuple", "score", "unit", "ssbd_class", "indicator"],
    "ImpactCategoryIndicator": ["name", "unit", "impact_category"],
    "DataModel": ["iri", "source", "uncertainty_type"],
}
UML_POS = {  # package, x, y
    "RetrosynthesisRoute": ("chem", 8, 40), "RetrosynthesisNode": ("chem", 8, 152), "SynthesisRoute": ("chem", 8, 268),
    "ReactionNode": ("chem", 192, 40), "Equation": ("chem", 192, 178), "ReactionParticipant": ("chem", 192, 276),
    "Molecule": ("chem", 192, 360),
    "Inventory": ("lci", 384, 40), "LCIActivityNode": ("lci", 384, 140), "ChemicalObject": ("lci", 384, 362),
    "LCIExchange": ("lci", 568, 40), "FlowObject": ("lci", 568, 218), "Location": ("lci", 568, 316),
    "LCIAResult": ("lcia", 760, 40), "ImpactCategoryScore": ("lcia", 760, 152), "ImpactCategoryIndicator": ("lcia", 760, 278),
    "DataModel": ("base", 760, 372),
}
UML_EDGES = [
    ("RetrosynthesisRoute", "nodes", "RetrosynthesisNode"), ("SynthesisRoute", "nodes", "ReactionNode"),
    ("ReactionNode", "detailed_equation", "Equation"), ("ReactionNode", "target_molecule", "Molecule"),
    ("Equation", "reactants", "ReactionParticipant"), ("ReactionParticipant", "molecule", "Molecule"),
    ("Inventory", "nodes", "LCIActivityNode"), ("LCIActivityNode", "exchanges", "LCIExchange"),
    ("LCIActivityNode", "location", "Location"), ("LCIExchange", "flow_object", "FlowObject"),
    ("LCIAResult", "scores", "ImpactCategoryScore"), ("ImpactCategoryScore", "indicator", "ImpactCategoryIndicator"),
    ("ChemicalObject", "molecule", "Molecule"),
]


def fig_uml():
    import lca_models.chemistry as chem
    import lca_models.core.models as core

    classes = {n: getattr(core, n, None) or getattr(chem, n) for n in UML_FIELDS}
    BW, HH, RH = 176, 32, 13.5
    W, H = 944, 470

    def fy(name, field):
        return UML_POS[name][2] + HH + 11 + UML_FIELDS[name].index(field) * RH

    def short(tp):
        s = str(tp)
        for junk in ["typing.", "lca_models.core.models.", "lca_models.chemistry.chemistry_models.",
                     "lca_models.chemistry.synthesis_models.", "<class '", "'>", "uuid.", "datetime."]:
            s = s.replace(junk, "")
        s = s.replace("Literal['biosphere', 'technosphere', 'production']", "Literal[…]")
        s = s.replace("Descriptor", "")
        return s if len(s) < 19 else s[:17] + "…"

    pk = {"chem": [], "lci": [], "lcia": [], "base": []}
    py = {k: [] for k in pk}
    rdf = {k: [] for k in pk}
    iri = {k: [] for k in pk}
    for name, (p, x, y) in UML_POS.items():
        M = classes[name]
        n = len(UML_FIELDS[name])
        h = HH + 8 + n * RH
        prefix, local = M.ontology_prefix, M.ontology_iri
        base = name == "DataModel"
        pk[p] += [block(x, y, BW, h, fill=WHITE),
                  rect(x, y, BW, HH - 12 if not base else HH, fill=INK if not base else GREY),
                  text(x + 8, y + 14, name, 11.5, CREAM, weight="bold"),
                  line((x, y + HH), (x + BW, y + HH), GREY_LT, 1)]
        if base:
            pk[p] += [text(x + 8, y + 28, "pydantic BaseModel, every class", 9, CREAM, style="italic")]
        else:
            iri[p] += [text(x + 8, y + 31, prefix + ":", 10, NS[prefix], weight="bold"),
                       text(x + 8 + tw(prefix + ":", 10, "bold") + 1, y + 31, local, 10, NS[prefix], weight="bold")]
        for k, fld in enumerate(UML_FIELDS[name]):
            yy = y + HH + 11 + k * RH
            if base:
                finfo = core.DataModel.model_fields[fld]
            else:
                finfo = M.model_fields[fld]
            pred = (finfo.json_schema_extra or {}).get("rdf_predicate", f"{prefix}:{fld}")
            py[p].append(text(x + 8, yy, fld, 9.5, INK, weight="bold"))
            py[p].append(text(x + BW - 6, yy, short(finfo.annotation), 8.5, MUTED, "end"))
            pns, _, ploc = pred.partition(":")
            rdf[p].append(text(x + 8, yy, pns + ":", 9.5, NS.get(pns, MUTED), weight="bold"))
            rdf[p].append(text(x + 8 + tw(pns + ":", 9.5, "bold") + 1, yy, ploc, 9.5, INK, weight="bold"))
    edges = []
    for src, fld, dst in UML_EDGES:
        sp, sx, sy = UML_POS[src]
        dp, dx, dy = UML_POS[dst]
        y = fy(src, fld) - 3.5
        if dx > sx:             # to the right
            p, q = (sx + BW, y), (dx, dy + 14)
            e = harrow(p, q, GREY, 1.2, length=7, half=3.6)
        elif dx < sx:           # to the left
            p, q = (sx, y), (dx + BW, dy + 14)
            e = harrow(p, q, GREY, 1.2, length=7, half=3.6)
        else:                   # same column: loop on the right side
            p, q = (sx + BW, y), (dx + BW, dy + 10)
            e = cubic_arrow(p, (sx + BW + 16, y), (dx + BW + 16, dy + 10), q, GREY, 1.2, 7, 3.6)
        dashed = src == "ChemicalObject"
        diamond = path(f"M{f(p[0])} {f(p[1])} l{f(5 if p[0] == sx + BW else -5)} -3 l{f(5 if p[0] == sx + BW else -5)} 3 "
                       f"l{f(-5 if p[0] == sx + BW else 5)} 3 Z", INK, 1, fill=INK)
        edges.append((e.replace('stroke-width="1.2"', 'stroke-width="1.2" stroke-dasharray="4 3"') if dashed else e) + diamond)
    # inheritance ChemicalObject -> FlowObject (hollow triangle)
    _, cx, cy = UML_POS["ChemicalObject"]
    _, fx, fy_ = UML_POS["FlowObject"]
    inh = (path(f"M{cx + BW} {cy + 14} C{cx + BW + 20} {cy + 14} {fx - 30} {fy_ + 60} {fx - 8} {fy_ + 56}", GREY, 1.2)
           + path(f"M{fx} {fy_ + 54} L{fx - 10} {fy_ + 50} L{fx - 8} {fy_ + 61} Z", GREY, 1.2, fill=WHITE))
    pkg_bg = g("pkg-labels",
               rect(2, 4, 372, H - 6, fill=WHITE, opacity=0.28), rect(378, 4, 374, H - 6, fill=WHITE, opacity=0.28),
               rect(756, 4, 186, 356, fill=WHITE, opacity=0.28),
               text(10, 24, "lca_models.chemistry", 12, INK, weight="bold"),
               text(386, 24, "lca_models.core: LCI", 12, INK, weight="bold"),
               text(764, 24, "lca_models.core: LCIA", 12, INK, weight="bold"))
    body = [pkg_bg, g("edges", *edges, inh)]
    for p in ["chem", "lci", "lcia", "base"]:
        body.append(g(f"pkg-{p}", *pk[p], g(f"{p}-py", *py[p]), g(f"{p}-rdf", *rdf[p]), g(f"{p}-iri", *iri[p])))
    write("fig-lca-models-uml.svg", svg(W, H, "\n".join(body), "lca_models: pydantic classes mapped to ontology classes"))


def fig_erdantic():
    try:
        import erdantic
        import lca_models.chemistry as chem
        import lca_models.core.models as core
    except ImportError as e:
        print("erdantic / lca_models not importable, skipping:", e)
        return
    for name, model in [("erd-inventory", core.Inventory), ("erd-lcia", core.LCIAResult),
                        ("erd-synthesis", chem.SynthesisRoute)]:
        erdantic.draw(model, out=str(OUT / f"{name}.svg"))
        print("wrote", OUT / f"{name}.svg")


# ============================================================== Octocrylene route
def fig_route():
    W, H = 900, 330
    PH = 26

    def pill(x, y, label, tip, w=None, stroke=INK, fill=WHITE, color=INK, weight="bold", size=10.5, pad=12):
        w = w or tw(label, size, weight) + pad
        return (block(x, y - PH / 2, w, PH, fill=fill, stroke=stroke, sw=1.2)
                + text(x + w / 2, y + 4, label, size, color, "middle", weight, tip=tip)), w

    def rxn(c, n, name, color=INK):
        return "\n".join([circle(c, 12, fill=color), text(c[0], c[1] + 4.5, n, 12, WHITE, "middle", "900"),
                          text(c[0], c[1] - 18, name, 9.5, MUTED, "middle", style="italic")])

    ITEMS = {}
    base = []
    # top branch: Knoevenagel
    yT, yB = 78, 232
    s1, w1 = pill(300, yT - 22, "ethyl cyanoacetate", "CCOC(=O)CC#N", stroke=GREEN)
    s2, w2 = pill(300, yT + 22, "benzophenone", "O=C(c1ccccc1)c1ccccc1", stroke=GREEN)
    ITEMS["eca"] = (300, yT - 22, w1)
    ITEMS["bzp"] = (300, yT + 22, w2)
    base += [s1, s2, harrow((300 + w1, yT - 22), (488, yT), INK, 1.4), harrow((300 + w2, yT + 22), (488, yT), INK, 1.4),
             rxn((500, yT), "1", "Knoevenagel")]
    s3, w3 = pill(540, yT, "etocrylene", "CCOC(=O)C(C#N)=C(c1ccccc1)c1ccccc1")
    base += [arrow((512, yT), (538, yT), INK, 1.4), s3]
    # bottom branch: 2-EH chain
    chain = [("ethyl acetoacetate", "CCOC(=O)CC(C)=O"), ("1-bromobutane", "CCCCBr")]
    s4, w4 = pill(8, yB - 22, chain[0][0], chain[0][1], stroke=GREEN)
    s5, w5 = pill(8, yB + 22, chain[1][0], chain[1][1], stroke=GREEN)
    base += [s4, s5, harrow((8 + w4, yB - 22), (148, yB), INK, 1.4), harrow((8 + w5, yB + 22), (148, yB), INK, 1.4)]
    seq = [("2", "alkylation", "keto-ester", "CCCCC(C(C)=O)C(=O)OCC  ethyl 2-acetylhexanoate"),
           ("3", "reduction", "hydroxy-ester", "CCCCC(C(=O)OCC)C(C)O  ethyl 2-(1-hydroxyethyl)hexanoate"),
           ("4", "hydrolysis", "hydroxy-acid", "CCCCC(C(=O)O)C(C)O  2-(1-hydroxyethyl)hexanoic acid"),
           ("5", "reduction", "diol", "CCCCC(CO)C(C)O  2-butylbutane-1,3-diol"),
           ("6", "decarbonylation", "2-ethylhexanol", "CCCCC(CC)CO")]
    x = 160
    for n, rname, mol, tip in seq:
        base.append(rxn((x, yB), n, rname))
        s, w = pill(x + 28, yB, mol, tip)
        base += [arrow((x + 12, yB), (x + 26, yB), INK, 1.4), s]
        ITEMS[mol] = (x + 28, yB, w)
        x = x + 28 + w + 16
    ex, _, ew = ITEMS["2-ethylhexanol"]
    # transesterification
    r7 = (762, (yT + yB) / 2)
    base += [harrow((540 + w3, yT), (r7[0] - 12, r7[1]), INK, 1.4, k=0.6),
             harrow((ex + ew, yB), (r7[0] - 12, r7[1]), INK, 1.4, k=0.6),
             rxn(r7, "7", "transesterification")]
    s6, w6 = pill(794, r7[1], "Octocrylene", "CCCCC(CC)COC(=O)C(C#N)=C(c1ccccc1)c1ccccc1", fill=INK, color=CREAM,
                  stroke=INK, size=11.5)
    base += [arrow((774, r7[1]), (792, r7[1]), INK, 1.4), s6,
             text(8, 20, "AiZynthFinder route 0 of 3;  green = purchasable precursor (in stock)", 10.5, MUTED, style="italic")]
    retro = g("retro", *base)
    # balanced equations: co-reactants / by-products
    bp = [((500, yT + 34), "+ H₂O"), ((160, yB + 34), "+ HBr"), ((ITEMS["keto-ester"][0] + ITEMS["keto-ester"][2] + 17, yB + 34), "H₂ >"),
          ((ITEMS["hydroxy-ester"][0] + ITEMS["hydroxy-ester"][2] + 17, yB + 34), "H₂O > EtOH"),
          ((ITEMS["hydroxy-acid"][0] + ITEMS["hydroxy-acid"][2] + 17, yB + 34), "CH₄ > HCHO"),
          ((ITEMS["diol"][0] + ITEMS["diol"][2] + 17, yB + 34), "CO > CO₂"), ((r7[0] + 30, r7[1] + 34), "+ EtOH")]
    completed = g("completed", *[text(p[0], p[1], s, 9.5, ORANGE, "middle", "bold") for p, s in bp],
                  text(8, H - 8, "step 3: by-products / co-reactants added and every equation balanced (RDKit tools + validator)", 10.5, ORANGE,
                       style="italic"))
    # mapping to brightway: upstream replaced
    cut_x1 = ex - 8
    bwcut = g("bw-cut",
              rect(4, yB - 46, cut_x1, 96, fill=CREAM, opacity=0.78),
              rect(4, yB - 46, cut_x1, 96, stroke=GREY, sw=1.2, dash="5 4"),
              text(cut_x1 / 2 + 4, yB + 64, "steps 2–6 not modelled: ecoinvent already has “market for 2-ethylhexanol” (RER)", 10.5, INK,
                   "middle", "bold"),
              db((ex + 10, yB - 62), ORANGE, 1.0),
              text(ex + 24, yB - 51, "ecoinvent 3.12", 9.5, ORANGE, weight="bold"))
    gaps = []
    for k in ("eca", "bzp"):
        gx, gy, gw = ITEMS[k]
        gaps += [rect(gx - 3, gy - PH / 2 - 3, gw + 6, PH + 6, stroke=RED, sw=1.8, dash="4 3"),
                 line((gx - 22, gy - 8), (gx - 8, gy + 8), RED, 2.6), line((gx - 8, gy - 8), (gx - 22, gy + 8), RED, 2.6)]
    gaps += [text(296, yT - 46, "no ecoinvent match: removed (cut-off)", 10.5, RED, "start", "bold")]
    gap = g("gaps", *gaps)
    s2i_tag, s2i_w = tag(276, yT + 46, "candidates for smiles2impact (ML)", 10, fill=ORANGE, color=WHITE, h=18)
    s2i = g("s2i", s2i_tag,
            text(276 + s2i_w / 2, yT + 78, "impact predicted from the SMILES alone", 9.5, ORANGE, "middle", style="italic"))
    fg = g("foreground",
           text(W - 6, r7[1] - 54, "2 foreground activities", 10.5, ORANGE, "end", "bold"),
           text(W - 6, r7[1] - 66, "bw_inventory.json:", 10.5, ORANGE, "end", "bold"))
    write("fig-octocrylene-route.svg", svg(W, H, "\n".join([retro, completed, bwcut, gap, s2i, fg]),
                                          "Octocrylene: retrosynthesis route, balanced steps and Brightway mapping"))


if __name__ == "__main__":
    fig_ssbd()
    fig_paths()
    fig_arch()
    fig_prov()
    fig_route()
    try:
        fig_uml()
    except ImportError as e:
        print("lca_models not importable, skipping UML:", e)
    fig_erdantic()
    if "--png" in os.sys.argv:
        export_png()
