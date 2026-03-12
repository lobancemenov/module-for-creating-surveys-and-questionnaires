<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader />

    <main class="max-w-7xl mx-auto px-4 py-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Все опросы</h1>
        <RouterLink
            to="/surveys/create"
            class="btn btn-primary"
        >
          + Создать опрос
        </RouterLink>
      </div>

      <!-- Filters -->
      <div class="bg-white rounded-lg shadow p-4 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Поиск по названию
            </label>
            <input
                v-model="store.searchQuery"
                type="text"
                class="input-field"
                placeholder="Введите название..."
                @input="handleSearch"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Статус
            </label>
            <select
                v-model="filterActive"
                class="input-field"
                @change="handleFilter"
            >
              <option value="">Все</option>
              <option value="true">Активные</option>
              <option value="false">Неактивные</option>
            </select>
          </div>
          <div class="flex items-end">
            <button
                @click="resetFilters"
                class="btn btn-secondary w-full"
            >
              Сбросить фильтры
            </button>
          </div>
        </div>
      </div>

      <!-- Loading / Error / Content -->
      <div v-if="store.loading">
        <LoadingSpinner />
      </div>
      <div v-else-if="store.error">
        <ErrorAlert :message="store.error" />
      </div>
      <div v-else-if="filteredSurveys.length === 0" class="text-center py-12 bg-white rounded-lg shadow">
        <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
        <p class="text-gray-500 text-lg">Опросы не найдены</p>
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <SurveyCard
            v-for="survey in filteredSurveys"
            :key="survey.id"
            :survey="survey"
        />
      </div>
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useSurveyStore } from '@/stores/surveyStore'
import AppHeader from '@/components/common/AppHeader.vue'
import AppFooter from '@/components/common/AppFooter.vue'
import SurveyCard from '@/components/surveys/SurveyCard.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'

const store = useSurveyStore()
const filterActive = ref('')

const filteredSurveys = computed(() => {
  let result = store.surveys

  if (store.searchQuery) {
    result = result.filter(s =>
        s.title.toLowerCase().includes(store.searchQuery.toLowerCase())
    )
  }

  if (filterActive.value !== '') {
    result = result.filter(s => s.is_active === (filterActive.value === 'true'))
  }

  return result
})

function handleSearch() {
  // Можно добавить debouncing для оптимизации
}

function handleFilter() {
  // Фильтрация применяется через computed
}

function resetFilters() {
  store.searchQuery = ''
  filterActive.value = ''
}

onMounted(() => {
  store.fetchSurveys()
})
</script>

<style scoped>
.input-field {
  @apply w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none;
}

.btn {
  @apply px-6 py-2 rounded-lg font-medium transition-colors duration-200;
}

.btn-primary {
  @apply bg-blue-600 text-white hover:bg-blue-700;
}

.btn-secondary {
  @apply bg-gray-200 text-gray-800 hover:bg-gray-300;
}
</style>