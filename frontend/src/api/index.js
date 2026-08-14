import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  timeout: 15000,
})

// Attach JWT token to every request
api.interceptors.request.use(cfg => {
  const token = localStorage.getItem('jgr_token')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

// Global error handling
api.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('jgr_token')
      window.location.href = '/auth'
    }
    return Promise.reject(err)
  }
)

// ── AUTH ──────────────────────────────────────────────
export const authApi = {
  register: d  => api.post('/auth/register', d),
  login:    d  => api.post('/auth/login', d),
  me:       () => api.get('/auth/me'),
  updateProfile: d => api.put('/auth/profile', d),
}

// ── PRODUCTS ──────────────────────────────────────────
export const productsApi = {
  list:       params => api.get('/products', { params }),
  get:        id     => api.get(`/products/${id}`),
  categories: ()     => api.get('/products/categories'),
}

// ── ORDERS ────────────────────────────────────────────
export const ordersApi = {
  place:  d           => api.post('/orders', d),
  mine:   params      => api.get('/orders/my', { params }),
  get:    orderNumber => api.get(`/orders/${orderNumber}`),
}

// ── SETTINGS (public) ─────────────────────────────────
export const settingsApi = {
  public: () => api.get('/settings/public'),
}

// ── CONTACT ──────────────────────────────────────────
export const contactApi = {
  submit: d => api.post('/contact', d),
}

// ── ADMIN ─────────────────────────────────────────────
export const adminApi = {
  // Stats
  stats: () => api.get('/admin/stats'),

  // Products
  listProducts:   params => api.get('/admin/products', { params }),
  addProduct:     d      => api.post('/admin/products', d),
  updateProduct:  (id,d) => api.put(`/admin/products/${id}`, d),
  deleteProduct:  id     => api.delete(`/admin/products/${id}`),
  uploadImage:    form   => api.post('/admin/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  uploadLogo:     form   => api.post('/admin/settings/logo', form, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),

  // Orders
  listOrders:         params  => api.get('/admin/orders', { params }),
  updateOrderStatus:  (id, d) => api.put(`/admin/orders/${id}/status`, d),

  // Users
  listUsers:    params  => api.get('/admin/users', { params }),
  updateUser:   (id, d) => api.put(`/admin/users/${id}`, d),

  // Settings
  getSettings:    ()  => api.get('/admin/settings'),
  updateSettings: d   => api.put('/admin/settings', d),

  // Messages
  listMessages:   ()  => api.get('/admin/messages'),
  markMessageRead: id => api.put(`/admin/messages/${id}/read`),
  deleteMessage:   id => api.delete(`/admin/messages/${id}`),
}

export default api
