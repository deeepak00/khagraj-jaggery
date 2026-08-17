<template>
  <div style="position:relative">
    <nav class="navbar">
      <!-- Logo -->
      <router-link to="/" class="nav-logo" style="display:flex;align-items:center">
        <img v-if="site.get('site_logo')" :src="site.get('site_logo')" :alt="site.get('site_name')" style="height:76px;border-radius:6px;object-fit:contain" />
      </router-link>

      <!-- Links -->
      <ul class="nav-links">
        <li><router-link to="/"     active-class="active" exact>Home</router-link></li>
        <li><router-link to="/shop" active-class="active">Shop</router-link></li>
        <li><a href="#about"    @click.prevent="scrollTo('about')">About</a></li>
        <li><a href="#contact"  @click.prevent="scrollTo('contact')">Contact</a></li>
      </ul>

      <!-- Right side -->
      <div class="nav-right">
        <!-- Cart button (not shown in admin) -->
        <button v-if="!isAdminRoute" class="btn btn-dark btn-sm" style="border-radius:50px;position:relative;display:flex;align-items:center;gap:6px" @click="cartOpen = !cartOpen">
          <span>🛒</span>
          <span class="nav-desktop-item">Cart</span>
          <span v-if="cart.count" style="position:absolute;top:-7px;right:-7px;background:var(--gold);color:var(--brown);font-size:.7rem;font-weight:700;width:20px;height:20px;border-radius:50%;display:flex;align-items:center;justify-content:center">
            {{ cart.count }}
          </span>
        </button>

        <!-- Logged in -->
        <div v-if="auth.isLoggedIn" class="dropdown nav-desktop-item">
          <button class="btn btn-ghost btn-sm" @click.stop="dropdownOpen = !dropdownOpen">
            👤 {{ firstName }} ▾
          </button>
          <div v-if="dropdownOpen" class="dropdown-menu" @click.stop>
            <div class="dropdown-header">
              <div class="dropdown-name">{{ auth.user?.name }}</div>
              <div class="dropdown-email">{{ auth.user?.email }}</div>
            </div>
            <router-link v-if="!auth.isAdmin" class="dropdown-item" to="/my-orders" @click="dropdownOpen=false">📦 My Orders</router-link>
            <router-link v-if="auth.isAdmin" class="dropdown-item" to="/admin/dashboard" @click="dropdownOpen=false">⚙️ Admin Panel</router-link>
            <div class="dropdown-item danger" @click="logout">🚪 Logout</div>
          </div>
        </div>

        <!-- Guest -->
        <template v-else>
          <router-link to="/auth" class="btn btn-ghost btn-sm nav-desktop-item">Login</router-link>
          <router-link to="/auth?tab=register" class="btn btn-primary btn-sm nav-desktop-item">Register</router-link>
        </template>

        <!-- Hamburger toggle -->
        <button v-if="!isAdminRoute" class="mobile-menu-toggle" @click="mobileMenuOpen = !mobileMenuOpen" aria-label="Toggle Navigation">
          <span class="bar" :class="{ open: mobileMenuOpen }"></span>
          <span class="bar" :class="{ open: mobileMenuOpen }"></span>
          <span class="bar" :class="{ open: mobileMenuOpen }"></span>
        </button>
      </div>
    </nav>

    <!-- Mobile Nav Menu (Sliding Drawer) -->
    <div v-if="mobileMenuOpen && !isAdminRoute" class="mobile-nav-backdrop" @click="mobileMenuOpen = false"></div>
    <div class="mobile-nav-menu" :class="{ open: mobileMenuOpen && !isAdminRoute }">
      <!-- Close button / Header in drawer -->
      <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid rgba(200,136,42,.12);padding-bottom:16px;margin-bottom:20px">
        <span style="font-family:'Playfair Display',serif;font-weight:700;color:var(--brown);font-size:1.15rem">🧭 Navigation</span>
        <button class="btn btn-ghost btn-sm" @click="mobileMenuOpen = false" style="font-size:1.2rem;padding:4px 8px;line-height:1">×</button>
      </div>

      <!-- Navigation Links -->
      <ul style="list-style:none;display:flex;flex-direction:column;gap:18px;margin:0;padding:0">
        <li><router-link to="/"     style="font-size:1.05rem;font-weight:600;color:var(--brown);text-transform:uppercase;display:block" @click="mobileMenuOpen = false">Home</router-link></li>
        <li><router-link to="/shop" style="font-size:1.05rem;font-weight:600;color:var(--brown);text-transform:uppercase;display:block" @click="mobileMenuOpen = false">Shop</router-link></li>
        <li><a href="#about"    style="font-size:1.05rem;font-weight:600;color:var(--brown);text-transform:uppercase;display:block" @click.prevent="scrollTo('about'); mobileMenuOpen = false">About</a></li>
        <li><a href="#contact"  style="font-size:1.05rem;font-weight:600;color:var(--brown);text-transform:uppercase;display:block" @click.prevent="scrollTo('contact'); mobileMenuOpen = false">Contact</a></li>
      </ul>

      <!-- Divider / Bottom block -->
      <div style="border-top:1px solid rgba(200,136,42,.12);margin-top:auto;padding-top:20px">
        <!-- Logged in Mobile Details -->
        <div v-if="auth.isLoggedIn" style="display:grid;gap:16px">
          <div style="background:var(--cream2);padding:12px 14px;border-radius:10px">
            <div style="font-weight:600;color:var(--brown);font-size:.9rem">👤 {{ auth.user?.name }}</div>
            <div style="font-size:.75rem;color:var(--text-lt);margin-top:2px;word-break:break-all">{{ auth.user?.email }}</div>
          </div>
          <router-link v-if="!auth.isAdmin" class="btn btn-outline btn-sm" to="/my-orders" style="justify-content:center;border-radius:8px" @click="mobileMenuOpen=false">📦 My Orders</router-link>
          <router-link v-if="auth.isAdmin" class="btn btn-outline btn-sm" to="/admin/dashboard" style="justify-content:center;border-radius:8px" @click="mobileMenuOpen=false">⚙️ Admin Panel</router-link>
          <button class="btn btn-primary btn-sm" @click="logout(); mobileMenuOpen=false" style="justify-content:center;border-radius:8px">🚪 Logout</button>
        </div>

        <!-- Guest Mobile Details -->
        <div v-else style="display:grid;gap:12px">
          <router-link to="/auth" class="btn btn-outline btn-sm" style="justify-content:center;border-radius:8px" @click="mobileMenuOpen=false">Login</router-link>
          <router-link to="/auth?tab=register" class="btn btn-primary btn-sm" style="justify-content:center;border-radius:8px" @click="mobileMenuOpen=false">Register</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, inject } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { useSiteStore } from '@/stores/site'

const auth  = useAuthStore()
const cart  = useCartStore()
const site  = useSiteStore()
const route = useRoute()
const router = useRouter()

const dropdownOpen = ref(false)
const mobileMenuOpen = ref(false)
const cartOpen     = inject('cartOpen')

const isAdminRoute = computed(() => route.path.startsWith('/admin'))
const firstName    = computed(() => auth.user?.name?.split(' ')[0] || '')

function scrollTo(id) {
  mobileMenuOpen.value = false
  if (route.path !== '/') { router.push('/').then(() => setTimeout(() => document.getElementById(id)?.scrollIntoView({ behavior:'smooth' }), 200)) }
  else document.getElementById(id)?.scrollIntoView({ behavior:'smooth' })
}

async function logout() {
  auth.logout()
  dropdownOpen.value = false
  router.push('/')
}

// Close dropdown on outside click
function onDocClick() { dropdownOpen.value = false }
onMounted(()  => document.addEventListener('click', onDocClick))
onUnmounted(() => document.removeEventListener('click', onDocClick))
</script>
