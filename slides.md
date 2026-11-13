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
duration: 10min
layout: cover
---

# Leveraging <span class="hl">machine learning and agentic AI</span> to accelerate the in-silico Life Cycle Assessment of chemicals

<div class="authors">
<b>Gustavo Larrea-Gallegos<sup>1</sup></b>, Florian Cogoni<sup>1</sup>, Antonino Marvuglia<sup>1</sup>
</div>

<div class="affil">
<div><sup>1</sup>Environmental Sustainability Assessment and Circularity (SUSTAIN), Luxembourg Institute of Science and Technology, Luxembourg</div>
</div>

<div class="rule"></div>
<div class="event">EcoBalance 2026 - Nagoya, Japan</div>
<div class="date">November 13th, 2026</div>

---
clicks: 2
hide: True
---

<div class="grid grid-cols-[0.7fr_1.6fr] gap-10 h-full items-center">

<style>
.toc .numrow { margin-bottom: 1.9rem; }
.toc .numrow .head { font-size: 1.25rem; }
.toc .numrow .body { font-size: 0.95rem; margin-top: 0.3rem; }
.toc .chips { margin-top: 0.35rem; }
</style>

<div>
<div class="side-title">Outline</div>
</div>

<div class="toc">
<Step :from="0" class="numrow">
<div class="num">1</div>
<div><div class="head">ChemLCI: an agentic LCI builder</div>
<div class="body it">Context description</div>
</div>
</Step>
<Step :from="1" class="numrow">
<div class="num">2</div>
<div><div class="head">A semantic framework for agentic LCI</div>
<div class="body it">Ontologies and data models shared by humans and machines, and provenance by design</div>
</div>
</Step>
<Step :from="2" class="numrow">
<div class="num">3</div>
<div><div class="head">Example of a traceable AI generated LCI
</div>
</div>
</Step>
</div>

</div>

---

# The Safe and <span class="hl"> Sustainable </span> by Design framework


<div class="mt-3 flex justify-center">
<img src="./figures/ssbd-framework-2025.png" style="width:718px" alt="Revised SSbD framework: an iterative cycle of scoping analysis, selection of the SSbD scenario, safety and sustainability assessment, evaluation and documentation, repeated as the innovation matures towards the market">
</div>

<div class="source">Figure: Garmendia Aguirre et al. (2025), Safe and Sustainable by Design Chemicals and Materials. Revised framework (2025), JRC143022</div>

---
clicks: 1
---

# In silico assessment: *Fail <span class="hl">Early</span>, Fail <span class="hl">Cheap</span>*

## the earlier the stage, the simpler the LCA, and the more candidates to compare

<div class="grid grid-cols-[1.05fr_0.95fr] gap-8 items-center mt-2">

<div class="figcard">
<SvgFigure src="fig-lca-completeness"
  :dim="{ 'bar-plant': 1, 'bar-simulation': 1, 'bar-calculations': 1 }" />
</div>

<div class="text-[0.95rem]">
<Step :from="0" class="callout">
A core idea of SSbD: innovators should not find out that a chemical is <b>toxic</b> or <b>unsustainable</b> late in the process, or after its <b>market launch</b>.
</Step>
<Step :from="1" class="mt-5">

- At the **design-idea** stage we only have the **molecule**
- Many candidates, cheap changes: the LCA must be **fast, explorative and in silico**

</Step>
</div>
</div>

<div class="source">Figure: Larrea-Gallegos et al. (2025), adapted from Parvatker and Eckelman (2018)</div>

---
clicks: 3
hide: True
---

# Predicting impacts of <span class="hl">new chemicals</span>

## two methodological paths, and an agentic alternative

<div class="flex justify-center -mt-1">
<SvgFigure src="fig-paths" width="850px"
  :show="{ 'lane-p2': 1, 'lane-ours': 2, hitl: 3 }"
  :focus="{ 0: ['header', 'lane-p1'], 1: ['header', 'lane-p2'], 2: ['header', 'lane-ours'], 3: ['header', 'lane-ours', 'hitl'] }" />
</div>

<div class="source">Path 1: e.g. Zhang et al. (2024), Kleinekorte et al. (2023). Path 2: e.g. Langhorst et al. (2025)</div>

---
clicks: 4
---

# ChemLCI: an <span class="hl">agentic LCI builder</span> <span style="font-weight:500;font-size:1.05rem;color:var(--ie-orange)">(1 orchestrator, 7 agents, 8 steps)</span>

