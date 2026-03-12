<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader />

    <main class="max-w-4xl mx-auto px-4 py-8">
      <div class="mb-8">
        <RouterLink to="/surveys" class="text-blue-600 hover:underline">
          ← Назад к списку
        </RouterLink>
      </div>

      <div v-if="store.loading">
        <LoadingSpinner />
      </div>
      <div v-else-if="store.error">
        <ErrorAlert :message="store.error" />
      </div>
      <div v-else-if="survey" class="bg-white rounded-lg shadow overflow-hidden">
        <!-- Header -->
        <div class="bg-gradient-to-r from-blue-600 to-blue-700 px-6 py-8 text-white">
          <div class="flex justify-between items-start">
            <div>
              <h1 class="text-3xl font-bold mb-2">{{ survey.title }}</h1>
              <SurveyStatus :is-active="survey.is_active" />
            </div>
            <div class="flex gap-2">
              <RouterLink
                  :to="{ name: 'SurveyEdit', params: { id: survey.id } }"
                  class="btn btn-white"
              >
                Редактировать
              </RouterLink>
              <button
                  @click="toggleStatus"
                  class="btn btn-white"
                  :disabled="store.loading"
              >
                {{ survey.is_active ? 'Деактивировать' : 'Активировать' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Content -->
        <div class="p-6">
          <div class="mb-6">
            <h2 class="text-lg font-semibold text-gray-700 mb-2">Описание</h2>
            <p class="text-gray-600">
              {{ survey.description || 'Нет описания' }}
            </p>
          </div>

          <div class="mb-6">
            <h2 class="text-lg font-semibold text-gray-700 mb-2">Информация</h2>
            <dl class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <dt class="text-sm text-gray-500">ID опроса</dt>
                <dd class="text-gray-900 font-medium">#{{ survey.id }}</dd>
              </div>
              <div>
                <dt class="text-sm text-gray-500">Статус</dt>
                <dd class="text-gray-900 font-medium">
                  {{ survey.is_active ? 'Активен' : 'Неактивен' }}
                </dd>
              </div>
              <div>
                <dt class="text-sm text-gray-500">Дата создания</dt>
                <dd class="text-gray-900 font-medium">
                  {{ formatDate(survey.created_at) }}
                </dd>
              </div>
            </dl>
          </div>

          <!-- Delete Section -->
          <div class="border-t pt-6">
            <h2 class="text-lg font-semibold text-red-600 mb-2">Опасная зона</h2>
            <p class="text-gray-600 mb-4">
              Удаление опроса необратимо. Все данные будут потеряны.
            </p>
            <button
                @click="confirmDelete"
                class="btn btn-danger"
                :disabled="store.loading"
            >
              Удалить опрос
            </button>
          </div>
        </div>
      </div>
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSurveyStore } from '@/stores/surveyStore'
import AppHeader from '@/components/common/AppHeader.vue'
import AppFooter from '@/components/common/AppFooter.vue'
import SurveyStatus from '@/components/surveys/SurveyStatus.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'

const route = useRoute()
const router = useRouter()
const store = useSurveyStore()
const surveyId = ref(route.params.id)
const survey = ref(null)

onMounted(async () => {
  try {
    survey.value = await store.fetchSurveyById(surveyId.value)
  } catch (error) {
    router.push({ name: 'SurveyList' })
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

async function toggleStatus() {
  try {
    await store.toggleSurveyStatus(surveyId.value, !survey.value.is_active)
    survey.value = await store.fetchSurveyById(surveyId.value)
  } catch (error) {
    // Ошибка уже обработана в store
  }
}

async function confirmDelete() {
  if (confirm('Вы уверены, что хотите удалить этот опрос?')) {
    try {
      await store.deleteSurvey(surveyId.value)
      router.push({ name: 'SurveyList' })
    } catch (error) {
      // Ошибка уже обработана в store
    }
  }
}
</script>

<style scoped>
.btn {
  @apply px-4 py-2 rounded-lg font-medium transition-colors duration-200;
}

.btn-white {
  @apply bg-white text-blue-600 hover:bg-blue-50;
}

.btn-danger {
  @apply bg-red-600 text-white hover:bg-red-700;
}
</style>