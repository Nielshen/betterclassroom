import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/courses'
    },
    {
      path: '/dashboard/:courseId/:taskId',
      name: 'dashboard/:courseId/:taskId',
      component: () => import('../views/DashboardView.vue')
    },
    {
      path: '/student/:courseId/:taskId',
      name: 'student/:courseId/:taskId',
      component: () => import('../views/StudentTaskView.vue')
    },
    {
      path: '/createTask/:courseId',
      name: 'createTask/:courseId',
      component: () => import('../views/CreateTaskView.vue')
    },
    {
      path: '/createTask/:courseId/:taskId',
      name: 'createTask/:id:/:taskId',
      component: () => import('../views/CreateTaskView.vue')
    },
    {
      path: '/createCourse/:courseId',
      name: 'createCourse/:courseId',
      component: () => import('../views/CreateCourseView.vue')
    },
    {
      path: '/createCourse/',
      name: 'createCourse/',
      component: () => import('../views/CreateCourseView.vue')
    },
    {
      path: '/editTask/:courseId/:taskId',
      name: 'editTask:/courseId/:taskId',
      component: () => import('../views/CreateTaskView.vue')
    },
    {
      path: '/tasks',
      name: 'tasks',
      component: () => import('../views/TaskView.vue')
    },
    {
      path: '/courses',
      name: 'courses',
      component: () => import('../views/CourseView.vue')
    }
  ]
})

export default router
