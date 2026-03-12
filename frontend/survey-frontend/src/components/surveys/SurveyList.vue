<template>
  <div class="survey-list-container">
    <!-- Заголовок списка -->
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-900">
        {{ title }}
      </h2>
      <span class="text-sm text-gray-500">
        Найдено: {{ surveys.length }} из {{ total }}
      </span>
    </div>

    <!-- Фильтры -->
    <div v-if="showFilters" class="bg-gray-50 rounded-lg p-4 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- Поиск по названию -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            🔍 Поиск
          </label>
          <input
              v-model="localSearchQuery"
              type="text"
              class="input-field"
              placeholder="Название опроса..."
              @input="debouncedSearch"
          />
        </div>

        <!-- Фильтр по статусу -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            📊 Статус
          </label>
          <select
              v-model="localStatusFilter"
              class="input-field"
              @change="applyFilters"
          >
            <option value="">Все статусы</option>
            <option value="true">✅ Активные</option>
            <option value="false">❌ Неактивные</option>
          </select>
        </div>

        <!-- Кнопки действий -->
        <div class="flex items-end gap-2">
          <button
              @click="resetFilters"
              class="btn btn-secondary flex-1"
          >
            🔄 Сброс
          </button>
          <button
              @click="$emit('refresh')"
              class="btn btn-primary flex-1"
              :disabled="isLoading"
          >
            🔄 Обновить
          </button>
        </div>
      </div>
    </div>

    <!-- Состояния загрузки / ошибки / пустого списка -->
    <div v-if="isLoading && surveys.length === 0" class="text-center py-12">
      <LoadingSpinner />
      <p class="text-gray-500 mt-4">Загрузка опросов...</p>
    </div>

    <div v-else-if="error" class="text-center py-12">
      <ErrorAlert :message="error" />
      <button
          @click="$emit('refresh')"
          class="btn btn-primary mt-4"
      >
        Попробовать снова
      </button>
    </div>

    <div v-else-if="filteredSurveys.length === 0" class="text-center py-12 bg-white rounded-lg shadow">
      <svg class="w-16 h-16 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
      </svg>
      <p class="text-gray-500 text-lg mb-2">Опросы не найдены</p>
      <p class="text-gray-400 text-sm">Попробуйте изменить параметры поиска</p>
    </div>

    <!-- Сетка опросов -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <SurveyCard
          v-for="survey in filteredSurveys"
          :key="survey.id"
          :survey="survey"
          @toggle-status="handleToggleStatus"
          @delete="handleDelete"
      />
    </div>

    <!-- Пагинация (если нужно) -->
    <div v-if="showPagination && totalPages > 1" class="mt-8 flex justify-center items-center gap-2">
      <button
          @click="changePage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="btn btn-secondary px-4 py-2"
      >
        ← Назад
      </button>

      <span class="px-4 py-2 text-gray-600">
        Страница {{ currentPage }} из {{ totalPages }}
      </span>

      <button
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="btn btn-secondary px-4 py-2"
      >
        Вперёд →
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { debounce } from '@/utils/validators'
import SurveyCard from './SurveyCard.vue'
import LoadingSpinner from '../common/LoadingSpinner.vue'
import ErrorAlert from '../common/ErrorAlert.vue'

// ===== PROPS =====
const props = defineProps({
  surveys: {
    type: Array,
    required: true,
    default: () => []
  },
  total: {
    type: Number,
    default: 0
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  },
  title: {
    type: String,
    default: 'Все опросы'
  },
  showFilters: {
    type: Boolean,
    default: true
  },
  showPagination: {
    type: Boolean,
    default: false
  },
  itemsPerPage: {
    type: Number,
    default: 9
  }
})

// ===== EMITS =====
const emit = defineEmits(['refresh', 'search', 'filter', 'delete', 'toggle-status', 'page-change'])

// ===== LOCAL STATE =====
const localSearchQuery = ref('')
const localStatusFilter = ref('')
const currentPage = ref(1)

// ===== COMPUTED =====
const filteredSurveys = computed(() => {
  let result = props.surveys

  // Фильтр по поиску
  if (localSearchQuery.value) {
    result = result.filter(s =>
        s.title.toLowerCase().includes(localSearchQuery.value.toLowerCase())
    )
  }

  // Фильтр по статусу
  if (localStatusFilter.value !== '') {
    const isActive = localStatusFilter.value === 'true'
    result = result.filter(s => s.is_active === isActive)
  }

  return result
})

const totalPages = computed(() => {
  return Math.ceil(filteredSurveys.value.length / props.itemsPerPage)
})

const paginatedSurveys = computed(() => {
  if (!props.showPagination) return filteredSurveys.value

  const start = (currentPage.value - 1) * props.itemsPerPage
  const end = start + props.itemsPerPage
  return filteredSurveys.value.slice(start, end)
})

// ===== METHODS =====

// Debounced поиск
const debouncedSearch = debounce(() => {
  currentPage.value = 1
  emit('search', localSearchQuery.value)
  applyFilters()
}, 300)

// Применение фильтров
function applyFilters() {
  currentPage.value = 1
  emit('filter', {
    title: localSearchQuery.value,
    is_active: localStatusFilter.value === '' ? null : localStatusFilter.value === 'true'
  })
}

// Сброс фильтров
function resetFilters() {
  localSearchQuery.value = ''
  localStatusFilter.value = ''
  currentPage.value = 1
  emit('refresh')
}

// Изменение страницы
function changePage(page) {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  emit('page-change', page)
}

// Обработка переключения статуса
function handleToggleStatus(survey) {
  emit('toggle-status', survey)
}

// Обработка удаления
function handleDelete(survey) {
  emit('delete', survey)
}

// Watch для сброса пагинации при изменении данных
watch(() => props.surveys, () => {
  currentPage.value = 1
}, { deep: true })
</script>

<style scoped>
.input-field {
  @apply w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors;
}

.btn {
  @apply px-4 py-2 rounded-lg font-medium transition-colors duration-200;
}

.btn-primary {
  @apply bg-blue-600 text-white hover:bg-blue-700 disabled:bg-blue-400;
}

.btn-secondary {
  @apply bg-gray-200 text-gray-800 hover:bg-gray-300 disabled:bg-gray-100;
}
</style>