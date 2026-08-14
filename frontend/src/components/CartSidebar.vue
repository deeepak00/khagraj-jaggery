<template>
  <teleport to="body">
    <transition name="fade">
      <div v-if="open" class="cart-overlay" @click="open = false" />
    </transition>
    <transition name="slide-cart">
      <div v-if="open" class="cart-sidebar">
        <!-- Header -->
        <div style="padding:24px 24px 18px;border-bottom:1px solid rgba(200,136,42,.15);display:flex;align-items:center;justify-content:space-between">
          <h3 style="font-size:1.3rem;color:var(--brown)">🛒 Your Cart</h3>
          <button class="btn btn-ghost btn-icon" style="border-radius:50%" @click="open=false">✕</button>
        </div>

        <!-- Items -->
        <div style="flex:1;overflow-y:auto;padding:16px 24px">
          <div v-if="!cart.items.length" style="text-align:center;padding:60px 20px;color:var(--text-lt)">
            <div style="font-size:4rem;margin-bottom:16px">🏺</div>
            <p style="font-family:'Lora',serif;font-style:italic">Your cart is empty.<br>Add some sweet goodness!</p>
          </div>

          <div v-for="item in cart.items" :key="item.id"
               style="display:flex;gap:12px;padding:14px 0;border-bottom:1px solid rgba(200,136,42,.1);align-items:center">
            <div style="width:52px;height:52px;border-radius:10px;overflow:hidden;background:var(--cream2);flex-shrink:0">
              <img v-if="item.image_url" :src="item.image_url" :alt="item.name" style="width:100%;height:100%;object-fit:cover"/>
              <div v-else style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:1.6rem">🍯</div>
            </div>
            <div style="flex:1;min-width:0">
              <div style="font-family:'Playfair Display',serif;font-size:.92rem;color:var(--brown);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{{ item.name }}</div>
              <div style="font-size:.82rem;color:var(--amber);font-weight:500;margin-top:2px">₹{{ (item.price * item.qty).toFixed(0) }}</div>
            </div>
            <div style="display:flex;align-items:center;gap:6px;flex-shrink:0">
              <button class="qty-btn" @click="cart.decrease(item.id)">−</button>
              <span class="qty-num">{{ item.qty }}</span>
              <button class="qty-btn" @click="cart.increase(item.id)">+</button>
              <button class="btn btn-icon" style="background:none;border:none;color:#cc4444;cursor:pointer;font-size:1rem" @click="cart.remove(item.id)">🗑</button>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div style="padding:16px 24px 24px;border-top:1px solid rgba(200,136,42,.15);background:var(--cream2)">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
            <span style="font-size:.9rem;color:var(--text-md)">Total Amount</span>
            <span style="font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:700;color:var(--amber)">₹{{ cart.total.toFixed(0) }}</span>
          </div>
          <router-link to="/checkout" @click="open=false">
            <button class="btn btn-primary w-full" :disabled="!cart.items.length" style="border-radius:12px;justify-content:center">
              Proceed to Checkout →
            </button>
          </router-link>
          <router-link to="/shop" @click="open=false">
            <button class="btn btn-ghost w-full mt-sm" style="border-radius:12px;justify-content:center;font-size:.85rem">
              Continue Shopping
            </button>
          </router-link>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { inject } from 'vue'
import { useCartStore } from '@/stores/cart'

const cart = useCartStore()
const open = inject('cartOpen')
</script>

<style scoped>
.slide-cart-enter-active, .slide-cart-leave-active { transition: transform .3s cubic-bezier(.16,1,.3,1); }
.slide-cart-enter-from, .slide-cart-leave-to { transform: translateX(100%); }
.fade-enter-active, .fade-leave-active { transition: opacity .2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
