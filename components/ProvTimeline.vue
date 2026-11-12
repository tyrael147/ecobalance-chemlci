<script setup lang="ts">
/**
 * Workflow-level view of a ChemLCI provenance graph: one segment per lcont:WorkflowStep
 * (width proportional to wall-clock time, with a minimum), click a step to see which agents and
 * tools ran inside it. Data: data/octocrylene/run.json (scripts/extract_data.py).
 */
import { computed, ref } from 'vue'
import run from '../data/octocrylene/run.json'

const props = withDefaults(defineProps<{ initial?: number, compact?: boolean }>(), { initial: 3, compact: false })
const sel = ref(props.initial)
const total = run.steps.reduce((a, s) => a + s.seconds, 0)
const MIN = 5.5 // % minimum width so short steps stay clickable
const widths = computed(() => {
  const raw = run.steps.map(s => Math.max(MIN, (100 * s.seconds) / total))
  const k = 100 / raw.reduce((a, b) => a + b, 0)
  return raw.map(w => w * k)
})
const step = computed(() => run.steps.find(s => s.n === sel.value)!)
const calls = (s: any) => (s.counts.llm ?? 0) + (s.counts.tool ?? 0) + (s.counts.save ?? 0)
const maxCalls = Math.max(...run.steps.map(calls))
const fmtT = (s: number) => s < 60 ? `${Math.round(s)} s` : `${Math.floor(s / 60)} min ${Math.round(s % 60)} s`
const fmtK = (n: number) => n > 1e6 ? `${(n / 1e6).toFixed(2)} M` : n > 1e3 ? `${Math.round(n / 1e3)} k` : String(n)
const short = (t: string) => t.replace(/_agent$/, '').replace(/_/g, ' ')
const maxA = computed(() => Math.max(1, ...Object.values(step.value.agents) as number[]))
const maxT = computed(() => Math.max(1, ...Object.values(step.value.tools) as number[]))
</script>

<template>
  <div class="pt">
    <div class="pt-strip">
      <button v-for="(s, i) in run.steps" :key="s.n" class="pt-seg" :class="{ on: s.n === sel }"
              :style="{ width: `${widths[i]}%`, '--a': 0.25 + 0.75 * calls(s) / maxCalls }"
              :title="`${s.title}: ${fmtT(s.seconds)}, ${calls(s)} computations`" @click="sel = s.n">
        <span class="pt-n">{{ s.n }}</span>
        <span v-if="widths[i] > 12" class="pt-l">{{ s.title }}</span>
      </button>
    </div>
    <div class="pt-axis"><span>{{ run.start.slice(11, 16) }}</span><span class="muted">{{ run.minutes }} min, {{ run.counts.llm_inferences }} LLM inferences, {{ run.counts.tool_calls }} tool calls, {{ fmtK(run.tokens) }} tokens, {{ run.model }}</span><span>{{ run.end.slice(11, 16) }}</span></div>

    <div v-if="!compact" class="pt-detail">
      <div class="pt-head">
        <div class="pt-title"><span class="pt-big">{{ step.n }}</span> {{ step.title }}</div>
        <div class="pt-stats">
          <span><b>{{ fmtT(step.seconds) }}</b></span>
          <span><b>{{ step.counts.llm ?? 0 }}</b> LLM</span>
          <span><b>{{ step.counts.tool ?? 0 }}</b> tool calls</span>
          <span><b>{{ fmtK(step.tokens) }}</b> tokens</span>
        </div>
        <div class="pt-io">
          <template v-if="step.inputs.length"><span class="k-edge">ssbd:hasInput</span>
            <span v-for="f in step.inputs" :key="`i${f}`" class="k-file">{{ f }}</span></template>
          <template v-if="step.outputs.length"><span class="k-edge">ssbd:hasOutput</span>
            <span v-for="f in step.outputs" :key="`o${f}`" class="k-file">{{ f }}</span></template>
        </div>
      </div>
      <div class="pt-cols">
        <div>
          <div class="pt-lbl"><span class="k-cls">lcont:LLMAgent</span> LLM inferences per agent</div>
          <div v-for="(n, a) in step.agents" :key="a" class="pt-bar">
            <span class="pt-name">{{ short(String(a)) }}</span>
            <span class="pt-fill ag" :style="{ width: `${60 * (n as number) / maxA}%` }" /><span class="pt-v">{{ n }}</span>
          </div>
        </div>
        <div>
          <div class="pt-lbl"><span class="k-cls">lcont:ToolCall</span> calls per tool</div>
          <div v-for="(n, t) in step.tools" :key="t" class="pt-bar">
            <span class="pt-name">{{ String(t) }}</span>
            <span class="pt-fill tl" :style="{ width: `${50 * (n as number) / maxT}%` }" /><span class="pt-v">{{ n }}</span>
          </div>
          <div v-if="!Object.keys(step.tools).length" class="muted tiny">none</div>
        </div>
      </div>
    </div>
    <div v-if="!compact" class="k-legend pt-legend">
      <span><i class="pt-sw" /> <span class="k-cls">lcont:WorkflowStep</span> width: duration, shade: number of computations</span>
      <span><span class="k-cls">class</span> ontology class (rdf:type)</span>
      <span><span class="k-file">file.json</span> lca_models object saved by the step</span>
      <span><span class="k-edge">ssbd:hasInput</span> predicate</span>
      <span><i class="pt-fill ag" style="width:1.2rem" /> <i class="pt-fill tl" style="width:1.2rem" /> counts recorded in the graph</span>
    </div>
  </div>
