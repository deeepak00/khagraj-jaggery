import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  // Public
  { path: '/',          name: 'home',     component: () => import('@/pages/HomePage.vue') },
  { path: '/shop',      name: 'shop',     component: () => import('@/pages/ShopPage.vue') },
  { path: '/auth',      name: 'auth',     component: () => import('@/pages/AuthPage.vue') },
  { path: '/checkout',  name: 'checkout', component: () => import('@/pages/CheckoutPage.vue') },
  { path: '/success/:orderNumber', name: 'success', component: () => import('@/pages/OrderSuccessPage.vue') },

  // Authenticated users
  {
    path: '/my-orders',
    name: 'my-orders',
    component: () => import('@/pages/MyOrdersPage.vue'),
    meta: { requiresAuth: true },
  },

  // Admin
  {
    path: '/admin',
    component: () => import('@/pages/admin/AdminLayout.vue'),
    meta: { requiresAdmin: true },
    children: [
      { path: '',          redirect: '/admin/dashboard' },
      { path: 'dashboard', name: 'admin-dashboard', component: () => import('@/pages/admin/DashboardPage.vue') },
      { path: 'products',  name: 'admin-products',  component: () => import('@/pages/admin/ProductsPage.vue') },
      { path: 'orders',    name: 'admin-orders',    component: () => import('@/pages/admin/OrdersPage.vue') },
      { path: 'users',     name: 'admin-users',     component: () => import('@/pages/admin/UsersPage.vue') },
      { path: 'settings',  name: 'admin-settings',  component: () => import('@/pages/admin/SettingsPage.vue') },
      { path: 'messages',  name: 'admin-messages',  component: () => import('@/pages/admin/MessagesPage.vue') },
    ],
  },

  // Catch-all
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: (to, from, saved) => saved || { top: 0 },
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()

  // Ensure session is restored before evaluating auth/admin guards
  await auth.restoreSession()

  if (to.meta.requiresAdmin && !auth.isAdmin) {
    return auth.isLoggedIn ? '/' : '/auth'
  }
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return `/auth?redirect=${to.fullPath}`
  }
})


export default router
