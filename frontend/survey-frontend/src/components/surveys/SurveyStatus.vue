<template>
  <span
      class="px-3 py-1 rounded-full text-xs font-medium"
      :class="isActive ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
  >
    {{ isActive ? '✓ Активен' : '✗ Неактивен' }}
  </span>
</template>

<script setup>
defineProps({
  isActive: {
    type: Boolean,
    required: true
  }
})
</script>