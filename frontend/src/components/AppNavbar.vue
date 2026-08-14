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
        <button v-if="!isAdminRoute" class="btn btn-dark btn-sm" style="border-radius:50px;position:relative" @click="cartOpen = !cartOpen">
          🛒 Cart
          <span v-if="cart.count" style="position:absolute;top:-7px;right:-7px;background:var(--gold);color:var(--brown);font-size:.7rem;font-weight:700;width:20px;height:20px;border-radius:50%;display:flex;align-items:center;justify-content:center">
            {{ cart.count }}
          </span>
        </button>

        <!-- Logged in -->
        <div v-if="auth.isLoggedIn" class="dropdown">
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
          <router-link to="/auth" class="btn btn-ghost btn-sm">Login</router-link>
          <router-link to="/auth?tab=register" class="btn btn-primary btn-sm">Register</router-link>
        </template>

        <!-- Hamburger toggle -->
        <button v-if="!isAdminRoute" class="mobile-menu-toggle" @click="mobileMenuOpen = !mobileMenuOpen" aria-label="Toggle Navigation">
          <span class="bar" :class="{ open: mobileMenuOpen }"></span>
          <span class="bar" :class="{ open: mobileMenuOpen }"></span>
          <span class="bar" :class="{ open: mobileMenuOpen }"></span>
        </button>
      </div>
    </nav>

    <!-- Mobile Nav Menu -->
    <div v-if="mobileMenuOpen && !isAdminRoute" class="mobile-nav-menu">
      <ul>
        <li><router-link to="/"     @click="mobileMenuOpen = false">Home</router-link></li>
        <li><router-link to="/shop" @click="mobileMenuOpen = false">Shop</router-link></li>
        <li><a href="#about"    @click.prevent="scrollTo('about'); mobileMenuOpen = false">About</a></li>
        <li><a href="#contact"  @click.prevent="scrollTo('contact'); mobileMenuOpen = false">Contact</a></li>
      </ul>
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

// Split logo text: first word plain, rest amber
const siteName   = computed(() => site.get('site_name', 'GurMahima'))
const siteSuffix = computed(() => {
  const parts = siteName.value.split(/(?=[A-Z])/)
  return parts.length > 1 ? parts.slice(1).join('') : ''
})

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

