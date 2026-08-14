<template>
  <div>
    <!-- Announcement banner -->
    <div v-if="!route.path.startsWith('/admin') && site.announcementActive() && site.get('announcement_text')"
         class="announcement-bar">
      {{ site.get('announcement_text') }}
    </div>

    <AppNavbar />
    <CartSidebar />
    <AppToast />

    <main>
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <AppFooter v-if="!route.path.startsWith('/admin')" />
  </div>
</template>

<script setup>
import { onMounted, ref, provide } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useSiteStore } from '@/stores/site'
import AppNavbar   from '@/components/AppNavbar.vue'
import AppFooter   from '@/components/AppFooter.vue'
import CartSidebar from '@/components/CartSidebar.vue'
import AppToast    from '@/components/AppToast.vue'

const auth = useAuthStore()
const site = useSiteStore()
const route = useRoute()

const cartOpen = ref(false)
provide('cartOpen', cartOpen)

onMounted(async () => {
  await Promise.all([auth.restoreSession(), site.fetchPublic()])
  // Update document title
  document.title = site.get('site_name', 'GurMahima')
})
</script>


<style>
.announcement-bar {
  position: absolute;
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 101;
  background: var(--amber);
  color: var(--white);
  text-align: center;
  padding: 8px 24px;
  font-family: 'DM Sans', sans-serif;
  font-size: .88rem;
  font-weight: 500;
  border-radius: 50px;
  box-shadow: 0 4px 16px rgba(44,24,16,.15);
  width: fit-content;
  max-width: 90%;
  white-space: nowrap;
}
.fade-enter-active, .fade-leave-active { transition: opacity .18s ease; }
.fade-enter-from,  .fade-leave-to      { opacity: 0; }
</style>
