<template>
  <header class="bg-white shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <RouterLink to="/" class="flex items-center space-x-2">
          <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
          </svg>
          <span class="text-xl font-bold text-gray-800">{{ appName }}</span>
        </RouterLink>

        <nav class="flex space-x-4">
          <RouterLink
              to="/surveys"
              class="nav-link"
              active-class="nav-link-active"
          >
            Опросы
          </RouterLink>
          <RouterLink
              to="/surveys/create"
              class="nav-link"
              active-class="nav-link-active"
          >
            Создать
          </RouterLink>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup>
const appName = import.meta.env.VITE_APP_NAME || 'Survey Manager'
</script>

<style scoped>
.nav-link {
  @apply px-3 py-2 text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors;
}

.nav-link-active {
  @apply text-blue-600 border-b-2 border-blue-600;
}
</style>