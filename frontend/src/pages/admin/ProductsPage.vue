<template>
  <div>
    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:28px;flex-wrap:wrap;gap:12px">
      <div>
        <h2 style="font-size:1.9rem;color:var(--brown);margin-bottom:4px">Products 🟫</h2>
        <p style="font-size:.9rem;color:var(--text-lt)">Add, edit and manage your jaggery product catalogue.</p>
      </div>
      <button class="btn btn-primary" @click="openAdd">+ Add Product</button>
    </div>

    <!-- Search -->
    <div style="margin-bottom:20px;display:flex;gap:12px;flex-wrap:wrap">
      <input class="form-control" v-model="search" placeholder="Search products..." style="max-width:300px" @input="debouncedLoad"/>
      <select class="form-control" v-model="filterStatus" @change="load()" style="width:160px">
        <option value="">All Status</option>
        <option value="active">Active</option>
        <option value="inactive">Inactive</option>
      </select>
    </div>

    <div class="card" style="overflow:hidden">
      <div v-if="loading" class="loader"><div class="spinner"></div></div>
      <div class="table-wrap" v-else>
        <table class="data-table">
          <thead>
            <tr><th style="width:60px">Image</th><th>Name</th><th>Category</th><th>Price</th><th>Stock</th><th>Status</th><th>Featured</th><th>Actions</th></tr>
          </thead>
          <tbody>
            <tr v-for="p in filtered" :key="p.id">
              <td>
                <div style="width:48px;height:48px;border-radius:8px;overflow:hidden;background:var(--cream2)">
                  <img v-if="p.image_url" :src="p.image_url" :alt="p.name" style="width:100%;height:100%;object-fit:cover"/>
                  <div v-else style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:1.4rem">🍯</div>
                </div>
              </td>
              <td>
                <div style="font-weight:600;color:var(--brown)">{{ p.name }}</div>
                <span v-if="p.badge" style="font-size:.68rem;background:var(--amber);color:var(--white);padding:2px 8px;border-radius:50px">{{ p.badge }}</span>
              </td>
              <td style="text-transform:capitalize;font-size:.85rem">{{ p.category }}</td>
              <td><strong>₹{{ p.price }}</strong><span style="font-size:.75rem;color:var(--text-lt)"> /{{ p.unit }}</span></td>
              <td>
                <span :style="`font-size:.82rem;font-weight:600;color:${p.stock>20?'var(--green)':'var(--red)'}`">{{ p.stock }} units</span>
              </td>
              <td><span class="badge" :class="p.active?'badge-active':'badge-inactive'">{{ p.active ? 'Active' : 'Inactive' }}</span></td>
              <td>
                <span v-if="p.featured" style="color:var(--gold);font-size:1.1rem">⭐</span>
                <span v-else style="color:var(--text-lt);font-size:.8rem">—</span>
              </td>
              <td>
                <div style="display:flex;gap:6px">
                  <button class="btn btn-primary btn-sm" @click="openEdit(p)">Edit</button>
                  <button class="btn btn-ghost btn-sm" @click="toggleActive(p)">{{ p.active ? 'Hide' : 'Show' }}</button>
                  <button class="btn btn-danger btn-sm" @click="confirmDelete(p)">Del</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Product Modal -->
    <teleport to="body">
      <div v-if="modal.show" class="modal-overlay" @click.self="modal.show=false">
        <div class="modal" style="max-width:620px">
          <h3 class="modal-title">{{ modal.mode==='add' ? 'Add New Product' : 'Edit Product' }}</h3>
          <p class="modal-sub">{{ modal.mode==='add' ? 'Fill in the details to add a new product.' : 'Update the product details.' }}</p>

          <div class="form-group">
            <label class="form-label">Product Name <span style="color:var(--amber)">*</span></label>
            <input class="form-control" v-model="modal.data.name" placeholder="e.g. Pure Sugarcane Jaggery Block"/>
          </div>
          <div class="form-group">
            <label class="form-label">Description</label>
            <textarea class="form-control" v-model="modal.data.description" placeholder="Describe the product..."></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Price (₹) <span style="color:var(--amber)">*</span></label>
              <input class="form-control" type="number" v-model="modal.data.price" placeholder="0" min="0"/>
            </div>
            <div class="form-group">
              <label class="form-label">Unit</label>
              <select class="form-control" v-model="modal.data.unit">
                <option value="kg">kg</option><option value="500g">500g</option>
                <option value="250g">250g</option><option value="500ml">500ml</option>
                <option value="litre">litre</option><option value="piece">piece</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Category</label>
              <select class="form-control" v-model="modal.data.category">
                <option value="sugarcane">Sugarcane</option>
                <option value="palm">Palm</option>
                <option value="flavored">Flavored</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Badge</label>
              <select class="form-control" v-model="modal.data.badge">
                <option value="">None</option><option value="Bestseller">Bestseller</option>
                <option value="Organic">Organic</option><option value="Premium">Premium</option>
                <option value="Rare">Rare</option><option value="New">New</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Stock (units)</label>
              <input class="form-control" type="number" v-model="modal.data.stock" min="0"/>
            </div>
            <div class="form-group">
              <label class="form-label">Visibility</label>
              <select class="form-control" v-model="modal.data.active">
                <option :value="true">Active — visible to customers</option>
                <option :value="false">Inactive — hidden</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label" style="display:flex;align-items:center;gap:8px;cursor:pointer">
              <input type="checkbox" v-model="modal.data.featured" style="width:18px;height:18px;accent-color:var(--amber)"/>
              ⭐ Mark as Featured (shown on homepage)
            </label>
          </div>

          <!-- Multi-Image upload -->
          <div class="form-group">
            <label class="form-label">Product Images (Up to 5 images)</label>
            <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-top:8px">
              <!-- Uploaded images -->
              <div v-for="(url, idx) in modal.data.image_urls" :key="url" 
                   style="position:relative;width:80px;height:80px;border-radius:10px;overflow:hidden;border:2px solid rgba(45,106,79,0.15)">
                <img :src="url" style="width:100%;height:100%;object-fit:cover"/>
                <!-- Delete overlay -->
                <button type="button" @click="removeImage(idx)"
                        style="position:absolute;top:4px;right:4px;width:18px;height:18px;border-radius:50%;background:rgba(192,57,43,0.95);color:white;border:none;display:flex;align-items:center;justify-content:center;font-size:0.7rem;cursor:pointer;line-height:1">
                  ×
                </button>
              </div>
              
              <!-- Add button -->
              <div v-if="!modal.data.image_urls || modal.data.image_urls.length < 5" 
                   style="width:80px;height:80px;border-radius:10px;border:2px dashed rgba(45,106,79,0.3);display:flex;align-items:center;justify-content:center;background:var(--cream2);cursor:pointer;position:relative"
                   @click="$refs.fileInput.click()">
                <span style="font-size:1.6rem;color:var(--amber)">+</span>
                <input type="file" accept="image/*" ref="fileInput" style="display:none" @change="uploadImage"/>
              </div>
            </div>
            <div style="font-size:.78rem;color:var(--text-lt);margin-top:6px">PNG, JPG, WEBP — first image acts as primary showcase.</div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-ghost btn-sm" @click="modal.show=false">Cancel</button>
            <button class="btn btn-primary btn-sm" :disabled="modal.saving" @click="save">
              {{ modal.saving ? 'Saving...' : (modal.mode==='add' ? 'Add Product' : 'Save Changes') }}
            </button>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useToastStore } from '@/stores/toast'
