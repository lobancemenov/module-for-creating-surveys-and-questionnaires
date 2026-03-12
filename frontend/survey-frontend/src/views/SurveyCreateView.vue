<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader />

    <main class="max-w-2xl mx-auto px-4 py-8">
      <div class="mb-8">
        <RouterLink to="/surveys" class="text-blue-600 hover:underline">
          ← Назад к опросам
        </RouterLink>
        <h1 class="text-3xl font-bold text-gray-900 mt-4">Создать новый опрос</h1>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <SurveyForm
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
import { useRouter } from 'vue-router'
import { useSurveyStore } from '@/stores/surveyStore'
import AppHeader from '@/components/common/AppHeader.vue'
import AppFooter from '@/components/common/AppFooter.vue'
import SurveyForm from '@/components/surveys/SurveyForm.vue'

const router = useRouter()
const store = useSurveyStore()

async function handleSubmit(formData) {
  try {
    await store.createSurvey(formData)
    router.push({ name: 'SurveyList' })
  } catch (error) {
    // Ошибка уже обработана в store
  }
}

function handleCancel() {
  router.push({ name: 'SurveyList' })
}
</script>