---
theme: default
title: Leveraging machine learning and agentic AI to accelerate the in-silico LCA of chemicals
info: |
  ## Leveraging machine learning and agentic AI to accelerate the in-silico Life Cycle Assessment of chemicals
  Gustavo Larrea-Gallegos, Florian Cogoni, Antonino Marvuglia (LIST) — EcoBalance 2026.

author: Gustavo Larrea-Gallegos
colorSchema: light
aspectRatio: 16/9
canvasWidth: 980
fonts:
  # Raleway is served from public/fonts/raleway (see style.css)
  sans: Raleway
  provider: none
transition: fade
drawings:
  persist: false
mdc: true
duration: 11min
layout: cover
---

# Leveraging <span class="hl">machine learning and agentic AI</span> to accelerate the in-silico Life Cycle Assessment of chemicals

<div class="lead">Rapid Inventory Modelling with ChemLCI: interoperable, provenance-first LCI drafts</div>

<div class="authors">
<b>Gustavo Larrea-Gallegos<sup>1</sup></b>, Florian Cogoni<sup>1</sup>, Antonino Marvuglia<sup>1</sup>
</div>

<div class="affil">
<div><sup>1</sup>Environmental Sustainability Assessment and Circularity (SUSTAIN), Luxembourg Institute of Science and Technology, Luxembourg</div>
</div>

<div class="rule"></div>
<div class="event">EcoBalance 2026 - Nagoya, Japan</div>
<div class="date">November 2026</div>

---
clicks: 3
---

# Sustainability <span class="hl">by design</span> means deciding with little data

## Safe and Sustainable by Design (SSbD): assess while the molecule is still an idea

<div class="grid grid-cols-[1.25fr_1fr] gap-8 items-center mt-1">

<div class="figcard">
<SvgFigure src="fig-ssbd-design"
  :show="{ 'curve-knowledge': 1, 'zone-insilico': 2, candidates: 3 }" />
</div>

<div class="text-[0.9rem]">
<Step :from="0">

- SSbD asks for **hazard, safety and environmental** assessment along the whole innovation process

</Step>
<Step :from="1">

- But the data for a detailed LCI only arrives **when the design is already fixed**

</Step>
<Step :from="2">

- At low TRL, LCA has to be **in-silico and explorative**: screen, compare, iterate

</Step>
<Step :from="3" class="callout mt-4 small">
Chemical selection needs <b>many fast, explicit and comparable inventories</b>, not one perfect LCI.
</Step>
</div>
</div>

<div class="source">SSbD framework: Caldeira et al. (2022), JRC</div>

---
clicks: 4
---

# Predicting impacts of <span class="hl">new chemicals</span>

## two methodological paths, and an agentic alternative

<div class="flex justify-center -mt-1">
<SvgFigure src="fig-paths" width="850px"
  :show="{ 'lane-p2': 1, 'lane-ours': 2, hitl: 3 }"
  :focus="{ 0: ['header', 'lane-p1'], 1: ['header', 'lane-p2'], 2: ['header', 'lane-ours'], 3: ['header', 'lane-ours', 'hitl'], 4: [] }" />
</div>

<Step :from="4" class="callout small -mt-2" style="max-width:52rem">
<b>Rapid Inventory Modelling (RIM)</b>, by analogy with Rapid Application Development: <i>prototype first, refine later</i>. The value is in fast, editable LCI drafts, not in precise predictions.
</Step>

<div class="source">Path 1: e.g. Zhang et al. (2024), Kleinekorte et al. (2023) · Path 2: e.g. Langhorst et al. (2025)</div>

---
clicks: 5
---

# ChemLCI: an <span class="hl">agentic LCI builder</span> <span style="font-weight:500;font-size:1.05rem;color:var(--ie-orange)">· 1 orchestrator, 7 agents, 8 steps</span>

