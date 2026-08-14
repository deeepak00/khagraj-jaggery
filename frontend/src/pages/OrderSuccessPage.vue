<template>
  <section class="order-success">
    <div class="check">✓</div>
    <h1>Thank you for your order!</h1>
    <p>Your order <strong>{{ orderNumber }}</strong> has been placed successfully.</p>
    <p class="sub">We've sent a confirmation to your email. You can track its status from My Orders.</p>
    <div class="actions">
      <router-link to="/my-orders" class="btn primary">View My Orders</router-link>
      <router-link to="/shop" class="btn">Continue Shopping</router-link>
    </div>
  </section>
</template>

<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()
const orderNumber = route.params.orderNumber
</script>

<style scoped>
.order-success {
  max-width: 560px;
  margin: 80px auto;
  text-align: center;
  padding: 0 20px;
  font-family: 'DM Sans', sans-serif;
}
.check {
  width: 72px; height: 72px;
  border-radius: 50%;
  background: #27ae60;
  color: #fff;
  font-size: 2rem;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 24px;
}
h1 { margin-bottom: 12px; color: #2C1810; }
.sub { color: #9B7B5A; margin-bottom: 32px; }
.actions { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
.btn {
  padding: 12px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  border: 1px solid #2C1810;
  color: #2C1810;
}
.btn.primary { background: #2C1810; color: #fff; }
</style>
