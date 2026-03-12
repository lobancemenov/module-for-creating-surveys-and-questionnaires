export function validateSurveyForm(data) {
    const errors = {
        title: null,
        description: null,
        hasError: false
    }

    // Title validation
    if (!data.title || data.title.trim() === '') {
        errors.title = 'Название опроса обязательно'
        errors.hasError = true
    } else if (data.title.length < 3) {
        errors.title = 'Название должно быть не менее 3 символов'
        errors.hasError = true
    } else if (data.title.length > 200) {
        errors.title = 'Название не должно превышать 200 символов'
        errors.hasError = true
    }

    // Description validation
    if (data.description && data.description.length > 1000) {
        errors.description = 'Описание не должно превышать 1000 символов'
        errors.hasError = true
    }

    return errors
}

export function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return re.test(email)
}

export function debounce(func, wait) {
    let timeout
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout)
            func(...args)
        }
        clearTimeout(timeout)
        timeout = setTimeout(later, wait)
    }
}