<template>
  <div>
    <div style="margin-bottom:28px">
      <h2 style="font-size:1.9rem;color:var(--brown);margin-bottom:4px">Customer Messages 💬</h2>
      <p style="font-size:.9rem;color:var(--text-lt)">View and manage inquiries submitted by users through the Contact Us form.</p>
    </div>

    <div v-if="loading" class="loader"><div class="spinner"></div></div>

    <div v-else-if="messages.length === 0" class="card text-center" style="padding:48px 24px">
      <span style="font-size:3rem;display:block;margin-bottom:16px">✉️</span>
      <h4 style="font-size:1.2rem;color:var(--brown);margin-bottom:8px">No Messages Yet</h4>
      <p style="color:var(--text-lt);max-width:400px;margin:0 auto">When users submit the contact form on your website, their inquiries and details will show up here.</p>
    </div>

    <div v-else style="display:grid;gap:20px">
      <div v-for="m in messages" :key="m.id" class="card" :style="{ borderLeft: m.is_read ? '4px solid rgba(45,106,79,0.2)' : '4px solid var(--amber)' }">
        <div class="card-header" style="display:flex;justify-content:space-between;align-items:center;padding:20px 24px">
          <div>
            <h3 style="font-size:1.15rem;color:var(--brown);margin-bottom:2px">{{ m.name }}</h3>
            <span style="font-size:.78rem;color:var(--text-lt)">{{ formatDate(m.created_at) }}</span>
          </div>
          <span :class="['badge', m.is_read ? 'badge-success' : 'badge-warning']" style="padding:4px 10px;border-radius:50px;font-size:.72rem;font-weight:600;text-transform:uppercase;letter-spacing:.05em">
            {{ m.is_read ? 'Read' : 'Unread' }}
          </span>
        </div>
        
        <div class="card-body" style="padding:20px 24px">
          <div style="background:var(--cream2);padding:12px 16px;border-radius:8px;font-size:.9rem;color:var(--brown);margin-bottom:16px;display:flex;align-items:center;gap:8px">
            <span style="font-weight:600">📞 Contact Details:</span>
            <span>{{ m.contact || 'Not provided' }}</span>
          </div>
          <p style="font-family:'Lora',serif;font-size:1rem;color:var(--text-md);line-height:1.6;white-space:pre-wrap">{{ m.message }}</p>
        </div>

        <div class="card-footer" style="padding:16px 24px;border-top:1px solid rgba(200,136,42,.12);display:flex;justify-content:flex-end;gap:12px">
          <button v-if="!m.is_read" class="btn btn-ghost btn-sm" @click="markAsRead(m.id)">✔️ Mark as Read</button>
          <button class="btn btn-outline btn-sm" @click="confirmDelete(m.id)" style="color:var(--red);border-color:rgba(192,57,43,.3)">🗑️ Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { adminApi } from '@/api'
import { useToastStore } from '@/stores/toast'

const toast = useToastStore()
const messages = ref([])
const loading = ref(true)

async function fetchMessages() {
  loading.value = true
  try {
    const { data } = await adminApi.listMessages()
    messages.value = data
  } catch {
    toast.error('Failed to load messages')
  } finally {
    loading.value = false
  }
}

async function markAsRead(id) {
  try {
    await adminApi.markMessageRead(id)
    toast.success('Message marked as read')
    const m = messages.value.find(x => x.id === id)
    if (m) m.is_read = true
  } catch {
    toast.error('Failed to mark message as read')
  }
}

async function confirmDelete(id) {
  if (!confirm('Are you sure you want to delete this message?')) return
  try {
    await adminApi.deleteMessage(id)
    toast.success('Message deleted')
    messages.value = messages.value.filter(x => x.id !== id)
  } catch {
    toast.error('Failed to delete message')
  }
}

function formatDate(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  return d.toLocaleString('en-IN', {
    dateStyle: 'medium',
    timeStyle: 'short'
  })
}

fetchMessages()
</script>

<style scoped>
.badge-success {
  background: rgba(45,106,79,.1);
  color: var(--amber);
}
.badge-warning {
  background: rgba(216,150,20,.1);
  color: var(--gold);
}
</style>