<div class="flex justify-center mt-1">
<SvgFigure src="fig-chemlci-arch" width="830px"
  :show="{ 'prov-bar': 5 }"
  :focus="{ 1: ['user', 'orchestrator', 'row-labels', 'step-1', 'step-2'], 2: ['user', 'orchestrator', 'row-labels', 'step-3', 'step-4'], 3: ['user', 'orchestrator', 'row-labels', 'step-5', 'step-6'], 4: ['user', 'orchestrator', 'row-labels', 'step-7', 'step-8'], 5: [] }" />
</div>

---
clicks: 2
---

# From a handful of tools to a <span class="hl">toolbox</span>

## what changed since LCM 2025

<div class="grid grid-cols-[0.8fr_2fr] gap-6 mt-1">

<div class="block" style="opacity:.85">
<div class="accent" style="font-weight:800">LCM 2025 · Palermo</div>
<div class="tiny muted mb-2">4 agents · 6 tools</div>
<div class="small"><b>agents</b></div>
<span class="tag">conductor</span><span class="tag">synthesis designer</span><span class="tag">chemical “expert” (deep research)</span><span class="tag">LCA builder</span>
<div class="small mt-2"><b>tools</b></div>
<span class="tag">PubChem SMILES</span><span class="tag hi">AiZynthFinder</span><span class="tag">balance check</span><span class="tag hi">ecoinvent 3.11 RAG</span><span class="tag hi">SMILES → impact (XGBoost)</span><span class="tag">BW json</span>
</div>

<Step :from="1">
<div class="block">
<div class="flex items-baseline gap-3"><span class="accent" style="font-weight:800">ChemLCI 2026</span><span class="tiny muted">8 agents · 24 registered tools · ecoinvent 3.12 · Brightway 2.5</span></div>
<div class="grid grid-cols-2 gap-x-5 gap-y-1 mt-1 text-[0.72rem]">
<div><b>identification</b><br><span class="tag">PubChem</span><span class="tag">CIR resolver</span></div>
<div><b>retrosynthesis microservices</b><br><span class="tag hi">AiZynthFinder</span><span class="tag hi">ASKCOS</span><span class="tag">route chooser</span></div>
<div><b>chemistry (RDKit)</b><br><span class="tag">split reaction</span><span class="tag">balance reaction</span><span class="tag">missing atoms</span><span class="tag">by-products</span><span class="tag">co-reactants</span></div>
<div><b>validators (lca_models)</b><br><span class="tag">equation format</span><span class="tag">equation balance</span><span class="tag">draft format</span><span class="tag">Brightway inventory</span></div>
<div><b>ecoinvent 3.12</b><br><span class="tag">process search</span><span class="tag">flow search</span><span class="tag hi">semantic search</span><span class="tag">process node</span><span class="tag">biosphere flow</span></div>
<div><b>LCIA (Brightway 2.5)</b> · <b>session</b><br><span class="tag">LCIA methods</span><span class="tag">run LCIA</span><span class="tag">save / load</span><span class="tag">location</span><span class="tag">go to task</span></div>
</div>
<div class="tiny muted mt-2"><span class="tag hi">ML</span> = machine-learning model served as a microservice · every tool is registered with <code>@chemlci_tool</code> (software type, model type, uncertainty level)</div>
</div>
</Step>
</div>

<Step :from="2" class="grid grid-cols-4 gap-3 mt-3">
<div class="callout small"><b>Provenance</b><br>every call recorded as a graph</div>
<div class="callout small"><b>Dispatcher</b><br>parallel routes &amp; candidates</div>
<div class="callout small"><b>Resume</b><br>restart any step from edited files</div>
<div class="callout small"><b>Grounded chemistry</b><br>balancing by RDKit tools, not by the LLM</div>
</Step>

---
clicks: 3
---

# lca_models: a shared <span class="hl">data language</span>

