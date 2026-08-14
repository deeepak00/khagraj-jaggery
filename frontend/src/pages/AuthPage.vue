<template>
  <div style="min-height:100vh;display:flex;align-items:center;justify-content:center;padding:108px 24px 48px;background:linear-gradient(135deg,var(--cream) 60%,var(--cream2) 100%)">
    <div style="background:var(--white);border-radius:var(--radius-xl);padding:48px 40px;width:100%;max-width:420px;box-shadow:0 8px 48px var(--shadow-md);border:1px solid rgba(200,136,42,.12)">

      <!-- Logo -->
      <div class="text-center" style="margin-bottom:28px">
        <div style="font-family:'Playfair Display',serif;font-size:1.9rem;font-weight:700;color:var(--brown)">
          {{ site.get('site_name','GurMahima') }}
        </div>
        <div style="font-size:.82rem;color:var(--text-lt);margin-top:4px">Welcome back — or join us today 🍯</div>
      </div>

      <!-- Tabs -->
      <div style="display:flex;background:var(--cream2);border-radius:10px;padding:4px;margin-bottom:24px">
        <button v-for="t in ['login','register']" :key="t"
          style="flex:1;padding:10px;border:none;border-radius:8px;font-size:.88rem;font-weight:500;cursor:pointer;transition:all .2s;text-transform:capitalize"
          :style="tab===t?'background:var(--white);color:var(--brown);box-shadow:0 2px 8px var(--shadow)':'background:transparent;color:var(--text-md)'"
          @click="tab=t; clearErrors()">
          {{ t }}
        </button>
      </div>

      <!-- Error banner -->
      <div v-if="errors.general" style="background:rgba(192,57,43,.1);border:1px solid rgba(192,57,43,.25);border-radius:10px;padding:12px 16px;margin-bottom:16px;font-size:.85rem;color:var(--red)">
        {{ errors.general }}
      </div>

      <!-- Register fields -->
      <template v-if="tab==='register'">
        <div class="form-group">
          <label class="form-label">Full Name <span class="req">*</span></label>
          <input class="form-control" :class="{error:errors.name}" v-model="form.name" placeholder="Your full name" />
          <span v-if="errors.name" class="form-error">{{ errors.name }}</span>
        </div>
        <div class="form-group">
          <label class="form-label">Email <span class="req">*</span></label>
          <input class="form-control" :class="{error:errors.email}" type="email" v-model="form.email" placeholder="you@example.com" />
          <span v-if="errors.email" class="form-error">{{ errors.email }}</span>
        </div>
        <div class="form-group">
          <label class="form-label">Phone</label>
          <input class="form-control" type="tel" v-model="form.phone" placeholder="+91 9876543210" />
        </div>

        <div class="form-group">
          <label class="form-label">Password <span class="req">*</span></label>
          <input class="form-control" :class="{error:errors.password}" type="password" v-model="form.password" placeholder="Min 6 characters" @keyup.enter="submit" />
          <span v-if="errors.password" class="form-error">{{ errors.password }}</span>
        </div>
      </template>

      <!-- Login fields -->
      <template v-else>
        <div class="form-group">
          <label class="form-label">Email <span class="req">*</span></label>
          <input class="form-control" :class="{error:errors.email}" type="email" v-model="form.email" placeholder="you@example.com" />
          <span v-if="errors.email" class="form-error">{{ errors.email }}</span>
        </div>
        <div class="form-group">
          <label class="form-label">Password <span class="req">*</span></label>
          <input class="form-control" :class="{error:errors.password}" type="password" v-model="form.password" placeholder="Your password" @keyup.enter="submit" />
          <span v-if="errors.password" class="form-error">{{ errors.password }}</span>
        </div>
      </template>

      <button class="btn btn-primary w-full" style="justify-content:center;border-radius:12px;margin-top:4px" :disabled="loading" @click="submit">
        {{ loading ? 'Please wait...' : (tab==='login' ? 'Login →' : 'Create Account →') }}
      </button>

      <p style="text-align:center;margin-top:18px;font-size:.85rem;color:var(--text-lt)">
        {{ tab==='login' ? "Don't have an account?" : 'Already have an account?' }}
        <a style="color:var(--amber);cursor:pointer;font-weight:500" @click="tab = tab==='login'?'register':'login'; clearErrors()">
          {{ tab==='login' ? 'Register here' : 'Login here' }}
        </a>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useSiteStore } from '@/stores/site'

const auth   = useAuthStore()
const site   = useSiteStore()
const router = useRouter()
const route  = useRoute()

const tab     = ref(route.query.tab === 'register' ? 'register' : 'login')
const loading = ref(false)
const errors  = ref({})
const form    = ref({ name:'', email:'', phone:'', password:'' })

function clearErrors() { errors.value = {} }

// Watch query parameters for switching tabs
watch(() => route.query.tab, (newTab) => {
  tab.value = newTab === 'register' ? 'register' : 'login'
  clearErrors()
})


async function submit() {
  clearErrors()
  const f = form.value

  if (tab.value === 'register' && !f.name.trim()) { errors.value.name = 'Name required'; return }
  if (!f.email.trim()) { errors.value.email = 'Email required'; return }
  if (!f.password)     { errors.value.password = 'Password required'; return }

  loading.value = true
  try {
    let user
    if (tab.value === 'login') {
      user = await auth.login(f.email, f.password)
    } else {
      user = await auth.register({ name:f.name, email:f.email, phone:f.phone, password:f.password })
    }
    const redirect = route.query.redirect || (user.role === 'admin' ? '/admin/dashboard' : '/')
    router.push(redirect)
  } catch (err) {
    errors.value.general = err.response?.data?.error || 'Something went wrong. Please try again.'
  } finally {
    loading.value = false
  }
}

onMounted(() => { if (auth.isLoggedIn) router.push('/') })
</script>

<style scoped>
.req { color: var(--amber); margin-left: 2px; }
</style>
