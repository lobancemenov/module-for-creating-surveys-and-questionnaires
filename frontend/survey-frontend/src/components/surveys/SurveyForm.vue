<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <!-- Title -->
    <div>
      <label for="title" class="block text-sm font-medium text-gray-700 mb-2">
        Название опроса <span class="text-red-500">*</span>
      </label>
      <input
          id="title"
          v-model="formData.title"
          type="text"
          :disabled="loading"
          class="input-field"
          :class="{ 'border-red-500': errors.title }"
          placeholder="Введите название опроса"
      />
      <p v-if="errors.title" class="mt-1 text-sm text-red-600">
        {{ errors.title }}
      </p>
    </div>

    <!-- Description -->
    <div>
      <label for="description" class="block text-sm font-medium text-gray-700 mb-2">
        Описание
      </label>
      <textarea
          id="description"
          v-model="formData.description"
          :disabled="loading"
          rows="4"
          class="input-field"
          :class="{ 'border-red-500': errors.description }"
          placeholder="Опишите цель опроса..."
      />
      <p v-if="errors.description" class="mt-1 text-sm text-red-600">
        {{ errors.description }}
      </p>
    </div>

    <!-- Is Active -->
    <div class="flex items-center">
      <input
          id="is_active"
          v-model="formData.is_active"
          type="checkbox"
          :disabled="loading"
          class="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
      />
      <label for="is_active" class="ml-2 text-sm text-gray-700">
        Опрос активен
      </label>
    </div>

    <!-- Submit Button -->
    <div class="flex gap-4">
      <button
          type="submit"
          :disabled="loading"
          class="btn btn-primary flex-1"
      >
        <span v-if="loading">Сохранение...</span>
        <span v-else>{{ isEdit ? 'Обновить' : 'Создать' }}</span>
      </button>

      <button
          type="button"
          @click="$emit('cancel')"
          :disabled="loading"
          class="btn btn-secondary flex-1"
      >
        Отмена
      </button>
    </div>

    <!-- Error Alert -->
    <div v-if="submitError" class="alert alert-error">
      {{ submitError }}
    </div>
  </form>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { validateSurveyForm } from '@/utils/validators'

const props = defineProps({
  initialData: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  },
  submitError: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['submit', 'cancel'])

const isEdit = ref(!!props.initialData)

const formData = reactive({
  title: props.initialData?.title || '',
  description: props.initialData?.description || '',
  is_active: props.initialData?.is_active ?? true
})

const errors = reactive({
  title: null,
  description: null
})

// Watch for initialData changes
watch(() => props.initialData, (newData) => {
  if (newData) {
    formData.title = newData.title
    formData.description = newData.description || ''
    formData.is_active = newData.is_active ?? true
    isEdit.value = true
  }
}, { immediate: true })

function handleSubmit() {
  // Валидация
  const validationErrors = validateSurveyForm(formData)
  errors.title = validationErrors.title
  errors.description = validationErrors.description

  if (validationErrors.hasError) return

  emit('submit', { ...formData })
}
</script>

<style scoped>
.input-field {
  @apply w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors;
}

.input-field:disabled {
  @apply bg-gray-100 cursor-not-allowed;
}

.btn {
  @apply px-6 py-2 rounded-lg font-medium transition-colors duration-200;
}

.btn-primary {
  @apply bg-blue-600 text-white hover:bg-blue-700 disabled:bg-blue-400;
}

.btn-secondary {
  @apply bg-gray-200 text-gray-800 hover:bg-gray-300 disabled:bg-gray-100;
}

.alert-error {
  @apply mt-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg;
}
</style>