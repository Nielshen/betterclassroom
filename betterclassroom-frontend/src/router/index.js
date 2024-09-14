import { createRouter, createWebHistory } from 'vue-router'
import { useDataStore } from '../stores/dataStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: "/register", // Professor
      name: "register",
      component: () => import('../views/ProfessorRegisterView.vue')
    },
    {
      path: "/login", // Professor
      name: "login",
      component: () => import('../views/ProfessorLoginView.vue')
    },
    {
      path: "/changePassword", // Professor
      name: "changePassword",
      component: () => import('../views/ProfessorChangePasswordView.vue')
    },
    {
      path: '/dashboard/:courseId/:taskId', // Professor
      name: 'dashboard/:courseId/:taskId',
      component: () => import('../views/DashboardView.vue')
    },
    {
      path: '/student/:courseId/:taskId', // Student
      name: 'student/:courseId/:taskId',
      component: () => import('../views/StudentTaskView.vue')
    },
    {
      path: '/createTask/:courseId', // Professor
      name: 'createTask/:courseId',
      component: () => import('../views/CreateTaskView.vue')
    },
    {
      path: '/createTask/:courseId/:taskId', // Professor
      name: 'createTask/:id:/:taskId',
      component: () => import('../views/CreateTaskView.vue')
    },
    {
      path: '/createCourse/:courseId', // Professor
      name: 'createCourse/:courseId',
      component: () => import('../views/CreateCourseView.vue')
    },
    {
      path: '/createCourse/', // Professor
      name: 'createCourse/',
      component: () => import('../views/CreateCourseView.vue')
    },
    {
      path: '/editTask/:courseId/:taskId', // Professor
      name: 'editTask:/courseId/:taskId',
      component: () => import('../views/CreateTaskView.vue')
    },
    {
      path: '/tasks', // Professor
      name: 'tasks',
      component: () => import('../views/TaskView.vue')
    },
    {
      path: '/courses', // Professor
      name: 'courses',
      component: () => import('../views/CourseView.vue')
    },
    { 
      path: '/DashboardStudentView/:courseId/:taskId',
        name: 'DashboardStudentView/:courseId/:taskId',
        component: () => import('../views/DashboardStudentView.vue')
      }
    ]    
  })

router.beforeEach((to, from, next) => {
  const professorRoutes = [
    '/dashboard/:courseId/:taskId',
    '/createTask/:courseId',
    '/createTask/:courseId/:taskId',
    '/createCourse/:courseId',
    '/createCourse/',
    '/editTask/:courseId/:taskId',
    '/tasks',
    '/courses'
  ]
  const authRequired = professorRoutes.some(route => to.path.startsWith(route))
  const store = useDataStore()
  const loggedIn = store.isProfessor

  if (authRequired && !loggedIn) {
    return next('/login')
  }

  next()
})

export default router
