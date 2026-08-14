<template>
  <div style="min-height:100vh;padding:108px 0 60px;background:var(--cream2)">
    <div class="container" style="max-width:900px">
      <h2 style="font-size:2rem;color:var(--brown);margin-bottom:6px">My Orders</h2>
      <p style="font-size:.95rem;color:var(--text-lt);margin-bottom:32px">All your past and current orders in one place.</p>

      <div v-if="loading" class="loader"><div class="spinner"></div></div>

      <div v-else-if="!orders.length" style="text-align:center;padding:80px 20px;color:var(--text-lt)">
        <div style="font-size:4rem;margin-bottom:16px">📦</div>
        <p style="font-family:'Lora',serif">No orders yet.
          <router-link to="/shop" style="color:var(--amber)">Start shopping!</router-link>
        </p>
      </div>

      <div v-else class="card" style="overflow:hidden">
        <div class="table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th>Order #</th><th>Date</th><th>Items</th><th>Total</th><th>Status</th><th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="o in orders" :key="o.id">
                <td><strong style="color:var(--amber)">{{ o.order_number }}</strong></td>
                <td style="font-size:.82rem">{{ fmtDate(o.created_at) }}</td>
                <td style="font-size:.85rem;color:var(--text-md)">
                  {{ o.items.length }} item(s) — {{ o.items.slice(0,2).map(i=>i.name.split(' ')[0]).join(', ') }}{{ o.items.length>2?'…':'' }}
                </td>
                <td><strong>₹{{ o.total?.toFixed(0) }}</strong></td>
                <td><span class="badge" :class="`badge-${o.status}`">{{ o.status }}</span></td>
                <td>
                  <button class="btn btn-ghost btn-sm" @click="openDetail(o)">Details</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Order detail modal -->
    <teleport to="body">
      <div v-if="selected" class="modal-overlay" @click.self="selected=null">
        <div class="modal">
          <h3 class="modal-title">Order #{{ selected.order_number }}</h3>
          <p class="modal-sub">Placed on {{ fmtDate(selected.created_at) }}</p>

          <div v-if="selected.expected_delivery_date" style="margin-bottom:20px;background:rgba(45,106,79,0.06);border:1px solid rgba(45,106,79,0.15);border-radius:12px;padding:12px 16px;">
            <span style="font-size:1.1rem">🚚</span> <strong>Expected Delivery:</strong> {{ selected.expected_delivery_date }}
          </div>

          <div class="form-section-title">Delivery Address</div>
          <p style="font-size:.9rem;color:var(--text-md)">
            {{ selected.address }}, {{ selected.city }}, {{ selected.state }} – {{ selected.pincode }}
          </p>
          <p v-if="selected.notes" style="font-size:.85rem;color:var(--text-lt);font-style:italic;margin-top:6px">Note: {{ selected.notes }}</p>

          <div class="form-section-title">Items</div>
          <div v-for="item in selected.items" :key="item.id"
               style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(200,136,42,.1);font-size:.88rem;color:var(--text-md)">
            <span>{{ item.name }} × {{ item.qty }}</span>
            <span>₹{{ (item.price*item.qty).toFixed(0) }}</span>
          </div>
          <div style="margin-top:14px;border-top:1.5px solid rgba(200,136,42,.15);padding-top:10px;font-size:.85rem;color:var(--text-md);display:grid;gap:6px">
            <div style="display:flex;justify-content:space-between">
              <span>Subtotal</span><span>₹{{ (selected.subtotal || selected.total)?.toFixed(0) }}</span>
            </div>
            <div v-if="selected.discount_amount > 0" style="display:flex;justify-content:space-between;color:var(--red)">
              <span>Discount</span><span>- ₹{{ selected.discount_amount.toFixed(0) }}</span>
            </div>
            <div style="display:flex;justify-content:space-between">
              <span>Shipping/Delivery</span>
              <span>{{ selected.shipping_fee === 0 ? 'FREE' : `₹${selected.shipping_fee?.toFixed(0)}` }}</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-weight:700;font-size:1.05rem;color:var(--brown);border-top:1px dashed rgba(200,136,42,.15);padding-top:6px;margin-top:2px">
              <span>Grand Total</span><span>₹{{ selected.total?.toFixed(0) }}</span>
            </div>
          </div>

          <!-- Timeline -->
          <div v-if="selected.history?.length" style="margin-top:20px">
            <div class="form-section-title">Status History Timeline</div>
            <div style="position:relative;padding-left:20px;margin-top:10px;display:flex;flex-direction:column;gap:16px">
              <!-- timeline vertical bar -->
              <div style="position:absolute;left:4px;top:8px;bottom:8px;width:2px;background:rgba(45,106,79,0.15)"></div>
              
              <div v-for="h in selected.history" :key="h.id" style="position:relative;display:flex;flex-direction:column;align-items:flex-start">
                <!-- timeline dot -->
                <div style="position:absolute;left:-20px;top:4px;width:10px;height:10px;border-radius:50%;background:var(--amber);border:2px solid var(--white);box-shadow:0 0 0 3px rgba(45,106,79,0.1)"></div>
                
                <div style="display:flex;align-items:center;gap:10px;font-size:.85rem;font-weight:600">
                  <span class="badge" :class="`badge-${h.status}`" style="padding:2px 8px;font-size:0.72rem">{{ h.status }}</span>
                  <span style="color:var(--text-lt);font-size:0.75rem;font-weight:400">{{ fmtDate(h.created_at) }}</span>
                </div>
                <div v-if="h.note" style="font-size:0.8rem;color:var(--text-lt);margin-top:4px;font-style:italic">
                  Note: {{ h.note }}
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-ghost btn-sm" @click="selected=null">Close</button>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ordersApi } from '@/api'

const orders   = ref([])
const loading  = ref(true)
const selected = ref(null)

const fmtDate = (d) => d ? new Date(d).toLocaleDateString('en-IN', { day:'2-digit', month:'short', year:'numeric' }) : '—'

onMounted(async () => {
  try {
    const { data } = await ordersApi.mine()
    orders.value = data.orders
  } catch { /* silent */ } finally { loading.value = false }
})

async function openDetail(o) {
  try {
    const { data } = await ordersApi.get(o.order_number)
    selected.value = data
  } catch {
    selected.value = o
  }
}
</script>
