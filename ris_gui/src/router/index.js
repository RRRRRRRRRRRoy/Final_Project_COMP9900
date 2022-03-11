import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Index',
    component: () => import('../views/Index.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/newLogin.vue')
  },
  {
    path: '/register',
    name: 'newRegister',
    component: () => import('../views/newRegister.vue')
  },
  // {
  //   path: '/user',
  //   name: 'Profile',
  //   component: () => import('../views/Profile.vue')
  // },
  {
    path: '/register1',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/forgot',
    name: 'Forgot',
    component: () => import('../views/Forgot.vue')
  },
  {
    path: '/:catchAll(.*)',
    name: '404',
    component: () => import('../views/404.vue')
  },
  {
    path: '/myproperties',
    name: 'MyProperties',
    component: () => import('../views/MyProperties.vue')
  },
  {
    path: '/houseinfo',
    name: 'HouseInfo',
    component: () => import('../views/HouseInfo.vue')
  },
  {
    path: '/plan',
    name: 'Plan',
    component: () => import('../views/ItineraryPlan.vue')
  },
  {
    path: '/reportOverview',
    name: 'ReportOverview',
    component: () => import('../views/InspectionReport.vue')
  },
  {
    path: '/newProperties',
    name: 'NewProperties',
    component: () => import('../views/NewProperties.vue')
  },
  {
    path: '/addInspectionReport',
    name: 'AddInspectionReport',
    component: () => import('../views/AddInspectionReport.vue')
  },
  {
    path: '/propertyDetail',
    name: 'propertyDetail',
    component: () => import('../views/propertyDetail.vue')
  },
  {
    path: '/reportDetail',
    name: 'reportDetail',
    component: () => import('../views/ReportDetailPage.vue')
  },
  {
    path: '/reportAndPlan',
    name: 'ReportAndPlan',
    component: () => import('../views/ReportWithPlan.vue')
  },
  {
    path: '/reportModify',
    name: 'ReportModify',
    component: () => import('../views/ReportModifyPage.vue')
  },
  // {
  //   path: '/about',
  //   name: 'About',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  // }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to) => {
  let token = localStorage.getItem('Token')
  let role = localStorage.getItem('role')
  if (token && (to.path === '/login' || to.path === '/register' || to.path === '/forgot')) {
    return '/'
  }
  else if (!token
    // && to.path !== '/'
    && to.path !== '/register'
    && to.path !== '/forgot'
    && to.path !== '/login'
  ) {
    return '/login'
  } else if (role === 'tenant' && to.path !== '/') { return '/' }
})

export default router
