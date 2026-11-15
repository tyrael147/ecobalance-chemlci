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
 * Keys starting with "." are class selectors (e.g. ".task", ".calimero"): in show / hide / dim they
 * select every element with that class; in focus they keep bright the top-level groups with that class.
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

// ids referenced inside the SVG (gradients, clip paths, markers, patterns) get a per-instance prefix,
// so the same figure on two slides (or two figures with the same Illustrator ids) cannot collide
const uid = `svgf${Math.random().toString(36).slice(2, 8)}`
function scopeIds(s: string) {
  const refs = new Set<string>()
  for (const m of s.matchAll(/url\(\s*['"]?#([^)'"\s]+)['"]?\s*\)|href="#([^"]+)"/g))
    refs.add(m[1] ?? m[2])
  if (!refs.size)
    return s
  const esc = (x: string) => x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const alt = [...refs].map(esc).join('|')
  return s
    .replace(new RegExp(`id="(${alt})"`, 'g'), (_m, id) => `id="${uid}-${id}"`)
    .replace(new RegExp(`url\\(\\s*['"]?#(${alt})['"]?\\s*\\)`, 'g'), (_m, id) => `url(#${uid}-${id})`)
    .replace(new RegExp(`href="#(${alt})"`, 'g'), (_m, id) => `href="#${uid}-${id}"`)
}

// class names defined in the figure's own <style> (Illustrator "cls-1", ...) are global in HTML:
// prefix them too, so two inlined figures cannot restyle each other
function scopeClasses(s: string) {
  const names = new Set<string>()
  for (const st of s.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)) {
    for (const m of st[1].matchAll(/\.([A-Za-z_][\w-]*)(?=[^{}]*\{)/g))
      names.add(m[1])
  }
  if (!names.size)
    return s
  const pre = (n: string) => names.has(n) ? `${uid}-${n}` : n
  return s
    .replace(/(<style[^>]*>)([\s\S]*?)(<\/style>)/g, (_m, a, css: string, b) =>
      a + css.replace(/\.([A-Za-z_][\w-]*)(?=[^{}]*\{)/g, (_x, n) => `.${pre(n)}`) + b)
    .replace(/\sclass="([^"]*)"/g, (_m, cls: string) => ` class="${cls.split(/\s+/).map(pre).join(' ')}"`)
}

const raw = computed(() => {
  const s = files[`../figures/${props.src}.svg`]
  if (!s)
    return `<p style="color:#e50051">missing figure: ${props.src}</p>`
  // drop XML prolog and let CSS size the figure
  return scopeClasses(scopeIds(s))
    .replace(/<\?xml[^>]*>/, '')
    .replace(/<svg([^>]*)>/, (_m, attrs: string) => `<svg${attrs.replace(/\s(width|height)="[^"]*"/g, '')}>`)
})

const { $clicks } = useSlideContext()
const root = ref<HTMLElement>()

function nodes(el: HTMLElement, key: string) {
  return Array.from(el.querySelectorAll<SVGElement>(key.startsWith('.') ? key : `[id="${key}"]`))
}

function update() {
  const el = root.value
  if (!el)
    return
  const clicks = $clicks.value
  for (const [id, at] of Object.entries(props.show)) {
    for (const node of nodes(el, id))
      node.classList.toggle('svgfig-hidden', clicks < at || (id in props.hide && clicks >= props.hide[id]))
  }
  for (const [id, at] of Object.entries(props.hide)) {
    if (id in props.show)
      continue
    for (const node of nodes(el, id))
      node.classList.toggle('svgfig-hidden', clicks >= at)
  }
  for (const [id, at] of Object.entries(props.dim)) {
    for (const node of nodes(el, id))
      node.classList.toggle('svgfig-dim', clicks >= at)
  }
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
    const kept = !!active && active.some(k => k.startsWith('.') ? g.classList.contains(k.slice(1)) : k === g.id)
    g.classList.toggle('svgfig-dim', !!active && active.length > 0 && !kept)
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
