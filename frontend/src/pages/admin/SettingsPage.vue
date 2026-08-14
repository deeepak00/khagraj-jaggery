<template>
  <div>
    <div style="margin-bottom:28px">
      <h2 style="font-size:1.9rem;color:var(--brown);margin-bottom:4px">Site Settings 🎨</h2>
      <p style="font-size:.9rem;color:var(--text-lt)">Control every aspect of your website — content, branding, and contact info.</p>
    </div>

    <div v-if="loading" class="loader"><div class="spinner"></div></div>

    <div v-else style="display:grid;grid-template-columns:1fr 1fr;gap:24px">

      <!-- Branding -->
      <div class="card">
        <div class="card-header"><h3>🎨 Branding</h3></div>
        <div class="card-body">
          <div class="form-group">
            <label class="form-label">Site Name</label>
            <input class="form-control" v-model="form.site_name" placeholder="KhagRaj"/>
          </div>
          <div class="form-group">
            <label class="form-label">Tagline</label>
            <input class="form-control" v-model="form.site_tagline" placeholder="Pure Jaggery, Ancient Goodness"/>
          </div>
          <div class="form-group">
            <label class="form-label">Logo Image</label>
            <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap">
              <div v-if="form.site_logo" style="width:80px;height:48px;border-radius:8px;overflow:hidden;border:1.5px solid rgba(200,136,42,.2);padding:4px;background:var(--cream2);display:flex;align-items:center;justify-content:center">
                <img :src="form.site_logo" style="max-width:100%;max-height:100%;object-fit:contain"/>
              </div>
              <div style="font-size:.8rem;color:var(--text-lt)">🔒 Logo modification is locked</div>
            </div>
          </div>
        </div>
      </div>

      <!-- About Section -->
      <div class="card">
        <div class="card-header"><h3>📖 About Section</h3></div>
        <div class="card-body">
          <div class="form-group">
            <label class="form-label">About Title</label>
            <input class="form-control" v-model="form.about_title" placeholder="Made with Tradition, Served with Pride"/>
          </div>
          <div class="form-group">
            <label class="form-label">About Text</label>
            <textarea class="form-control" v-model="form.about_text" style="min-height:120px" placeholder="Tell your brand story..."></textarea>
          </div>
        </div>
      </div>

      <!-- Contact Info -->
      <div class="card">
        <div class="card-header"><h3>📞 Contact Information</h3></div>
        <div class="card-body">
          <div class="form-group">
            <label class="form-label">Phone Number</label>
            <input class="form-control" v-model="form.contact_phone" placeholder="+91-6394050508, +91-8601982296"/>
          </div>
          <div class="form-group">
            <label class="form-label">Email Address</label>
            <input class="form-control" type="email" v-model="form.contact_email" placeholder="khagrajindia2017@gmail.com"/>
          </div>
          <div class="form-group">
            <label class="form-label">Address</label>
            <textarea class="form-control" v-model="form.contact_address" placeholder="Full address..."></textarea>
          </div>
          <div class="form-group">
            <label class="form-label">Working Hours</label>
            <input class="form-control" v-model="form.working_hours" placeholder="Mon–Sat, 9:00 AM – 6:00 PM"/>
          </div>
        </div>
      </div>

      <!-- Social & WhatsApp -->
      <div class="card">
        <div class="card-header"><h3>📱 Social Media</h3></div>
        <div class="card-body">
          <div class="form-group">
            <label class="form-label">WhatsApp Number <span style="font-size:.75rem;color:var(--text-lt)">(with country code, no spaces)</span></label>
            <input class="form-control" v-model="form.whatsapp_number" placeholder="919876543210"/>
          </div>
          <div class="form-group">
            <label class="form-label">Instagram URL</label>
            <input class="form-control" v-model="form.instagram_url" placeholder="https://instagram.com/your_handle"/>
          </div>
          <div class="form-group">
            <label class="form-label">Facebook URL</label>
            <input class="form-control" v-model="form.facebook_url" placeholder="https://facebook.com/your_page"/>
          </div>
        </div>
      </div>
      <!-- Shipping & Discounts -->
      <div class="card">
        <div class="card-header"><h3>💰 Shipping & Discounts</h3></div>
        <div class="card-body">
          <div class="form-group">
            <label class="form-label">Seasonal Discount Percentage (%)</label>
            <input class="form-control" type="number" min="0" max="100" v-model="form.seasonal_discount_percent" placeholder="e.g. 10"/>
          </div>
          <div class="form-group">
            <label class="form-label">Free Delivery Threshold Amount (₹)</label>
            <input class="form-control" type="number" min="0" v-model="form.shipping_free_threshold" placeholder="e.g. 500"/>
          </div>
          <div class="form-group">
            <label class="form-label">Standard Delivery Charge (₹)</label>
            <input class="form-control" type="number" min="0" v-model="form.shipping_base_fee" placeholder="e.g. 50"/>
          </div>
        </div>
      </div>

      <!-- Announcement Banner -->
      <div class="card">
        <div class="card-header"><h3>📢 Announcement Banner</h3></div>
        <div class="card-body">
          <div class="form-group">
            <label class="form-label">Banner Text</label>
            <input class="form-control" v-model="form.announcement_text" placeholder="e.g. 🎉 Free delivery on orders above ₹500!"/>
          </div>
          <div class="form-group">
            <label class="form-label" style="display:flex;align-items:center;gap:10px;cursor:pointer">
              <input type="checkbox" v-model="announcementActive" style="width:18px;height:18px;accent-color:var(--amber)"/>
              Show banner on website
            </label>
          </div>
        </div>
      </div>

      <!-- Team Management -->
      <div class="card" style="grid-column:1/-1">
        <div class="card-header"><h3>👥 Team Management (About Us)</h3></div>
        <div class="card-body" style="display:grid;grid-template-columns:repeat(auto-fit, minmax(300px, 1fr));gap:24px">
          
          <!-- Manager 1: Lal Ji -->
          <div style="background:var(--cream2);padding:20px;border-radius:12px;border:1px solid rgba(200,136,42,.15)">
            <h4 style="margin-bottom:12px;color:var(--brown);font-size:1.05rem">Manager 1: Founder</h4>
            <div class="form-group">
              <label class="form-label">Name</label>
              <input class="form-control" v-model="form.manager_lalji_name" placeholder="Lal Ji"/>
            </div>
            <div class="form-group">
              <label class="form-label">Role</label>
              <input class="form-control" v-model="form.manager_lalji_role" placeholder="Founder"/>
            </div>
            <div class="form-group">
              <label class="form-label">Biography</label>
              <textarea class="form-control" v-model="form.manager_lalji_bio" style="min-height:70px" placeholder="Lal Ji bio..."></textarea>
            </div>
            <div class="form-group">
              <label class="form-label">Photo</label>
              <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">
                <div v-if="form.manager_lalji_photo" style="width:50px;height:50px;border-radius:50%;overflow:hidden;border:1.5px solid rgba(200,136,42,.2)">
                  <img :src="form.manager_lalji_photo" style="width:100%;height:100%;object-fit:cover"/>
                </div>
                <div v-else style="width:50px;height:50px;border-radius:50%;background:var(--amber-lt);display:flex;align-items:center;justify-content:center;color:var(--amber);font-weight:bold;font-size:1.2rem">
                  L
                </div>
                <div>
                  <input type="file" accept="image/*" ref="photoLaljiInput" style="display:none" @change="e => uploadManagerPhoto(e, 'manager_lalji_photo')"/>
                  <button class="btn btn-ghost btn-sm" @click="$refs.photoLaljiInput.click()">📷 Upload</button>
                  <button v-if="form.manager_lalji_photo" class="btn btn-ghost btn-sm" @click="form.manager_lalji_photo=''" style="color:var(--red)">Remove</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Manager 2: Awadhesh Maurya -->
          <div style="background:var(--cream2);padding:20px;border-radius:12px;border:1px solid rgba(200,136,42,.15)">
            <h4 style="margin-bottom:12px;color:var(--brown);font-size:1.05rem">Manager 2: Son (Operations)</h4>
            <div class="form-group">
              <label class="form-label">Name</label>
              <input class="form-control" v-model="form.manager_awadhesh_name" placeholder="Mr. Awadhesh Maurya"/>
            </div>
            <div class="form-group">
              <label class="form-label">Role</label>
              <input class="form-control" v-model="form.manager_awadhesh_role" placeholder="Co-Director"/>
            </div>
            <div class="form-group">
              <label class="form-label">Biography</label>
              <textarea class="form-control" v-model="form.manager_awadhesh_bio" style="min-height:70px" placeholder="Awadhesh bio..."></textarea>
            </div>
            <div class="form-group">
              <label class="form-label">Photo</label>
              <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">
                <div v-if="form.manager_awadhesh_photo" style="width:50px;height:50px;border-radius:50%;overflow:hidden;border:1.5px solid rgba(200,136,42,.2)">
                  <img :src="form.manager_awadhesh_photo" style="width:100%;height:100%;object-fit:cover"/>
                </div>
                <div v-else style="width:50px;height:50px;border-radius:50%;background:var(--amber-lt);display:flex;align-items:center;justify-content:center;color:var(--amber);font-weight:bold;font-size:1.2rem">
                  A
                </div>
                <div>
                  <input type="file" accept="image/*" ref="photoAwadheshInput" style="display:none" @change="e => uploadManagerPhoto(e, 'manager_awadhesh_photo')"/>
                  <button class="btn btn-ghost btn-sm" @click="$refs.photoAwadheshInput.click()">📷 Upload</button>
                  <button v-if="form.manager_awadhesh_photo" class="btn btn-ghost btn-sm" @click="form.manager_awadhesh_photo=''" style="color:var(--red)">Remove</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Manager 3: Arjun Maurya -->
          <div style="background:var(--cream2);padding:20px;border-radius:12px;border:1px solid rgba(200,136,42,.15)">
            <h4 style="margin-bottom:12px;color:var(--brown);font-size:1.05rem">Manager 3: Son (Reach)</h4>
            <div class="form-group">
              <label class="form-label">Name</label>
              <input class="form-control" v-model="form.manager_arjun_name" placeholder="Mr. Arjun Maurya"/>
            </div>
            <div class="form-group">
              <label class="form-label">Role</label>
              <input class="form-control" v-model="form.manager_arjun_role" placeholder="Co-Director"/>
            </div>
            <div class="form-group">
              <label class="form-label">Biography</label>
              <textarea class="form-control" v-model="form.manager_arjun_bio" style="min-height:70px" placeholder="Arjun bio..."></textarea>
            </div>
            <div class="form-group">
              <label class="form-label">Photo</label>
              <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">
                <div v-if="form.manager_arjun_photo" style="width:50px;height:50px;border-radius:50%;overflow:hidden;border:1.5px solid rgba(200,136,42,.2)">
                  <img :src="form.manager_arjun_photo" style="width:100%;height:100%;object-fit:cover"/>
                </div>
                <div v-else style="width:50px;height:50px;border-radius:50%;background:var(--amber-lt);display:flex;align-items:center;justify-content:center;color:var(--amber);font-weight:bold;font-size:1.2rem">
                  A
                </div>
                <div>
                  <input type="file" accept="image/*" ref="photoArjunInput" style="display:none" @change="e => uploadManagerPhoto(e, 'manager_arjun_photo')"/>
                  <button class="btn btn-ghost btn-sm" @click="$refs.photoArjunInput.click()">📷 Upload</button>
                  <button v-if="form.manager_arjun_photo" class="btn btn-ghost btn-sm" @click="form.manager_arjun_photo=''" style="color:var(--red)">Remove</button>
                </div>
              </div>
            </div>
          </div>

      </div>
    </div>

      <!-- Customer Testimonials -->
      <div class="card" style="grid-column:1/-1">
        <div class="card-header"><h3>💬 Customer Testimonials</h3></div>
        <div class="card-body" style="display:grid;grid-template-columns:repeat(auto-fit, minmax(300px, 1fr));gap:24px">
          
          <!-- Testimonial 1 -->
          <div style="background:var(--cream2);padding:20px;border-radius:12px;border:1px solid rgba(200,136,42,.15)">
            <h4 style="margin-bottom:12px;color:var(--brown);font-size:1.05rem">Testimonial 1</h4>
            <div class="form-group">
              <label class="form-label">Name</label>
              <input class="form-control" v-model="form.testimonial_1_name" placeholder="Meera K."/>
            </div>
            <div class="form-group">
              <label class="form-label">Subheading / Role</label>
              <input class="form-control" v-model="form.testimonial_1_role" placeholder="Verified Buyer • Mumbai"/>
            </div>
            <div class="form-group">
              <label class="form-label">Comment Text</label>
              <textarea class="form-control" v-model="form.testimonial_1_text" style="min-height:70px" placeholder="Comment..."></textarea>
            </div>
            <div class="form-group">
              <label class="form-label">Photo</label>
              <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">
                <div v-if="form.testimonial_1_photo" style="width:50px;height:50px;border-radius:50%;overflow:hidden;border:1.5px solid rgba(200,136,42,.2)">
                  <img :src="form.testimonial_1_photo" style="width:100%;height:100%;object-fit:cover"/>
                </div>
                <div v-else style="width:50px;height:50px;border-radius:50%;background:var(--amber-lt);display:flex;align-items:center;justify-content:center;color:var(--amber);font-weight:bold;font-size:1.2rem">
                  T1
                </div>
                <div>
                  <input type="file" accept="image/*" ref="testimonial1PhotoInput" style="display:none" @change="e => uploadManagerPhoto(e, 'testimonial_1_photo')"/>
                  <button class="btn btn-ghost btn-sm" @click="$refs.testimonial1PhotoInput.click()">📷 Upload</button>
                  <button v-if="form.testimonial_1_photo" class="btn btn-ghost btn-sm" @click="form.testimonial_1_photo=''" style="color:var(--red)">Remove</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Testimonial 2 -->
          <div style="background:var(--cream2);padding:20px;border-radius:12px;border:1px solid rgba(200,136,42,.15)">
            <h4 style="margin-bottom:12px;color:var(--brown);font-size:1.05rem">Testimonial 2</h4>
            <div class="form-group">
              <label class="form-label">Name</label>
              <input class="form-control" v-model="form.testimonial_2_name" placeholder="Rajesh S."/>
            </div>
            <div class="form-group">
              <label class="form-label">Subheading / Role</label>
              <input class="form-control" v-model="form.testimonial_2_role" placeholder="Sweet Shop Owner • Delhi"/>
            </div>
            <div class="form-group">
              <label class="form-label">Comment Text</label>
              <textarea class="form-control" v-model="form.testimonial_2_text" style="min-height:70px" placeholder="Comment..."></textarea>
            </div>
            <div class="form-group">
              <label class="form-label">Photo</label>
              <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">
                <div v-if="form.testimonial_2_photo" style="width:50px;height:50px;border-radius:50%;overflow:hidden;border:1.5px solid rgba(200,136,42,.2)">
                  <img :src="form.testimonial_2_photo" style="width:100%;height:100%;object-fit:cover"/>
                </div>
                <div v-else style="width:50px;height:50px;border-radius:50%;background:var(--amber-lt);display:flex;align-items:center;justify-content:center;color:var(--amber);font-weight:bold;font-size:1.2rem">
                  T2
                </div>
                <div>
                  <input type="file" accept="image/*" ref="testimonial2PhotoInput" style="display:none" @change="e => uploadManagerPhoto(e, 'testimonial_2_photo')"/>
                  <button class="btn btn-ghost btn-sm" @click="$refs.testimonial2PhotoInput.click()">📷 Upload</button>
                  <button v-if="form.testimonial_2_photo" class="btn btn-ghost btn-sm" @click="form.testimonial_2_photo=''" style="color:var(--red)">Remove</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Testimonial 3 -->
          <div style="background:var(--cream2);padding:20px;border-radius:12px;border:1px solid rgba(200,136,42,.15)">
            <h4 style="margin-bottom:12px;color:var(--brown);font-size:1.05rem">Testimonial 3</h4>
            <div class="form-group">
              <label class="form-label">Name</label>
              <input class="form-control" v-model="form.testimonial_3_name" placeholder="Anjali P."/>
            </div>
            <div class="form-group">
              <label class="form-label">Subheading / Role</label>
              <input class="form-control" v-model="form.testimonial_3_role" placeholder="Fitness Blogger • Pune"/>
            </div>
            <div class="form-group">
              <label class="form-label">Comment Text</label>
              <textarea class="form-control" v-model="form.testimonial_3_text" style="min-height:70px" placeholder="Comment..."></textarea>
            </div>
            <div class="form-group">
              <label class="form-label">Photo</label>
              <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">
                <div v-if="form.testimonial_3_photo" style="width:50px;height:50px;border-radius:50%;overflow:hidden;border:1.5px solid rgba(200,136,42,.2)">
                  <img :src="form.testimonial_3_photo" style="width:100%;height:100%;object-fit:cover"/>
                </div>
                <div v-else style="width:50px;height:50px;border-radius:50%;background:var(--amber-lt);display:flex;align-items:center;justify-content:center;color:var(--amber);font-weight:bold;font-size:1.2rem">
                  T3
                </div>
                <div>
                  <input type="file" accept="image/*" ref="testimonial3PhotoInput" style="display:none" @change="e => uploadManagerPhoto(e, 'testimonial_3_photo')"/>
                  <button class="btn btn-ghost btn-sm" @click="$refs.testimonial3PhotoInput.click()">📷 Upload</button>
                  <button v-if="form.testimonial_3_photo" class="btn btn-ghost btn-sm" @click="form.testimonial_3_photo=''" style="color:var(--red)">Remove</button>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- Branches Info -->
      <div class="card" style="grid-column:1/-1">
        <div class="card-header"><h3>🏢 Our Branches Information</h3></div>
        <div class="card-body">
          <div class="form-group">
            <label class="form-label">Branches Details</label>
            <textarea class="form-control" v-model="form.branches_info" style="min-height:120px" placeholder="Enter branch names, addresses, and details..."></textarea>
          </div>
        </div>
      </div>

      <!-- Save Button -->
      <div style="grid-column:1/-1;display:flex;justify-content:flex-end;gap:12px">
        <button class="btn btn-ghost" @click="load()">Discard Changes</button>
        <button class="btn btn-primary btn-lg" :disabled="saving" @click="save">
          {{ saving ? 'Saving...' : '💾 Save All Settings' }}
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useToastStore } from '@/stores/toast'
import { useSiteStore }  from '@/stores/site'
import { adminApi }      from '@/api'

