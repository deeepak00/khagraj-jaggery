<template>
  <div>
    <div style="margin-bottom:28px">
      <h2 style="font-size:1.9rem;color:var(--brown);margin-bottom:4px">Orders 📦</h2>
      <p style="font-size:.9rem;color:var(--text-lt)">View and manage all customer orders. Update status to trigger email notifications.</p>
    </div>

    <!-- Filters -->
    <div style="display:flex;gap:12px;align-items:center;margin-bottom:20px;flex-wrap:wrap">
      <input class="form-control" v-model="search" placeholder="Search by name, phone, order #..." style="max-width:280px" @input="debouncedLoad"/>
      <div class="filter-tabs" style="margin-bottom:0;justify-content:flex-start">
        <button v-for="s in statusFilters" :key="s"
          class="filter-tab" :class="{active:statusFilter===s}"
          @click="statusFilter=s;load()" style="padding:7px 16px;font-size:.78rem">
          {{ s }}
        </button>
      </div>
    </div>

    <div class="card" style="overflow:hidden">
      <div v-if="loading" class="loader"><div class="spinner"></div></div>
      <div class="table-wrap" v-else>
        <table class="data-table">
          <thead>
            <tr><th>Order #</th><th>Customer</th><th>Date</th><th>Items</th><th>Total</th><th>Status</th><th>Action</th></tr>
          </thead>
          <tbody>
            <tr v-if="!orders.length">
              <td colspan="7" style="text-align:center;padding:40px;color:var(--text-lt)">No orders found.</td>
            </tr>
            <tr v-for="o in orders" :key="o.id">
              <td><strong style="color:var(--amber);font-size:.82rem">{{ o.order_number }}</strong></td>
              <td>
                <div style="font-weight:500;color:var(--brown)">{{ o.customer_name }}</div>
                <div style="font-size:.75rem;color:var(--text-lt)">{{ o.phone }}</div>
              </td>
              <td style="font-size:.82rem">{{ fmtDate(o.created_at) }}</td>
              <td style="font-size:.82rem;color:var(--text-md)">{{ o.items.length }} item(s)</td>
              <td><strong>₹{{ o.total?.toFixed(0) }}</strong></td>
              <td><span class="badge" :class="`badge-${o.status}`">{{ o.status }}</span></td>
              <td><button class="btn btn-primary btn-sm" @click="openDetail(o)">View & Update</button></td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" style="padding:16px 20px;border-top:1px solid rgba(200,136,42,.1);display:flex;gap:8px;justify-content:flex-end;align-items:center">
        <button class="btn btn-ghost btn-sm" :disabled="page===1" @click="page--;load()">← Prev</button>
        <span style="font-size:.85rem;color:var(--text-md)">{{ page }} / {{ totalPages }}</span>
        <button class="btn btn-ghost btn-sm" :disabled="page===totalPages" @click="page++;load()">Next →</button>
      </div>
    </div>

    <!-- Order Detail Modal -->
    <teleport to="body">
      <div v-if="selected" class="modal-overlay" @click.self="selected=null">
        <div class="modal" style="max-width:640px">
          <h3 class="modal-title">Order #{{ selected.order_number }}</h3>
          <p class="modal-sub">
            {{ fmtDate(selected.created_at) }} — 
            <span class="badge" :class="`badge-${selected.status}`">{{ selected.status }}</span>
            <span v-if="selected.expected_delivery_date" style="margin-left:12px;color:var(--amber);font-weight:600">
              🚚 Expected: {{ selected.expected_delivery_date }}
            </span>
          </p>

          <!-- Customer -->
          <div class="form-section-title">Customer</div>
          <div style="background:var(--cream2);border-radius:10px;padding:14px 16px;font-size:.9rem;color:var(--text-md)">
            👤 <strong>{{ selected.customer_name }}</strong> &nbsp;|&nbsp;
            📞 {{ selected.phone }}
            <template v-if="selected.email">&nbsp;|&nbsp; ✉️ {{ selected.email }}</template>
          </div>

          <!-- Address -->
          <div class="form-section-title">Delivery Address</div>
          <p style="font-size:.9rem;color:var(--text-md)">{{ selected.address }}, {{ selected.city }}, {{ selected.state }} – {{ selected.pincode }}</p>
          <p v-if="selected.notes" style="font-size:.85rem;color:var(--text-lt);font-style:italic;margin-top:6px">Note: {{ selected.notes }}</p>

          <!-- Items -->
          <div class="form-section-title">Items Ordered</div>
          <div v-for="item in selected.items" :key="item.id"
               style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(200,136,42,.1);font-size:.88rem;color:var(--text-md)">
            <span>{{ item.name }} × {{ item.qty }}</span>
            <span>₹{{ (item.price * item.qty).toFixed(0) }}</span>
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

          <!-- Status Update -->
          <div class="form-section-title">Update Status & Expected Delivery</div>
          <div v-if="selected.email" style="background:rgba(58,92,42,.08);border:1px solid rgba(58,92,42,.2);border-radius:10px;padding:10px 14px;margin-bottom:14px;font-size:.82rem;color:var(--green)">
            ✉️ Customer will receive an email notification when status changes.
          </div>
          <div v-else style="background:rgba(200,136,42,.08);border:1px solid rgba(200,136,42,.2);border-radius:10px;padding:10px 14px;margin-bottom:14px;font-size:.82rem;color:var(--amber-dk)">
            ⚠️ No email address — notification will not be sent.
          </div>
          
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px">
            <div class="form-group" style="margin-bottom:0">
              <label class="form-label">New Status</label>
              <select class="form-control" v-model="newStatus">
                <option v-for="s in statuses" :key="s" :value="s">{{ s }}</option>
              </select>
            </div>
            <div class="form-group" style="margin-bottom:0">
              <label class="form-label">Expected Delivery</label>
              <input class="form-control" v-model="expectedDeliveryDate" placeholder="e.g. 20-Aug-2026 or 3-5 days" />
            </div>
          </div>
          
          <div class="form-group">
            <label class="form-label">Note (optional)</label>
            <input class="form-control" v-model="statusNote" placeholder="e.g. Dispatched via BlueDart — tracking #XYZ" />
          </div>
          
          <button class="btn btn-primary w-full" :disabled="updating"
            style="justify-content:center;border-radius:12px;margin-bottom:16px" @click="updateStatus">
            {{ updating ? 'Updating...' : 'Save Changes' }}
          </button>

          <!-- History Timeline (Same as user timeline) -->
          <div v-if="selected.history?.length" style="margin-top:4px">
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
import { ref } from 'vue'
import { useToastStore } from '@/stores/toast'
import { adminApi, ordersApi } from '@/api'

