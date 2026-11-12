#!/usr/bin/env python3
"""
Extract the compact JSON files used by the interactive slides from a ChemLCI run.

Input  : supporting_material/Octocrylene_example_2026_11_2/74268b26/
           prov_*.ttl            (PROV-O / lcont / SSbD provenance graph, written by adk_prov)
           bw_inventory.json     (lca_models.Inventory, Brightway-ready)
           inventory_draft.json  (lca_models.Inventory, before ecoinvent matching)
           lcia_results.json     (lca_models.LCIAResult)
           retros/retro_*.json   (lca_models.RetrosynthesisRoute)
           run.log               (only used for the "no suitable ecoinvent node" messages)

Output : data/octocrylene/run.json        -> run + workflow-step summary   (ProvTimeline.vue)
         data/octocrylene/trace.json      -> per-exchange lineage           (ProvTrace.vue)
         data/octocrylene/*.json          -> copies of the artefacts shown in JsonTree.vue

Usage  : python -I scripts/extract_data.py      (needs rdflib)
"""
import collections
import glob
import json
import re
import shutil
import sys
from pathlib import Path

import rdflib

ROOT = Path(__file__).resolve().parent.parent
RUN = ROOT / "supporting_material" / "Octocrylene_example_2026_11_2" / "74268b26"
OUT = ROOT / "data" / "octocrylene"
OUT.mkdir(parents=True, exist_ok=True)

LC = rdflib.Namespace("http://ontologies.list.lu/lcont#")
PROV = rdflib.Namespace("http://www.w3.org/ns/prov#")
DC = rdflib.Namespace("http://purl.org/dc/terms/")
SS = rdflib.Namespace("https://w3id.org/ssbd/")
RDF, RDFS = rdflib.RDF, rdflib.RDFS

g = rdflib.Graph()
g.parse(glob.glob(str(RUN / "prov_*.ttl"))[0])
nm = g.namespace_manager


def curie(x):
    return x.n3(nm)


def s(x):
    return None if x is None else str(x)


def hms(t):
    return s(t)[11:19] if t else None


def secs(t0, t1):
    from datetime import datetime
    return round((datetime.fromisoformat(str(t1)) - datetime.fromisoformat(str(t0))).total_seconds(), 1)


def fname(uri):
    return rdflib.term.URIRef(uri).split("/")[-1].replace("%2F", "/").split("/")[-1]


# ------------------------------------------------------------------ run + steps
comp = next(g.subjects(RDF.type, LC.Computation))
model = next(g.subjects(RDF.type, SS.LargeLanguageModel))
type_count = collections.Counter(curie(o) for o in g.objects(None, RDF.type))

steps = []
for st in sorted(g.subjects(RDF.type, LC.WorkflowStep), key=lambda u: int(str(u).rsplit("_", 1)[1])):
    parts = set(g.objects(st, DC.hasPart)) | set(g.objects(st, SS.hasSubProcess))
    kinds = collections.Counter()
    agents = collections.Counter()
    tools = collections.Counter()
    tokens = 0
    for p in parts:
        types = {curie(t) for t in g.objects(p, RDF.type)}
        title = s(g.value(p, DC.title)) or s(g.value(p, RDFS.label)) or ""
        if "lcont:LLMInference" in types:
            kinds["llm"] += 1
            m = re.match(r"model_call — (\S+)", title)
            if m:
                agents[m.group(1)] += 1
            tokens += int(g.value(p, LC.totalTokenCount) or 0)
        elif "lcont:ArtifactSave" in types:
            kinds["save"] += 1
        elif "lcont:ToolCall" in types:
            kinds["tool"] += 1
            m = re.match(r"tool_call — (\S+)", title)
            if m:
                tools[m.group(1)] += 1
        elif "lcont:UserInteraction" in types:
            kinds["user"] += 1
    t0, t1 = g.value(st, PROV.startedAtTime), g.value(st, PROV.endedAtTime)
    steps.append({
        "n": int(str(st).rsplit("_", 1)[1]),
        "label": s(g.value(st, RDFS.label)),
        "title": s(g.value(st, DC.title)),
        "start": hms(t0), "end": hms(t1), "seconds": secs(t0, t1),
        "counts": dict(kinds),
        "tokens": tokens,
        "agents": dict(agents.most_common()),
        "tools": dict(tools.most_common()),
        "inputs": sorted({fname(x) for x in g.objects(st, SS.hasInput)}),
        "outputs": sorted({fname(x) for x in g.objects(st, SS.hasOutput)}),
    })

t0, t1 = g.value(comp, PROV.startedAtTime), g.value(comp, PROV.endedAtTime)
run = {
    "title": s(g.value(comp, DC.title)),
    "workflow_id": str(comp).rsplit("/", 1)[1],
    "query": "I want LCI for Octocrylene produced in Europe.",
    "start": s(t0), "end": s(t1),
    "minutes": round(secs(t0, t1) / 60, 1),
    "model": s(g.value(model, DC.title)),
    "triples": len(g),
    "counts": {
        "llm_inferences": type_count["lcont:LLMInference"],
        "tool_calls": type_count["lcont:ToolCall"],
        "artifact_saves": type_count["lcont:ArtifactSave"],
        "agents": type_count["lcont:LLMAgent"],
        "workflow_steps": type_count["lcont:WorkflowStep"],
        "background_candidates": type_count["lcont:BackgroundActivity"],
        "data_nodes": type_count["ssbd:Data"],
    },
    "tokens": sum(int(v) for v in g.objects(None, LC.totalTokenCount)),
    "steps": steps,
}

