<script setup lang="ts">
/**
 * Tabbed, collapsible JSON explorer for the artefacts of a ChemLCI run.
 *
 *   <JsonExplorer :tabs="[{ label: 'retro', cls: 'RetrosynthesisRoute', data: retro }, ...]" height="330px" />
 *
 * `cls` is the lca_models class the file validates against (shown as a badge).
 */
import { computed, ref } from 'vue'
import JsonNode from './JsonNode.vue'

const props = withDefaults(defineProps<{
  tabs: { label: string, cls?: string, step?: string, data: unknown, open?: number }[]
  height?: string
  initial?: number
}>(), { height: '320px', initial: 0 })

const active = ref(props.initial)
const tab = computed(() => props.tabs[active.value])
const size = computed(() => `${(JSON.stringify(tab.value.data).length / 1024).toFixed(1)} kB`)
</script>

<template>
  <div class="jx">
    <div class="jx-tabs">
      <button v-for="(t, i) in tabs" :key="t.label" :class="{ on: i === active }" @click="active = i">
        <span v-if="t.step" class="jx-step">{{ t.step }}</span>{{ t.label }}
      </button>
    </div>
    <div class="jx-meta">
      <span v-if="tab.cls" class="jx-cls">lca_models.{{ tab.cls }}</span>
      <span class="muted">{{ size }}, click to expand</span>
      <span class="jx-legend"><span class="jx-hl">iri, source, uncertainty_type</span> on every object</span>
    </div>
    <div class="jx-body" :style="{ height }">
      <JsonNode :key="active" :value="tab.data" :open="tab.open ?? 2" />
    </div>
  </div>
</template>

<style>
.jx { background: #fff; box-shadow: var(--shadow); }
.jx-tabs { display: flex; gap: 0; background: var(--ie-bg-dark); }
.jx-tabs button { font: 600 0.66rem var(--font); color: var(--ie-cream); padding: 0.3rem 0.65rem; border: 0; background: transparent; cursor: pointer; }
.jx-tabs button.on { background: var(--ie-orange); color: #fff; }
.jx-step { display: inline-block; font-weight: 900; margin-right: 0.3rem; opacity: 0.85; }
.jx-meta { display: flex; gap: 0.7rem; align-items: center; padding: 0.25rem 0.6rem; font-size: 0.58rem; border-bottom: 1px solid var(--ie-rule); }
.jx-cls { font-family: ui-monospace, Menlo, monospace; font-weight: 700; color: #104862; }
.jx-legend { margin-left: auto; color: var(--ie-muted); }
.jx-hl { background: var(--ie-orange); color: #fff; padding: 0 3px; font-family: ui-monospace, Menlo, monospace; }
.jx-body { overflow: auto; padding: 0.35rem 0.6rem; }
</style>
