<template>
  <h1 class="vertical-title">中国传统色卡</h1>
  <div class="container">
    <div class="grid-container">
      <ColorCard
          v-for="color in colors"
          :key="color.name"
          :color="color"
          @click="showColorDetail"
      />
    </div>
  </div>
  <ToastMessage :toasts="toasts" />
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

.vertical-title {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 120px;
  background: #000;
  color: white;
  margin: 0;
  padding: 2rem 1.5rem;
  writing-mode: vertical-lr;
  text-orientation: upright;
  font-size: 3em;
  letter-spacing: 0.5em;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.5);
}

.container {
  max-width: calc(1500px - 120px);
  width: 100%;
  padding: 2rem 2rem 2rem 1rem;
  margin: 0 auto;
  transform: translateX(60px);
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
