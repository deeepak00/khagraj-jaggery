<template>
  <div>
    <div class="admin-header">
      <h2>Good day, {{ auth.user?.name?.split(' ')[0] }} 👋</h2>
      <p>Here's what's happening at KhagRaj today.</p>
    </div>

    <div v-if="loading" class="loader"><div class="spinner"></div></div>

    <template v-else>
      <!-- Stat cards -->
      <div class="stats-grid">
        <div class="stat-card" v-for="s in statCards" :key="s.label">
          <div class="stat-card-icon">{{ s.icon }}</div>
          <div class="stat-card-val" :class="s.color">{{ s.val }}</div>
          <div class="stat-card-label">{{ s.label }}</div>
        </div>
      </div>

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:24px">
        <!-- Revenue Chart -->
        <div class="card">
          <div class="card-header"><h3>Revenue — Last 7 Days</h3></div>
          <div class="card-body" style="padding-top:12px">
            <div style="display:flex;align-items:flex-end;gap:8px;height:140px">
              <div v-for="d in stats.revenue_chart" :key="d.date"
                   style="flex:1;display:flex;flex-direction:column;align-items:center;gap:4px">
                <div :style="`height:${barHeight(d.revenue)}px;width:100%;background:var(--amber);border-radius:4px 4px 0 0;transition:height .3s;min-height:4px`"></div>
                <div style="font-size:.68rem;color:var(--text-lt);white-space:nowrap">{{ d.date }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Orders by status -->
        <div class="card">
          <div class="card-header"><h3>Orders by Status</h3></div>
          <div class="card-body">
            <div v-for="(count, status) in stats.status_counts" :key="status"
                 style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
              <span class="badge" :class="`badge-${status}`" style="min-width:90px;text-align:center">{{ status }}</span>
              <div style="flex:1;background:var(--cream2);border-radius:4px;height:8px;overflow:hidden">
                <div :style="`width:${statusPct(count)}%;height:100%;background:var(--amber);border-radius:4px`"></div>
              </div>
              <span style="font-size:.85rem;font-weight:600;color:var(--brown);min-width:24px;text-align:right">{{ count }}</span>
            </div>
          </div>
        </div>
      </div>

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px">
        <!-- Popular Products -->
        <div class="card">
          <div class="card-header">
            <h3>⭐ Popular Products</h3>
            <router-link to="/admin/products"><button class="btn btn-ghost btn-sm">Manage →</button></router-link>
          </div>
          <div class="table-wrap">
            <table class="data-table">
              <thead><tr><th>Product</th><th>Orders</th><th>Stock</th></tr></thead>
              <tbody>
                <tr v-for="p in stats.popular_products" :key="p.id">
                  <td>
                    <div style="font-weight:500;color:var(--brown)">{{ p.name }}</div>
                    <div style="font-size:.75rem;color:var(--text-lt)">₹{{ p.price }}/{{ p.unit }}</div>
                  </td>
                  <td><span style="font-weight:600;color:var(--amber)">{{ p.order_count }}</span></td>
                  <td><span :class="p.stock > 20 ? 'badge badge-delivered' : 'badge badge-cancelled'">{{ p.stock }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Recent Orders -->
        <div class="card">
          <div class="card-header">
            <h3>📦 Recent Orders</h3>
            <router-link to="/admin/orders"><button class="btn btn-ghost btn-sm">All Orders →</button></router-link>
          </div>
          <div class="table-wrap">
            <table class="data-table">
              <thead><tr><th>Customer</th><th>Total</th><th>Status</th></tr></thead>
              <tbody>
                <tr v-for="o in stats.recent_orders" :key="o.id">
                  <td>
                    <div style="font-weight:500;color:var(--brown)">{{ o.customer_name }}</div>
                    <div style="font-size:.75rem;color:var(--text-lt)">{{ fmtDate(o.created_at) }}</div>
                  </td>
                  <td><strong>₹{{ o.total?.toFixed(0) }}</strong></td>
                  <td><span class="badge" :class="`badge-${o.status}`">{{ o.status }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { adminApi }     from '@/api'

const auth    = useAuthStore()
const loading = ref(true)
const stats   = ref({ total_orders:0, total_revenue:0, pending_orders:0, delivered_orders:0, total_users:0, total_products:0, status_counts:{}, revenue_chart:[], popular_products:[], recent_orders:[] })

const statCards = computed(() => [
  { icon:'📦', label:'Total Orders',    val: stats.value.total_orders,   color:'amber' },
  { icon:'💰', label:'Total Revenue',   val: `₹${stats.value.total_revenue?.toLocaleString('en-IN')}`, color:'green' },
  { icon:'⏳', label:'Pending Orders',  val: stats.value.pending_orders, color:'' },
  { icon:'🎉', label:'Delivered',       val: stats.value.delivered_orders, color:'green' },
  { icon:'👥', label:'Registered Users',val: stats.value.total_users,    color:'amber' },
  { icon:'🟫', label:'Active Products', val: stats.value.total_products, color:'' },
  { icon:'💵', label:'Avg. Order Value',val: stats.value.total_orders ? `₹${Math.round(stats.value.total_revenue / stats.value.total_orders)}` : '₹0', color:'' },
  { icon:'✅', label:'Delivery Rate',   val: stats.value.total_orders ? `${Math.round(stats.value.delivered_orders/stats.value.total_orders*100)}%` : '0%', color:'green' },
])

const maxRevenue = computed(() => Math.max(...(stats.value.revenue_chart?.map(d=>d.revenue)||[1])))
const barHeight  = (rev) => maxRevenue.value ? Math.max(8, Math.round((rev / maxRevenue.value) * 120)) : 8

const totalOrders  = computed(() => Object.values(stats.value.status_counts || {}).reduce((a,b)=>a+b,0))
const statusPct    = (count) => totalOrders.value ? Math.round(count/totalOrders.value*100) : 0

const fmtDate = d => d ? new Date(d).toLocaleDateString('en-IN',{day:'2-digit',month:'short'}) : '—'

onMounted(async () => {
  try {
    const { data } = await adminApi.stats()
    stats.value = data
  } catch { /* silent */ } finally { loading.value = false }
})
</script>

<style scoped>
.admin-header { margin-bottom: 28px; }
.admin-header h2 { font-size: 1.9rem; color: var(--brown); margin-bottom: 4px; }
.admin-header p  { font-size: .9rem; color: var(--text-lt); }
</style>
