<template>
  <div>
    <!-- HERO SECTION -->
    <section class="hero" id="home" style="position:relative;overflow:hidden;display:flex;align-items:center;min-height:100vh;padding:120px 0 80px;background:var(--cream)">
      <!-- Background subtle floating circles for decoration -->
      <div style="position:absolute;top:10%;left:5%;width:150px;height:150px;background:rgba(45,106,79,0.03);border-radius:50%;filter:blur(40px);pointer-events:none"></div>
      <div style="position:absolute;bottom:10%;left:35%;width:250px;height:250px;background:rgba(224,159,27,0.04);border-radius:50%;filter:blur(60px);pointer-events:none"></div>

      <!-- Left side subtle background watermark -->
      <div class="hide-mobile" style="position:absolute;top:66%;left:-17%;transform:translateY(-50%);width:120%;max-width:1450px;opacity:0.3;pointer-events:none;z-index:1">
        <img :src="'/uploads/hero_bg_left.png'" style="width:100%;height:auto;object-fit:contain" />
      </div>

      <!-- Right-aligned Split-Screen video (takes exactly the right half of the viewport height and width) -->
      <div class="hero-split-video">
        <video 
          autoplay 
          loop 
          muted 
          playsinline 
        >
          <source src="/video.mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </div>

      <!-- Left Content (Container aligned) -->
      <div class="container" style="position:relative;z-index:2;width:100%;display:flex;align-items:center;">
        <div style="max-width:580px;display:flex;flex-direction:column;align-items:center;text-align:center">
          <!-- Hero badge logo -->
          <div style="margin-bottom:32px;display:flex;justify-content:center">
            <img :src="'/uploads/hero_badge.png'" alt="Sugarcane Fields Logo" style="max-height:300px;max-width:100%;width:auto;object-fit:contain;margin-top:-25px" />
          </div>
          <!-- Brand storytelling quote block -->
          <div style="margin-top:16px;position:relative;max-width:540px">
            <p style="font-family:'Lora',serif;font-size:1.35rem;color:var(--brown);line-height:1.8;margin-bottom:28px;font-style:italic">
              Handcrafted in <span style="color:var(--amber);font-weight:600;font-style:normal">small batches</span> using traditional methods.<br>
              No chemicals, no additives — just <span style="background:linear-gradient(120deg, var(--amber) 0%, #2d6a4f 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:700;font-style:normal">pure, golden sweetness</span>.
            </p>
            
            <div style="display:inline-flex;align-items:center;gap:12px;font-size:0.75rem;font-weight:700;color:var(--text-lt);letter-spacing:0.16em;text-transform:uppercase;margin-top:8px">
              <span style="width:24px;height:1px;background:rgba(45,106,79,0.2)"></span>
              BY LAL JI FOODS
              <span style="width:24px;height:1px;background:rgba(45,106,79,0.2)"></span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TRUST STRIP BANNER -->
    <div style="background:var(--brown);color:var(--cream);padding:24px 0;border-top:1px solid rgba(255,255,255,0.06);border-bottom:1px solid rgba(255,255,255,0.06);position:relative;z-index:10">
      <div class="container" style="display:flex;justify-content:space-around;align-items:center;flex-wrap:wrap;gap:24px">
        <div style="display:flex;align-items:center;gap:10px;font-family:'Playfair Display',serif;font-size:1.05rem;font-weight:600">
          <span style="color:var(--amber-lt);font-size:1.4rem">🛡️</span> 100% Organic & Chemical-Free
        </div>
        <div style="display:flex;align-items:center;gap:10px;font-family:'Playfair Display',serif;font-size:1.05rem;font-weight:600">
          <span style="color:var(--amber-lt);font-size:1.4rem">🧪</span> Lab-Certified Purity
        </div>
        <div style="display:flex;align-items:center;gap:10px;font-family:'Playfair Display',serif;font-size:1.05rem;font-weight:600">
          <span style="color:var(--amber-lt);font-size:1.4rem">🏡</span> Handcrafted Batches
        </div>
        <div style="display:flex;align-items:center;gap:10px;font-family:'Playfair Display',serif;font-size:1.05rem;font-weight:600">
          <span style="color:var(--amber-lt);font-size:1.4rem">🚚</span> Free Shipping Across India
        </div>
      </div>
    </div>

    <!-- FEATURED PRODUCTS -->
    <section class="section" style="background:var(--cream2)">
      <div class="container">
        <div class="text-center mb-lg">
          <div class="section-tag" style="background:var(--cream);border-color:rgba(45,106,79,0.1)">Handpicked for You</div>
          <h2 class="section-title">Featured Products</h2>
          <p class="section-subtitle">Our most-loved jaggery varieties, straight from the production house.</p>
        </div>

        <div v-if="loadingFeatured" class="loader"><div class="spinner"></div></div>
        <div v-else style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:28px">
          <ProductCard v-for="p in featured" :key="p.id" :product="p" />
        </div>

        <div class="text-center mt-lg">
          <router-link to="/shop">
            <button class="btn btn-outline btn-lg" style="border-width:2px">View All Products →</button>
          </router-link>
        </div>
      </div>
    </section>

    <!-- WHY CHOOSE US -->
    <section class="section" style="background:var(--cream)">
      <div class="container">
        <div class="text-center mb-lg">
          <div class="section-tag" style="background:var(--cream2);border-color:rgba(45,106,79,0.1)">Superior Quality</div>
          <h2 class="section-title">The KhagRaj Difference</h2>
          <p class="section-subtitle">Why our traditional methods stand head and shoulders above standard alternatives.</p>
        </div>
        
        <div class="responsive-grid-3" style="gap:32px">
          <div v-for="w in whyUs.slice(0,3)" :key="w.title" style="background:var(--white);border-radius:24px;padding:40px;box-shadow:0 10px 30px rgba(45,106,79,0.04);border:1px solid rgba(45,106,79,0.06);text-align:center;transition:transform .3s,box-shadow .3s"
               @mouseenter="e=>e.currentTarget.style.cssText+=';transform:translateY(-8px);box-shadow:0 20px 50px rgba(45,106,79,0.08)'"
               @mouseleave="e=>e.currentTarget.style.cssText=e.currentTarget.style.cssText.replace(';transform:translateY(-8px);box-shadow:0 20px 50px rgba(45,106,79,0.08)','')">
            <div style="font-size:3.2rem;margin-bottom:20px;display:inline-block;padding:16px;background:var(--cream);border-radius:20px">{{ w.icon }}</div>
            <h3 style="font-size:1.25rem;color:var(--brown);margin-bottom:14px;font-family:'Playfair Display',serif;font-weight:700">{{ w.title }}</h3>
            <p style="font-size:.9rem;color:var(--text-lt);line-height:1.65;margin:0">{{ w.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- OUR STORY & LAL JI FOODS BACKING -->
    <section class="section" style="background:var(--brown);color:var(--cream);position:relative;overflow:hidden" id="about">
      <!-- Decoration element -->
      <div class="hide-mobile" style="position:absolute;bottom:-10%;left:-5%;width:300px;height:300px;background:rgba(255,255,255,0.02);border-radius:50%;filter:blur(50px)"></div>

      <div class="container story-grid">
        <div>
          <div class="section-tag" style="color:var(--amber-lt);background:rgba(45,106,79,0.15);border-color:rgba(45,106,79,0.3)">Our Story</div>
          <h2 style="font-size:2.8rem;color:var(--cream);margin:16px 0 24px;font-family:'Playfair Display',serif;font-weight:700">{{ site.get('about_title') }}</h2>
          <p style="color:rgba(243,248,252,0.8);font-size:1.05rem;line-height:1.75;margin-bottom:28px;font-family:'Lora',serif;white-space:pre-wrap">{{ site.get('about_text') }}</p>
          
          <div style="display:flex;align-items:center;gap:18px;background:rgba(255,255,255,0.04);border-radius:16px;padding:20px;border:1px solid rgba(255,255,255,0.08)">
            <span style="font-size:2.5rem">🤝</span>
            <div>
              <h4 style="font-family:'Playfair Display',serif;color:var(--amber-lt);margin:0 0 4px;font-size:1.1rem;font-weight:700">Backed by Lal Ji Foods</h4>
              <p style="font-size:0.82rem;color:rgba(243,248,252,0.65);margin:0;line-height:1.5">Sourcing and processing built on the heritage and quality assurance of Lal Ji Foods, building trust in every bite.</p>
            </div>
          </div>
        </div>
        
        <!-- Features checklist card -->
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:24px;padding:40px;box-shadow:0 20px 48px rgba(0,0,0,0.15)">
          <h3 style="font-family:'Playfair Display',serif;color:var(--cream);margin-bottom:24px;font-size:1.4rem;font-weight:700">Heritage Promise</h3>
          <ul style="list-style:none;display:flex;flex-direction:column;gap:20px;margin:0;padding:0">
            <li v-for="f in features" :key="f.text" style="display:flex;align-items:flex-start;gap:14px;font-family:'Lora',serif;font-size:.95rem;color:rgba(243,248,252,0.85);line-height:1.5">
              <span style="font-size:1.3rem;line-height:1;flex-shrink:0">{{ f.icon }}</span>
              <span>{{ f.text }}</span>
            </li>
          </ul>
        </div>
      </div>

      <!-- Leadership Team Section -->
      <div class="container" style="margin-top:80px;border-top:1px solid rgba(255,255,255,0.08);padding-top:60px">
        <div class="text-center mb-lg">
          <div class="section-tag" style="color:var(--amber-lt);background:rgba(45,106,79,0.15);border-color:rgba(45,106,79,0.3)">Leadership</div>
          <h2 style="font-size:2.2rem;color:var(--cream);margin-top:12px;font-family:'Playfair Display',serif">Our Team & Founders</h2>
        </div>
        
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(280px, 1fr));gap:32px">
          <!-- Lal Ji -->
          <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:20px;padding:32px;text-align:center;transition:all .3s ease">
            <div style="width:120px;height:120px;border-radius:50%;overflow:hidden;margin:0 auto 20px;border:3px solid rgba(200,136,42,.3);background:var(--cream2);display:flex;align-items:center;justify-content:center">
              <img v-if="site.get('manager_lalji_photo')" :src="site.get('manager_lalji_photo')" style="width:100%;height:100%;object-fit:cover"/>
              <span v-else style="font-size:3rem;line-height:1">👴</span>
            </div>
            <h3 style="font-family:'Playfair Display',serif;font-size:1.3rem;color:var(--cream);margin-bottom:4px">{{ site.get('manager_lalji_name','Lal Ji') }}</h3>
            <div style="font-size:.78rem;font-weight:600;color:var(--amber-lt);text-transform:uppercase;letter-spacing:.08em;margin-bottom:12px">{{ site.get('manager_lalji_role','Founder') }}</div>
            <p style="font-size:.9rem;color:rgba(243,248,252,0.7);line-height:1.6;margin:0">{{ site.get('manager_lalji_bio') }}</p>
          </div>

          <!-- Awadhesh Maurya -->
          <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:20px;padding:32px;text-align:center;transition:all .3s ease">
            <div style="width:120px;height:120px;border-radius:50%;overflow:hidden;margin:0 auto 20px;border:3px solid rgba(200,136,42,.3);background:var(--cream2);display:flex;align-items:center;justify-content:center">
              <img v-if="site.get('manager_awadhesh_photo')" :src="site.get('manager_awadhesh_photo')" style="width:100%;height:100%;object-fit:cover"/>
              <span v-else style="font-size:3rem;line-height:1">👨‍💼</span>
            </div>
            <h3 style="font-family:'Playfair Display',serif;font-size:1.3rem;color:var(--cream);margin-bottom:4px">{{ site.get('manager_awadhesh_name','Mr. Awadhesh Maurya') }}</h3>
            <div style="font-size:.78rem;font-weight:600;color:var(--amber-lt);text-transform:uppercase;letter-spacing:.08em;margin-bottom:12px">{{ site.get('manager_awadhesh_role','Co-Director') }}</div>
            <p style="font-size:.9rem;color:rgba(243,248,252,0.7);line-height:1.6;margin:0">{{ site.get('manager_awadhesh_bio') }}</p>
          </div>

          <!-- Arjun Maurya -->
          <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:20px;padding:32px;text-align:center;transition:all .3s ease">
            <div style="width:120px;height:120px;border-radius:50%;overflow:hidden;margin:0 auto 20px;border:3px solid rgba(200,136,42,.3);background:var(--cream2);display:flex;align-items:center;justify-content:center">
              <img v-if="site.get('manager_arjun_photo')" :src="site.get('manager_arjun_photo')" style="width:100%;height:100%;object-fit:cover"/>
              <span v-else style="font-size:3rem;line-height:1">👨‍💻</span>
            </div>
            <h3 style="font-family:'Playfair Display',serif;font-size:1.3rem;color:var(--cream);margin-bottom:4px">{{ site.get('manager_arjun_name','Mr. Arjun Maurya') }}</h3>
            <div style="font-size:.78rem;font-weight:600;color:var(--amber-lt);text-transform:uppercase;letter-spacing:.08em;margin-bottom:12px">{{ site.get('manager_arjun_role','Co-Director') }}</div>
            <p style="font-size:.9rem;color:rgba(243,248,252,0.7);line-height:1.6;margin:0">{{ site.get('manager_arjun_bio') }}</p>
          </div>
        </div>
      </div>

      <!-- Branches Section -->
      <div v-if="parsedBranches.length > 0" class="container" style="margin-top:70px;border-top:1px solid rgba(255,255,255,0.08);padding-top:60px;padding-bottom:20px">
        <div class="text-center mb-lg">
          <div class="section-tag" style="color:var(--amber-lt);background:rgba(45,106,79,0.15);border-color:rgba(45,106,79,0.3)">Network</div>
          <h2 style="font-size:2.2rem;color:var(--cream);margin-top:12px;font-family:'Playfair Display',serif">Our Branch Locations</h2>
        </div>
        
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(280px, 1fr));gap:28px">
          <div v-for="branch in parsedBranches" :key="branch.title" style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:24px;box-shadow:0 10px 30px rgba(0,0,0,0.1)">
            <h3 style="font-family:'Playfair Display',serif;color:var(--amber-lt);font-size:1.15rem;margin-bottom:12px;font-weight:700;display:flex;align-items:center;gap:8px">
              🏢 {{ branch.title }}
            </h3>
            <p style="font-size:.88rem;color:rgba(243,248,252,0.75);line-height:1.6;white-space:pre-wrap;margin:0;font-family:'Lora',serif">
              {{ branch.details }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- TESTIMONIAL PANEL -->
    <section class="section" style="background:var(--cream2)">
      <div class="container">
        <div class="text-center mb-lg">
          <div class="section-tag" style="background:var(--cream);border-color:rgba(45,106,79,0.1)">Customer Reviews</div>
          <h2 class="section-title">What Our Patrons Say</h2>
          <p class="section-subtitle">Real feedback from homes and chefs who choose KhagRaj for sweetening their daily lives.</p>
        </div>

        <div class="responsive-grid-3" style="gap:28px">
          <div v-for="t in testimonials" :key="t.name" style="background:var(--white);border-radius:20px;padding:32px;box-shadow:0 8px 24px rgba(45,106,79,0.03);border:1px solid rgba(45,106,79,0.05);display:flex;flex-direction:column;justify-content:space-between">
            <div style="font-size:1.1rem;color:var(--amber);margin-bottom:16px">★★★★★</div>
            <p style="font-family:'Lora',serif;font-size:0.92rem;color:var(--text-md);line-height:1.65;margin:0 0 20px;font-style:italic">
              "{{ t.text }}"
            </p>
            <div style="display:flex;align-items:center;gap:12px;border-top:1px solid rgba(45,106,79,0.06);padding-top:16px">
              <img v-if="t.photo" :src="t.photo" style="width:40px;height:40px;border-radius:50%;object-fit:cover"/>
              <div v-else style="width:40px;height:40px;border-radius:50%;background:var(--cream2);display:flex;align-items:center;justify-content:center;font-weight:700;color:var(--amber);font-size:0.9rem">
                {{ getInitials(t.name) }}
              </div>
              <div>
                <h4 style="font-family:'Playfair Display',serif;font-size:0.9rem;color:var(--brown);margin:0">{{ t.name }}</h4>
                <span style="font-size:0.7rem;color:var(--text-lt)">{{ t.role }}</span>
              </div>
            </div>
          </div>
        </div>

        <div style="text-align:center;margin-top:36px">
          <p style="font-size:0.92rem;color:var(--text-lt);margin:0">
            Want to give your testimonials? 
            <a href="#contact" @click.prevent="scrollTo('contact')" style="color:var(--amber);font-weight:600;text-decoration:underline;margin-left:4px">Reach us</a>
          </p>
        </div>
      </div>
    </section>

    <!-- CONTACT SECTION -->
    <section class="section" style="background:var(--cream)" id="contact">
      <div class="container">
        <div class="contact-grid">
          <!-- Info -->
          <div>
            <div class="section-tag" style="background:var(--cream2);border-color:rgba(45,106,79,0.1)">Talk to Us</div>
            <h2 class="section-title" style="text-align:left;margin-top:16px">Let's Connect</h2>
            <p class="section-subtitle" style="text-align:left;margin-bottom:40px">Have questions about bulk orders, customization or shipping? Send us a message.</p>

            <div class="contact-info-grid">
              <div v-for="c in contactItems" :key="c.label" style="background:var(--white);padding:20px;border-radius:16px;box-shadow:0 6px 16px rgba(45,106,79,0.02);border:1px solid rgba(45,106,79,0.04)">
                <div style="font-size:1.6rem;margin-bottom:8px">{{ c.icon }}</div>
                <div style="font-size:.72rem;color:var(--text-lt);text-transform:uppercase;letter-spacing:.05em;font-weight:600">{{ c.label }}</div>
                <div style="font-family:'Lora',serif;color:var(--text-md);margin-top:2px;font-size:.9rem;font-weight:500;word-break:break-word">{{ c.val }}</div>
              </div>
            </div>
          </div>

          <!-- Form -->
          <div style="background:var(--white);border-radius:24px;padding:44px;box-shadow:0 12px 40px rgba(45,106,79,0.04);border:1px solid rgba(45,106,79,0.08)">
            <h4 style="font-family:'Playfair Display',serif;font-size:1.3rem;color:var(--brown);margin-bottom:24px;font-weight:700">Send us a Message</h4>
            <div class="form-group">
              <label class="form-label">Your Name</label>
              <input class="form-control" v-model="contact.name" placeholder="e.g. Ravi Kumar" />
            </div>
            <div class="form-group">
              <label class="form-label">Phone / Email</label>
              <input class="form-control" v-model="contact.contact" placeholder="e.g. +91 98765 43210" />
            </div>
            <div class="form-group">
              <label class="form-label">Message</label>
              <textarea class="form-control" v-model="contact.message" placeholder="Tell us what you are looking for..." style="height:120px;resize:none"></textarea>
            </div>
            <button class="btn btn-primary w-full" style="justify-content:center;border-radius:12px;padding:14px;font-weight:600;font-size:1rem" @click="sendContact">
              Send Message 📨
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useSiteStore }  from '@/stores/site'
import { useToastStore } from '@/stores/toast'
import { productsApi, contactApi }   from '@/api'
import ProductCard       from '@/components/ProductCard.vue'

