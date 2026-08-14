import { defineStore } from 'pinia'
import { ref } from 'vue'

let _id = 0

export const useToastStore = defineStore('toast', () => {
  const toasts = ref([])

  function push(message, type = 'info', duration = 3000) {
    const id = ++_id
    toasts.value.push({ id, message, type })
    setTimeout(() => remove(id), duration)
    return id
  }

  function remove(id) {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }

  const success = (msg, duration) => push(msg, 'success', duration)
  const error   = (msg, duration) => push(msg, 'error', duration)
  const info    = (msg, duration) => push(msg, 'info', duration)

  return { toasts, push, remove, success, error, info }
})
