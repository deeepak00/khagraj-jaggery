<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <aside class="admin-sidebar">
      <div style="padding:24px 20px 16px;border-bottom:1px solid rgba(200,136,42,.15)">
        <div style="font-family:'Playfair Display',serif;font-size:1.2rem;color:var(--cream);font-weight:700">
          ⚙️ Admin Panel
        </div>
        <div style="font-size:.78rem;color:rgba(253,246,227,.4);margin-top:3px">{{ auth.user?.name }}</div>
      </div>

      <div class="admin-nav-section">Dashboard</div>
      <router-link to="/admin/dashboard" custom v-slot="{isActive, navigate}">
        <div class="admin-nav-item" :class="{active:isActive}" @click="navigate">
          <span class="admin-nav-icon">📊</span> Overview
        </div>
      </router-link>

      <div class="admin-nav-section">Manage</div>
      <router-link to="/admin/orders" custom v-slot="{isActive, navigate}">
        <div class="admin-nav-item" :class="{active:isActive}" @click="navigate">
          <span class="admin-nav-icon">📦</span> Orders
          <span v-if="pendingCount" style="margin-left:auto;background:var(--amber);color:var(--white);font-size:.7rem;padding:2px 8px;border-radius:50px">
            {{ pendingCount }}
          </span>
        </div>
      </router-link>

      <router-link to="/admin/products" custom v-slot="{isActive, navigate}">
        <div class="admin-nav-item" :class="{active:isActive}" @click="navigate">
          <span class="admin-nav-icon">🟫</span> Products
        </div>
      </router-link>

      <router-link to="/admin/users" custom v-slot="{isActive, navigate}">
        <div class="admin-nav-item" :class="{active:isActive}" @click="navigate">
          <span class="admin-nav-icon">👥</span> Users
        </div>
      </router-link>

      <router-link to="/admin/settings" custom v-slot="{isActive, navigate}">
        <div class="admin-nav-item" :class="{active:isActive}" @click="navigate">
          <span class="admin-nav-icon">🎨</span> Site Settings
        </div>
      </router-link>

      <router-link to="/admin/messages" custom v-slot="{isActive, navigate}">
        <div class="admin-nav-item" :class="{active:isActive}" @click="navigate">
          <span class="admin-nav-icon">💬</span> Messages
        </div>
      </router-link>

      <div class="admin-nav-section">Account</div>
      <router-link to="/" custom v-slot="{navigate}">
        <div class="admin-nav-item" @click="navigate">
          <span class="admin-nav-icon">🏠</span> Back to Site
        </div>
      </router-link>
      <div class="admin-nav-item" @click="logout">
        <span class="admin-nav-icon">🚪</span> Logout
      </div>
    </aside>

    <!-- Content -->
    <main class="admin-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { adminApi } from '@/api'

const auth   = useAuthStore()
const router = useRouter()
const pendingCount = ref(0)

async function logout() {
  auth.logout()
  router.push('/')
}

onMounted(async () => {
  try {
    const { data } = await adminApi.stats()
    pendingCount.value = data.pending_orders
  } catch { /* silent */ }
})
</script>
