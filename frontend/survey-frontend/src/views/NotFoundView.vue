<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center">
    <div class="text-center">
      <h1 class="text-9xl font-bold text-gray-300">404</h1>
      <p class="text-2xl text-gray-600 mb-8">Страница не найдена</p>
      <RouterLink to="/" class="btn btn-primary">
        На главную
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.btn {
  @apply px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors;
}
</style>