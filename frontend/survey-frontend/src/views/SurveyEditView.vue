<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader />

    <main class="max-w-2xl mx-auto px-4 py-8">
      <div class="mb-8">
        <RouterLink
            :to="{ name: 'SurveyDetail', params: { id: surveyId } }"
            class="text-blue-600 hover:underline"
        >
          ← Назад к опросу
        </RouterLink>
        <h1 class="text-3xl font-bold text-gray-900 mt-4">Редактировать опрос</h1>
      </div>

      <div v-if="store.loading && !surveyData">
        <LoadingSpinner />
      </div>
      <div v-else-if="store.error && !surveyData">
        <ErrorAlert :message="store.error" />
      </div>
      <div v-else class="bg-white rounded-lg shadow p-6">
        <SurveyForm
            :initial-data="surveyData"
            :loading="store.loading"
            :submit-error="store.error"
            @submit="handleSubmit"
            @cancel="handleCancel"
        />
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
import SurveyForm from '@/components/surveys/SurveyForm.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'

const route = useRoute()
const router = useRouter()
const store = useSurveyStore()
const surveyId = ref(route.params.id)
const surveyData = ref(null)

onMounted(async () => {
  try {
    surveyData.value = await store.fetchSurveyById(surveyId.value)
  } catch (error) {
    router.push({ name: 'SurveyList' })
  }
})

async function handleSubmit(formData) {
  try {
    await store.updateSurvey(surveyId.value, formData)
    router.push({ name: 'SurveyDetail', params: { id: surveyId.value } })
  } catch (error) {
    // Ошибка уже обработана в store
  }
}

function handleCancel() {
  router.push({ name: 'SurveyDetail', params: { id: surveyId.value } })
}
</script>