const toast                = useToastStore()
const orders               = ref([])
const loading              = ref(true)
const page                 = ref(1)
const totalPages           = ref(1)
const search               = ref('')
const statusFilter         = ref('all')
const selected             = ref(null)
const newStatus            = ref('')
const statusNote           = ref('')
const expectedDeliveryDate = ref('')
const updating             = ref(false)
let   searchTimer          = null

const statuses       = ['pending','confirmed','processing','shipped','delivered','cancelled']
const statusFilters  = ['all', ...statuses]

const fmtDate = d => d ? new Date(d).toLocaleDateString('en-IN',{day:'2-digit',month:'short',year:'numeric'}) : '—'

async function load() {
  loading.value = true
  try {
    const { data } = await adminApi.listOrders({ page:page.value, status:statusFilter.value, q:search.value })
    orders.value     = data.orders
    totalPages.value = data.pages
  } catch { /* silent */ } finally { loading.value = false }
}

function debouncedLoad() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(load, 350)
}

async function openDetail(o) {
  try {
    // Fetch fresh copy from get_order endpoint which has full history
    const { data } = await ordersApi.get(o.order_number)
    selected.value = data
    expectedDeliveryDate.value = data.expected_delivery_date || ''
  } catch { 
    selected.value = o 
    expectedDeliveryDate.value = o.expected_delivery_date || ''
  }
  newStatus.value  = selected.value.status
  statusNote.value = ''
}

async function updateStatus() {
  if (!selected.value) return
  updating.value = true
  try {
    const { data } = await adminApi.updateOrderStatus(selected.value.id, { 
      status: newStatus.value, 
      note: statusNote.value,
      expected_delivery_date: expectedDeliveryDate.value
    })
    // Refresh list item
    const i = orders.value.findIndex(o => o.id === data.id)
    if (i > -1) orders.value[i] = data
    selected.value = data
    newStatus.value  = data.status
    statusNote.value = ''
    expectedDeliveryDate.value = data.expected_delivery_date || ''
    toast.success('Changes saved successfully')
  } catch (e) { toast.error(e.response?.data?.error || 'Update failed') }
  finally { updating.value = false }
}

load()
</script>