const toast  = useToastStore()
const site   = useSiteStore()
const loading       = ref(true)
const saving        = ref(false)

const form = ref({
  site_name:'', site_tagline:'', site_logo:'',
  hero_title:'', hero_subtitle:'',
  about_title:'', about_text:'',
  contact_phone:'', contact_email:'', contact_address:'', working_hours:'',
  whatsapp_number:'', instagram_url:'', facebook_url:'',
  announcement_text:'', announcement_active:'false',
  manager_lalji_name:'', manager_lalji_role:'', manager_lalji_bio:'', manager_lalji_photo:'',
  manager_awadhesh_name:'', manager_awadhesh_role:'', manager_awadhesh_bio:'', manager_awadhesh_photo:'',
  manager_arjun_name:'', manager_arjun_role:'', manager_arjun_bio:'', manager_arjun_photo:'',
  branches_info:'',
  shipping_free_threshold:'', shipping_base_fee:'', seasonal_discount_percent:'',
  testimonial_1_name:'', testimonial_1_role:'', testimonial_1_text:'', testimonial_1_photo:'',
  testimonial_2_name:'', testimonial_2_role:'', testimonial_2_text:'', testimonial_2_photo:'',
  testimonial_3_name:'', testimonial_3_role:'', testimonial_3_text:'', testimonial_3_photo:'',
})

const announcementActive = computed({
  get: () => form.value.announcement_active === 'true',
  set: (v) => { form.value.announcement_active = v ? 'true' : 'false' },
})

async function load() {
  loading.value = true
  try {
    const currentSettings = site.settings.value || site.settings
    form.value = { ...form.value, ...currentSettings }
    const { data } = await adminApi.getSettings()
    form.value = { ...form.value, ...data }
  } catch { /* silent */ } finally { loading.value = false }
}

async function save() {
  saving.value = true
  try {
    await adminApi.updateSettings(form.value)
    await site.fetchPublic()
    toast.success('Settings saved successfully!')
  } catch { toast.error('Failed to save settings') } finally { saving.value = false }
}


async function uploadManagerPhoto(e, fieldName) {
  const file = e.target.files[0]; if (!file) return
  toast.info('Uploading photo...')
  try {
    const fd = new FormData(); fd.append('file', file)
    const { data } = await adminApi.uploadImage(fd)
    form.value[fieldName] = data.url
    toast.success('Photo uploaded successfully!')
  } catch {
    toast.error('Photo upload failed')
  }
}

load()
</script>
