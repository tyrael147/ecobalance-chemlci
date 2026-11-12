<script setup lang="ts">
/**
 * One node of a collapsible JSON tree (used by JsonExplorer.vue).
 * Keys of the lca_models DataModel base class (iri, source, uncertainty_type)
 * are highlighted so the audience can see that every object carries them.
 */
import { computed, ref } from 'vue'

defineOptions({ name: 'JsonNode' })

const props = withDefaults(defineProps<{
  value: unknown
  name?: string | number
  depth?: number
  open?: number          // auto-expand nodes up to this depth
  highlight?: string[]
}>(), { depth: 0, open: 1, highlight: () => ['iri', 'source', 'uncertainty_type', 'ssbd_class'] })

const isObj = computed(() => props.value !== null && typeof props.value === 'object')
const isArr = computed(() => Array.isArray(props.value))
const entries = computed(() => isObj.value ? Object.entries(props.value as object) : [])
const expanded = ref(props.depth < props.open)

const preview = computed(() => {
  if (isArr.value)
    return `[${(props.value as unknown[]).length}]`
  const o = props.value as Record<string, unknown>
  const label = o.name ?? o.target_name ?? o.category_key ?? o.node_id ?? o.reaction_SMILES
  const n = Object.keys(o).length
  return label ? `{${n}} ${String(label).slice(0, 48)}` : `{${n}}`
})

const scalar = computed(() => {
  const v = props.value
  if (typeof v === 'string')
    return { cls: 'str', txt: `"${v.length > 90 ? `${v.slice(0, 88)}…` : v}"`, full: v }
  if (typeof v === 'number')
    return { cls: 'num', txt: Number.isInteger(v) ? String(v) : String(+v.toPrecision(5)), full: String(v) }
  if (typeof v === 'boolean')
    return { cls: 'bool', txt: String(v), full: String(v) }
  return { cls: 'null', txt: 'null', full: 'null' }
})
const hl = computed(() => typeof props.name === 'string' && props.highlight.includes(props.name))
</script>

<template>
  <div class="jn">
    <div class="jn-row" :class="{ clickable: isObj }" @click.stop="isObj && (expanded = !expanded)">
      <span v-if="isObj" class="jn-caret">{{ expanded ? '▾' : '▸' }}</span>
      <span v-else class="jn-caret" />
      <span v-if="name !== undefined" class="jn-key" :class="{ hl }">{{ name }}</span>
      <span v-if="name !== undefined" class="jn-colon">: </span>
      <span v-if="isObj" class="jn-preview">{{ preview }}</span>
      <span v-else :class="`jn-${scalar.cls}`" :title="scalar.full">{{ scalar.txt }}</span>
    </div>
    <div v-if="isObj && expanded" class="jn-children">
      <JsonNode v-for="[k, v] in entries" :key="k" :name="isArr ? Number(k) : k" :value="v"
                :depth="depth + 1" :open="open" :highlight="highlight" />
    </div>
  </div>
</template>

<style>
.jn { font-family: ui-monospace, 'JetBrains Mono', Menlo, monospace; font-size: 0.62rem; line-height: 1.45; }
.jn-row { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.jn-row.clickable { cursor: pointer; }
.jn-row.clickable:hover { background: #fdeee4; }
.jn-caret { display: inline-block; width: 0.9em; color: var(--ie-orange); }
.jn-children { padding-left: 0.95em; border-left: 1px dotted var(--ie-rule); margin-left: 0.3em; }
.jn-key { color: #104862; font-weight: 600; }
.jn-key.hl { color: #fff; background: var(--ie-orange); padding: 0 3px; }
.jn-colon { color: var(--ie-muted); }
.jn-preview { color: var(--ie-muted); font-style: italic; }
.jn-str { color: #3b7d23; }
.jn-num { color: #c55a11; font-weight: 600; }
.jn-bool, .jn-null { color: #7a4ea3; }
</style>
