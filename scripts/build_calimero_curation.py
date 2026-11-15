"""Generate figures/fig-calimero-curation.svg (stdlib only). Run: python3 -I scripts/build_calimero_curation.py"""
import os

K = 0.82  # source px (1903 wide) -> viewBox units
INK, BEIGE, GREEN, BLUE, ORANGE, NAVY = "#1f1f1f", "#fcefdf", "#d5ecd4", "#eef4fb", "#e07a5f", "#1a1446"
ARROW = "#333333"
FS = 33


def text(x, y, s, anchor="middle"):
    return (f'<text x="{x}" y="{y + 11}" text-anchor="{anchor}">{s}</text>')


def lines(x, ys, strs):
    return "".join(text(x, y, s) for y, s in zip(ys, strs))


def arrow(x, y1, y2):
    return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2 - 24}" stroke="{ARROW}" stroke-width="5"/>'
            f'<polygon points="{x - 17},{y2 - 34} {x + 17},{y2 - 34} {x},{y2}" fill="{ARROW}"/>')


def head(x, y2):
    return f'<polygon points="{x - 17},{y2 - 34} {x + 17},{y2 - 34} {x},{y2}" fill="{ARROW}"/>'


def rect(x1, y1, x2, y2, fill, rx=0):
    return (f'<rect x="{x1}" y="{y1}" width="{x2 - x1}" height="{y2 - y1}" rx="{rx}" '
            f'fill="{fill}" stroke="{INK}" stroke-width="5"/>')


def diamond(cx, l, r, fill, strs):
    pts = f"{cx},543 {r},692 {cx},843 {l},692"
    return (f'<polygon points="{pts}" fill="{fill}" stroke="{INK}" stroke-width="5" stroke-linejoin="miter"/>'
            + lines(cx, [642, 690, 738], strs))


def group(gid, body):
    return f'<g id="{gid}" transform="scale({K})">{body}</g>'


# source
db = (f'<path d="M868,28 V148 Q868,168 950,168 Q1032,168 1032,148 V28" fill="#fff" fill-opacity="0" stroke="{NAVY}" stroke-width="6"/>'
      f'<path d="M868,28 Q868,8 950,8 Q1032,8 1032,28 Q1032,46 950,46 Q868,46 868,28 Z" fill="{ORANGE}" stroke="{NAVY}" stroke-width="6"/>'
      f'<path d="M868,70 Q868,88 950,88 Q1032,88 1032,70" fill="none" stroke="{NAVY}" stroke-width="6"/>'
      f'<path d="M868,116 Q868,134 950,134 Q1032,134 1032,116" fill="none" stroke="{NAVY}" stroke-width="6"/>')
for y in (60, 101, 142):
    db += f'<circle cx="895" cy="{y}" r="7" fill="{NAVY}"/>'
source = (db + lines(741, [62, 108], ["5899 organic", "chemicals (C)"])
          + text(1060, 86, "EF 3.1 CF", "start") + arrow(950, 168, 250))

# standardize
std = (rect(662, 253, 1240, 357, "#ffffff", 52) + text(950, 303, "Standardize SMILES")
       + text(837, 401, "5227 C")
       + f'<path d="M950,357 V434 Q950,449 935,449 H331 Q316,449 316,464 V516" fill="none" stroke="{ARROW}" stroke-width="5"/>'
       + f'<path d="M950,449 H965 H1571 Q1586,449 1586,464 V516" fill="none" stroke="{ARROW}" stroke-width="5"/>'
       + f'<line x1="950" y1="449" x2="950" y2="516" stroke="{ARROW}" stroke-width="5"/>'
       + head(316, 540) + head(950, 540) + head(1586, 540))


def column(cx, x1, x2, fill, ys, cnt, units, boxes, ytxt, cxl, cxr, dy):
    s = ""
    s += arrow(cx, 843, ys[0])
    for i, (top, bot) in enumerate(ys_boxes(ys, dy)):
        s += rect(x1, top, x2, bot, fill)
        s += lines(cx, [top + 27, top + 75], boxes[i])
        if i < 3:
            s += arrow(cx, bot, ys_boxes(ys, dy)[i + 1][0])
    return s


def ys_boxes(ys, dy):
    h = [(0, 105), (188, 292), (375, 479), (561, 665)]
    return [(ys[0] + a, ys[0] + b) for a, b in h]


def counts(cxl, cxr, ys, rows, tag):
    s = ""
    for y, (c, v) in zip(ys, rows):
        s += text(cxl, y, c) + text(cxr, y, v)
    return s


mordred_boxes = [["Remove descriptors &gt;60% missing", "values"],
                 ["Remove descriptors with near-zero", "variance"],
                 ["Remove high correlated descriptors", "(0.95 Correlation coefficients)"],
                 ["Remove outliers with 5%", "contamination"]]
bm = column(316, 6, 626, BEIGE, [912], None, None, mordred_boxes, None, None, None, 0)
mordred = (diamond(316, 30, 603, BEIGE, ["Generate", "Mordred", "Descriptors (D)"]) + bm
           + counts(185, 448, [836, 1041, 1227, 1414, 1600],
                    [("5227 C", "1880 D"), ("5227 C", "1501D"), ("5227 C", "1407 D"), ("5227 C", "675 D"), ("4965 C", "675 D")], "m"))

chemprop = (diamond(951, 673, 1230, GREEN, ["Generate Graph", "Representatives", "with Chemprop"])
            + text(792, 836, "5227 C") + arrow(951, 843, 1285)
            + rect(723, 1285, 1180, 1575, GREEN)
            + lines(951, [1381, 1428, 1476], ["Keep the same retained", "Mordred-filtered", "chemical set"])
            + text(788, 1600, "4965 C"))

bg = column(1586, 1276, 1896, BLUE, [912], None, None, mordred_boxes, None, None, None, 0)
grover = (diamond(1586, 1299, 1873, BLUE, ["Generate", "GROVER", "Embeddings (E)"]) + bg
          + counts(1437, 1733, [836, 1039, 1225, 1412, 1598],
                   [("5227 C", "5000 E"), ("5227 C", "5000 E"), ("5227 C", "4992 E"), ("5227 C", "4928 E"), ("4965 C", "4928 E")], "g"))

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1560 1340" '
       f'font-family="Raleway, Arial, sans-serif" font-weight="700" font-size="{FS}" fill="{INK}">'
       + group("source", source) + group("standardize", std) + group("branch-mordred", mordred)
       + group("branch-chemprop", chemprop) + group("branch-grover", grover) + "</svg>\n")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures", "fig-calimero-curation.svg")
with open(out, "w") as f:
    f.write(svg)