<div class="relative">
<div class="flex justify-center mt-2">
<SvgFigure src="fig-chemlci-arch" width="880px"
  :show="{ 'prompt-smiles': 1 }"
  :focus="{ 1: ['user', 'prompt-smiles', 'orchestrator', 'row-labels', 'step-1', 'step-2'], 2: ['user', 'prompt-smiles', 'orchestrator', 'row-labels', 'step-3', 'step-4'], 3: ['user', 'prompt-smiles', 'orchestrator', 'row-labels', 'step-5', 'step-6'], 4: ['user', 'prompt-smiles', 'orchestrator', 'row-labels', 'step-7', 'step-8'] }" />
</div>

<Step :from="3" :to="4" class="absolute s2i-float" style="right:0px; top:104px; width:214px">
<div class="block" style="padding:0.45rem 0.55rem 0.35rem">
<div class="flex items-baseline justify-between"><b class="accent small">smiles2impact</b><span class="tag hi" style="font-size:0.58rem">ML microservice</span></div>
<img src="./figures/smiles2impact.jpg" style="width:100%;margin-top:2px" alt="smiles2impact parity plot">
<div class="tiny muted">Impacts predicted from molecular descriptors (Path 1) for inputs with no ecoinvent match. EF v3.1 climate change shown.</div>
</div>
</Step>
</div>

<style>
.s2i-float { transform: rotate(1.2deg); }
.s2i-float.step-hidden { transform: rotate(1.2deg) translateY(6px); }
</style>

---
clicks: 4
---

# There is a proliferation of <span class="hl">AI-based LCA tools</span>