<div class="relative -mt-1">
<SvgFigure src="fig-lca-models-uml" width="880px"
  :show="{ 'chem-iri': 1, 'lci-iri': 1, 'lcia-iri': 1, 'chem-rdf': 2, 'lci-rdf': 2, 'lcia-rdf': 2, 'base-rdf': 2 }"
  :hide="{ 'chem-py': 2, 'lci-py': 2, 'lcia-py': 2, 'base-py': 2 }" />

<div class="stack absolute" style="left:4px; top:318px; width:168px">
<Step :from="0" :to="1" class="callout tiny"><b>pydantic classes</b> define and <b>validate</b> every agent output.<br>Octocrylene run: 6 LLM-invented UUIDs rejected.</Step>
<Step :from="1" :to="2" class="callout tiny">each class is bound to an <b>ontology class</b>:<br><code>@ontology_class("Flow", prefix="oriont")</code><br><span style="color:#2f7fb5">ssbd</span> · <span style="color:#80350e">oriont</span> · <span style="color:#7a4ea3">emmo</span> · <span style="color:#f46524">lcont</span></Step>
<Step :from="2" :to="3" class="callout tiny">each field carries its <b>RDF predicate</b>: <code>to_rdf_node()</code> → JSON-LD straight into the provenance graph; content-hash IRIs (same ecoinvent code ⇒ same IRI).</Step>
<Step :from="3" class="callout tiny"><b>interoperability</b>: AiZynthFinder and ASKCOS both return a <code>RetrosynthesisRoute</code>; an <code>Inventory</code> imports into Brightway.</Step>
</div>
</div>

<div class="source" style="left:auto;right:6rem">git.list.lu/pink/lca_models · erdantic diagrams in the supplementary material</div>

---
clicks: 4
---

# Provenance <span class="hl">by design</span>: the run is a graph

## PROV-O + SSbD core ontology + lcont · recorded at runtime by agent callbacks (adk_prov)

<div class="flex justify-center -mt-2">
<SvgFigure src="fig-prov-layers" width="820px"
  :show="{ 'level-step': 1, 'level-call': 2, 'level-data': 3 }"
  :focus="{ 4: ['bands', 'level-call', 'level-data'] }" />
</div>


---
clicks: 4
---

# Octocrylene: from <span class="hl">one sentence</span> to an LCI

## UV filter used in sunscreens · “I want LCI for Octocrylene produced in Europe.”

<div class="flex justify-center -mt-1">
<SvgFigure src="fig-octocrylene-route" width="840px"
  :show="{ completed: 1, 'bw-cut': 2, gaps: 3, foreground: 4 }" />
</div>

<div class="mt-1" style="padding: 0 1rem">
<ProvTimeline compact :initial="0" />
</div>

---

# Outputs are <span class="hl">data objects</span>, not text

## explore the artefacts of the Octocrylene run

<script setup>
import bw from './data/octocrylene/bw_inventory.json'
import lcia from './data/octocrylene/lcia_results.json'
import route from './data/octocrylene/completed_route.json'
import retro from './data/octocrylene/retro_0.json'
const cc = lcia.scores.find(s => s.category_key.endsWith('climate change / global warming potential (GWP100)')) ?? lcia.scores[1]
const tabs = [
  { step: '2', label: 'retro_0.json', cls: 'RetrosynthesisRoute', data: retro, open: 2 },
  { step: '3', label: 'completed_route.json', cls: 'SynthesisRoute', data: route, open: 1 },
  { step: '6', label: 'bw_inventory.json', cls: 'Inventory', data: bw, open: 2 },
  { step: '7', label: 'lcia_results.json', cls: 'LCIAResult', data: lcia, open: 1 },
]
</script>

<div class="grid grid-cols-[2.1fr_1fr] gap-5 -mt-1">
<JsonExplorer :tabs="tabs" :initial="2" height="318px" />

