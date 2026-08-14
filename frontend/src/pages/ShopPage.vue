<template>
  <div style="padding-top:88px;min-height:100vh;background:var(--cream2)">
    <div class="container" style="padding-top:48px;padding-bottom:80px">
      <!-- Header -->
      <div class="text-center mb-lg" style="padding-bottom:16px">
        <div class="section-tag">Our Range</div>
        <h1 class="section-title">Premium Jaggery Collection</h1>
        <p class="section-subtitle">From classic sugarcane blocks to rare palm varieties — free of chemicals.</p>
      </div>

      <!-- Search + Filters -->
      <div style="display:flex;gap:14px;align-items:center;margin-bottom:28px;flex-wrap:wrap">
        <div style="flex:1;min-width:220px;position:relative">
          <input class="form-control" v-model="search" placeholder="🔍  Search products..." @input="onSearch" style="padding-left:14px"/>
        </div>
        <select class="form-control" v-model="sortBy" @change="load()" style="width:180px">
          <option value="">Sort: Default</option>
          <option value="price_asc">Price: Low → High</option>
          <option value="price_desc">Price: High → Low</option>
          <option value="popular">Most Popular</option>
        </select>
      </div>

      <!-- Category tabs -->
      <div class="filter-tabs">
        <button v-for="tab in categories" :key="tab.value"
          class="filter-tab" :class="{active: activeCategory === tab.value}"
          @click="activeCategory = tab.value; load()">
          {{ tab.label }}
        </button>
      </div>

      <!-- Grid -->
      <div v-if="loading" class="loader"><div class="spinner"></div></div>
      <div v-else-if="!products.length" style="text-align:center;padding:80px 20px;color:var(--text-lt)">
        <div style="font-size:4rem;margin-bottom:16px">🔍</div>
        <p style="font-family:'Lora',serif">No products found. Try a different search.</p>
      </div>
      <div v-else style="display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:24px">
        <ProductCard v-for="p in displayProducts" :key="p.id" :product="p" />
      </div>

      <!-- Load more -->
      <div v-if="hasMore" class="text-center mt-lg">
        <button class="btn btn-outline btn-lg" :disabled="loadingMore" @click="loadMore">
          {{ loadingMore ? 'Loading...' : 'Load More' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { productsApi } from '@/api'
import ProductCard from '@/components/ProductCard.vue'

const route = useRoute()

const products       = ref([])
const loading        = ref(true)
const loadingMore    = ref(false)
const search         = ref('')
const activeCategory = ref('')
const sortBy         = ref('')
const page           = ref(1)
const totalPages     = ref(1)
let   searchTimer    = null

const hasMore = computed(() => page.value < totalPages.value)

const categories = [
  { label:'All',       value:''         },
  { label:'Sugarcane', value:'sugarcane'},
  { label:'Palm',      value:'palm'     },
  { label:'Flavored',  value:'flavored' },
  { label:'Featured',  value:'__featured'},
]

const displayProducts = computed(() => {
  let list = [...products.value]
  if (sortBy.value === 'price_asc')  list.sort((a,b) => a.price - b.price)
  if (sortBy.value === 'price_desc') list.sort((a,b) => b.price - a.price)
  if (sortBy.value === 'popular')    list.sort((a,b) => b.order_count - a.order_count)
  return list
})

async function load(reset = true) {
  if (reset) { page.value = 1; products.value = [] }
  loading.value = true
  try {
    const params = { page: page.value }
    if (search.value)         params.q        = search.value
    if (activeCategory.value && activeCategory.value !== '__featured') params.category = activeCategory.value
    if (activeCategory.value === '__featured') params.featured = true
    const { data } = await productsApi.list(params)
    products.value  = reset ? data.products : [...products.value, ...data.products]
    totalPages.value = data.pages
  } catch { /* silent */ } finally { loading.value = false }
}

async function loadMore() {
  page.value++
  loadingMore.value = true
  await load(false)
  loadingMore.value = false
}

function onSearch() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => load(), 400)
}

watch(() => route.query, (q) => {
  activeCategory.value = q.category || ''
  if (q.featured) activeCategory.value = '__featured'
  search.value = q.q || ''
  load()
}, { deep: true, immediate: true })
</script>
