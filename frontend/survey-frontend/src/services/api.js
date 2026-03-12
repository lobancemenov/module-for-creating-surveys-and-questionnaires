import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 10000,
})

// Interceptors
api.interceptors.request.use(
    (config) => {
        console.log('Request:', config.method.toUpperCase(), config.url)
        return config
    },
    (error) => {
        console.error('Request Error:', error)
        return Promise.reject(error)
    }
)

api.interceptors.response.use(
    (response) => {
        console.log('Response:', response.status, response.config.url)
        return response
    },
    (error) => {
        console.error('Response Error:', error.response?.status, error.response?.data)

        if (error.response?.status === 405) {
            console.error('Method Not Allowed - проверьте CORS настройки!')
        }

        return Promise.reject(error)
    }
)

export const surveyApi = {
    getAll: () => api.get('/surveys'),
    getById: (id) => api.get(`/surveys/${id}`),
    search: (params) => api.get('/surveys/search', { params }),
    create: (data) => api.post('/surveys', data),
    update: (id, data) => api.put(`/surveys/${id}`, data),
    delete: (id) => api.delete(`/surveys/${id}`),
    toggleStatus: (id, is_active) => api.put(`/surveys/${id}`, { is_active }),
}

export default api