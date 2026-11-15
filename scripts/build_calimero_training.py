"""Build figures/fig-calimero-training.svg (hand-built vector, stdlib only)."""
import os

K = "#2b2b2b"; B = "#2fa8f0"; T = "#2ab3a6"
FONT = 'font-family="Raleway, Arial, sans-serif" font-weight="700"'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures", "fig-calimero-training.svg")


def text(x, y, s, size=30, fill=K, anchor="middle", rot=None):
    tr = f' transform="rotate({rot} {x} {y})"' if rot else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" {FONT}{tr}>{s}</text>'


def head(x, y, d, col):
    """Arrowhead with tip at (x,y); d = r,l,u,d."""
    L, W = 28, 15
    pts = {"r": [(x, y), (x - L, y - W), (x - L, y + W)],
           "l": [(x, y), (x + L, y - W), (x + L, y + W)],
           "d": [(x, y), (x - W, y - L), (x + W, y - L)],
           "u": [(x, y), (x - W, y + L), (x + W, y + L)]}[d]
    return f'<polygon points="{" ".join(f"{a},{b}" for a, b in pts)}" fill="{col}"/>'


def arrow(d, tip, direction, col=K):
    return (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="4" stroke-linejoin="round"/>'
            + head(*tip, direction, col))


def line(d, col=K):
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="4" stroke-linejoin="round"/>'


def pill(x, y, w=98, h=20):
    k = 10
    return (f'<polygon points="{x+k},{y} {x+w-k},{y} {x+w},{y+h/2} {x+w-k},{y+h} {x+k},{y+h} {x},{y+h/2}" '
            f'fill="#fff" stroke="#111" stroke-width="3.5"/>')


def diamond(cx, cy, r=9):
    return f'<polygon points="{cx},{cy-r} {cx+r},{cy} {cx},{cy+r} {cx-r},{cy}" fill="#fff" stroke="#111" stroke-width="3.5"/>'


def cross(cx, cy):
    return (f'<path d="M{cx-12},{cy-12} L{cx+12},{cy+12} M{cx+12},{cy-12} L{cx-12},{cy+12}" stroke="#111" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="M{cx-12},{cy-12} L{cx+12},{cy+12} M{cx+12},{cy-12} L{cx-12},{cy+12}" stroke="#e86aa6" stroke-width="5" stroke-linecap="round"/>')


def check(cx, cy):
    d = f"M{cx-15},{cy} L{cx-4},{cy+11} L{cx+16},{cy-11}"
    return (f'<path d="{d}" fill="none" stroke="#111" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{B}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')


groups = {}

# ---- train-data
g = []
g.append('<path d="M37,170 V285 A76,22 0 0 0 190,285 V170 Z" fill="#fff" stroke="#1f1b3a" stroke-width="6"/>')
g.append('<path d="M37,222 A76,20 0 0 0 190,222 M37,256 A76,20 0 0 0 190,256" fill="none" stroke="#1f1b3a" stroke-width="6"/>')
g.append('<ellipse cx="113.5" cy="170" rx="76.5" ry="20" fill="#e47c56" stroke="#1f1b3a" stroke-width="6"/>')
for y in (202, 241, 279):
    g.append(f'<circle cx="62" cy="{y}" r="6" fill="#1f1b3a"/>')
g.append(text(124, 82, "EF 3.1 CF, CAS"))
g.append(text(124, 127, "and SMILES"))
g.append(text(113, 392, "TRAINING"))
g.append(arrow("M113,360 V335", (113, 307), "u"))
groups["train-data"] = g

# ---- process
g = []
g.append(arrow("M190,228 H298", (328, 228), "r"))
g.append('<path d="M420,182 H436 A27,27 0 0 1 436,229 H434" fill="none" stroke="#2f4a3f" stroke-width="4"/>')
g.append('<polygon points="422,229 434,221 434,237" fill="#2f4a3f"/>')
g.append('<path d="M376,228 H362 A27,27 0 0 0 362,275 H376" fill="none" stroke="#2f4a3f" stroke-width="4"/>')
g.append('<circle cx="350" cy="182" r="17" fill="#6cc56a"/><circle cx="350" cy="182" r="7" fill="#2f6b3a"/>')
for y in (168, 214, 260):
    g.append(f'<rect x="376" y="{y}" width="44" height="29" rx="6" fill="#f0cf3e"/>')
    g.append(f'<path d="M386,{y+10} H408 M386,{y+19} H402" stroke="#fff" stroke-width="4" stroke-linecap="round"/>')