# ------------------------------------------------------------------ ecoinvent selections
selections = []
for call, eco in g.subject_objects(LC.selectedActivity):
    assoc = [str(x).rsplit("/", 1)[1] for x in g.objects(call, PROV.wasAssociatedWith)]
    used = next((s(g.value(u, PROV.value)) for u in g.objects(call, PROV.used) if g.value(u, PROV.value)), None)
    try:
        args = json.loads(used) if used else {}
    except json.JSONDecodeError:
        args = {}
    selections.append({
        "call": str(call).rsplit("/", 1)[1],
        "query": s(g.value(call, LC.searchQuery)),
        "args": args,
        "tool": next((a.replace("__tool", "") for a in assoc if a.endswith("__tool")), None),
        "agent": next((a for a in assoc if not a.endswith("__tool")), None),
        "time": hms(g.value(call, PROV.startedAtTime)),
        "selected": s(g.value(eco, RDFS.label)),
        "code": s(g.value(eco, LC.backgroundDbCode)),
        "candidates": sorted({s(g.value(c, RDFS.label)) for c in g.objects(call, LC.returnedCandidate)}),
    })

# background "oriont:Activity" nodes (what ends up in the inventory) keyed by ecoinvent code
bg_nodes = {}
for a in g.subjects(RDF.type, LC.BackgroundActivity):
    if "oriont:Activity_" not in curie(a):
        continue
    bg_nodes[s(g.value(a, LC.backgroundDbCode))] = {
        "iri": curie(a),
        "label": s(g.value(a, RDFS.label)),
        "generated_by": len(list(g.objects(a, PROV.wasGeneratedBy))),
    }

# ------------------------------------------------------------------ inventory + lineage
bw = json.load(open(RUN / "bw_inventory.json"))
draft = json.load(open(RUN / "inventory_draft.json"))
by_id = {n["id"]: n for n in bw["nodes"]}

no_match = sorted(set(re.findall(r"No suitable ecoinvent node found for: ([^\"]+?)(?:, EUR)?\"", open(RUN / "run.log").read())))


def best_selection(name, code):
    cands = [x for x in selections if x["code"] == code]
    if not cands:
        return None
    key = name.lower().split(",")[0]
    cands.sort(key=lambda x: (key not in (x["query"] or "").lower(), x["time"]))
    return cands[0]


activities = []
for node in bw["nodes"]:
    if node["database"].startswith("ecoinvent"):
        continue
    exch = []
    for e in node["exchanges"]:
        item = {
            "name": e["name"], "amount": e["amount"], "unit": e["unit"], "type": e["type"],
            "comment": e.get("comment"), "agent": e.get("source"),
        }
        src = by_id.get(e.get("from_activity"))
        if e["type"] == "biosphere":
            item["kind"] = "biosphere"
        elif src and src["database"].startswith("ecoinvent"):
            item["kind"] = "background"
            item["ecoinvent"] = {"code": src["code"], "location": src["location"]["code"], "database": src["database"]}
            item["prov_node"] = bg_nodes.get(src["code"])
            item["selection"] = best_selection(e["name"], src["code"])
        else:
            item["kind"] = "foreground"
        exch.append(item)
    activities.append({"name": node["name"], "location": node["location"]["code"], "comment": node.get("comment"), "exchanges": exch})

# exchanges present in the draft but absent from the final Brightway inventory
final_names = {(a["name"], e["name"]) for a in activities for e in a["exchanges"]}
dropped = []
for node in draft["nodes"]:
    if node["name"] not in {a["name"] for a in activities}:
        continue
    for e in node.get("exchanges", []):
        if (node["name"], e["name"]) in final_names or e["amount"] < 0 and e["name"] == "Water":
            continue
        reason = "no suitable ecoinvent node found" if any(e["name"].lower() == m.lower() for m in no_match) \
            else "matched, but removed while fixing the inventory (validate_bw_inventory loop)"
        sel = next((x for x in selections if e["name"].lower() in (x["query"] or "").lower()), None)
        dropped.append({"activity": node["name"], "name": e["name"], "amount": e["amount"], "unit": e["unit"],
                        "comment": e.get("comment"), "reason": reason, "selection": sel})

trace = {
    "activities": activities,
    "dropped": dropped,
    "no_match": no_match,
    "replaced_upstream": [n["name"] for n in draft["nodes"] if n.get("exchanges") and n["name"] not in {a["name"] for a in activities}],
    "selections": selections,
    "agent_model": run["model"],
}

json.dump(run, open(OUT / "run.json", "w"), indent=1, ensure_ascii=False)
json.dump(trace, open(OUT / "trace.json", "w"), indent=1, ensure_ascii=False)

# artefacts shown as explorable JSON trees
for f in ["bw_inventory.json", "lcia_results.json", "completed_route.json", "retros/retro_0.json"]:
    shutil.copy(RUN / f, OUT / Path(f).name)

print(f"run: {run['minutes']} min, {run['counts']}, tokens={run['tokens']}", file=sys.stderr)
print(f"activities={len(activities)} dropped={len(dropped)} selections={len(selections)} no_match={no_match}", file=sys.stderr)