<div class="flex flex-col gap-3">
<div class="block text-center">
<div class="tiny muted">EF v3.1 climate change</div>
<div style="font-weight:900;font-size:2rem;color:var(--ie-orange);line-height:1.1">{{ cc.score.toFixed(2) }}</div>
<div class="small"><b>{{ cc.unit }}</b> / kg octocrylene</div>
<div class="tiny muted mt-1">21 EF v3.1 categories · Brightway 2.5 · ecoinvent 3.12 cut-off</div>
</div>
<div class="block small">
<b>2</b> foreground activities<br><b>7</b> ecoinvent nodes, each with its <i>code</i><br><b>iri</b> + <b>ssbd_class</b> on every score
</div>
<div class="callout tiny">A <b>draft</b>: two precursors are missing (next slides). Directly reusable in Brightway or any other engine.</div>
</div>
</div>

---
clicks: 1
---

# Tracing back <span class="hl">how the agents computed</span>

<div class="stack">
<Step :from="0" :to="1">

## workflow → step → agents & tools: click a step

<ProvTimeline :initial="6" />

</Step>
<Step :from="1">

## output → lineage: click an exchange of the inventory

<div style="height:24.5rem"><ProvTrace initial="Toluene" /></div>

</Step>
</div>

---
clicks: 3
---

# Limitations and <span class="hl">next steps</span>

<style>
.numrow .head { font-size: 1.2rem; }
.numrow .body { font-size: 0.95rem; margin-top: 0.3rem; }
</style>

<div class="grid grid-cols-2 gap-x-10 gap-y-10 mt-12">
<Step :from="0" class="numrow">
<div class="num">1</div>
<div><div class="head">Validation & error propagation</div>
<div class="body it">Benchmark drafts against reference LCIs; propagate the uncertainty already tagged on every object and tool.</div></div>
</Step>
<Step :from="1" class="numrow">
<div class="num">2</div>
<div><div class="head">Gaps are pruned, not filled</div>
<div class="body it">Benzophenone and ethyl cyanoacetate had no ecoinvent match and were cut off. Reconnect the SMILES → impact model (Path 1) as a flagged gap-filler.</div></div>
</Step>
<Step :from="2" class="numrow">
<div class="num">3</div>
<div><div class="head">Narrative ≠ data</div>
<div class="body it">The final LLM summary describes a 7-step route; the computed inventory has 2 steps + ecoinvent 2-ethylhexanol. Trust the provenance-linked objects; generate reports from the graph.</div></div>
</Step>
<Step :from="3" class="numrow">
<div class="num">4</div>
<div><div class="head">Expert rationale & cost</div>
<div class="body it">Energy, solvents and emissions are LLM heuristics: bring in industrial expert rules and human review. One route: ~18 min, ~4.9 M tokens with a small model.</div></div>
</Step>
</div>

---
clicks: 2
---

<div class="grid grid-cols-[0.8fr_1.45fr] gap-10 h-full items-center">

<style>
.numrow { margin-bottom: 1.6rem; }
.numrow .head { font-size: 1.2rem; }
.numrow .body { font-size: 0.95rem; margin-top: 0.3rem; }
</style>

<div>
<div class="side-title">Rapid <span class="hl">Inventory</span> Modelling</div>
<div class="accent mt-4" style="font-weight:500;font-style:italic">fast prototypes of LCIs for chemicals at early design stages</div>
</div>

<div>
<Step :from="0" class="numrow">
<div class="num">1</div>
<div><div class="head">Explicit LCIs in minutes</div>
<div class="body it">Agents + ML tools draft computable inventories for many candidates: prototypes to iterate on, not predictions to trust.</div></div>
</Step>
<Step :from="1" class="numrow">
<div class="num">2</div>
<div><div class="head">Interoperable by construction</div>
<div class="body it">Shared pydantic / ontology models make agent outputs validated, Brightway-ready and exchangeable between tools.</div></div>
</Step>
<Step :from="2" class="numrow">
<div class="num">3</div>
<div><div class="head">Provenance first</div>
<div class="body it">Every number traces back to the tool call, the candidates, the agent and the model behind it: auditing and humans in the loop.</div></div>
</Step>
</div>

