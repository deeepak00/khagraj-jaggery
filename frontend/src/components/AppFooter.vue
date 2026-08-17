<template>
  <footer style="background:var(--brown);color:var(--cream);padding:60px 0 0">
    <div class="container">
      <div class="footer-grid">
        <!-- Brand -->
        <div>
          <div style="display:flex;align-items:center;margin-bottom:16px">
            <img v-if="site.get('site_logo')" :src="site.get('site_logo')" style="height:76px;border-radius:6px;object-fit:contain" />
          </div>

          <p style="font-family:'Lora',serif;font-size:.88rem;color:rgba(253,246,227,.55);line-height:1.7;margin-bottom:20px">
            {{ site.get('site_tagline','Pure Jaggery, Ancient Goodness') }} — Handcrafted with love, delivered fresh.
          </p>
          <div style="display:flex;gap:12px">
            <a v-if="site.get('whatsapp_number')" :href="`https://wa.me/${site.get('whatsapp_number')}`" target="_blank"
               style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.1);display:flex;align-items:center;justify-content:center;font-size:1.1rem;transition:background .2s"
               title="WhatsApp">💬</a>
            <a v-if="site.get('instagram_url')" :href="site.get('instagram_url')" target="_blank"
               style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.1);display:flex;align-items:center;justify-content:center;font-size:1.1rem">📷</a>
            <a v-if="site.get('facebook_url')" :href="site.get('facebook_url')" target="_blank"
               style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.1);display:flex;align-items:center;justify-content:center;font-size:1.1rem">👍</a>
          </div>
        </div>

        <!-- Quick links -->
        <div>
          <div class="footer-col-title">Quick Links</div>
          <ul style="list-style:none;display:flex;flex-direction:column;gap:10px">
            <li><router-link to="/"     class="footer-link">Home</router-link></li>
            <li><router-link to="/shop" class="footer-link">Shop</router-link></li>
            <li><a class="footer-link" @click="scrollTo('about')">About Us</a></li>
            <li><a class="footer-link" @click="scrollTo('contact')">Contact</a></li>
          </ul>
        </div>

        <!-- Products -->
        <div>
          <div class="footer-col-title">Products</div>
          <ul style="list-style:none;display:flex;flex-direction:column;gap:10px">
            <li><router-link to="/shop?category=sugarcane" class="footer-link">Sugarcane Jaggery</router-link></li>
            <li><router-link to="/shop?category=palm"      class="footer-link">Palm Jaggery</router-link></li>
            <li><router-link to="/shop?category=flavored"  class="footer-link">Flavored Jaggery</router-link></li>
            <li><router-link to="/shop?featured=true"      class="footer-link">Featured Items</router-link></li>
          </ul>
        </div>

        <!-- Contact -->
        <div>
          <div class="footer-col-title">Contact</div>
          <div style="display:flex;flex-direction:column;gap:12px">
            <div v-if="site.get('contact_phone')" class="footer-contact-item">
              📞 <span>{{ site.get('contact_phone') }}</span>
            </div>
            <div v-if="site.get('contact_email')" class="footer-contact-item">
              ✉️ <span>{{ site.get('contact_email') }}</span>
            </div>
            <div v-if="site.get('working_hours')" class="footer-contact-item">
              🕐 <span>{{ site.get('working_hours') }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div style="border-top:1px solid rgba(200,136,42,.2);padding:20px 0;margin-top:8px">
      <div class="container" style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px">
        <p style="font-size:.82rem;color:rgba(253,246,227,.35)">
          © {{ new Date().getFullYear() }} {{ site.get('site_name','GurMahima') }}. All rights reserved. Made with 🍯 in India.
        </p>
        <p style="font-size:.82rem;color:rgba(253,246,227,.25)">No chemicals. No compromises.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { useSiteStore } from '@/stores/site'

const site   = useSiteStore()
const router = useRouter()
const route  = useRoute()

function scrollTo(id) {
  if (route.path !== '/') { router.push('/').then(() => setTimeout(() => document.getElementById(id)?.scrollIntoView({ behavior:'smooth' }), 200)) }
  else document.getElementById(id)?.scrollIntoView({ behavior:'smooth' })
}
</script>

<style scoped>
.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 40px;
  margin-bottom: 48px;
}

@media (max-width: 900px) {
  .footer-grid {
    grid-template-columns: 1fr;
    gap: 32px;
  }
}

.footer-col-title { font-size:.78rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--amber-lt);margin-bottom:18px; }
.footer-link { font-size:.88rem;color:rgba(253,246,227,.55);transition:color .2s;cursor:pointer; }
.footer-link:hover { color:var(--amber-lt); }
.footer-contact-item { display:flex;align-items:flex-start;gap:8px;font-size:.85rem;color:rgba(253,246,227,.6); }
</style>
