<script setup lang="ts">
/**
 * "Where does this number come from?" Pick an exchange of the Octocrylene inventory
 * and walk back its lineage in the provenance graph:
 *   exchange (oriont:Flow) > oriont:Activity > prov:wasDerivedFrom ecoinvent node
 *   > lcont:selectedActivity of a lcont:ToolCall (with all lcont:returnedCandidate)
 *   > lcont:LLMAgent / LLM > lcont:WorkflowStep > lcont:Computation
 * Each card: ontology class (orange chip), file it lives in (blue chip), record (bold),
 * attributes recorded on the node (grey italic); cards are linked by predicates.
 * Data: data/octocrylene/trace.json (scripts/extract_data.py).
 */
import { computed, ref } from 'vue'
import trace from '../data/octocrylene/trace.json'
import run from '../data/octocrylene/run.json'

interface Item { group: string, activity: string, ex: any, dropped?: boolean }
const items: Item[] = [
  ...trace.activities.flatMap((a: any) => a.exchanges.map((ex: any) => ({ group: a.name, activity: a.name, ex }))),
  ...trace.dropped.map((d: any) => ({ group: 'in the draft, not in the final inventory', activity: d.activity, ex: d, dropped: true })),
]
const groups = [...new Set(items.map(i => i.group))]
const props = withDefaults(defineProps<{ initial?: string }>(), { initial: 'Toluene' })
const sel = ref(items.findIndex(i => i.ex.name === props.initial && !i.dropped))
const it = computed(() => items[sel.value])
const kind = (i: Item) => i.dropped ? 'gap' : i.ex.kind
const step6 = run.steps.find(s => s.n === 6)!
const step3 = run.steps.find(s => s.n === 3)!

interface Card { cls: string, file?: string, title: string, sub?: string, edge?: string, list?: string[], pick?: string, tone?: string }
const chain = computed<Card[]>(() => {
  const i = it.value
  const e = i.ex
  const amount = `${e.amount} ${e.unit}`
  if (i.dropped) {
    const c: Card[] = [{ cls: 'oriont:Flow', file: 'inventory_draft.json', title: `${amount} ${e.name}, input to ${i.activity}`, sub: e.comment, tone: 'gap' }]
    if (e.selection) {
      c.push({ cls: 'lcont:ToolCall', edge: 'matched by', title: `${e.selection.tool}(“${e.selection.query}”)`, sub: `selected: ${e.selection.selected}`, list: e.selection.candidates, pick: e.selection.selected })
      c.push({ cls: 'lcont:ToolCall', edge: 'but', title: 'validate_bw_inventory: removed while fixing 17 structural errors', sub: 'hollow or orphan nodes, invalid codes, invented UUIDs: the agent pruned instead of repairing', tone: 'gap' })
    }
    else {
      c.push({ cls: 'lcont:LLMAgent', edge: 'searched by', title: `EcoinventSearchAgent: “No suitable ecoinvent node found for: ${e.name}”`, sub: 'search_ecoinvent_processes and semantic search (embeddings), 14:33', tone: 'gap' })
      c.push({ cls: 'lcont:LLMAgent', edge: 'so', title: 'BW2LCIbuilder_agent: input removed, cut-off in the final inventory', sub: 'impact under-estimated: a candidate for smiles2impact (Path 1)', tone: 'gap' })
    }
    return c
  }
  const head: Card = { cls: 'oriont:Flow', file: 'bw_inventory.json', title: `${amount} ${e.name}, input to ${i.activity}`, sub: e.comment ? `“${e.comment}”, ${e.agent}` : undefined }
  if (e.kind === 'background' && e.selection) {
    const s = e.selection
    return [
      head,
      { cls: 'oriont:Activity', edge: 'oriont:isOutputOf', title: e.prov_node?.label ?? e.name, sub: e.prov_node?.iri },
      { cls: 'lcont:BackgroundActivity', edge: 'prov:wasDerivedFrom', title: `${s.selected}  [${e.ecoinvent.location}]`, sub: `ecoinvent 3.12 (lcont:inDatabase), code ${e.ecoinvent.code}` },
      { cls: 'lcont:ToolCall', edge: 'lcont:selectedActivity of', title: `${s.tool}(${Object.entries(s.args).map(([k, v]) => `${k}=“${v}”`).join(', ')})`, sub: `${s.time}, ${s.candidates.length} lcont:returnedCandidate`, list: s.candidates, pick: s.selected },
      { cls: 'lcont:LLMAgent', edge: 'prov:wasAssociatedWith', title: `${s.agent}, ${trace.agent_model}`, sub: 'sub-agent invoked by BW2LCIbuilder_agent (agent-as-tool)' },
      { cls: 'lcont:WorkflowStep', edge: 'ssbd:hasSubProcess of', title: `step 6, Brightway LCI, in “${run.title}”`, sub: `${step6.counts.llm} LLM inferences and ${step6.counts.tool} tool calls in this step; query: “${run.query}”` },
    ]
  }
  if (e.kind === 'foreground') {
    return [
      head,
      { cls: 'oriont:Activity', edge: 'oriont:isOutputOf', title: `${e.name} production (Knoevenagel condensation)`, sub: 'no ecoinvent node, so modelled from the route' },
      { cls: 'lcont:Inventory', file: 'inventory_draft.json', edge: 'prov:wasDerivedFrom', title: 'step 5: InventoryDrafter_agent', sub: '1 : 1 molar ratio, MW 277.3 / 361.5 = 0.767 kg per kg Octocrylene' },
      { cls: 'lcont:SynthesisRoute', file: 'completed_route.json', edge: 'ssbd:hasInput', title: 'step 3: SynthesisCompleter and EquationBalancer', sub: `${step3.counts.llm} LLM inferences, ${step3.tools.validate_equation_balance} × validate_equation_balance, ${step3.tools.balance_reaction_smiles} × RDKit balancer` },
      { cls: 'lcont:RetrosynthesisRoute', file: 'retro_0.json', edge: 'ssbd:hasInput', title: 'step 2: predict_retrosynthesis (AiZynthFinder)', sub: 'route 0 of 3; the tool is typed emmo:MachineLearningModel' },
    ]
  }
  return [
    head,
    { cls: 'lcont:BiosphereFlow', edge: 'matched to', title: 'ecoinvent 3.12 biosphere (search_ecoinvent_flows, get_biosphere_flow)', sub: 'elementary flow selected by the agent' },
    { cls: 'lcont:LLMInference', edge: 'amount from', title: 'InventoryDrafter_agent heuristic', sub: 'e.g. CO₂ as a share of product mass: a placeholder, flagged with its source', tone: 'gap' },
  ]
})
</script>

