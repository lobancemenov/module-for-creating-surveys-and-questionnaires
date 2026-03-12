<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader />

    <main class="max-w-7xl mx-auto px-4 py-12">
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          Добро пожаловать в {{ appName }}
        </h1>
        <p class="text-xl text-gray-600 mb-8">
          Управление опросами и анкетами в одном месте
        </p>
        <div class="flex justify-center gap-4">
          <RouterLink
              to="/surveys"
              class="btn btn-primary px-8 py-3"
          >
            Смотреть опросы
          </RouterLink>
          <RouterLink
              to="/surveys/create"
              class="btn btn-secondary px-8 py-3"
          >
            Создать опрос
          </RouterLink>
        </div>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <div class="stat-card">
          <div class="stat-value">{{ store.totalSurveys }}</div>
          <div class="stat-label">Всего опросов</div>
        </div>
        <div class="stat-card">
          <div class="stat-value text-green-600">{{ store.activeSurveys.length }}</div>
          <div class="stat-label">Активных</div>
        </div>
        <div class="stat-card">
          <div class="stat-value text-red-600">{{ store.inactiveSurveys.length }}</div>
          <div class="stat-label">Неактивных</div>
        </div>
      </div>

      <!-- Recent Surveys -->
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-2xl font-semibold mb-4">Последние опросы</h2>
        <div v-if="store.loading">
          <LoadingSpinner />
        </div>
        <div v-else-if="store.surveys.length === 0" class="text-center py-8">
          <p class="text-gray-500">Опросов пока нет</p>
          <RouterLink to="/surveys/create" class="text-blue-600 hover:underline">
            Создать первый опрос →
          </RouterLink>
        </div>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <SurveyCard
              v-for="survey in store.surveys.slice(0, 6)"
              :key="survey.id"
              :survey="survey"
          />
        </div>
      </div>
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useSurveyStore } from '@/stores/surveyStore'
import AppHeader from '@/components/common/AppHeader.vue'
import AppFooter from '@/components/common/AppFooter.vue'
import SurveyCard from '@/components/surveys/SurveyCard.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

const store = useSurveyStore()
const appName = import.meta.env.VITE_APP_NAME || 'Survey Manager'

onMounted(() => {
  store.fetchSurveys()
})
</script>

<style scoped>
.stat-card {
  @apply bg-white rounded-lg shadow p-6 text-center;
}

.stat-value {
  @apply text-4xl font-bold text-gray-900;
}

.stat-label {
  @apply text-gray-600 mt-2;
}

.btn {
  @apply rounded-lg font-medium transition-colors duration-200;
}

.btn-primary {
  @apply bg-blue-600 text-white hover:bg-blue-700;
}

.btn-secondary {
  @apply bg-gray-200 text-gray-800 hover:bg-gray-300;
}
</style>