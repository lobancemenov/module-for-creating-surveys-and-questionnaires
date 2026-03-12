<template>
  <footer class="bg-white border-t border-gray-200 mt-auto">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">

        <!-- Компания / Проект -->
        <div>
          <div class="flex items-center space-x-2 mb-4">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
            </svg>
            <span class="text-lg font-bold text-gray-800">{{ appName }}</span>
          </div>
          <p class="text-gray-600 text-sm">
            Модуль для создания и управления опросами и анкетами.
            Быстро, удобно, надёжно.
          </p>
        </div>

        <!-- Навигация -->
        <div>
          <h3 class="text-sm font-semibold text-gray-700 uppercase tracking-wider mb-4">
            Навигация
          </h3>
          <ul class="space-y-2">
            <li>
              <RouterLink to="/" class="text-gray-600 hover:text-blue-600 text-sm transition-colors">
                Главная
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/surveys" class="text-gray-600 hover:text-blue-600 text-sm transition-colors">
                Все опросы
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/surveys/create" class="text-gray-600 hover:text-blue-600 text-sm transition-colors">
                Создать опрос
              </RouterLink>
            </li>
          </ul>
        </div>

        <!-- Контакты / Инфо -->
        <div>
          <h3 class="text-sm font-semibold text-gray-700 uppercase tracking-wider mb-4">
            Информация
          </h3>
          <ul class="space-y-2 text-sm text-gray-600">
            <li class="flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              Версия: {{ appVersion }}
            </li>
            <li class="flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/>
              </svg>
              <a :href="apiDocsUrl" target="_blank" class="hover:text-blue-600 transition-colors">
                API Документация
              </a>
            </li>
            <li class="flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/>
              </svg>
              Backend: FastAPI
            </li>
            <li class="flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4"/>
              </svg>
              Frontend: Vue.js 3
            </li>
          </ul>
        </div>
      </div>

      <!-- Нижняя линия -->
      <div class="border-t border-gray-200 mt-8 pt-8">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <p class="text-sm text-gray-500">
            © {{ currentYear }} {{ appName }}. Все права защищены.
          </p>
          <div class="flex space-x-6 mt-4 md:mt-0">
            <a href="#" class="text-gray-400 hover:text-gray-600 text-sm transition-colors">
              Политика конфиденциальности
            </a>
            <a href="#" class="text-gray-400 hover:text-gray-600 text-sm transition-colors">
              Условия использования
            </a>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'

const appName = import.meta.env.VITE_APP_NAME || 'Survey Manager'
const appVersion = import.meta.env.VITE_APP_VERSION || '1.0.0'
const apiDocsUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const currentYear = new Date().getFullYear()
</script>

<style scoped>
footer {
  position: sticky;
  top: 100vh;
}
</style>