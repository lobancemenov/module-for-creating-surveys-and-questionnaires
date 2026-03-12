import { ref, computed, onMounted } from 'vue'
import { useSurveyStore } from '@/stores/surveyStore'
import { surveyApi } from '@/services/api'

/**
 * Composable для работы с опросами
 * @param {Object} options - Опции (autoFetch, initialFilters)
 * @returns {Object} - Методы и состояния для работы с опросами
 */
export function useSurveys(options = {}) {
    const {
        autoFetch = true,
        initialFilters = {}
    } = options

    const store = useSurveyStore()

    // Локальное состояние
    const localLoading = ref(false)
    const localError = ref(null)
    const filters = ref({
        title: initialFilters.title || '',
        is_active: initialFilters.is_active ?? null,
        skip: initialFilters.skip || 0,
        limit: initialFilters.limit || 10
    })

    // Вычисляемые свойства из store
    const surveys = computed(() => store.surveys)
    const currentSurvey = computed(() => store.currentSurvey)
    const totalSurveys = computed(() => store.totalSurveys)
    const activeSurveys = computed(() => store.activeSurveys)
    const inactiveSurveys = computed(() => store.inactiveSurveys)
    const isLoading = computed(() => store.loading || localLoading.value)
    const error = computed(() => store.error || localError.value)

    // ===== МЕТОДЫ =====

    // Загрузка всех опросов
    async function loadSurveys() {
        try {
            await store.fetchSurveys()
        } catch (err) {
            localError.value = err.message
        }
    }

    // Загрузка одного опроса по ID
    async function loadSurveyById(id) {
        try {
            return await store.fetchSurveyById(id)
        } catch (err) {
            localError.value = err.message
            throw err
        }
    }

    // Создание нового опроса
    async function createSurvey(surveyData) {
        try {
            const result = await store.createSurvey(surveyData)
            return result
        } catch (err) {
            localError.value = err.response?.data?.detail || 'Ошибка создания'
            throw err
        }
    }

    // Обновление опроса
    async function updateSurvey(id, surveyData) {
        try {
            const result = await store.updateSurvey(id, surveyData)
            return result
        } catch (err) {
            localError.value = err.response?.data?.detail || 'Ошибка обновления'
            throw err
        }
    }

    // Удаление опроса
    async function deleteSurvey(id) {
        try {
            await store.deleteSurvey(id)
            return true
        } catch (err) {
            localError.value = err.response?.data?.detail || 'Ошибка удаления'
            throw err
        }
    }

    // Переключение статуса
    async function toggleStatus(id, isActive) {
        try {
            const result = await store.toggleSurveyStatus(id, isActive)
            return result
        } catch (err) {
            localError.value = err.response?.data?.detail || 'Ошибка изменения статуса'
            throw err
        }
    }

    // Поиск опросов с фильтрами
    async function searchSurveys(searchParams) {
        localLoading.value = true
        try {
            const result = await store.searchSurveys(searchParams)
            return result
        } catch (err) {
            localError.value = err.response?.data?.detail || 'Ошибка поиска'
            throw err
        } finally {
            localLoading.value = false
        }
    }

    // Применение фильтров
    function applyFilters(newFilters) {
        filters.value = { ...filters.value, ...newFilters }
        return searchSurveys(filters.value)
    }

    // Сброс фильтров
    function resetFilters() {
        filters.value = {
            title: '',
            is_active: null,
            skip: 0,
            limit: 10
        }
        store.resetFilters()
        return loadSurveys()
    }

    // Очистка текущего опроса
    function clearCurrent() {
        store.clearCurrentSurvey()
        localError.value = null
    }

    // Очистка ошибки
    function clearError() {
        store.error = null
        localError.value = null
    }

    // Автозагрузка при монтировании
    if (autoFetch) {
        onMounted(() => {
            loadSurveys()
        })
    }

    // ===== RETURN =====
    return {
        // State
        surveys,
        currentSurvey,
        isLoading,
        error,
        filters,
        // Computed
        totalSurveys,
        activeSurveys,
        inactiveSurveys,
        // Methods
        loadSurveys,
        loadSurveyById,
        createSurvey,
        updateSurvey,
        deleteSurvey,
        toggleStatus,
        searchSurveys,
        applyFilters,
        resetFilters,
        clearCurrent,
        clearError
    }
}

export default useSurveys