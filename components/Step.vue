<script setup lang="ts">
/**
 * Visible while  from <= $clicks < to.  Use inside `.stack` to swap captions in place,
 * or with only `from` as a cumulative reveal. Pair with `clicks: N` in the slide frontmatter.
 */
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'

const props = withDefaults(defineProps<{ from?: number, to?: number }>(), { from: 0, to: Number.POSITIVE_INFINITY })
const { $clicks } = useSlideContext()
const visible = computed(() => $clicks.value >= props.from && $clicks.value < props.to)
</script>

<template>
  <div class="step" :class="{ 'step-hidden': !visible }">
    <slot />
  </div>
</template>

<style>
.step { transition: opacity 0.4s ease, transform 0.4s ease; }
.step-hidden { opacity: 0; transform: translateY(6px); pointer-events: none; }
</style>