</template>

<style>
.pt-strip { display: flex; gap: 2px; height: 2.1rem; }
.pt-seg { position: relative; border: 0; cursor: pointer; background: rgba(53, 53, 53, var(--a)); color: var(--ie-cream);
  display: flex; align-items: center; gap: 0.35rem; padding: 0 0.4rem; overflow: hidden; font-family: var(--font); transition: transform .15s; }
.pt-seg:hover { transform: translateY(-2px); }
.pt-seg.on { background: var(--ie-orange); color: #fff; }
.pt-n { font-weight: 900; font-size: 1rem; }
.pt-l { font-size: 0.6rem; font-weight: 700; white-space: nowrap; }
.pt-axis { display: flex; justify-content: space-between; font-size: 0.56rem; margin-top: 0.15rem; color: var(--ie-dark); }
.pt-detail { background: #fff; box-shadow: var(--shadow); margin-top: 0.45rem; padding: 0.45rem 0.7rem; border-left: 4px solid var(--ie-orange); }
.pt-head { display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; }
.pt-title { font-weight: 800; font-size: 0.85rem; }
.pt-big { color: var(--ie-orange); font-weight: 900; font-size: 1.1rem; }
.pt-stats { display: flex; gap: 0.7rem; font-size: 0.64rem; }
.pt-io { margin-left: auto; font-size: 0.58rem; display: flex; gap: 0.35rem; align-items: center; flex-wrap: wrap; }
.pt-legend { margin-top: 0.5rem; }
.pt-sw { display: inline-block; width: 1.6rem; height: 0.7rem; background: linear-gradient(90deg, rgba(53,53,53,.25), rgba(53,53,53,1)); }
.pt-cols { display: grid; grid-template-columns: 1fr 1.2fr; gap: 1.2rem; margin-top: 0.3rem; }
.pt-lbl { font-size: 0.56rem; font-weight: 600; color: var(--ie-muted); font-style: italic; margin-bottom: 0.15rem; }
.pt-lbl .k-cls { font-style: normal; }
.pt-bar { display: flex; align-items: center; gap: 0.3rem; font-size: 0.58rem; line-height: 1.25; }
.pt-name { width: 45%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-family: ui-monospace, Menlo, monospace; }
.pt-fill { height: 0.5rem; display: inline-block; }
.pt-fill.ag { background: var(--ie-orange); }
.pt-fill.tl { background: var(--ie-dark); }
.pt-v { font-weight: 700; }
</style>
