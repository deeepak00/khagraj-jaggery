<template>
  <div>
    <div style="margin-bottom:28px">
      <h2 style="font-size:1.9rem;color:var(--brown);margin-bottom:4px">Users 👥</h2>
      <p style="font-size:.9rem;color:var(--text-lt)">All registered customers and admins. Activate/deactivate accounts.</p>
    </div>

    <div style="margin-bottom:18px">
      <input class="form-control" v-model="search" placeholder="Search by name or email..." style="max-width:300px" @input="debouncedLoad"/>
    </div>

    <div v-if="loading" class="loader"><div class="spinner"></div></div>
    <template v-else>
      <!-- Desktop Table View -->
      <div class="card admin-desktop-only" style="overflow:hidden">
        <div class="table-wrap">
          <table class="data-table">
            <thead>
              <tr><th>Name</th><th>Email</th><th>Phone</th><th>Role</th><th>Status</th><th>Joined</th><th>Action</th></tr>
            </thead>
            <tbody>
              <tr v-if="!users.length">
                <td colspan="7" style="text-align:center;padding:40px;color:var(--text-lt)">No users found.</td>
              </tr>
              <tr v-for="u in users" :key="u.id">
                <td>
                  <div style="display:flex;align-items:center;gap:10px">
                    <div style="width:36px;height:36px;border-radius:50%;background:var(--cream2);display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0">
                      {{ u.name?.[0]?.toUpperCase() || '?' }}
                    </div>
                    <div>
                      <div style="font-weight:500;color:var(--brown)">{{ u.name }}</div>
                    </div>
                  </div>
                </td>
                <td style="font-size:.85rem">{{ u.email }}</td>
                <td style="font-size:.85rem;color:var(--text-lt)">{{ u.phone || '—' }}</td>
                <td><span class="badge" :class="`badge-${u.role}`">{{ u.role }}</span></td>
                <td><span class="badge" :class="u.is_active?'badge-active':'badge-inactive'">{{ u.is_active ? 'Active' : 'Inactive' }}</span></td>
                <td style="font-size:.82rem;color:var(--text-lt)">{{ fmtDate(u.created_at) }}</td>
                <td>
                  <div style="display:flex;gap:6px">
                    <button v-if="u.role !== 'admin'" class="btn btn-ghost btn-sm" @click="toggleActive(u)">
                      {{ u.is_active ? 'Deactivate' : 'Activate' }}
                    </button>
                    <span v-else style="font-size:.78rem;color:var(--text-lt)">Super Admin</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Mobile Card List View -->
      <div class="admin-mobile-only">
        <div v-if="!users.length" style="text-align:center;padding:40px;color:var(--text-lt)">No users found.</div>
        <div v-else style="display:grid;gap:16px">
          <div v-for="u in users" :key="u.id" class="card" style="padding:16px;display:flex;flex-direction:column;gap:12px">
            <div style="display:flex;gap:12px;align-items:center">
              <div style="width:40px;height:40px;border-radius:50%;background:var(--cream2);display:flex;align-items:center;justify-content:center;font-size:1.1rem;font-weight:bold;color:var(--brown);flex-shrink:0">
                {{ u.name?.[0]?.toUpperCase() || '?' }}
              </div>
              <div style="flex:1">
                <div style="font-weight:600;color:var(--brown)">{{ u.name }}</div>
                <div style="font-size:.78rem;color:var(--text-lt)">{{ u.email }}</div>
              </div>
            </div>
            <div style="display:flex;justify-content:space-between;border-top:1px dashed rgba(200,136,42,.15);padding-top:10px;font-size:.82rem">
              <div>📞 {{ u.phone || 'No phone' }}</div>
              <div style="display:flex;gap:6px">
                <span class="badge" :class="`badge-${u.role}`">{{ u.role }}</span>
                <span class="badge" :class="u.is_active?'badge-active':'badge-inactive'">{{ u.is_active ? 'Active' : 'Inactive' }}</span>
              </div>
            </div>
            <div v-if="u.role !== 'admin'" style="display:flex;justify-content:flex-end;border-top:1px dashed rgba(200,136,42,.15);padding-top:10px">
              <button class="btn btn-ghost btn-sm" @click="toggleActive(u)">
                {{ u.is_active ? 'Deactivate' : 'Activate' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useToastStore } from '@/stores/toast'
import { adminApi } from '@/api'

const toast       = useToastStore()
const users       = ref([])
const loading     = ref(true)
const search      = ref('')
let   searchTimer = null

const fmtDate = d => d ? new Date(d).toLocaleDateString('en-IN',{day:'2-digit',month:'short',year:'numeric'}) : '—'

async function load() {
  loading.value = true
  try {
    const { data } = await adminApi.listUsers({ q: search.value })
    users.value = data
  } catch { /* silent */ } finally { loading.value = false }
}

function debouncedLoad() { clearTimeout(searchTimer); searchTimer = setTimeout(load, 350) }

async function toggleActive(u) {
  try {
    const { data } = await adminApi.updateUser(u.id, { is_active: !u.is_active })
    const i = users.value.findIndex(x => x.id === u.id)
    if (i > -1) users.value[i] = data
    toast.success(`User ${data.is_active ? 'activated' : 'deactivated'}`)
  } catch { toast.error('Update failed') }
}

load()
</script>
