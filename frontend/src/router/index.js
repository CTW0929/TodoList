import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/tasks',
    name: 'Tasks',
    component: () => import('../views/Tasks.vue')
  },
  {
    path: '/gantt',
    name: 'Gantt',
    component: () => import('../views/Gantt.vue')
  },
  {
    path: '/stats',
    name: 'Stats',
    component: () => import('../views/Stats.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router