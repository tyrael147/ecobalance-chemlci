<script setup lang="ts">
/**
 * Inline an SVG from ./figures and drive it with slide clicks.
 *
 *   <SvgFigure src="fig2-lca-vs-abm"
 *              :show="{ 'b-label': 2, 'b-space': 2 }"     // group id -> click at which it appears
 *              :hide="{ 'a-old': 3 }"                   // group id -> click at which it disappears
 *              :focus="{ 1: ['a-consumer'], 2: [] }"     // click -> ids kept bright (others dimmed)
 *              :dim="{ 'bar-plant': 1 }" />               // group id (any depth) -> click from which it is dimmed
 *
 * Group ids are the `<g id="...">` layers inside the SVG (they survive an
 * Illustrator round-trip as layer / group names). `focus` uses the last key
 * <= current click; an empty list clears the highlight. Only top-level groups
 * (direct children of <svg>) are dimmed.
 */
import { computed, onMounted, ref, watch } from 'vue'
import { useSlideContext } from '@slidev/client'

const props = withDefaults(defineProps<{
  src: string
  show?: Record<string, number>
  /** group id -> click at which it disappears (swap two layers with show + hide) */
  hide?: Record<string, number>
  focus?: Record<number, string[]>
  /** group id (any depth) -> click from which it is dimmed */
  dim?: Record<string, number>
  /** fixed focus, independent of clicks (e.g. small "navigator" figures) */
  highlight?: string[]
  width?: string
}>(), { show: () => ({}), hide: () => ({}), focus: () => ({}), dim: () => ({}), width: '100%' })

const files = import.meta.glob('../figures/*.svg', { query: '?raw', import: 'default', eager: true }) as Record<string, string>
const raw = computed(() => {
  const s = files[`../figures/${props.src}.svg`]
  if (!s)
    return `<p style="color:#e50051">missing figure: ${props.src}</p>`
  // drop XML prolog and let CSS size the figure
  return s
    .replace(/<\?xml[^>]*>/, '')
    .replace(/<svg([^>]*)>/, (_m, attrs: string) => `<svg${attrs.replace(/\s(width|height)="[^"]*"/g, '')}>`)
})

const { $clicks } = useSlideContext()
const root = ref<HTMLElement>()

function update() {
  const el = root.value
  if (!el)
    return
  const clicks = $clicks.value
  for (const [id, at] of Object.entries(props.show)) {
    const node = el.querySelector<SVGElement>(`[id="${id}"]`)
    node?.classList.toggle('svgfig-hidden', clicks < at || (id in props.hide && clicks >= props.hide[id]))
  }
  for (const [id, at] of Object.entries(props.hide)) {
    if (id in props.show)
      continue
    el.querySelector<SVGElement>(`[id="${id}"]`)?.classList.toggle('svgfig-hidden', clicks >= at)
  }
  for (const [id, at] of Object.entries(props.dim))
    el.querySelector<SVGElement>(`[id="${id}"]`)?.classList.toggle('svgfig-dim', clicks >= at)
  let active: string[] | undefined = props.highlight
  if (!active) {
    const keys = Object.keys(props.focus).map(Number).filter(k => k <= clicks).sort((a, b) => a - b)
    if (keys.length)
      active = props.focus[keys[keys.length - 1]]
  }
  const svg = el.querySelector('svg')
  if (!svg)
    return
  for (const g of Array.from(svg.children)) {
    if (g.tagName.toLowerCase() !== 'g' || !g.id)
      continue
    g.classList.toggle('svgfig-dim', !!active && active.length > 0 && !active.includes(g.id))
  }
}

onMounted(update)
watch([$clicks, () => props.src, () => props.highlight], () => requestAnimationFrame(update))
</script>

<template>
  <div ref="root" class="svgfig" :style="{ width }" v-html="raw" />
</template>

<style>
.svgfig svg {
  width: 100%;
  height: auto;
  display: block;
  overflow: visible;
}
.svgfig svg g[id] {
  transition: opacity 0.45s ease;
}
.svgfig .svgfig-dim {
  opacity: 0.16;
}
.svgfig .svgfig-hidden {
  opacity: 0 !important;
  pointer-events: none;
}
</style>