import { adminApi } from '@/api'

const toast  = useToastStore()
const products     = ref([])
const loading      = ref(true)
const search       = ref('')
const filterStatus = ref('')
const uploading    = ref(false)
const fileInput    = ref(null)
let   searchTimer  = null

const filtered = computed(() => {
  let list = products.value
  if (search.value) list = list.filter(p => p.name.toLowerCase().includes(search.value.toLowerCase()))
  if (filterStatus.value === 'active')   list = list.filter(p => p.active)
  if (filterStatus.value === 'inactive') list = list.filter(p => !p.active)
  return list
})

const modal = ref({ show:false, mode:'add', saving:false, data:{} })

async function load() {
  loading.value = true
  try {
    const { data } = await adminApi.listProducts()
    products.value = data
  } catch { /* silent */ } finally { loading.value = false }
}

function debouncedLoad() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(load, 350)
}

function openAdd() {
  modal.value = { show:true, mode:'add', saving:false, data:{ name:'', description:'', price:'', unit:'kg', category:'sugarcane', badge:'', image_url:'', image_urls:[], stock:100, active:true, featured:false } }
}

function openEdit(p) {
  modal.value = { show:true, mode:'edit', saving:false, data:{ ...p, image_urls: p.image_urls || [] } }
}

function removeImage(idx) {
  modal.value.data.image_urls.splice(idx, 1)
  if (modal.value.data.image_urls.length > 0) {
    modal.value.data.image_url = modal.value.data.image_urls[0]
  } else {
    modal.value.data.image_url = ''
  }
}

async function uploadImage(e) {
  const file = e.target.files[0]
  if (!file) return
  uploading.value = true
  try {
    const fd = new FormData(); fd.append('file', file)
    const { data } = await adminApi.uploadImage(fd)
    if (!modal.value.data.image_urls) {
      modal.value.data.image_urls = []
    }
    modal.value.data.image_urls.push(data.url)
    if (!modal.value.data.image_url) {
      modal.value.data.image_url = data.url
    }
    toast.success('Image uploaded!')
  } catch { toast.error('Upload failed') } finally { uploading.value = false }
}

async function save() {
  const d = modal.value.data
  if (!d.name || !d.price) { toast.error('Name and price are required'); return }
  modal.value.saving = true
  try {
    if (modal.value.mode === 'add') {
      const { data } = await adminApi.addProduct(d)
      products.value.unshift(data)
    } else {
      const { data } = await adminApi.updateProduct(d.id, d)
      const i = products.value.findIndex(p => p.id === d.id)
      if (i > -1) products.value[i] = data
    }
    modal.value.show = false
    toast.success(`Product ${modal.value.mode === 'add' ? 'added' : 'updated'}!`)
  } catch (e) { toast.error(e.response?.data?.error || 'Save failed') }
  finally { modal.value.saving = false }
}

async function toggleActive(p) {
  try {
    const { data } = await adminApi.updateProduct(p.id, { ...p, active: !p.active })
    const i = products.value.findIndex(x => x.id === p.id)
    if (i > -1) products.value[i] = data
    toast.success(`Product ${data.active ? 'shown' : 'hidden'}`)
  } catch { toast.error('Update failed') }
}

async function confirmDelete(p) {
  if (!confirm(`Hide "${p.name}" from the store?`)) return
  try {
    await adminApi.deleteProduct(p.id)
    const i = products.value.findIndex(x => x.id === p.id)
    if (i > -1) products.value[i].active = false
    toast.success('Product hidden')
  } catch { toast.error('Delete failed') }
}

load()
</script>
