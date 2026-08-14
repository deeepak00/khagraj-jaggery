<template>
  <teleport to="body">
    <div class="toast-stack">
      <transition-group name="toast-fade" tag="div">
        <div
          v-for="t in toast.toasts"
          :key="t.id"
          class="toast-item"
          :class="t.type"
          @click="toast.remove(t.id)"
        >
          {{ t.message }}
        </div>
      </transition-group>
    </div>
  </teleport>
</template>

<script setup>
import { useToastStore } from '@/stores/toast'
const toast = useToastStore()
</script>

<style scoped>
.toast-stack {
  position: fixed;
  top: 16px;
  right: 16px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.toast-item {
  min-width: 220px;
  max-width: 340px;
  padding: 12px 16px;
  border-radius: 8px;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  font-size: .9rem;
  box-shadow: 0 4px 16px rgba(0,0,0,.18);
  cursor: pointer;
  background: #2C1810;
}
.toast-item.success { background: #27ae60; }
.toast-item.error   { background: #c0392b; }
.toast-item.info    { background: #2980b9; }
.toast-fade-enter-active, .toast-fade-leave-active { transition: all .2s ease; }
.toast-fade-enter-from, .toast-fade-leave-to { opacity: 0; transform: translateX(20px); }
</style>
