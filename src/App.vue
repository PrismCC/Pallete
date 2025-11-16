<template>
  <div class="container">
    <h1>中国传统色卡</h1>
    <div class="grid-container">
      <ColorCard
          v-for="color in colors"
          :key="color.name"
          :color="color"
          @click="showColorDetail"
      />
    </div>
    <ToastMessage :toasts="toasts" />
  </div>
  <transition name="modal">
    <ColorDetail
        v-if="selectedColor"
        :color="selectedColor"
        @close="selectedColor = null"
        @toast="addToast"
    />
  </transition>
</template>

<script setup>
import {provide, ref} from 'vue'
import ColorCard from './components/ColorCard.vue'
import ColorDetail from './components/ColorDetail.vue'
import ToastMessage from './components/ToastMessage.vue'

const colors = ref([])
const selectedColor = ref(null)
const showColorDetail = (color) => {
  selectedColor.value = color
}

// tag 颜色映射
const tagColors = {
  '红': '#FFC1C180',
  '橘': '#FFE0C180',
  '黄': '#FEFFC180',
  '绿': '#E4FFC180',
  '青': '#C1FFF480',
  '蓝': '#C1DCFF80',
  '紫': '#D6C1FF80',
  '粉': '#FFC1ED80',
  '白': '#FFFFFF80',
  '灰': '#DCDCDC80',
  '黑': '#AFAFAF80',
  '棕': '#C5B08F80'
}
provide('tagColors', tagColors)

fetch('/colors.json')
    .then(response => response.json())
    .then(data => {
      colors.value = Object.values(data)
    })

const toasts = ref([])
const addToast = (message) => {
  const id = Date.now() + Math.random().toString(36).slice(2)
  toasts.value.unshift({ id, message })
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }, 5000)
}
</script>

<style>
:root {
  --card-radius: 12px;
}

body {
  background: #f5f5f5;
  color: black;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 4rem 2rem;
  padding: 1rem;
}

.modal-enter-active,
.modal-leave-active {
  transition: 0.3s ease-in-out;
  transition-property: opacity, transform;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
