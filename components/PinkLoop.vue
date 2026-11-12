<script setup lang="ts">
/**
 * PINK in one picture (static): candidate chemicals / materials are screened
 * in silico by services for functionality, cost, safety and sustainability, and the
 * PINKISH platform balances them (multi-objective) into SSbD-ranked candidates.
 */
withDefaults(defineProps<{ active?: boolean }>(), { active: true })

const services = [
  { y: 22, label: 'functionality', sub: 'property prediction' },
  { y: 60, label: 'cost', sub: 'techno-economics' },
  { y: 98, label: 'safety', sub: 'hazard, exposure' },
  { y: 136, label: 'sustainability', sub: 'in-silico LCA (ChemLCI)', hi: true },
]
const IN = (y: number) => `M58 92 C 95 92, 95 ${y + 15}, 132 ${y + 15}`
const OUT = (y: number) => `M262 ${y + 15} C 300 ${y + 15}, 300 92, 334 92`
</script>

<template>
  <div class="pinkloop">
    <svg v-if="active" viewBox="0 0 470 178" width="100%">
      <!-- candidates -->
      <g>
        <g v-for="(dy, i) in [-24, 0, 24]" :key="i" :transform="`translate(30 ${92 + dy})`">
          <path d="M0 -8 L7 -4 L7 4 L0 8 L-7 4 L-7 -4 Z" fill="#fff" stroke="#353535" stroke-width="1.4" />
          <circle r="3.2" fill="none" stroke="#353535" stroke-width="0.9" />
        </g>
        <text x="30" y="140" text-anchor="middle" class="pk-lbl" fill="#353535">candidates</text>
        <text x="30" y="151" text-anchor="middle" class="pk-sub" fill="#66645d">SMILES</text>
      </g>
      <!-- connectors -->
      <g>
        <path v-for="s in services" :key="`i${s.y}`" :d="IN(s.y)" fill="none" stroke="#bdb7a0" stroke-width="1.2" />
        <path v-for="s in services" :key="`o${s.y}`" :d="OUT(s.y)" fill="none" stroke="#bdb7a0" stroke-width="1.2" />
      </g>
      <!-- services -->
      <g v-for="(s, i) in services" :key="s.label">
        <rect x="134" :y="s.y + 2" width="128" height="30" fill="#000" opacity=".13" />
        <rect x="132" :y="s.y" width="128" height="30" :fill="s.hi ? '#f46524' : '#fff'" />
        <text x="140" :y="s.y + 13" class="pk-lbl" :fill="s.hi ? '#fff' : '#353535'">{{ s.label }}</text>
        <text x="140" :y="s.y + 24" class="pk-sub" :fill="s.hi ? '#fde3d3' : '#66645d'">{{ s.sub }}</text>
      </g>
      <!-- PINKISH -->
      <g>
        <rect x="338" y="62" width="122" height="64" fill="#000" opacity=".16" />
        <rect x="336" y="60" width="122" height="64" fill="#353535" />
        <text x="346" y="80" class="pk-lbl" fill="#fcf6d7" style="font-size:12px">PINKISH</text>
        <text x="346" y="94" class="pk-sub" fill="#f8bd90">decision support</text>
        <text x="346" y="105" class="pk-sub" fill="#f8bd90">generative AI</text>
        <text x="346" y="116" class="pk-sub" fill="#f8bd90">dashboard</text>
        <text x="397" y="146" text-anchor="middle" class="pk-lbl" fill="#f46524">SSbD-ranked candidates</text>
        <text x="397" y="158" text-anchor="middle" class="pk-sub" fill="#66645d">balance: multi-objective</text>
      </g>
    </svg>
  </div>
</template>

<style>
.pinkloop svg { display: block; overflow: visible; }
.pinkloop .pk-lbl { font: 700 10.5px var(--font); }
.pinkloop .pk-sub { font: italic 500 8.6px var(--font); }
</style>
