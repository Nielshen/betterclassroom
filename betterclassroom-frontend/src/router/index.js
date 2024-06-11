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
      component: () => import('../views/DashboardViewTest.vue')
    },
    {
      path: "/student/:courseId/:taskId",
      name: "student/:courseId/:taskId",
      component: () => import('../views/StudentTaskView.vue')
    },
    {
      path: '/students',
      name: 'studenten',
      component: () => import('../views/StudentenView.vue')
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
      path: '/editTask/:courseId/:taskid',
      name: 'editTask',
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
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