g.append('<circle cx="444" cy="274" r="21" fill="#58b865"/>')
g.append('<path d="M434,274 L441,281 L455,266" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
g.append(text(398, 104, "Process data"))
g.append(arrow("M470,228 H575", (605, 228), "r"))
groups["process"] = g

# ---- train-curated
g = []
for i, y in enumerate((179, 211, 243, 277)):
    g.append(diamond(622, y))
    g.append(pill(648, y - 10))
g.append(text(680, 334, "Curated data"))
g.append(text(680, 378, "for training"))
groups["train-curated"] = g

# ---- models
g = []
for y0, h, lab in ((68, 84, "ML and DL models"), (188, 78, "Cluster"), (302, 78, "AD")):
    g.append(f'<rect x="932" y="{y0}" width="298" height="{h}" rx="{h/2}" fill="#fff" stroke="#111" stroke-width="4"/>')
    g.append(text(1081, y0 + h / 2 + 11, lab))
g.append(line("M755,228 H840"))
g.append(arrow("M840,228 V128 Q840,110 858,110 H898", (928, 110), "r"))
g.append(arrow("M840,228 H898", (928, 228), "r"))
g.append(arrow("M840,228 V322 Q840,340 858,340 H898", (928, 340), "r"))
groups["models"] = g

# ---- performance
g = []
g.append(text(1507, 25, "Model- and cluster-"))
g.append(text(1507, 69, "specific performance"))
g.append('<rect x="1417" y="95" width="83" height="143" fill="#fbecd3"/>')
g.append('<rect x="1500" y="95" width="83" height="143" fill="#e3ebf6"/>')
g.append('<rect x="1417" y="95" width="166" height="143" fill="none" stroke="#111" stroke-width="5"/>')
g.append('<path d="M1500,85 V240" stroke="#111" stroke-width="4" stroke-dasharray="14 5"/>')
g.append(cross(1460, 126)); g.append(cross(1460, 166)); g.append(check(1462, 208))
for y in (124, 165, 208):
    g.append(check(1543, y))
g.append(arrow("M1230,110 H1305 Q1325,110 1325,130 V148 Q1325,166 1343,166 H1385", (1415, 166), "r"))
g.append(line("M1230,226 H1305 Q1325,226 1325,206 V184 Q1325,166 1343,166"))
groups["performance"] = g

# ---- predict-input
g = []
g.append(text(123, 577, "PREDICTING", fill=T))
g.append(arrow("M123,592 V622", (123, 652), "d"))
g.append(text(0, 685, "Phosphoric acid", anchor="start"))
g.append(text(0, 730, "CAS: 7664-38-2", anchor="start"))
g.append(text(0, 774, "SMILES: OP(=O)(O)O", anchor="start"))
g.append(text(334, 658, "SMILES"))
g.append(arrow("M250,677 H380 Q398,677 398,659 V335", (398, 300), "u", B))
g.append(arrow("M470,228 H517 Q535,228 535,246 V614 Q535,632 553,632 H552", (605, 632), "r", B))
groups["predict-input"] = g

# ---- predict-curated
g = []
g.append(text(677, 551, "Curated data"))
g.append(text(677, 595, "for predicting"))
g.append(diamond(622, 634)); g.append(pill(648, 624))
groups["predict-curated"] = g

# ---- within-ad
g = []
cx, cy = 982, 637
for r, c in ((75, "#c9413f"), (55, "#fff"), (40, "#c9413f"), (24, "#fff"), (14, "#8a2f2f")):
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" stroke="#7a2626" stroke-width="3"/>')
g.append(f'<path d="M{cx},{cy} L1052,566" stroke="#1d2a55" stroke-width="7" stroke-linecap="round"/>')
g.append('<path d="M1034,574 L1042,556 L1052,566 Z M1044,584 L1060,576 L1052,566 Z" fill="#1d2a55"/>')
g.append('<path d="M1038,564 L1048,552 L1070,572 L1058,582 Z" fill="#2c4a9a" stroke="#1d2a55" stroke-width="3" stroke-linejoin="round"/>')
g.append(text(983, 756, "Within AD"))
g.append(arrow("M1081,380 V448 Q1081,466 1063,466 H1008 Q988,466 988,486 V520", (988, 549), "d", B))
g.append(arrow("M755,632 H877", (906, 632), "r"))
groups["within-ad"] = g

# ---- assign-cluster
g = []
g.append('<rect x="1241" y="538" width="147" height="147" rx="6" fill="#bfe3f7" stroke="#2b2b2b" stroke-width="5" stroke-dasharray="14 8"/>')
for x, y, c in ((1259, 556, "#e0559b"), (1321, 556, "#eca72a"), (1259, 618, "#8bd05a")):
    g.append(f'<rect x="{x}" y="{y}" width="52" height="52" rx="4" fill="{c}" stroke="#1d2a35" stroke-width="4"/>')
g.append('<path d="M1340,628 Q1340,618 1350,618 Q1360,618 1360,628 V652 L1385,656 Q1398,660 1397,676 L1392,712 Q1390,722 1380,722 H1340 Q1326,708 1322,690 L1322,682 Q1330,676 1340,684 Z" fill="#f5ead6" stroke="#2b2b2b" stroke-width="4" stroke-linejoin="round"/>')
g.append(text(1310, 756, "Assign cluster"))
g.append(arrow("M1232,226 H1300 Q1318,226 1318,244 V485", (1318, 535), "d", B))
g.append(text(1288, 358, "cluster model", rot=90))
g.append(arrow("M1070,632 H1192", (1222, 632), "r"))
g.append(arrow("M1416,632 H1482 Q1500,632 1500,614 V285", (1500, 253), "u"))
g.append(text(1476, 493, "Cluster Number", rot=-90))
groups["assign-cluster"] = g

# ---- best-model
g = []
g.append(arrow("M1583,166 H1657 Q1675,166 1675,184 V545", (1675, 575), "d", B))
g.append(text(1700, 288, "Best model", rot=90))
g.append('<rect x="1584" y="583" width="182" height="136" rx="9" fill="#fff" stroke="#111" stroke-width="4"/>')
g.append('<path d="M1675,618 V634 M1628,634 H1721 M1628,634 V650 M1721,634 V650 M1628,670 V680 M1604,680 H1650 M1604,680 V690 M1650,680 V690 M1721,670 V680 M1698,680 H1744 M1698,680 V690 M1744,680 V690" fill="none" stroke="#2b2b2b" stroke-width="3.5"/>')
g.append('<circle cx="1675" cy="608" r="11" fill="#f0c33c" stroke="#2b2b2b" stroke-width="3"/>')
for x, y in ((1628, 659), (1721, 659)):
    g.append(f'<circle cx="{x}" cy="{y}" r="9" fill="#8bd05a" stroke="#2b2b2b" stroke-width="3"/>')
for x in (1606, 1650, 1700, 1744):
    g.append(f'<circle cx="{x}" cy="695" r="9" fill="#f0c33c" stroke="#2b2b2b" stroke-width="3"/>')
g.append(arrow("M1770,651 H1795", (1826, 651), "r"))
g.append(text(1862, 660, "CF", fill=T))
g.append(arrow("M680,655 V774 Q680,792 698,792 H1657 Q1675,792 1675,774 V760", (1675, 727), "u"))
groups["best-model"] = g

svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1880 800">']
for gid, items in groups.items():
    svg.append(f'<g id="{gid}">')
    svg.extend(items)
    svg.append('</g>')
svg.append('</svg>')
with open(OUT, "w") as f:
    f.write("\n".join(svg) + "\n")
print("wrote", os.path.normpath(OUT))