<template>
  <div class="tr">
    <div class="tr-left">
      <div class="tr-list">
        <template v-for="gname in groups" :key="gname">
          <div class="tr-group">{{ gname }}</div>
          <button v-for="i in items.map((x, k) => ({ x, k })).filter(o => o.x.group === gname)" :key="i.k"
                  class="tr-item" :class="[kind(i.x), { on: i.k === sel }]" @click="sel = i.k">
            <span class="tr-dot" />
            <span class="tr-name">{{ i.x.ex.name }}</span>
            <span class="tr-amt">{{ i.x.ex.amount }} {{ i.x.ex.unit }}</span>
          </button>
        </template>
        <div class="tr-legend"><span class="tr-dot foreground" /> foreground <span class="tr-dot background" /> ecoinvent <span class="tr-dot biosphere" /> biosphere <span class="tr-dot gap" /> gap</div>
      </div>
      <div class="tr-key">
        <div class="tr-key-h">how to read a card</div>
        <div><span class="k-cls">lcont:ToolCall</span> ontology class of the node</div>
        <div><span class="k-file">bw_inventory.json</span> file the object lives in</div>
        <div><b>record</b> the node in the provenance graph</div>
        <div><span class="k-sub">grey italic</span> attributes recorded on the node</div>
        <div class="tr-key-edge"><span class="k-edge">prov:used</span> predicate linking two nodes</div>
        <div><span class="tr-key-cand">candidate</span> <span class="tr-key-cand pick">selected</span> what the search returned</div>
        <div><span class="tr-key-gap" /> gap or problem</div>
      </div>
    </div>
    <div class="tr-chain">
      <template v-for="(c, k) in chain" :key="`${sel}-${k}`">
        <div v-if="c.edge" class="tr-edge"><span class="k-edge">{{ c.edge }}</span></div>
        <div class="tr-card" :class="c.tone">
          <div class="tr-cls"><span class="k-cls">{{ c.cls }}</span><span v-if="c.file" class="k-file">{{ c.file }}</span></div>
          <div class="tr-title">{{ c.title }}</div>
          <div v-if="c.sub" class="tr-sub k-sub">{{ c.sub }}</div>
          <div v-if="c.list" class="tr-cands">
            <span v-for="x in c.list" :key="x" :class="{ pick: x === c.pick }">{{ x }}</span>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<style>