const site    = useSiteStore()
const toast   = useToastStore()


const featured       = ref([])
const popular        = ref([])
const loadingFeatured = ref(true)
const contact        = ref({ name:'', contact:'', message:'' })

const stats = [
  { val:'8+',   label:'Product Varieties' },
  { val:'100%', label:'Natural & Pure'    },
  { val:'500+', label:'Happy Customers'   },
]
const features = [
  { icon:'🌿', text:'No artificial additives, preservatives or chemical bleaching agents.' },
  { icon:'🏡', text:'Family-run production house with a decade of traditional jaggery-making.' },
  { icon:'🌾', text:'Directly sourced from trusted local farmers — supporting fair trade.' },
  { icon:'📦', text:'Hygienically packed and delivered fresh to your doorstep across India.' },
]
const aboutCards = [
  { icon:'🌅', title:'Farm to Table',   text:'Freshly harvested sugarcane processed within 24 hours.' },
  { icon:'🔥', title:'Open-Pan Cooking',text:'Traditional open-pan method for authentic caramelized richness.' },
  { icon:'🤲', title:'Handcrafted',     text:'Every batch shaped and cooled by hand.' },
]
const whyUs = [
  { icon:'🧪', title:'Lab-Tested Purity',     desc:'Every batch undergoes quality checks for zero adulteration.' },
  { icon:'🚚', title:'Fast Doorstep Delivery', desc:'Ships across India in eco-friendly packaging, 3–5 business days.' },
  { icon:'💰', title:'Farmer-Fair Pricing',    desc:'No middlemen — fair prices for farmers and customers alike.' },
  { icon:'🌱', title:'Sustainably Produced',   desc:'Zero synthetic pesticides. Waste composted back to fields.' },
  { icon:'🏆', title:'Bulk & Wholesale',       desc:'Special pricing for restaurants, shops, and large households.' },
  { icon:'💬', title:'Responsive Support',     desc:'Our team responds within hours. Real people who care.' },
]
const contactItems = computed(() => [
  { icon:'📍', label:'Address',       val: site.get('contact_address') },
  { icon:'📞', label:'Phone',         val: site.get('contact_phone')   },
  { icon:'✉️', label:'Email',         val: site.get('contact_email')   },
  { icon:'🕐', label:'Working Hours', val: site.get('working_hours')   },
].filter(c => c.val))

