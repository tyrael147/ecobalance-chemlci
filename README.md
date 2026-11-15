# EcoBalance 2026 talk (Slidev)

*Experiences from the use of AI-based approaches to enhance LCA workflows* (Gustavo Larrea-Gallegos, LIST).
20-minute talk in four parts: AI in sustainability research, CALIMERO (ML data-gap filling of toxicity CFs),
PINK / ChemLCI (the earlier *Leveraging machine learning and agentic AI ...* deck, kept as part 3) and MECO-EPD
(agentic classification of EPDs). Same look and feel as the `ecobalance-abm` deck.

```bash
npm install
npm run dev      # http://localhost:3030  (press "p" for presenter mode)
npm run export   # PDF (needs playwright-chromium)
```

The speech, one section per slide with `[click]` markers, is in `_private_source_docs/speech_ai_lca.md`
(the ChemLCI-only speech stays in `speech.md`); the slide-by-slide brief is `_private_source_docs/presentation_information_ai_lca.md`.

## Structure

| path | what |
|---|---|
| `slides.md` | 13 main slides + supplementary slides (tool registry, erdantic, SPARQL, LCIA table, references) |
| `figures/*.svg` | **vector figures (edit in Illustrator)**; one named `<g id>` per layer, revealed on click |
| `figures/png/*.png` | PNG copies (300 dpi, transparent) |
| `components/SvgFigure.vue` | inlines an SVG; `show` / `hide` / `focus` its groups by click; keys starting with `.` are class selectors; ids referenced by `url(#..)` and classes of the figure's own `<style>` are prefixed per instance (no clashes between Illustrator `cls-N`) |
| `components/Step.vue` | click-driven reveal |
| `components/JsonExplorer.vue`, `JsonNode.vue` | collapsible explorer of the ChemLCI artefacts (slide 9) |
| `components/ProvTimeline.vue` | workflow → step → agents/tools drill-down of the provenance graph (slides 8, 10) |
| `components/ProvTrace.vue` | lineage of each inventory exchange back to tool call, candidates, agent, step (slide 10) |
| `data/octocrylene/` | compact JSON derived from `supporting_material/Octocrylene_example_2026_11_2/74268b26` |
| `scripts/extract_data.py` | provenance TTL + artefacts → `data/octocrylene/*.json` (needs `rdflib`) |
| `scripts/build_figures.py` | generates the SVGs (UML/erdantic figures need `lca_models` + `erdantic`; `--png` needs Inkscape) |
| `scripts/build_ontology_figures.py` | `fig-onto-core.svg`, `fig-onto-chem.svg`: VOWL-style ontology layer (`onto`) and UML layer (`uml`) of lca_models, swapped on click; `fig-onto-prov.svg`: provenance classes of LifeCycleOnto.ttl (ontology layer only) |
| `scripts/build_green_economy.py` | `fig-green-economy.svg` from `green_economy.svg` + the two mapping files in `_private_source_docs` |
| `scripts/build_calimero_*.py`, `data/calimero/` | CALIMERO figures redrawn from the paper PNGs (heatmap cells and bar values sampled from the PNGs) |
| `scripts/build_cptax_waffle.py` | `fig-cptax-waffle.svg` (OpenEPD vs cptax categories) |
| `figures/rim/*.jpg` | screenshots of public AI-for-LCA tools (Rapid Inventory Modelling slide) |
| `layouts/`, `slide-bottom.vue`, `style.css`, `public/` | IE-day colours, Raleway, LIST logo (copied from `ecobalance-abm`) |

## Regenerating data and figures

```bash
uv venv /tmp/deckenv && uv pip install --python /tmp/deckenv/bin/python rdflib erdantic -e <path>/lca_models
/tmp/deckenv/bin/python -I scripts/extract_data.py
/tmp/deckenv/bin/python -I scripts/build_figures.py --png
```

Once an SVG has been edited in Illustrator it becomes the source of truth: keep the group ids and do not re-run
the generator for that figure. Figure → group ids used in `slides.md`:

| figure | groups driven by clicks |
|---|---|
| `fig-ssbd-design` | `curve-knowledge`, `zone-insilico`, `candidates` |
| `fig-paths` | `header`, `lane-p1`, `lane-p2`, `lane-ours`, `hitl` |
| `fig-chemlci-arch` | `user`, `orchestrator`, `row-labels`, `step-1` … `step-8`, `prov-bar` |
| `fig-lca-models-uml` | `pkg-*`, `{chem,lci,lcia,base}-{py,rdf,iri}` (python fields ↔ RDF predicates) |
| `fig-prov-layers` | `bands`, `level-workflow`, `level-step`, `level-call`, `level-data` |
| `fig-octocrylene-route` | `retro`, `completed`, `bw-cut`, `gaps`, `foreground` |
| `fig-green-economy` | `grid`, `col-sai`, `proj-band`, `task-*` / `proj-*` (classes `.task`, `.proj`, `.calimero`, `.pink`, `.meco`) |
| `fig-calimero-curation` | `source`, `standardize`, `branch-mordred`, `branch-chemprop`, `branch-grover` |
| `fig-calimero-training` | `train-data`, `process`, `train-curated`, `models`, `performance`, `predict-input`, `predict-curated`, `within-ad`, `assign-cluster`, `best-model` |
| `fig-calimero-performance` | `title`, `axes`, `colorbar`, `cell-r{0..21}-c{0..9}` |
| `fig-calimero-case-study` | `axes`, `legend`, `bars-without`, `bars-with` |
| `fig-meco-problem` | `problem1`, `problem2`, `object`, `consumer-human`, `consumer-ai`, `terms-consumer`, `provider`, `terms-provider`, `semantic-left`, `semantic-right`, `cost-left`, `cost-right`, `nlp-direct`, `indexing` |
| `fig-meco-classification` | `inputs`, `classification`, `extraction`, `database` |
| `fig-meco-exploration` | `cptax`, `exploration`, `step-1` … `step-4`, `isolated`, `schema`, `extraction`, `output` |
| `fig-cptax-waffle` | `unchanged`, `modified`, `moved`, `new`, `dropped`, `caption` |

Do not write inline `<svg>` with unitless presentation attributes (e.g. `font-size="15"`) in `slides.md`: UnoCSS
attributify turns them into global utilities (`font-size: 3.75rem`) that hit every figure using the same value.
Put such drawings in `figures/*.svg` and use `<SvgFigure>`.

## Fonts

Raleway (SIL OFL) is shipped in `public/fonts/raleway/`. Install the `.ttf` files for Illustrator.
