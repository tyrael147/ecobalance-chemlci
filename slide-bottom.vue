<script setup lang="ts">
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'

// IE-day style chrome: short dash top-left, page number bottom-left, LIST logo bottom-right
const { $slidev, $page } = useSlideContext()
const layout = computed(() => {
  const route = $slidev.nav.slides[$page.value - 1]
  return route?.meta?.layout ?? route?.meta?.slide?.frontmatter?.layout ?? 'default'
})
const dark = computed(() => ['cover', 'section', 'end'].includes(layout.value))
</script>

<template>
  <div class="ie-chrome" :class="{ dark }">
    <span class="ie-dash" />
    <span v-if="!dark" class="ie-pageno">{{ $page }}</span>
    <img class="ie-logo" :src="dark ? 'brand/list-logo-light.svg' : 'brand/list-logo.svg'" alt="Luxembourg Institute of Science and Technology">
  </div>
</template>