<style>
.collage { display: grid; grid-template-columns: repeat(3, 1fr); gap: 9px; }
.shot { position: relative; background: #fff; box-shadow: var(--shadow); padding: 3px; }
.shot:nth-child(odd) { transform: rotate(-1.2deg); }
.shot:nth-child(even) { transform: rotate(0.9deg); }
.shot img { display: block; width: 100%; aspect-ratio: 16/10; object-fit: cover; object-position: top; }
.shot .cap { font-size: 0.55rem; line-height: 1.2; padding: 2px 2px 0; color: var(--ie-dark); }
.shot .cap b { color: var(--ie-orange); }
.shot.otf { display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; background: var(--ie-bg-dark); color: var(--ie-cream); font-size: 0.66rem; padding: 0.5rem; }
.rim-src { max-width: 42.5rem; }
.duo { display: grid; grid-template-columns: 1fr auto 1fr; align-items: stretch; gap: 0.4rem; }
.duo-card { background: #fff; box-shadow: var(--shadow); padding: 0.5rem 0.65rem 0.5rem; border-top: 4px solid var(--ie-orange); }
.duo-card.dark { background: var(--ie-bg-dark); color: var(--ie-cream); }
.duo-k { font-size: 0.6rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--ie-orange); }
.duo-name { font-family: monospace; font-weight: 700; font-size: 1.05rem; line-height: 1.25; }
.duo-sub { font-size: 0.66rem; line-height: 1.3; font-style: italic; opacity: 0.85; margin-top: 0.1rem; }
.duo-plus { align-self: center; font-weight: 900; font-size: 1.7rem; color: var(--ie-orange); }
</style>

<div class="grid grid-cols-[1.15fr_1fr] gap-6 mt-2">

<div>
<div class="collage">
<div class="shot"><img src="./figures/rim/zhang-arxiv.jpg" alt=""><div class="cap"><b>Zhang et al. 2026</b>: multimodal LCA agents</div></div>
<div class="shot"><img src="./figures/rim/spidergen.jpg" alt=""><div class="cap"><b>SpiderGen</b>: LLM process flows for LCA</div></div>
<div class="shot"><img src="./figures/rim/benchmark.jpg" alt=""><div class="cap"><b>Donaldson et al. 2025</b>: LLMs-in-LCA benchmark</div></div>
<div class="shot"><img src="./figures/rim/fauldier.jpg" alt=""><div class="cap"><b>FAULDIER</b>: LLM-assisted LCI</div></div>
<div class="shot"><img src="./figures/rim/olca-mcp.jpg" alt=""><div class="cap"><b>openLCA MCP</b> server</div></div>
<div class="shot"><img src="./figures/rim/tiangong.jpg" alt=""><div class="cap"><b>TianGong LCA</b> MCP</div></div>
<div class="shot"><img src="./figures/rim/ecoagent.jpg" alt=""><div class="cap"><b>EcoAgent</b>: AI assistant for LCA</div></div>
<div class="shot"><img src="./figures/rim/ecoratings.jpg" alt=""><div class="cap"><b>EcoRatings</b>: LCA agent</div></div>
<div class="shot otf"><div><b>+ frontier models</b><br>writing an LCA calculator<br><i>on the fly</i></div><div class="mt-1" style="font-family:monospace;font-size:0.56rem;color:var(--ie-orange-lt)">&gt; build me a tool that…</div></div>
</div>
<div class="tiny muted mt-2">Screenshots of public pages, November 2026.</div>
</div>

<div class="text-[0.84rem]">
<Step :from="0">

- AI-based LCA tools appear every month: research agents, copilots, MCP servers
- Frontier models now even **implement such tools on the fly**

</Step>
<Step :from="1" class="callout small mt-3">
By analogy with <b>Rapid Application Development</b> in software, we are seeing a proliferation of <b>Rapid Inventory Modelling (RIM)</b> tools. 
</Step>
<Step :from="2" class="mt-3">

</Step>
<Step :from="3" class="mt-2">
<div class="block small" style="padding:0.55rem 0.8rem">
We need the <b>software that computes</b> and the <b>technology that makes it traceable</b> and interoperable.
</div>
</Step>

<Step :from="4" class="mt-3">
<div class="duo">
<div class="duo-card dark">
<div class="duo-k">computes</div>
<div class="duo-name">ChemLCI</div>
<div class="duo-sub">agents and ML tools draft the inventory</div>
</div>
<div class="duo-plus">+</div>
<div class="duo-card">
<div class="duo-k">traces</div>
<div class="duo-name">lca_models</div>
<div class="duo-sub">data models, ontologies and provenance</div>
</div>
</div>
</Step>

</div>
</div>

<div class="source rim-src">Zhang et al. (2026) Nature Electronics; Sitaraman et al. (2025) arXiv:2511.10684; Donaldson et al. (2025) arXiv:2510.19886; github.com/ljlazar/fauldier; github.com/Below280/B280-olca-MCP; github.com/linancn/tiangong-lca-mcp; ecoagent.tech; ecoratings.ai</div>

---
clicks: 1
hide: True
---

<style>
h1 { font-size: 1.55rem !important; }
</style>

# lca_models.<span class="hl">core</span> provides the semantic framework of LCA data

<div class="stack -mt-1 mb-1">
<Step :from="0" :to="1"><h2 style="margin:0">ontology view: what an inventory <i>means</i>, aligned with ORIONT, EMMO and the SSbD core</h2></Step>
<Step :from="1"><h2 style="margin:0">data model view: what an agent <i>must produce</i>, pydantic classes validate every output</h2></Step>
</div>

<div class="flex justify-start">
<SvgFigure src="fig-onto-core" width="830px" :show="{ uml: 1 }" :hide="{ onto: 1 }" />
</div>


---
clicks: 1
---

<style>
h1 { font-size: 1.55rem !important; }
</style>

# lca_models.<span class="hl">chemistry</span> provides semantics for the chemistry domain in LCA

<div class="stack -mt-1 mb-1">
<Step :from="0" :to="1"><h2 style="margin:0">ontology view: a route is a chain of reaction steps acting on EMMO molecules, bridged to LCI flows</h2></Step>
<!--<Step :from="1"><h2 style="margin:0">data model view: AiZynthFinder and ASKCOS both return a <i>RetrosynthesisRoute</i></h2></Step>-->
</div>

<div class="flex justify-start">
<SvgFigure src="fig-onto-chem" width="830px" :show="{ uml: 1 }" :hide="{ onto: 1 }" />
</div>


---

# Provenance <span class="hl">by design</span>: the run is a graph

## PROV-O, SSbD core ontology and lcont, recorded at runtime by ChemLCI

<div class="flex justify-center -mt-1">
<SvgFigure src="fig-prov-layers" width="935px" />
</div>

<!--# Provenance <span class="hl">by design</span>: the ontology behind the graph

## provenance classes of LifeCycleOnto.ttl that adk_prov writes into prov_&lt;run&gt;.ttl

<div class="flex justify-start">
<SvgFigure src="fig-onto-prov" width="830px" />
</div>-->

---
clicks: 5
---

# Octocrylene: from <span class="hl">one sentence</span> to an LCI

## UV filter used in sunscreens: “I want LCI for Octocrylene produced in Europe.”

<div class="flex justify-center -mt-1">
<SvgFigure src="fig-octocrylene-route" width="920px"
  :show="{ completed: 1, 'bw-cut': 2, gaps: 3, s2i: 4, foreground: 5 }" />
</div>


---

# Outputs are <span class="hl">data objects</span>, not text

## artefacts of the Octocrylene run

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
<div class="tiny muted mt-1">21 EF v3.1 categories, Brightway 2.5, ecoinvent 3.12 cut-off</div>
</div>
<div class="block small">
<b>2</b> foreground activities<br><b>7</b> ecoinvent nodes, each with its <i>code</i><br><b>iri</b> + <b>ssbd_class</b> on every score
</div>
<div class="callout tiny">A <b>draft</b>: two precursors are missing, candidates for <b>smiles2impact</b>. Directly reusable in Brightway or any other engine.</div>
</div>
</div>

---

# Tracing back <span class="hl">how the agents computed</span>

## workflow &gt; step &gt; agents and tools

<ProvTimeline :initial="6" />

---

# Tracing back <span class="hl">how the agents computed</span>

## output &gt; lineage: click an exchange of the inventory

<div style="height:25.5rem"><ProvTrace initial="Toluene" /></div>

---
clicks: 2
---

# Limitations and <span class="hl">next steps</span>

<style>
.numrow .head { font-size: 1.2rem; }
.numrow .body { font-size: 0.95rem; margin-top: 0.3rem; }
</style>

<div class="flex flex-col gap-y-9 mt-12" style="max-width:44rem">
<Step :from="0" class="numrow">
<div class="num">1</div>
<div><div class="head">Validation and error propagation</div>
<div class="body it">Benchmark drafts against reference LCIs; propagate the uncertainty already tagged on every object and tool.</div></div>
</Step>
<Step :from="1" class="numrow">
<div class="num">2</div>
<div><div class="head">Making the provenance usable</div>
<div class="body it">The final orchestrator summary describes a 7-step route, but the provenance graph is huge! We need to design visualization instruments to maximise the use of the provenance graph for final users.</div></div>
</Step>
<Step :from="2" class="numrow">
<div class="num">3</div>
<div><div class="head">Expert rationale and cost</div>
<div class="body it">Energy, solvents and emissions are LLM heuristics: bring in industrial expert rules and human review. One route: ~18 min, ~4.9 M tokens with a small model.</div></div>
</Step>
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
</div>

<div class="funders">
<div class="f-row">
<img src="./figures/logos/pink.png" class="f-pink" alt="PINK project">
<div class="f-sep"></div>
<img src="./figures/logos/eu-flag.png" class="f-eu" alt="Flag of the European Union">
<img src="./figures/logos/sbfi.png" class="f-sbfi" alt="Swiss Confederation, State Secretariat for Education, Research and Innovation SERI">
<img src="./figures/logos/ukri-innovateuk.png" class="f-ukri" alt="UKRI Innovate UK">
</div>
</div>

<div class="f-txt">PINK has received funding from the European Union's Horizon Europe Research and Innovation programme under grant agreement <span style="white-space:nowrap">No. 101137809</span>.</div>

<style>
.funders { position: absolute; left: 2.7rem; bottom: 1.6rem; }
.funders .f-row { display: flex; align-items: center; gap: 1.3rem; }
.funders img { display: block; flex-shrink: 0; }
.funders .f-pink { height: 32px; }
.funders .f-sep { width: 1px; height: 40px; background: #5a5a5a; }
.funders .f-eu { height: 32px; }
.funders .f-sbfi { height: 50px; }
.funders .f-ukri { height: 32px; }
.f-txt { position: absolute; left: 50%; top: 19.5rem; transform: translateX(-50%); width: 40rem; text-align: center; font-size: 1.15rem; line-height: 1.45; font-weight: 500; color: var(--ie-cream); }
</style>

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
<tr><td>retrosynthesis</td><td>predict_retrosynthesis (AiZynthFinder | ASKCOS), choose_retrosynthesis_route</td><td>emmo:MachineLearningModel</td><td>2, 0</td></tr>
<tr><td>chemistry (RDKit)</td><td>split_reaction_smiles, balance_reaction_smiles</td><td>deterministic</td><td>0</td></tr>
<tr><td></td><td>identify_missing_atoms, suggest_byproduct_combinations, suggest_coreactant_combinations</td><td>heuristic search</td><td>2, 3</td></tr>
<tr><td>validators</td><td>equation_format_validator, validate_equation_balance, draft_format_validator, validate_bw_inventory</td><td>pydantic / lca_models</td><td>0</td></tr>
<tr><td>brightway</td><td>search_ecoinvent_processes, search_ecoinvent_flows, get_biosphere_flow, get_process_node</td><td>database search</td><td>0, 1</td></tr>
<tr><td></td><td>get_activities_embeddings</td><td>semantic (embedding) search</td><td>3</td></tr>
<tr><td></td><td><b class="accent">smiles2impact</b> (new)</td><td>emmo:MachineLearningModel</td><td>3</td></tr>
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
clicks: 3
---

# lca_models: python fields and <span class="hl">RDF predicates</span>

<div class="relative -mt-1">
<SvgFigure src="fig-lca-models-uml" width="880px"
  :show="{ 'chem-iri': 1, 'lci-iri': 1, 'lcia-iri': 1, 'chem-rdf': 2, 'lci-rdf': 2, 'lcia-rdf': 2, 'base-rdf': 2 }"
  :hide="{ 'chem-py': 2, 'lci-py': 2, 'lcia-py': 2, 'base-py': 2 }" />

<div class="stack absolute" style="left:4px; top:318px; width:168px">
<Step :from="0" :to="1" class="callout tiny"><b>pydantic classes</b> define and <b>validate</b> every agent output.<br>Octocrylene run: 6 LLM-invented UUIDs rejected.</Step>
<Step :from="1" :to="2" class="callout tiny">each class is bound to an <b>ontology class</b>:<br><code>@ontology_class("Flow", prefix="oriont")</code><br><span style="color:#2f7fb5">ssbd</span>, <span style="color:#80350e">oriont</span>, <span style="color:#7a4ea3">emmo</span>, <span style="color:#f46524">lcont</span></Step>
<Step :from="2" :to="3" class="callout tiny">each field carries its <b>RDF predicate</b>: <code>to_rdf_node()</code> writes JSON-LD straight into the provenance graph; content-hash IRIs (the same ecoinvent code gives the same IRI).</Step>
<Step :from="3" class="callout tiny"><b>interoperability</b>: AiZynthFinder and ASKCOS both return a <code>RetrosynthesisRoute</code>; an <code>Inventory</code> imports into Brightway.</Step>
</div>
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
<p>Donaldson, A., Balaji, B., Oriekezie, C., Kumar, M., and Patouillard, L. (2025). An expert-grounded benchmark of general purpose LLMs in LCA. <i>arXiv:2510.19886</i>.</p>
<p>Garmendia Aguirre, I., Abbate, E., Bracalente, G., Mancini, L., Cappucci, G. M., et al. (2025). <i>Safe and Sustainable by Design Chemicals and Materials. Revised framework (2025)</i>. Bracalente, G., Abbate, E., and Garmendia Aguirre, I. (editors). Publications Office of the European Union, Luxembourg. https://data.europa.eu/doi/10.2760/5103785, JRC143022.</p>
<p>Genheden, S., Thakkar, A., Chadimová, V., Reymond, J.-L., Engkvist, O., and Bjerrum, E. (2020). AiZynthFinder: a fast, robust and flexible open-source software for retrosynthetic planning. <i>Journal of Cheminformatics</i>, 12, 70.</p>
<p>Kleinekorte, J., et al. (2023). <i>[complete reference as cited in the LCM 2025 deck]</i></p>
<p>Langhorst, T., et al. (2025). <i>[complete reference as cited in the LCM 2025 deck]</i></p>
<p>Larrea-Gallegos, G. M., Hofer, S., Hofstätter, N., Punz, B., Watzek, N., Lölsberg, W., … and Himly, M. (2025). Integrate &amp; balance aspects for safe and sustainable innovation: Needs analysis on SSbD categories and product development stage requirements to cover the entire life cycle.</p>
<p>Lebo, T., Sahoo, S., and McGuinness, D. (2013). <i>PROV-O: The PROV Ontology</i>. W3C Recommendation.</p>
<p>Mutel, C. (2017). Brightway: An open source framework for Life Cycle Assessment. <i>Journal of Open Source Software</i>, 2(12), 236.</p>
<p>Parvatker, A. G., and Eckelman, M. J. (2018). Comparative evaluation of chemical life cycle inventory generation methods and implications for life cycle assessment results. <i>ACS Sustainable Chemistry and Engineering</i>, 7, 350.</p>
<p>Sitaraman, A., Balaji, B., and Agarwal, Y. (2025). SpiderGen: Towards procedure generation for carbon life cycle assessments with generative AI. <i>arXiv:2511.10684</i>.</p>
<p>Tu, Z., et al. (2025). ASKCOS: open-source, data-driven synthesis planning. <i>Accounts of Chemical Research</i>.</p>
<p>Zhang, Z., et al. (2026). Sustainability assessment using multimodal AI agents. <i>Nature Electronics</i> (arXiv:2507.17012).</p>
<p>Zhang, et al. (2024). <i>[complete reference as cited in the LCM 2025 deck]</i></p>
<p>SSbD core ontology: https://w3id.org/ssbd/. ORIENTING ontology (ORIONT): https://orienting.eu/oriont. EMMO: https://w3id.org/emmo. VOWL notation: Lohmann et al. (2016). PINK: https://pink-project.eu</p>

</div>
