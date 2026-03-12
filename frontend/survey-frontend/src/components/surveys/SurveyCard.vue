<template>
  <div
      class="survey-card bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-300"
      :class="{ 'opacity-60': !survey.is_active }"
  >
    <div class="flex justify-between items-start mb-4">
      <h3 class="text-xl font-semibold text-gray-800 line-clamp-1">
        {{ survey.title }}
      </h3>
      <SurveyStatus :is-active="survey.is_active" />
    </div>

    <p class="text-gray-600 mb-4 line-clamp-2">
      {{ survey.description || 'Нет описания' }}
    </p>

    <div class="flex items-center text-sm text-gray-500 mb-4">
      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
      </svg>
      {{ formatDate(survey.created_at) }}
    </div>

    <div class="flex gap-2">
      <RouterLink
          :to="{ name: 'SurveyDetail', params: { id: survey.id } }"
          class="btn btn-primary flex-1"
      >
        Просмотр
      </RouterLink>
      <RouterLink
          :to="{ name: 'SurveyEdit', params: { id: survey.id } }"
          class="btn btn-secondary flex-1"
      >
        Редактировать
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import SurveyStatus from './SurveyStatus.vue'

defineProps({
  survey: {
    type: Object,
    required: true
  }
})

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>