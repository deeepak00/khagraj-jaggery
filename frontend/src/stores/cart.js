import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useToastStore } from './toast'

export const useCartStore = defineStore('cart', () => {
  const items = ref(JSON.parse(localStorage.getItem('jgr_cart') || '[]'))

  const count = computed(() => items.value.reduce((s, i) => s + i.qty, 0))
  const total = computed(() => items.value.reduce((s, i) => s + i.price * i.qty, 0))

  function _persist() {
    localStorage.setItem('jgr_cart', JSON.stringify(items.value))
  }

  function add(product) {
    const toast = useToastStore()
    const ex = items.value.find(i => i.id === product.id)
    if (ex) {
      ex.qty++
    } else {
      items.value.push({
        id:        product.id,
        name:      product.name,
        price:     product.price,
        unit:      product.unit,
        image_url: product.image_url,
        qty:       1,
      })
    }
    _persist()
    toast.success(`${product.name} added to cart`)
  }

  function increase(id) {
    const item = items.value.find(i => i.id === id)
    if (item) { item.qty++; _persist() }
  }

  function decrease(id) {
    const item = items.value.find(i => i.id === id)
    if (!item) return
    if (item.qty <= 1) remove(id)
    else { item.qty--; _persist() }
  }

  function remove(id) {
    items.value = items.value.filter(i => i.id !== id)
    _persist()
  }

  function clear() {
    items.value = []
    localStorage.removeItem('jgr_cart')
  }

  function getItem(id) {
    return items.value.find(i => i.id === id)
  }

  return { items, count, total, add, increase, decrease, remove, clear, getItem }
})
