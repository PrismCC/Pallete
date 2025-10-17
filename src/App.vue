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
  </div>
  <ColorDetail
      v-if="selectedColor"
      :color="selectedColor"
      @close="selectedColor = null"
  />
</template>

<script setup>
import { ref } from 'vue'
import ColorCard from './components/ColorCard.vue'
import ColorDetail from './components/ColorDetail.vue'

const colors = ref([])
const selectedColor = ref(null)
const showColorDetail = (color) => {
  selectedColor.value = color
}

fetch('/colors.json')
    .then(response => response.json())
    .then(data => {
      colors.value = Object.values(data)
    })
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
</style>
