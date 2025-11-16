<template>
  <h1 class="vertical-title">中国传统色卡</h1>
  <div class="container">
    <div class="filter-container">
      <!-- 固定顺序的标签 -->
      <span
          v-for="tag in tagOrder"
          :key="tag"
          class="tag"
          :style="{
          backgroundColor: selectedTags.includes(tag) ? tagColors[tag] : '#f0f0f0',
          color: isTagAvailable(tag) ? '#333' : '#aaa',
        }"
          :class="{ disabled: !isTagAvailable(tag) }"
          @mouseover="handleTagHover(tag, $event)"
          @mouseout="handleTagOut(tag, $event)"
          @click="toggleTag(tag)"
      >
        {{ tag }}
      </span>
      <!-- 重置按钮 -->
      <span class="reset-btn" @click="resetTags" title="重置筛选">🔄</span>
    </div>
    <div class="grid-container">
      <ColorCard
          v-for="color in filteredColors"
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
import {computed, provide, ref} from 'vue'
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

const selectedTags = ref([])

const toggleTag = (tag) => {
  const index = selectedTags.value.indexOf(tag)
  if (index === -1) {
    selectedTags.value.push(tag)
  } else {
    selectedTags.value.splice(index, 1)
  }
}

// 过滤后的颜色列表
const filteredColors = computed(() => {
  if (!selectedTags.value.length) return colors.value
  return colors.value.filter(color =>
      selectedTags.value.every(tag => color.tags?.includes(tag))
  )
})

const tagOrder = ['红','橘','黄','绿','青','蓝','紫','粉','白','灰','黑','棕']

// 标签可用性判断
const isTagAvailable = (tag) => {
  return filteredColors.value.some(color => color.tags?.includes(tag))
}

// 鼠标悬停效果处理
const handleTagHover = (tag, event) => {
  if (!selectedTags.value.includes(tag) && isTagAvailable(tag)) {
    event.target.style.backgroundColor = `${tagColors[tag]}CC`  // 添加透明度
  }
}

const handleTagOut = (tag, event) => {
  if (!selectedTags.value.includes(tag)) {
    event.target.style.backgroundColor = '#f0f0f0'
  }
}

// 重置逻辑
const resetTags = () => {
  selectedTags.value = []
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

.filter-container {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 2rem;
  padding: 0.8rem 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.tag {
  padding: 0.4rem 1rem;
  border-radius: 20px;
  border: 1px solid #e0e0e0;
  font-size: 0.9em;
  cursor: pointer;
  transition:
      background-color 0.2s ease,
      transform 0.1s ease;
}

.tag:not(.disabled):hover {
  transform: translateY(-1px);
}

.tag.disabled {
  cursor: not-allowed;
  pointer-events: none;
}

.reset-btn {
  font-size: 1.4em;
  padding: 0.1em 0.3em;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  line-height: 1;
  border-radius: 8px;
  display: inline-block;
  transform-origin: center;
  margin-left: auto;
}

.reset-btn:hover {
  transform: rotate(-180deg) scale(1.2);
}

.reset-btn:active {
  transform: rotate(180deg) scale(0.9);
  transition-duration: 0.3s;
}

</style>
