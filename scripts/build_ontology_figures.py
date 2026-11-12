#!/usr/bin/env python3
"""
Ontology view (WebVOWL-like notation) and UML view of the lca_models modules.

  fig-onto-core.svg   lca_models.core      (LCI + LCIA + documentation)
  fig-onto-chem.svg   lca_models.chemistry (molecules, reactions, routes, LCI bridge)
  fig-onto-prov.svg   provenance classes of LifeCycleOnto.ttl used by adk_prov (ontology view only)

Each SVG holds two top-level layers that share the node positions:
  <g id="onto">  classes as circles (VOWL colours: light blue = own namespace
                 lcont, dark blue = reused / external class), object properties
                 as labelled boxes on the edges, subclass axioms as dashed lines.
  <g id="uml">   the same concepts as pydantic classes: fields + types, composition
                 (field) and inheritance, and the ontology class bound to each one
                 with @ontology_class(...).
The slides swap the layers on click (SvgFigure :show / :hide).

Classes, fields, predicates and superclasses were taken from
git.list.lu/pink/lca_models (src/lca_models/*, ontology/LifeCycleOnto.ttl).
Same flat-SVG conventions as build_figures.py (Illustrator-friendly).

Usage:  python -I scripts/build_ontology_figures.py
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_figures import (FONT, GREY, GREY_LT, INK, MUTED, ORANGE, WHITE, CREAM, block, esc, f, g, head, line,  # noqa: E402
                           path, rect, svg, text, tw, write)

# VOWL notation colours (WebVOWL vowl.css)
V_CLASS = "#aaccff"
V_EXT = "#3366cc"
V_PROP = "#aaccff"
NSCOL = {"lcont": ORANGE, "oriont": "#80350e", "emmo": "#7a4ea3", "ssbd": "#2f7fb5"}

R = 43          # class circle radius
BW = 156        # UML box width
HH = 34         # UML header height
RH = 13.8       # UML field row height
FS = dict(cls=10.8, pre=9, sup=9.6, edge=10.4, leg=10.8, ufield=9.7, utype=9.0, uhead=10.8, ulab=9.4)


def camel_lines(name, maxlen=12):
    """Split a CamelCase name into lines of <= maxlen chars."""
    parts, cur = [], ""
    for k, ch in enumerate(name):
        nxt = name[k + 1] if k + 1 < len(name) else ""
        if ch.isupper() and cur and (not cur[-1].isupper() or nxt.islower()):
            parts.append(cur)
            cur = ch
        else:
            cur += ch
    parts.append(cur)
    out, ln = [], ""
    for p in parts:
        if ln and len(ln) + len(p) > maxlen:
            out.append(ln)
            ln = p
        else:
            ln += p
    out.append(ln)
    return out


# ------------------------------------------------------------------ geometry
def circle_pt(c, towards, r=R):
    dx, dy = towards[0] - c[0], towards[1] - c[1]
    n = math.hypot(dx, dy) or 1
    return (c[0] + dx / n * r, c[1] + dy / n * r)


def box_pt(c, hw, hh, towards):
    dx, dy = towards[0] - c[0], towards[1] - c[1]
    t = min(hw / abs(dx) if dx else 1e9, hh / abs(dy) if dy else 1e9)
    return (c[0] + dx * t, c[1] + dy * t)


# ------------------------------------------------------------------ VOWL layer
def vowl_class(cx, cy, prefix, name, sup=None, tip=None, sup_top=False):
    ext = prefix != "lcont"
    fill, col = (V_EXT, WHITE) if ext else (V_CLASS, INK)
    rows = camel_lines(name)
    out = [f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{R}" fill="{fill}" stroke="{INK}" stroke-width="1.6">'
           f'<title>{esc(tip or f"{prefix}:{name}")}</title></circle>']
    lh = FS["cls"] * 1.17
    y0 = cy - (len(rows) - 1) * lh / 2 + 3
    out.append(text(cx, y0 - lh - 1, f"{prefix}:", FS["pre"], col if ext else NSCOL[prefix], "middle", "bold"))
    for i, r_ in enumerate(rows):
        out.append(text(cx, y0 + i * lh, r_, FS["cls"], col, "middle", "bold"))
    if sup:
        out.append(text(cx, cy - R - 6 if sup_top else cy + R + 13, f"⊑ {sup}", FS["sup"], MUTED, "middle", style="italic"))
    return "\n".join(out)


def vowl_edge(a, b, label, kind="obj", bend=0.0, lpos=0.5):
    p, q = circle_pt(a, b), circle_pt(b, a)
    mx, my = p[0] + (q[0] - p[0]) * lpos, p[1] + (q[1] - p[1]) * lpos
    if bend:
        nx, ny = -(q[1] - p[1]), q[0] - p[0]
        n = math.hypot(nx, ny) or 1
        cx_, cy_ = (p[0] + q[0]) / 2 + nx / n * bend, (p[1] + q[1]) / 2 + ny / n * bend
        d = f"M{f(p[0])} {f(p[1])} Q{f(cx_)} {f(cy_)} {f(q[0])} {f(q[1])}"
        mx, my = (p[0] + 2 * cx_ + q[0]) / 4, (p[1] + 2 * cy_ + q[1]) / 4
        tang = (q[0] - cx_, q[1] - cy_)
    else:
        d = f"M{f(p[0])} {f(p[1])} L{f(q[0])} {f(q[1])}"
        tang = (q[0] - p[0], q[1] - p[1])
    if kind == "sub":
        out = [path(d, INK, 1.3, dash="5 3"), head(q, tang, WHITE, 9, 5),
               path(_tri(q, tang), INK, 1.2)]
        w = tw("Subclass of", FS["sup"]) + 8
        out += [rect(mx - w / 2, my - 8, w, 15, fill=CREAM, stroke="none"),
                text(mx, my + 3.5, "Subclass of", FS["sup"], INK, "middle", style="italic")]
        return "\n".join(out)
    if kind == "note":       # not an ontology axiom: workflow annotation
        out = [path(d, GREY, 1.4, dash="2 3"), head(q, tang, GREY, 8, 4.2)]
        w = tw(label, FS["sup"], "bold") + 10
        out += [rect(mx - w / 2, my - 9, w, 17, fill=CREAM, stroke=GREY, sw=0.8),
                text(mx, my + 3.5, label, FS["sup"], MUTED, "middle", "bold", style="italic")]
        return "\n".join(out)
    out = [path(d, INK, 1.3), head(q, tang, INK, 8, 4.2)]
    w = tw(label, FS["edge"]) + 10
    out += [rect(mx - w / 2, my - 9, w, 17, fill=V_PROP, stroke="none"),
            text(mx, my + 3.6, label, FS["edge"], INK, "middle")]
    return "\n".join(out)


def _tri(tip, direction, length=9, half=5):
    n_ = math.hypot(*direction) or 1
    ux, uy = direction[0] / n_, direction[1] / n_
    bx, by = tip[0] - ux * length, tip[1] - uy * length
    return (f"M{f(tip[0])} {f(tip[1])} L{f(bx - uy * half)} {f(by + ux * half)} "
            f"L{f(bx + uy * half)} {f(by - ux * half)} Z")


# ------------------------------------------------------------------ UML layer
def uml_size(fields):
    return BW / 2, (HH + 6 + len(fields) * RH) / 2


def uml_class(cx, cy, pyname, prefix, oname, fields):
    hw, hh = uml_size(fields)
    x, y = cx - hw, cy - hh
    out = [block(x, y, BW, 2 * hh, fill=WHITE),
           rect(x, y, BW, HH, fill=INK),
           text(x + 7, y + 14.5, pyname, FS["uhead"] if len(pyname) < 21 else FS["uhead"] - 1.2, CREAM, weight="bold"),
           text(x + 7, y + 28, f"{prefix}:", FS["pre"], "#cfc9ad", style="italic"),
           text(x + 7 + tw(f"{prefix}:", FS["pre"]) * 1.2 + 4, y + 28, oname,
                min(FS["pre"], FS["pre"] * (BW - 20 - tw(f"{prefix}:", FS["pre"]) * 1.2) / (tw(oname, FS["pre"], "bold") * 1.1)),
                "#f8bd90", weight="bold")]
    for k, (fn, tp) in enumerate(fields):
        yy = y + HH + 12.5 + k * RH
        out.append(text(x + 7, yy, fn, FS["ufield"], INK, weight="bold"))
        out.append(text(x + BW - 6, yy, tp, FS["utype"], MUTED, "end"))
    return "\n".join(out)


def uml_edge(a, fa, b, fb, label, kind="comp", mult=""):
    ha, hb = uml_size(fa), uml_size(fb)
    p, q = box_pt(a, *ha, b), box_pt(b, *hb, a)
    tang = (q[0] - p[0], q[1] - p[1])
    d = f"M{f(p[0])} {f(p[1])} L{f(q[0])} {f(q[1])}"
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    if kind == "inh":
        out = [path(d, GREY, 1.3), path(_tri(q, tang, 10, 6), INK, 1.2, fill=WHITE)]
        return "\n".join(out)
    if kind == "note":
        out = [path(d, GREY, 1.4, dash="2 3"), head(q, tang, GREY, 8, 4.2)]
        out += [text(mx, my - 14 - 11 * k, ln, FS["ulab"], MUTED, "middle", "bold", style="italic")
                for k, ln in enumerate(reversed(label.split("\n")))]
        return "\n".join(out)
    n_ = math.hypot(*tang) or 1
    ux, uy = tang[0] / n_, tang[1] / n_
    dia = (f"M{f(p[0])} {f(p[1])} L{f(p[0] + ux * 6 - uy * 3.6)} {f(p[1] + uy * 6 + ux * 3.6)} "
           f"L{f(p[0] + ux * 12)} {f(p[1] + uy * 12)} L{f(p[0] + ux * 6 + uy * 3.6)} {f(p[1] + uy * 6 - ux * 3.6)} Z")
    out = [path(d, GREY, 1.3), path(dia, INK, 1, fill=INK), head(q, tang, GREY, 7, 3.6)]
    if abs(tang[0]) > 3 * abs(tang[1]):      # horizontal: label above the line, multiplicity below
        rows = label.split("\n")
        out += [text(mx + 3, my - 5 - 11.5 * (len(rows) - 1 - k), r_, FS["ulab"], ORANGE, "middle", "bold") for k, r_ in enumerate(rows)]
        if mult:
            out.append(text(mx + 3, my + 13, mult, FS["ulab"], ORANGE, "middle", "bold"))
    else:
        lab = label.replace("\n", "") + (f" {mult}" if mult else "")
        w = tw(lab, FS["ulab"], "bold") + 8
        out += [rect(mx - w / 2, my - 8.5, w, 15.5, fill=CREAM, stroke="none", opacity=0.92),
                text(mx, my + 3.3, lab, FS["ulab"], ORANGE, "middle", "bold")]
    return "\n".join(out)


# ------------------------------------------------------------------ self loop
def vowl_loop(c, label, angle=90):
    """Object property from a class to itself: a loop leaving the circle in direction `angle` (deg, SVG y down)."""
    th = math.radians(angle)
    a0, a1 = th - math.radians(28), th + math.radians(28)
    p = (c[0] + R * math.cos(a0), c[1] + R * math.sin(a0))
    q = (c[0] + R * math.cos(a1), c[1] + R * math.sin(a1))
    k = 58
    c1 = (p[0] + k * math.cos(a0 - 0.35), p[1] + k * math.sin(a0 - 0.35))
    c2 = (q[0] + k * math.cos(a1 + 0.35), q[1] + k * math.sin(a1 + 0.35))
    d = f"M{f(p[0])} {f(p[1])} C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(q[0])} {f(q[1])}"
    lx, ly = c[0] + (R + 42) * math.cos(th), c[1] + (R + 42) * math.sin(th)
    w = tw(label, FS["edge"]) + 10
    return "\n".join([path(d, INK, 1.3), head(q, (q[0] - c2[0], q[1] - c2[1]), INK, 8, 4.2),
                      rect(lx - w / 2, ly - 9, w, 17, fill=V_PROP, stroke="none"),
                      text(lx, ly + 3.6, label, FS["edge"], INK, "middle")])


# ------------------------------------------------------------------ legends
def _flow(x, y, items):
    """Lay out legend items left to right. item = (kind, label[, extra])."""
    out, s = [], FS["leg"]
    for it in items:
        kind, lab = it[0], it[1]
        if kind == "file":
            out += [path(f"M{x} {y - 11} h8 l4 4 v10 h-12 Z", INK, 1.1, fill=WHITE),
                    text(x + 17, y, lab, s, INK, weight="bold")]
            x += 17 + tw(lab, s, "bold") * 1.12 + 22
            continue
        if kind == "own":
            out.append(f'<circle cx="{f(x + 7)}" cy="{f(y - 4)}" r="7" fill="{V_CLASS}" stroke="{INK}" stroke-width="1"/>')
            dx = 18
        elif kind == "ext":
            out.append(f'<circle cx="{f(x + 7)}" cy="{f(y - 4)}" r="7" fill="{V_EXT}" stroke="{INK}" stroke-width="1"/>')
            dx = 18
        elif kind == "prop":
            out.append(rect(x, y - 11, 26, 14, fill=V_PROP))
            dx = 32
        elif kind == "sub":
            out.append(line((x, y - 4), (x + 28, y - 4), INK, 1.2, dash="5 3"))
            dx = 34
        elif kind == "comp":
            out += [path(f"M{x} {y - 4} l6 -3.6 l6 3.6 l-6 3.6 Z", INK, 1, fill=INK), line((x + 12, y - 4), (x + 34, y - 4), GREY, 1.3)]
            dx = 40
        elif kind == "inh":
            out += [line((x, y - 4), (x + 20, y - 4), GREY, 1.3), path(_tri((x + 30, y - 4), (1, 0), 10, 6), INK, 1.2, fill=WHITE)]
            dx = 36
        else:   # plain / note
            dx = 0
        style = "italic" if kind == "note" else "normal"
        out.append(text(x + dx, y, lab, s, MUTED if kind == "note" else INK, style=style))
        x += dx + tw(lab, s) * 1.08 + 20
    return out


# ------------------------------------------------------------------ assembly
def build(fname, title, W, H, nodes, edges, band=None, ttl="LifeCycleOnto.ttl", py_src="", uml_note="",
          ext_label="reused class (ORIONT, EMMO, SSbD core)", loops=(), with_uml=True):
    """nodes: id -> dict(pos, prefix, oname, sup, py, fields)."""
    onto, uml = [], []
    if band:
        bx, by, bw, bh, lab = band
        common = [rect(bx, by, bw, bh, fill=WHITE, opacity=0.55, rx=14),
                  rect(bx, by, bw, bh, stroke=GREY_LT, sw=1.2, rx=14, dash="6 4")]
        onto += common + [text(bx + 12, by + bh - 7, lab[0], FS["sup"], MUTED, style="italic")]
        uml += common + [text(bx + 12, by + bh - 7, lab[1], FS["sup"], MUTED, style="italic")]
    for e in edges:     # edges below nodes
        a, b, olabel, ulabel = e["a"], e["b"], e.get("o"), e.get("u")
        A, B = nodes[a], nodes[b]
        if olabel is not None:
            onto.append(vowl_edge(A["pos"], B["pos"], olabel, e.get("kind", "obj"), e.get("bend", 0)))
        if with_uml and ulabel is not None:
            uk = {"obj": "comp", "sub": "inh", "note": "note"}[e.get("kind", "obj")]
            uml.append(uml_edge(A["pos"], A["fields"], B["pos"], B["fields"], ulabel, uk, e.get("mult", "")))
    for nid, lab, ang in loops:
        onto.append(vowl_loop(nodes[nid]["pos"], lab, ang))
    for n in nodes.values():
        onto.append(vowl_class(*n["pos"], n["prefix"], n["oname"], n.get("sup"), tip=n.get("tip"), sup_top=n.get("sup_top", False)))
        if with_uml:
            uml.append(uml_class(*n["pos"], n["py"], n["prefix"], n["oname"], n["fields"]))
    ly = H - 10
    leg_o = _flow(4, ly, [("file", ttl), ("own", "lcont class (LIST, this work)"), ("ext", ext_label),
                          ("prop", "object property"), ("sub", "subclass of"), ("note", "⊑ superclass")])
    body = [g("onto", *onto, g("legend-onto", *leg_o))]
    if with_uml:
        leg_u = _flow(4, ly, [("file", py_src), ("comp", "field (composition)"), ("inh", "inheritance"),
                              ("plain", "header: pydantic class and bound ontology class"), ("note", uml_note)])
        body.append(g("uml", *uml, g("legend-uml", *leg_u)))
    write(fname, svg(W, H, "\n".join(body), title))


W_, H_ = 980, 462
C1, C2, C3, C4, C5 = 84, 292, 500, 708, 892
R1, R2, R3 = 66, 220, 374


# ============================================================== core
def fig_core():
    N = {
        "inv": dict(pos=(C1, R1), prefix="lcont", oname="Inventory", sup="oriont:ProductSystem", py="Inventory",
                    fields=[("name", "str"), ("comment", "str"), ("nodes", "list[…Activity]")]),
        "act": dict(pos=(C2, R1), prefix="oriont", oname="Activity", py="LCIActivityNode",
                    fields=[("name", "str"), ("unit", "str"), ("code", "str"), ("location", "Location"),
                            ("exchanges", "list[LCIExchange]")]),
        "flow": dict(pos=(C3, R1), prefix="oriont", oname="Flow", py="LCIExchange",
                     fields=[("name", "str"), ("amount", "float"), ("unit", "str"), ("type", "Literal[…]"),
                             ("flow_object", "FlowObject")]),
        "fo": dict(pos=(C4, R1), prefix="oriont", oname="FlowObject", py="FlowObject",
                   fields=[("name", "str"), ("cas_number", "str"), ("category", "str")]),
        "src": dict(pos=(C5, R1), prefix="lcont", oname="BibliographicSource", sup="dcterms:BibliographicResource",
                    py="BibliographicSource", fields=[("title", "str"), ("author", "str"), ("year", "str"), ("doi", "str")]),
        "sum": dict(pos=(C1, R2), prefix="lcont", oname="LCIASummary", sup="ssbd:Data", sup_top=True, py="LCIASummary",
                    fields=[("method_set", "str"), ("process", "str"), ("location", "Location")]),
        "loc": dict(pos=(C2, R2), prefix="oriont", oname="Location", py="Location",
                    fields=[("code", "str"), ("name", "str")]),
        "asm": dict(pos=(C3, R2), prefix="lcont", oname="Assumption", sup="lcont:Metadata", py="Assumption",
                    fields=[("text", "str"), ("based_on", "list[Reference]")]),
        "ref": dict(pos=(C4 + 50, R2), prefix="lcont", oname="Reference", sup="lcont:Metadata", py="Reference",
                    fields=[("local_id", "str"), ("bibliographic_source", "…Source")]),
        "res": dict(pos=(C1, R3), prefix="oriont", oname="LCIAResult", py="LCIAResult",
                    fields=[("functional_unit", "str"), ("scores", "list[…Score]"), ("summary", "LCIASummary")]),
        "score": dict(pos=(C2, R3), prefix="lcont", oname="ImpactCategoryScore",
                      sup="ssbd:LifeCycleImpactAssessmentCategorisation", py="ImpactCategoryScore",
                      fields=[("score", "float"), ("unit", "str"), ("ssbd_class", "str (IRI)"),
                              ("indicator", "…Indicator")]),
        "ind": dict(pos=(C3 + 20, R3), prefix="oriont", oname="ImpactCategoryIndicator", py="ImpactCategoryIndicator",
                    fields=[("name", "str"), ("unit", "str"), ("impact_category", "…Category")]),
        "cat": dict(pos=(C4 + 44, R3), prefix="oriont", oname="ImpactCategory", py="ImpactCategory",
                    fields=[("name", "str"), ("description", "str")]),
    }
    E = [
        dict(a="inv", b="act", o="hasActivity", u="nodes", mult="1..*"),
        dict(a="act", b="flow", o="hasExchange", u="exchanges", mult="*"),
        dict(a="flow", b="fo", o="hasObjectType", u="flow_\nobject"),
        dict(a="act", b="loc", o="hasLocation", u="location"),
        dict(a="act", b="asm", o="hasAssumption", u="assumptions*"),
        dict(a="asm", b="ref", o="basedOnReference", u="based_on"),
        dict(a="ref", b="src", o="refersToSource", u="bibliographic_source"),
        dict(a="res", b="score", o="hasImpactScore", u="scores", mult="*"),
        dict(a="score", b="ind", o="quantifiesImpactIndicator", u="indicator"),
        dict(a="ind", b="cat", o="assessesImpactCategory", u="impact_\ncategory"),
        dict(a="res", b="sum", o="hasLCIASummary", u="summary"),
        dict(a="sum", b="loc", o="hasLocation", u="location"),
    ]
    build("fig-onto-core.svg", "lca_models.core: ontology and UML views", W_, H_, N, E, py_src="lca_models/core",
          uml_note="every class ⊂ DataModel {iri, source, uncertainty_type}; * via DocumentedActivity")


# ============================================================== chemistry
def fig_chem():
    N = {
        "rr": dict(pos=(C1, R1), prefix="lcont", oname="RetrosynthesisRoute", py="RetrosynthesisRoute",
                   fields=[("target_SMILES", "str"), ("target_name", "str"), ("root_node_id", "str"),
                           ("nodes", "list[RetroNode]")]),
        "rs": dict(pos=(C2, R1), prefix="lcont", oname="RetrosynthesisStep", py="RetrosynthesisNode",
                   fields=[("node_id", "str"), ("reaction_SMILES", "str"), ("product_SMILES", "str"),
                           ("precursors_SMILES", "list[str]")]),
        "sr": dict(pos=(C3 - 12, R1), prefix="lcont", oname="SynthesisRoute", py="SynthesisRoute",
                   fields=[("root_node_id", "str"), ("nodes", "list[…Node]")]),
        "st": dict(pos=(C4 - 18, R1), prefix="lcont", oname="ReactionStep", py="ReactionNode",
                   fields=[("reaction_SMILES", "str"), ("target_molecule", "Molecule"), ("byproducts", "list[…]"),
                           ("detailed_equation", "Equation"), ("process_description", "str")]),
        "eq": dict(pos=(C5, R1), prefix="lcont", oname="ChemicalEquation", py="Equation",
                   fields=[("reaction_smiles", "str"), ("reactants", "list[…]"), ("products", "list[…]")]),
        "cf": dict(pos=(C1, R2), prefix="lcont", oname="ChemicalFlow", sup="oriont:Flow", py="ChemicalEdge",
                   fields=[("amount", "float"), ("unit", "str"), ("flow_object", "ChemicalObject")]),
        "co": dict(pos=(C2, R2), prefix="lcont", oname="ChemicalObject", sup="oriont:FlowObject", py="ChemicalObject",
                   fields=[("name", "str"), ("cas_number", "str"), ("molecule", "Molecule")]),
        "mol": dict(pos=(C3, R2 + 6), prefix="emmo", oname="Molecule", sup="ssbd:Data", py="Molecule",
                    fields=[("name", "str"), ("smiles", "SMILES…"), ("chemical_formula", "…Descriptor"),
                            ("molecular_weight", "…Descriptor"), ("inchi", "InChI…"),
                            ("physical_properties", "list[…]")]),
        "rp": dict(pos=(C5, R2), prefix="lcont", oname="ReactionParticipant", sup="ssbd:Data", py="ReactionParticipant",
                   fields=[("molecule", "Molecule"), ("stoichiometry", "int")]),
        "act": dict(pos=(C1, R3), prefix="lcont", oname="ChemicalProductionActivity", sup="lcont:DocumentedActivity",
                    py="ChemicalProductionNode",
                    fields=[("name", "str"), ("unit", "str"), ("reference_flow", "ChemicalEdge")]),
        "smi": dict(pos=(C2, R3), prefix="lcont", oname="SMILESDescriptor", sup="lcont:TextDescriptor", py="SMILESDescriptor",
                    fields=[("value", "str"), ("method", "str")]),
        "inchi": dict(pos=(C3, R3 + 6), prefix="emmo", oname="InChI", sup="lcont:TextDescriptor", py="InChIDescriptor",
                      fields=[("value", "str"), ("method", "str")]),
        "mw": dict(pos=(C4, R3), prefix="lcont", oname="MolecularWeight", sup=None, py="MolecularWeightDescriptor",
                   fields=[("value", "float"), ("unit", "str")]),
        "qd": dict(pos=(C5 + 4, R3 - 50), prefix="lcont", oname="QuantityDescriptor", sup="ssbd:NumericalData",
                   py="QuantityDescriptor", fields=[("value", "float"), ("unit", "str")]),
    }
    E = [
        dict(a="rr", b="rs", o="hasRetrosynthesisStep", u="nodes", mult="*"),
        dict(a="rs", b="sr", o="ChemLCI step 3", u="ChemLCI\nstep 3", kind="note"),
        dict(a="sr", b="st", o="hasReactionStep", u="nodes", mult="*"),
        dict(a="st", b="eq", o="hasDetailedEquation", u="detailed_\nequation"),
        dict(a="st", b="mol", o="hasTargetMolecule", u="target_molecule"),
        dict(a="eq", b="rp", o="hasReactant, hasProduct", u="reactants, products"),
        dict(a="rp", b="mol", o="hasMolecule", u="molecule"),
        dict(a="cf", b="co", o="hasObjectType", u="flow_\nobject"),
        dict(a="co", b="mol", o="representsMolecule", u="molecule"),
        dict(a="act", b="cf", o="hasDeterminingFlow", u="reference_flow"),
        dict(a="mol", b="smi", o="hasSMILES", u="smiles"),
        dict(a="mol", b="inchi", o="hasInChI", u="inchi"),
        dict(a="mol", b="mw", o="hasMolecularWeight", u="molecular_weight"),
        dict(a="mw", b="qd", o="", u="", kind="sub"),
    ]
    band = (3, R1 - 58, W_ - 6, 128,
            ("⊑ lcont:ChemicalReactionModel ⊑ emmo:AnalogicalIcon, ssbd:Information",
             "⊂ ChemicalReactionModel ⊂ DataModel"))
    build("fig-onto-chem.svg", "lca_models.chemistry: ontology and UML views", W_, H_, N, E, band=band,
          py_src="lca_models/chemistry", uml_note="every class ⊂ DataModel {iri, source, uncertainty_type}")


# ============================================================== provenance
def fig_prov():
    """Classes of LifeCycleOnto.ttl that adk_prov / ChemLCI write into prov_<run>.ttl."""
    N = {
        "user": dict(pos=(C1, R1), prefix="lcont", oname="User", sup="prov:Person"),
        "comp": dict(pos=(C2, R1), prefix="lcont", oname="Computation", sup="ssbd:Computation", sup_top=True),
        "sw": dict(pos=(C3 + 20, R1), prefix="ssbd", oname="Software"),
        "ds": dict(pos=(C5, R1), prefix="ssbd", oname="Dataset", sup="ssbd:Data"),
        "tool": dict(pos=(C1, R2), prefix="lcont", oname="ToolCall", sup="lcont:Computation", sup_top=True),
        "step": dict(pos=(C2, R2), prefix="lcont", oname="WorkflowStep", sup="ssbd:Process", sup_top=False),
        "llm": dict(pos=(C3, R2), prefix="lcont", oname="LLMInference", sup="lcont:Computation", sup_top=True),
        "lsw": dict(pos=(C4, R2), prefix="lcont", oname="LLMSoftware"),
        "model": dict(pos=(C5 + 22, R2), prefix="ssbd", oname="LargeLanguageModel"),
        "data": dict(pos=(C1, R3), prefix="ssbd", oname="Data"),
        "agent": dict(pos=(C2 + 40, R3), prefix="lcont", oname="LLMAgent", sup="prov:SoftwareAgent"),
        "prompt": dict(pos=(C3 + 70, R3), prefix="lcont", oname="Prompt", sup="ssbd:Information"),
        "resp": dict(pos=(C4 + 50, R3), prefix="lcont", oname="LLMResponse", sup="ssbd:Information"),
    }
    E = [
        dict(a="comp", b="user", o="wasAssociatedWith"),
        dict(a="comp", b="sw", o="hasSoftware"),
        dict(a="comp", b="ds", o="hasOutput", bend=-112),
        dict(a="comp", b="step", o="hasSubProcess"),
        dict(a="step", b="tool", o="hasSubProcess"),
        dict(a="step", b="llm", o="hasSubProcess"),
        dict(a="llm", b="lsw", o="hasSoftware"),
        dict(a="lsw", b="model", o="implementsModel"),
        dict(a="lsw", b="sw", o="", kind="sub"),
        dict(a="tool", b="data", o="used, generated"),
        dict(a="tool", b="agent", o="wasAssociatedWith"),
        dict(a="llm", b="agent", o="executedBy"),
        dict(a="llm", b="prompt", o="used"),
        dict(a="llm", b="resp", o="generated"),
    ]
    build("fig-onto-prov.svg", "Provenance classes of LifeCycleOnto.ttl used by adk_prov", W_, H_, N, E,
          ext_label="reused class (SSbD core)", loops=[("step", "isPredecessorOf", -138)], with_uml=False)


if __name__ == "__main__":
    fig_core()
    fig_chem()
    fig_prov()
