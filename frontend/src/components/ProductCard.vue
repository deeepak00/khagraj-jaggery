<template>
  <div class="product-card" @click="showModal = true" style="cursor:pointer">
    <div class="product-img">
      <img v-if="product.image_url" :src="product.image_url" :alt="product.name" loading="lazy" />
      <div v-else class="fallback">🍯</div>
      <span v-if="product.badge" class="product-badge" :class="product.badge.toLowerCase()">
        {{ product.badge }}
      </span>
      <span v-if="product.featured" class="product-badge" style="top:auto;bottom:12px;right:12px;background:var(--gold);color:var(--brown)">
        ⭐ Featured
      </span>
    </div>

    <div class="product-info">
      <div class="product-name">{{ product.name }}</div>
      <div class="product-desc">{{ product.description }}</div>

      <div class="product-footer">
        <div>
          <div class="product-price">
            ₹{{ product.price }}
            <small> / {{ product.unit }}</small>
          </div>
          <div v-if="product.stock <= 10 && product.stock > 0" style="font-size:.72rem;color:var(--red);margin-top:2px">
            Only {{ product.stock }} left!
          </div>
        </div>

        <!-- Out of stock -->
        <span v-if="product.stock === 0" style="background:rgba(192,57,43,.1);color:var(--red);border:1px solid rgba(192,57,43,.25);font-size:.75rem;padding:5px 12px;border-radius:50px">
          Out of Stock
        </span>

        <!-- Qty control (in cart) -->
        <div v-else-if="cartItem" class="qty-control">
          <button class="qty-btn" @click.stop="cart.decrease(product.id)">−</button>
          <span class="qty-num">{{ cartItem.qty }}</span>
          <button class="qty-btn" @click.stop="cart.increase(product.id)">+</button>
        </div>

        <!-- Add button -->
        <button v-else class="btn btn-dark btn-icon" @click.stop="cart.add(product)" title="Add to cart">
          +
        </button>
      </div>
    </div>

    <!-- Product Detail Modal (Carousel + Specs) -->
    <teleport to="body">
      <div v-if="showModal" class="modal-overlay" @click.self="showModal = false" style="z-index:999999">
        <div class="modal" style="max-width:780px;padding:0;overflow:hidden;border-radius:24px">
          <!-- Close button -->
          <button @click="showModal = false" 
                  style="position:absolute;top:20px;right:20px;z-index:100;width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.9);border:1px solid rgba(0,0,0,0.1);display:flex;align-items:center;justify-content:center;font-size:1.4rem;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,0.08);line-height:1">
            ×
          </button>

          <!-- Split Layout -->
          <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(320px, 1fr));width:100%;min-height:480px">
            <!-- Left: Carousel -->
            <div style="position:relative;background:var(--cream2);display:flex;align-items:center;justify-content:center;overflow:hidden;min-height:360px">
              <img :src="images[currentImgIdx]" :alt="product.name" 
                   style="width:100%;height:100%;object-fit:cover;min-height:360px" />

              <!-- Left Arrow -->
              <button v-if="images.length > 1" @click.stop="prevImg"
                      style="position:absolute;left:16px;top:50%;transform:translateY(-50%);width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.85);border:none;font-size:1rem;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,0.15)">
                ‹
              </button>
              
              <!-- Right Arrow -->
              <button v-if="images.length > 1" @click.stop="nextImg"
                      style="position:absolute;right:16px;top:50%;transform:translateY(-50%);width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.85);border:none;font-size:1rem;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,0.15)">
                ›
              </button>

              <!-- Dots indicators -->
              <div v-if="images.length > 1" 
                   style="position:absolute;bottom:16px;left:50%;transform:translateX(-50%);display:flex;gap:8px">
                <span v-for="(img, idx) in images" :key="idx" @click.stop="currentImgIdx = idx"
                      :style="{
                        width: '8px',
                        height: '8px',
                        borderRadius: '50%',
                        background: currentImgIdx === idx ? 'var(--amber)' : 'rgba(255,255,255,0.6)',
                        cursor: 'pointer',
                        transition: 'all 0.2s'
                      }">
                </span>
              </div>
            </div>

            <!-- Right: Product Details -->
            <div style="padding:40px;display:flex;flex-direction:column;justify-content:space-between;background:var(--white)">
              <div>
                <!-- Category / Badge -->
                <div style="display:flex;gap:8px;margin-bottom:12px;align-items:center">
                  <span v-if="product.category" 
                        style="font-size:0.72rem;text-transform:uppercase;font-weight:700;color:var(--amber);letter-spacing:0.05em">
                    {{ product.category }}
                  </span>
                  <span v-if="product.badge" 
                        style="font-size:0.68rem;background:var(--amber-lt);color:var(--brown);padding:2px 8px;border-radius:50px;font-weight:600">
                    {{ product.badge }}
                  </span>
                </div>

                <!-- Name -->
                <h3 style="font-family:'Playfair Display',serif;font-size:1.8rem;color:var(--brown);margin:0 0 16px;font-weight:700;line-height:1.2">
                  {{ product.name }}
                </h3>

                <!-- Price -->
                <div style="font-size:1.4rem;font-weight:700;color:var(--amber);margin-bottom:24px">
                  ₹{{ product.price }}
                  <span style="font-size:0.9rem;color:var(--text-lt);font-weight:500">/ {{ product.unit }}</span>
                </div>

                <!-- Description -->
                <p style="font-family:'Lora',serif;font-size:0.95rem;color:var(--text-md);line-height:1.6;margin:0 0 24px">
                  {{ product.description }}
                </p>
              </div>

              <div>
                <!-- Stock and Cart Actions -->
                <div style="display:flex;align-items:center;justify-content:space-between;padding-top:20px;border-top:1px solid rgba(0,0,0,0.06)">
                  <!-- Stock Indicator -->
                  <div>
                    <span v-if="product.stock === 0" style="color:var(--red);font-size:0.85rem;font-weight:600">Out of Stock</span>
                    <span v-else-if="product.stock <= 10" style="color:var(--red);font-size:0.85rem;font-weight:600">Only {{ product.stock }} left!</span>
                    <span v-else style="color:var(--green);font-size:0.85rem;font-weight:600">In Stock</span>
                  </div>

                  <!-- Cart Controller -->
                  <div v-if="product.stock > 0">
                    <div v-if="cartItem" class="qty-control" style="background:var(--cream2);padding:6px 12px;border-radius:50px">
                      <button class="qty-btn" @click.stop="cart.decrease(product.id)">−</button>
                      <span class="qty-num" style="font-weight:700;min-width:20px;text-align:center">{{ cartItem.qty }}</span>
                      <button class="qty-btn" @click.stop="cart.increase(product.id)">+</button>
                    </div>
                    <button v-else class="btn btn-primary" @click.stop="cart.add(product)" style="border-radius:50px;padding:10px 24px">
                      Add to Cart 🛒
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCartStore } from '@/stores/cart'

const props          = defineProps({ product: { type: Object, required: true } })
const cart           = useCartStore()
const cartItem       = computed(() => cart.getItem(props.product.id))

const showModal      = ref(false)
const currentImgIdx  = ref(0)

const images = computed(() => {
  const list = props.product.image_urls || []
  if (list.length === 0 && props.product.image_url) {
    return [props.product.image_url]
  }
  return list.length > 0 ? list : ['/uploads/default_product.png']
})

function prevImg() {
  if (images.value.length <= 1) return
  currentImgIdx.value = (currentImgIdx.value - 1 + images.value.length) % images.value.length
}

function nextImg() {
  if (images.value.length <= 1) return
  currentImgIdx.value = (currentImgIdx.value + 1) % images.value.length
}
</script>