const parsedBranches = computed(() => {
  const raw = site.get('branches_info')
  if (!raw) return []
  return raw.split('\n\n').map(part => {
    const lines = part.trim().split('\n')
    return {
      title: lines[0] || '',
      details: lines.slice(1).join('\n')
    }
  }).filter(b => b.title)
})

onMounted(async () => {
  try {
    const [f, p] = await Promise.all([
      productsApi.list({ featured: true, per_page: 4 }),
      productsApi.list({ per_page: 5 }),
    ])
    featured.value = f.data.products
    popular.value  = p.data.products.slice(0, 4)
  } catch { /* silent */ } finally {
    loadingFeatured.value = false
  }
})

function scrollTo(id) {
  document.getElementById(id)?.scrollIntoView({ behavior:'smooth' })
}

const testimonials = computed(() => [
  {
    name: site.get('testimonial_1_name') || 'Meera K.',
    role: site.get('testimonial_1_role') || 'Verified Buyer • Mumbai',
    text: site.get('testimonial_1_text') || 'KhagRaj has completely replaced white sugar in our kitchen. The quality of jaggery blocks is incredible, and you can smell the fresh sugarcane juice aroma the moment you open the box!',
    photo: site.get('testimonial_1_photo') || ''
  },
  {
    name: site.get('testimonial_2_name') || 'Rajesh S.',
    role: site.get('testimonial_2_role') || 'Sweet Shop Owner • Delhi',
    text: site.get('testimonial_2_text') || 'We run a high-end sweet shop and sourcing pure Palm Jaggery has always been a pain. Since finding KhagRaj, our customers have noticed a dramatic increase in product consistency and natural flavor!',
    photo: site.get('testimonial_2_photo') || ''
  },
  {
    name: site.get('testimonial_3_name') || 'Anjali P.',
    role: site.get('testimonial_3_role') || 'Fitness Blogger • Pune',
    text: site.get('testimonial_3_text') || 'The Ginger Jaggery powder is a lifesaver for winter. I dissolve it in my chai every evening. The taste is authentic and you can feel the warmth of ginger immediately. Excellent product.',
    photo: site.get('testimonial_3_photo') || ''
  }
])

function getInitials(name) {
  if (!name) return 'U'
  return name.split(' ').map(n => n[0]).filter(Boolean).join('').substring(0, 2).toUpperCase()
}

async function sendContact() {
  if (!contact.value.name || !contact.value.message) { toast.error('Please fill name and message'); return }
  try {
    await contactApi.submit(contact.value)
    toast.success("Message sent! We'll get back to you soon.")
    contact.value = { name:'', contact:'', message:'' }
  } catch (err) {
    toast.error(err.response?.data?.error || 'Failed to send message')
  }
}
</script>
