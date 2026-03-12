import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('@/views/HomeView.vue'),
        meta: { title: 'Главная' }
    },
    {
        path: '/surveys',
        name: 'SurveyList',
        component: () => import('@/views/SurveyListView.vue'),
        meta: { title: 'Все опросы' }
    },
    {
        path: '/surveys/create',
        name: 'SurveyCreate',
        component: () => import('@/views/SurveyCreateView.vue'),
        meta: { title: 'Создать опрос' }
    },
    {
        path: '/surveys/:id',
        name: 'SurveyDetail',
        component: () => import('@/views/SurveyDetailView.vue'),
        meta: { title: 'Просмотр опроса' },
        props: true
    },
    {
        path: '/surveys/:id/edit',
        name: 'SurveyEdit',
        component: () => import('@/views/SurveyEditView.vue'),
        meta: { title: 'Редактировать опрос' },
        props: true
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: () => import('@/views/NotFoundView.vue'),
        meta: { title: 'Страница не найдена' }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        } else {
            return { top: 0 }
        }
    }
})

// Guard - изменение заголовка страницы
router.beforeEach((to, from, next) => {
    const appName = import.meta.env.VITE_APP_NAME || 'Survey Manager'
    document.title = to.meta.title
        ? `${to.meta.title} | ${appName}`
        : appName
    next()
})

export default router