.tr { display: grid; grid-template-columns: 0.72fr 1.6fr; gap: 1rem; height: 100%; }
.tr-left { display: flex; flex-direction: column; gap: 0.5rem; min-height: 0; max-height: 23.6rem; }
.tr-list { background: #fff; box-shadow: var(--shadow); padding: 0.3rem 0.4rem; font-size: 0.62rem; overflow: auto; flex: 1; min-height: 0; }
.tr-key { background: #fff; box-shadow: var(--shadow); padding: 0.3rem 0.5rem; font-size: 0.55rem; line-height: 1.6; flex: none; }
.tr-key-h { font-weight: 800; color: var(--ie-orange); font-size: 0.56rem; }
.tr-key .k-cls, .tr-key .k-file { font-size: 0.52rem; }
.tr-key-edge { border-left: 2px solid #bdb7a0; padding-left: 0.35rem; margin-left: 0.15rem; }
.tr-key-cand { font-size: 0.5rem; padding: 0 0.3rem; background: #f2efe0; color: var(--ie-muted); }
.tr-key-cand.pick { background: var(--ie-orange); color: #fff; font-weight: 700; }
.tr-key-gap { display: inline-block; width: 0.9rem; height: 0.7rem; vertical-align: middle; background: #fff; border-left: 4px solid #c0392b; box-shadow: 1px 1px 0 rgba(0,0,0,.15); }
.tr-group { font-weight: 800; color: var(--ie-orange); font-size: 0.58rem; margin: 0.3rem 0 0.1rem; }
.tr-item { display: flex; align-items: center; gap: 0.35rem; width: 100%; border: 0; background: transparent; padding: 0.06rem 0.25rem; cursor: pointer; font: inherit; color: var(--ie-dark); text-align: left; }
.tr-item:hover { background: #fdeee4; }
.tr-item.on { background: var(--ie-bg-dark); color: var(--ie-cream); }
.tr-name { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.tr-amt { font-family: ui-monospace, Menlo, monospace; font-size: 0.56rem; opacity: 0.8; }
.tr-dot { display: inline-block; width: 0.5rem; height: 0.5rem; border-radius: 50%; flex: none; background: var(--ie-dark); }
.foreground > .tr-dot, .tr-dot.foreground { background: var(--ie-orange); }
.background > .tr-dot, .tr-dot.background { background: #2f7fb5; }
.biosphere > .tr-dot, .tr-dot.biosphere { background: #3b8a3a; }
.gap > .tr-dot, .tr-dot.gap { background: #c0392b; }
.tr-legend { margin-top: 0.4rem; font-size: 0.52rem; color: var(--ie-muted); display: flex; gap: 0.25rem; align-items: center; flex-wrap: wrap; }
.tr-chain { display: flex; flex-direction: column; gap: 0; max-height: 22.4rem; overflow: auto; }
.tr-card { background: #fff; box-shadow: var(--shadow); border-left: 4px solid var(--ie-dark); padding: 0.16rem 0.6rem; animation: trin .35s ease both; }
.tr-card:first-child { border-left-color: var(--ie-orange); }
.tr-card.gap { border-left-color: #c0392b; }
.tr-cls { font-size: 0.52rem; display: flex; gap: 0.35rem; margin-top: 0.08rem; }
.tr-title { font-weight: 700; font-size: 0.66rem; line-height: 1.22; }
.tr-sub { font-size: 0.58rem; line-height: 1.25; }
.tr-cands { display: flex; flex-wrap: wrap; gap: 0.15rem 0.3rem; margin-top: 0.15rem; }
.tr-cands span { font-size: 0.47rem; line-height: 1.35; padding: 0 0.3rem; background: #f2efe0; color: var(--ie-muted); }
.tr-cands span.pick { background: var(--ie-orange); color: #fff; font-weight: 700; }
.tr-edge { font-size: 0.54rem; margin-left: 1.1rem; padding: 0.05rem 0 0.05rem 0.45rem; border-left: 2px solid #bdb7a0; line-height: 1.3; }
@keyframes trin { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: none; } }
</style>