</div>

---
layout: end
---

# Thank <span class="hl">you</span>

<div class="contact">
<div class="lbl">contact information</div>
<div> gustavo.larrea@list.lu </div>
<div style="font-weight:700">Gustavo Larrea-Gallegos</div>
<div><i>Luxembourg Institute of Science and Technology (LIST)</i></div>
<div class="tiny mt-6" style="color:#cfc9ad">PINK has received funding from the European Union's Horizon Europe Research and Innovation programme under grant agreement No. 101137809.</div>
</div>

---
layout: section
---

# Supplementary <span class="hl">material</span>

---

# Tool registry

## every tool is annotated with <code>@chemlci_tool</code>; the metadata is written into the provenance graph

<table class="list-table mt-1">
<thead><tr><th style="width:17%">module</th><th style="width:43%">tool</th><th style="width:22%">type</th><th>uncertainty level</th></tr></thead>
<tbody>
<tr><td>pubchem / chemistry</td><td>get_chemical_from_pubchem, get_molecule_from_cir</td><td>database lookup</td><td>0</td></tr>
<tr><td>retrosynthesis</td><td>predict_retrosynthesis (AiZynthFinder | ASKCOS), choose_retrosynthesis_route</td><td>emmo:MachineLearningModel</td><td>2 · 0</td></tr>
<tr><td>chemistry (RDKit)</td><td>split_reaction_smiles, balance_reaction_smiles</td><td>deterministic</td><td>0</td></tr>
<tr><td></td><td>identify_missing_atoms · suggest_byproduct_combinations, suggest_coreactant_combinations</td><td>heuristic search</td><td>2 · 3</td></tr>
<tr><td>validators</td><td>equation_format_validator, validate_equation_balance, draft_format_validator, validate_bw_inventory</td><td>pydantic / lca_models</td><td>0</td></tr>
<tr><td>brightway</td><td>search_ecoinvent_processes, search_ecoinvent_flows, get_biosphere_flow · get_process_node</td><td>database search</td><td>0 · 1</td></tr>
<tr><td></td><td>get_activities_embeddings</td><td>semantic (embedding) search</td><td>3</td></tr>
<tr><td>lcia</td><td>search_lcia_methods, run_lcia</td><td>Brightway 2.5</td><td>0</td></tr>
<tr><td>io / session</td><td>save_json, load_json, save_location, go_to_task</td><td>state</td><td>0</td></tr>
</tbody>
</table>

---

# lca_models with <span class="hl">erdantic</span>

## entity-relationship diagrams generated directly from the pydantic models

<div class="grid grid-cols-3 gap-4 items-start mt-2">
<div><div class="small"><b>Inventory</b></div><SvgFigure src="erd-inventory" /></div>
<div><div class="small"><b>LCIAResult</b></div><SvgFigure src="erd-lcia" /></div>
<div><div class="small"><b>SynthesisRoute</b></div><SvgFigure src="erd-synthesis" /></div>
</div>

---

# Querying the provenance graph

## SPARQL: which tool call chose each ecoinvent node, and among how many candidates?

<div class="grid grid-cols-[1.1fr_1fr] gap-5 mt-1">

```sparql {all|3-5|6-9|all}
SELECT ?activity ?ecoinvent ?query ?agent
       (COUNT(?cand) AS ?candidates) WHERE {
  ?node  rdfs:label ?activity ;
         prov:wasDerivedFrom ?eco .
  ?eco   a lcont:BackgroundActivity ; rdfs:label ?ecoinvent .
  ?call  lcont:selectedActivity ?eco ;
         lcont:searchQuery ?query ;
         lcont:returnedCandidate ?cand ;
         prov:wasAssociatedWith ?agent .
  ?agent a lcont:LLMAgent .
} GROUP BY ?activity ?ecoinvent ?query ?agent
```

