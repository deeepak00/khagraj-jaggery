import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api'
import { useToastStore } from './toast'
import { useCartStore } from './cart'

export const useAuthStore = defineStore('auth', () => {
  const user  = ref(null)
  const token = ref(localStorage.getItem('jgr_token') || null)
  const isRestored = ref(false)

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin    = computed(() => user.value?.role === 'admin')

  async function restoreSession() {
    if (isRestored.value) return
    if (!token.value) {
      isRestored.value = true
      return
    }
    try {
      const { data } = await authApi.me()
      user.value = data
    } catch {
      logout()
    } finally {
      isRestored.value = true
    }
  }


  async function login(email, password) {
    const toast = useToastStore()
    const { data } = await authApi.login({ email, password })
    _setSession(data)
    toast.success(`Welcome back, ${data.user.name}!`)
    return data.user
  }

  async function register(payload) {
    const toast = useToastStore()
    const { data } = await authApi.register(payload)
    _setSession(data)
    toast.success(`Welcome, ${data.user.name}!`)
    return data.user
  }

  function logout() {
    token.value = null
    user.value  = null
    localStorage.removeItem('jgr_token')
    
    // Clear cart on logout for confidentiality
    try {
      const cart = useCartStore()
      cart.clear()
    } catch (e) {
      console.warn("Failed to clear cart:", e)
    }
  }

  async function updateProfile(payload) {
    const toast = useToastStore()
    const { data } = await authApi.updateProfile(payload)
    user.value = data
    toast.success('Profile updated!')
    return data
  }

  function _setSession(data) {
    token.value = data.token
    user.value  = data.user
    localStorage.setItem('jgr_token', data.token)
  }

  return { user, token, isLoggedIn, isAdmin, isRestored, restoreSession, login, register, logout, updateProfile }
})

