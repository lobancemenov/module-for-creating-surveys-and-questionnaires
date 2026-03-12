import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { surveyApi } from '@/services/api'

export const useSurveyStore = defineStore('survey', () => {
    // ===== STATE =====
    const surveys = ref([])
    const currentSurvey = ref(null)
    const loading = ref(false)
    const error = ref(null)
    const searchQuery = ref('')
    const filterActive = ref(null)

    // ===== GETTERS =====
    const activeSurveys = computed(() =>
        surveys.value.filter(s => s.is_active)
    )

    const inactiveSurveys = computed(() =>
        surveys.value.filter(s => !s.is_active)
    )

    const totalSurveys = computed(() => surveys.value.length)

    const filteredSurveys = computed(() => {
        let result = surveys.value

        if (searchQuery.value) {
            result = result.filter(s =>
                s.title.toLowerCase().includes(searchQuery.value.toLowerCase())
            )
        }

        if (filterActive !== null) {
            result = result.filter(s => s.is_active === filterActive.value)
        }

        return result
    })

    // ===== ACTIONS =====

    // Загрузка всех опросов
    async function fetchSurveys() {
        loading.value = true
        error.value = null
        try {
            const response = await surveyApi.getAll()
            surveys.value = response.data
        } catch (err) {
            error.value = err.response?.data?.detail || 'Ошибка загрузки опросов'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Загрузка одного опроса
    async function fetchSurveyById(id) {
        loading.value = true
        error.value = null
        try {
            const response = await surveyApi.getById(id)
            currentSurvey.value = response.data
            return response.data
        } catch (err) {
            error.value = err.response?.data?.detail || 'Опрос не найден'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Создание опроса
    async function createSurvey(surveyData) {
        loading.value = true
        error.value = null
        try {
            const response = await surveyApi.create(surveyData)
            surveys.value.unshift(response.data)
            return response.data
        } catch (err) {
            error.value = err.response?.data?.detail || 'Ошибка создания опроса'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Обновление опроса
    async function updateSurvey(id, surveyData) {
        loading.value = true
        error.value = null
        try {
            const response = await surveyApi.update(id, surveyData)
            const index = surveys.value.findIndex(s => s.id === id)
            if (index !== -1) {
                surveys.value[index] = response.data
            }
            if (currentSurvey.value?.id === id) {
                currentSurvey.value = response.data
            }
            return response.data
        } catch (err) {
            error.value = err.response?.data?.detail || 'Ошибка обновления опроса'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Удаление опроса
    async function deleteSurvey(id) {
        loading.value = true
        error.value = null
        try {
            await surveyApi.delete(id)
            surveys.value = surveys.value.filter(s => s.id !== id)
            if (currentSurvey.value?.id === id) {
                currentSurvey.value = null
            }
        } catch (err) {
            error.value = err.response?.data?.detail || 'Ошибка удаления опроса'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Переключение статуса
    async function toggleSurveyStatus(id, is_active) {
        loading.value = true
        error.value = null
        try {
            const response = await surveyApi.toggleStatus(id, is_active)
            const index = surveys.value.findIndex(s => s.id === id)
            if (index !== -1) {
                surveys.value[index] = response.data
            }
            return response.data
        } catch (err) {
            error.value = err.response?.data?.detail || 'Ошибка изменения статуса'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Поиск опросов
    async function searchSurveys(params) {
        loading.value = true
        error.value = null
        try {
            const response = await surveyApi.search(params)
            surveys.value = response.data
            return response.data
        } catch (err) {
            error.value = err.response?.data?.detail || 'Ошибка поиска'
            throw err
        } finally {
            loading.value = false
        }
    }

    // Очистка текущего опроса
    function clearCurrentSurvey() {
        currentSurvey.value = null
        error.value = null
    }

    // Сброс фильтров
    function resetFilters() {
        searchQuery.value = ''
        filterActive.value = null
    }

    // ===== RETURN =====
    return {
        // State
        surveys,
        currentSurvey,
        loading,
        error,
        searchQuery,
        filterActive,
        // Getters
        activeSurveys,
        inactiveSurveys,
        totalSurveys,
        filteredSurveys,
        // Actions
        fetchSurveys,
        fetchSurveyById,
        createSurvey,
        updateSurvey,
        deleteSurvey,
        toggleSurveyStatus,
        searchSurveys,
        clearCurrentSurvey,
        resetFilters,
    }
})