<table class="list-table">
<thead><tr><th>activity</th><th>selected ecoinvent node</th><th>query</th><th>#</th></tr></thead>
<tbody>
<tr><td>2-Ethylhexanol</td><td>market for 2-ethylhexanol</td><td>2-ethylhexanol</td><td>4</td></tr>
<tr><td>Toluene</td><td>market for toluene, liquid</td><td>toluene</td><td>10</td></tr>
<tr><td>Heat, process</td><td>market for heat, from steam, in chemical industry</td><td>market for heat</td><td>10</td></tr>
<tr><td>Ethanol</td><td>market for ethanol, without water, 99.7%, from ethylene</td><td>ethanol</td><td>9</td></tr>
<tr><td>Piperidine</td><td>piperidine production</td><td>piperidine</td><td>2</td></tr>
<tr><td>Piperidine</td><td>piperidine production</td><td><span class="accent"><b>nickel metal</b></span></td><td>10</td></tr>
</tbody>
</table>
</div>

<div class="tiny muted mt-2">Results for the Octocrylene run (excerpt, 14 rows). Queries also surface records to review, e.g. a “nickel metal” search linked to <i>piperidine production</i>.</div>

---

# LCIA results <span class="hl">(Octocrylene draft)</span>

<script setup>
import lcia from './data/octocrylene/lcia_results.json'
</script>

<div class="refs" style="columns:2;font-size:0.62rem">
<table class="list-table">
<thead><tr><th>EF v3.1 category</th><th style="text-align:right">score</th><th>unit</th></tr></thead>
<tbody>
<tr v-for="s in lcia.scores" :key="s.iri"><td>{{ s.indicator.name }}</td><td style="text-align:right">{{ s.score.toPrecision(3) }}</td><td>{{ s.unit }}</td></tr>
</tbody>
</table>
</div>

<div class="tiny muted mt-2">1 kg octocrylene, cradle-to-gate, ecoinvent 3.12 cut-off, Brightway 2.5. Draft: benzophenone and ethyl cyanoacetate are not included.</div>

---

# References

<div class="refs mt-1">

<p>Caldeira, C., Farcal, L., Garmendia Aguirre, I., et al. (2022). <i>Safe and sustainable by design chemicals and materials: Framework for the definition of criteria and evaluation procedure for chemicals and materials</i>. EUR 31100 EN, Publications Office of the European Union, Luxembourg.</p>
<p>Genheden, S., Thakkar, A., Chadimová, V., Reymond, J.-L., Engkvist, O., &amp; Bjerrum, E. (2020). AiZynthFinder: a fast, robust and flexible open-source software for retrosynthetic planning. <i>Journal of Cheminformatics</i>, 12, 70.</p>
<p>Kleinekorte, J., et al. (2023). <i>[complete reference as cited in the LCM 2025 deck]</i></p>
<p>Langhorst, T., et al. (2025). <i>[complete reference as cited in the LCM 2025 deck]</i></p>
<p>Lebo, T., Sahoo, S., &amp; McGuinness, D. (2013). <i>PROV-O: The PROV Ontology</i>. W3C Recommendation.</p>
<p>Mutel, C. (2017). Brightway: An open source framework for Life Cycle Assessment. <i>Journal of Open Source Software</i>, 2(12), 236.</p>
<p>Shir, O. M. (2024). <i>[complete reference as cited in the LCM 2025 deck]</i></p>
<p>Tu, Z., et al. (2025). ASKCOS: open-source, data-driven synthesis planning. <i>Accounts of Chemical Research</i>.</p>
<p>Zhang, et al. (2024). <i>[complete reference as cited in the LCM 2025 deck]</i></p>
<p>SSbD core ontology: https://w3id.org/ssbd/ · ORIENTING ontology (ORIONT): https://orienting.eu/oriont · EMMO: https://w3id.org/emmo</p>

</div>
