<template>
  <div style="min-height:100vh;padding:108px 0 60px;background:var(--cream2)">
    <div class="container">
      <router-link to="/shop"><button class="btn btn-ghost btn-sm" style="margin-bottom:24px">← Back to Shop</button></router-link>

      <div class="checkout-grid">
        <!-- FORM -->
        <div class="card">
          <div class="card-body">
            <h2 style="font-size:1.8rem;color:var(--brown);margin-bottom:6px">Complete Your Order</h2>
            <p style="font-size:.88rem;color:var(--text-lt);margin-bottom:20px">Fill in your details and we'll get your jaggery delivered fresh.</p>

            <!-- Guest nudge / logged-in banner -->
            <div v-if="!auth.isLoggedIn" style="background:rgba(200,136,42,.1);border:1.5px solid rgba(200,136,42,.3);border-radius:12px;padding:14px 18px;margin-bottom:20px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap">
              <div>
                <div style="font-size:.85rem;font-weight:600;color:var(--amber-dk)">💡 Save time on future orders</div>
                <div style="font-size:.8rem;color:var(--text-lt);margin-top:3px">Login to pre-fill your details and track order history.</div>
              </div>
              <router-link to="/auth?redirect=/checkout"><button class="btn btn-primary btn-sm">Login / Register</button></router-link>
            </div>
            <div v-else style="background:rgba(58,92,42,.08);border:1.5px solid rgba(58,92,42,.2);border-radius:12px;padding:12px 18px;margin-bottom:20px;display:flex;align-items:center;gap:10px">
              <span style="font-size:1.1rem">✅</span>
              <div style="font-size:.85rem;color:var(--green);font-weight:500">Logged in as <strong>{{ auth.user?.name }}</strong> — details pre-filled.</div>
            </div>

            <div class="form-section-title">Personal Details</div>
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Full Name <span style="color:var(--amber)">*</span></label>
                <input class="form-control" :class="{error:err.customer_name}" v-model="form.customer_name" placeholder="Your full name" />
                <span v-if="err.customer_name" class="form-error">{{ err.customer_name }}</span>
              </div>
              <div class="form-group">
                <label class="form-label">Phone <span style="color:var(--amber)">*</span></label>
                <input class="form-control" :class="{error:err.phone}" type="tel" v-model="form.phone" placeholder="+91 9876543210" />
                <span v-if="err.phone" class="form-error">{{ err.phone }}</span>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">Email</label>
              <input class="form-control" type="email" v-model="form.email" placeholder="Optional — for order updates" />
            </div>

            <div class="form-section-title">Delivery Address</div>
            <div class="form-group">
              <label class="form-label">Street Address <span style="color:var(--amber)">*</span></label>
              <input class="form-control" :class="{error:err.address}" v-model="form.address" placeholder="House no., street, locality" />
              <span v-if="err.address" class="form-error">{{ err.address }}</span>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">City <span style="color:var(--amber)">*</span></label>
                <input class="form-control" :class="{error:err.city}" v-model="form.city" placeholder="City" />
                <span v-if="err.city" class="form-error">{{ err.city }}</span>
              </div>
              <div class="form-group">
                <label class="form-label">State <span style="color:var(--amber)">*</span></label>
                <select class="form-control" :class="{error:err.state}" v-model="form.state">
                  <option value="">Select State</option>
                  <option v-for="s in states" :key="s">{{ s }}</option>
                </select>
                <span v-if="err.state" class="form-error">{{ err.state }}</span>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">PIN Code <span style="color:var(--amber)">*</span></label>
              <input class="form-control" :class="{error:err.pincode}" v-model="form.pincode" maxlength="6" placeholder="6-digit PIN" />
              <span v-if="err.pincode" class="form-error">{{ err.pincode }}</span>
            </div>

            <div class="form-section-title">Notes</div>
            <div class="form-group">
              <textarea class="form-control" v-model="form.notes" placeholder="Delivery instructions, preferred time, etc."></textarea>
            </div>

            <div style="background:rgba(200,136,42,.08);border:1.5px dashed rgba(200,136,42,.3);border-radius:12px;padding:14px 18px;margin-top:8px">
              <div style="font-size:.82rem;font-weight:600;color:var(--amber-dk);margin-bottom:4px">💳 Payment — Cash on Delivery</div>
              <div style="font-size:.8rem;color:var(--text-lt);line-height:1.5">Pay when your order arrives. UPI & card payments coming soon!</div>
            </div>
          </div>
        </div>

        <!-- ORDER SUMMARY -->
        <div class="card card-dark" style="position:sticky;top:88px">
          <div class="card-body">
            <h3 style="font-size:1.2rem;color:var(--cream);margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid rgba(200,136,42,.25)">📋 Order Summary</h3>

            <div v-for="item in cart.items" :key="item.id" style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;font-size:.88rem">
              <span style="color:rgba(253,246,227,.75)">{{ item.name }} × {{ item.qty }}</span>
              <span style="color:var(--amber-lt);font-weight:500">₹{{ (item.price*item.qty).toFixed(0) }}</span>
            </div>

            <hr style="border:none;border-top:1px solid rgba(200,136,42,.2);margin:14px 0"/>
            <div style="display:flex;justify-content:space-between;font-size:.88rem;margin-bottom:8px">
              <span style="color:rgba(253,246,227,.7)">Subtotal</span>
              <span style="color:var(--amber-lt)">₹{{ subtotal.toFixed(0) }}</span>
            </div>

            <div v-if="seasonalDiscountPercent > 0" style="display:flex;justify-content:space-between;font-size:.88rem;margin-bottom:8px">
              <span style="color:rgba(253,246,227,.7)">Seasonal Discount ({{ seasonalDiscountPercent }}%)</span>
              <span style="color:var(--amber-lt)">- ₹{{ discountAmount.toFixed(0) }}</span>
            </div>

            <div style="display:flex;justify-content:space-between;font-size:.88rem;margin-bottom:14px">
              <span style="color:rgba(253,246,227,.7)">Delivery</span>
              <span v-if="shippingFee === 0" style="color:var(--green-lt)">FREE</span>
              <span v-else style="color:var(--amber-lt)">₹{{ shippingFee.toFixed(0) }}</span>
            </div>
            <hr style="border:none;border-top:1px solid rgba(200,136,42,.2);margin:14px 0"/>
            <div style="display:flex;justify-content:space-between;align-items:center">
              <span style="font-size:.9rem;color:rgba(253,246,227,.8)">Grand Total</span>
              <span style="font-family:'Playfair Display',serif;font-size:1.7rem;font-weight:700;color:var(--gold)">₹{{ grandTotal.toFixed(0) }}</span>
            </div>

            <div style="background:rgba(255,255,255,.06);border-radius:10px;padding:12px 16px;margin:16px 0;font-size:.8rem;color:rgba(253,246,227,.5);line-height:1.6">
              🚚 Delivery in 3–5 business days<br>📦 Eco-friendly packaging<br>💯 100% pure jaggery
            </div>

            <button class="btn w-full" :disabled="placing || !cart.items.length"
              style="background:var(--gold);color:var(--brown);font-weight:700;border-radius:12px;justify-content:center;font-size:1rem;padding:15px"
              @click="placeOrder">
              {{ placing ? 'Placing Order...' : '✅ Place Order (COD)' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore }  from '@/stores/auth'
import { useCartStore }  from '@/stores/cart'
import { useSiteStore }  from '@/stores/site'
import { useToastStore } from '@/stores/toast'
import { ordersApi }     from '@/api'

const auth   = useAuthStore()
const cart   = useCartStore()
const site   = useSiteStore()
const toast  = useToastStore()
const router = useRouter()

const placing = ref(false)
const err     = ref({})
const form    = ref({ customer_name:'', email:'', phone:'', address:'', city:'', state:'', pincode:'', notes:'' })

const subtotal = computed(() => cart.total)

const seasonalDiscountPercent = computed(() => {
  const val = parseFloat(site.get('seasonal_discount_percent'))
  return isNaN(val) ? 0 : val
})

const discountAmount = computed(() => {
  return subtotal.value * (seasonalDiscountPercent.value / 100)
})

const freeThreshold = computed(() => {
  const val = parseFloat(site.get('shipping_free_threshold'))
  return isNaN(val) ? 500 : val
})

const baseShippingFee = computed(() => {
  const val = parseFloat(site.get('shipping_base_fee'))
  return isNaN(val) ? 50 : val
})

const shippingFee = computed(() => {
  return subtotal.value >= freeThreshold.value ? 0 : baseShippingFee.value
})

const grandTotal = computed(() => {
  return Math.max(0, subtotal.value - discountAmount.value + shippingFee.value)
})

onMounted(() => {
  if (auth.user) {
    form.value.customer_name = auth.user.name  || ''
    form.value.email         = auth.user.email || ''
    form.value.phone         = auth.user.phone || ''
  }
})

function validate() {
  const e = {}
  if (!form.value.customer_name.trim()) e.customer_name = 'Name is required'
  if (!form.value.phone.trim())         e.phone    = 'Phone is required'
  else if (!/^\+?[\d\s\-]{8,15}$/.test(form.value.phone)) e.phone = 'Invalid phone'
  if (!form.value.address.trim())       e.address  = 'Address is required'
  if (!form.value.city.trim())          e.city     = 'City is required'
  if (!form.value.state)                e.state    = 'State is required'
  if (!form.value.pincode.trim())       e.pincode  = 'PIN code required'
  else if (!/^\d{6}$/.test(form.value.pincode)) e.pincode = 'Enter valid 6-digit PIN'
  err.value = e
  return !Object.keys(e).length
}

async function placeOrder() {
  if (!validate()) { toast.error('Please fix the errors above'); return }
  placing.value = true
  try {
    const { data } = await ordersApi.place({
      ...form.value,
      items: cart.items.map(i => ({ id:i.id, name:i.name, qty:i.qty, price:i.price, unit:i.unit })),
      subtotal: subtotal.value,
      discount_amount: discountAmount.value,
      shipping_fee: shippingFee.value,
      total: grandTotal.value,
    })
    cart.clear()
    router.push(`/success/${data.order_number}`)
  } catch (e) {
    toast.error(e.response?.data?.error || 'Failed to place order. Please try again.')
  } finally { placing.value = false }
}

const states = ['Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chhattisgarh','Goa','Gujarat','Haryana','Himachal Pradesh','Jharkhand','Karnataka','Kerala','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand','West Bengal','Delhi','Jammu & Kashmir','Ladakh','Puducherry']
</script>
