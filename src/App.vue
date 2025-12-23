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
          border: selectedTags.includes(tag) ? `1px solid #7f7f7f` : '1px solid #e0e0e0'
        }"
          :class="{ disabled: !isTagAvailable(tag) }"
          @mouseover="handleTagHover(tag, $event)"
          @mouseout="handleTagOut(tag, $event)"
          @click="toggleTag(tag)"
      >
        {{ tag }}
      </span>
      <div class="filter-buttons">
        <span class="reset-btn" @click="handleReset">🔄</span>
        <span
            class="favorite-filter-btn"
            :class="{ active: isFavoritesMode }"
            @click="toggleFavoritesMode"
        >
          {{ isFavoritesMode ? '★' : '☆' }}
        </span>
        <!-- 添加自定义颜色按钮 -->
        <span class="add-color-btn" @click="showAddColorModal = true">➕</span>
      </div>
    </div>
    <div class="grid-container">
      <ColorCard
          v-for="color in filteredColors"
          :key="color.name + (color.custom ? '-custom' : '')"
          :color="color"
          @click="showColorDetail"
      />
    </div>
  </div>
  <ToastMessage :toasts="toasts"/>
  <transition name="modal">
    <ColorDetail
        v-if="selectedColor"
        :color="selectedColor"
        @close="selectedColor = null"
        @toast="addToast"
        @delete="deleteColor"
    />
  </transition>

  <!-- 添加自定义颜色模态框 -->
  <AddCustomColor
      :show="showAddColorModal"
      :tagOrder="tagOrder"
      :tagColors="tagColors"
      @close="showAddColorModal = false"
      @save="addCustomColor"
  />
</template>
<script setup>
import { computed, onMounted, provide, ref } from 'vue'
import ColorCard from './components/ColorCard.vue'
import ColorDetail from './components/ColorDetail.vue'
import ToastMessage from './components/ToastMessage.vue'
import AddCustomColor from './components/AddCustomColor.vue'
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
const LOCAL_STORAGE_CUSTOM_COLORS_KEY = 'customColors'
// 加载数据
onMounted(() => {
  const savedFavorites = localStorage.getItem('favorites')
  if (savedFavorites) favorites.value = JSON.parse(savedFavorites)

  // 加载自定义颜色
  const savedCustomColors = localStorage.getItem(LOCAL_STORAGE_CUSTOM_COLORS_KEY)
  if (savedCustomColors) {
    customColors.value = JSON.parse(savedCustomColors)
  }

  // 从JSON加载标准颜色
  fetch('/colors.json')
      .then(response => response.json())
      .then(data => {
        colors.value = [...Object.values(data), ...customColors.value]
      })
})
const customColors = ref([]) // 存储自定义颜色
const toasts = ref([])
const addToast = (message) => {
  const id = Date.now() + Math.random().toString(36).slice(2)
  toasts.value.unshift({ id, message })
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }, 5000)
}
const selectedTags = ref([])
const favorites = ref([])
const isFavoritesMode = ref(false)
const showAddColorModal = ref(false)
// 添加自定义颜色
const addCustomColor = (color) => {
  // 添加到自定义颜色列表
  customColors.value.push(color)

  // 更新主颜色列表
  colors.value.push(color)

  // 保存到localStorage
  localStorage.setItem(
      LOCAL_STORAGE_CUSTOM_COLORS_KEY,
      JSON.stringify(customColors.value)
  )

  addToast(`"${color.name}"已添加到颜色库`)
}
// 删除自定义颜色
const deleteColor = (color) => {
  // 从自定义颜色列表中移除
  customColors.value = customColors.value.filter(c => c.name !== color.name)

  // 从主颜色列表中移除
  colors.value = colors.value.filter(c => c.name !== color.name)

  // 更新localStorage
  localStorage.setItem(
      LOCAL_STORAGE_CUSTOM_COLORS_KEY,
      JSON.stringify(customColors.value)
  )

  addToast(`"${color.name}"已删除`)

  // 如果删除的是当前查看的颜色，清除选中状态
  if (selectedColor.value && selectedColor.value.name === color.name) {
    selectedColor.value = null
  }
}
const toggleTag = (tag) => {
  const index = selectedTags.value.indexOf(tag)
  index === -1
      ? selectedTags.value.push(tag)
      : selectedTags.value.splice(index, 1)
}
const toggleFavorite = (colorName) => {
  const index = favorites.value.indexOf(colorName)
  if (index === -1) {
    favorites.value.push(colorName)
  } else {
    favorites.value.splice(index, 1)
  }
  localStorage.setItem('favorites', JSON.stringify(favorites.value))
}
const toggleFavoritesMode = () => {
  isFavoritesMode.value = !isFavoritesMode.value
  if (isFavoritesMode.value) selectedTags.value = []
}
// 过滤后的颜色列表
const filteredColors = computed(() => {
  const sourceColors = isFavoritesMode.value
      ? colors.value.filter(c => favorites.value.includes(c.name))
      : colors.value
  return selectedTags.value.length
      ? sourceColors.filter(c =>
          selectedTags.value.every(t => c.tags?.includes(t))
      )
      : sourceColors
})
const tagOrder = ['红', '橘', '黄', '绿', '青', '蓝', '紫', '粉', '白', '灰', '黑', '棕']
// 标签可用性判断
const isTagAvailable = (tag) => {
  return filteredColors.value.some(color => color.tags?.includes(tag))
}
// 鼠标悬停效果处理
const handleTagHover = (tag, event) => {
  if (!selectedTags.value.includes(tag) && isTagAvailable(tag)) {
    event.target.style.backgroundColor = tagColors[tag]
  }
}
const handleTagOut = (tag, event) => {
  if (!selectedTags.value.includes(tag)) {
    event.target.style.backgroundColor = '#f0f0f0'
  }
}
const handleReset = () => {
  isFavoritesMode.value = false
  selectedTags.value = []
}
provide('tagColors', tagColors)
provide('favorites', favorites)
provide('toggleFavorite', toggleFavorite)
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
  gap: 0.7rem;
  margin-bottom: 2rem;
  padding: 0.8rem 1rem;
  min-height: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.tag {
  padding: 0.4rem 1rem;
  border-radius: 20px;
  border: 1px solid #e0e0e0;
  font-size: 0.9em;
  cursor: pointer;
  transition: background-color 0.2s ease,
  transform 0.1s ease;
}

.tag:not(.disabled):hover {
  transform: translateY(-1px);
}

.tag.disabled {
  cursor: not-allowed;
  pointer-events: none;
}

.filter-buttons {
  margin-left: auto;
  display: flex;
  gap: 0.5rem;
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
  cursor: pointer;
}

.reset-btn:hover {
  transform: rotate(-180deg) scale(1.2);
}

.reset-btn:active {
  transform: rotate(180deg) scale(0.9);
  transition-duration: 0.3s;
}

.favorite-filter-btn {
  font-size: 1.5em;
  padding: 0.1em 0.3em;
  line-height: 1;
  border-radius: 8px;
  display: inline-block;
  margin-left: auto;
}

/* 收藏按钮动画 */
.favorite-filter-btn {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  color: #FFD700; /* 黄色 */
  cursor: pointer;
}
/* 悬停效果 */
.favorite-filter-btn:hover {
  transform: scale(1.2);
  filter: brightness(1.1);
}
/* 点击动画 */
.favorite-filter-btn:active {
  transform: scale(0.9);
}
/* 收藏状态 */
.filled {
  color: #FFD700;
  text-shadow: 0 0 8px rgba(255, 215, 0, 0.3);
}
/* 添加平滑的缩放过渡 */
.star {
  display: inline-block;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform-origin: center;
}

.toast-enter-active {
  transition:
      transform 0.5s cubic-bezier(0.22, 0.61, 0.36, 1),
      opacity 0.5s ease-out;
}

.add-color-btn {
  font-size: 1.4em;
  padding: 0.1em 0.3em;
  line-height: 1;
  border-radius: 8px;
  display: inline-block;
  cursor: pointer;
  transition: all 0.3s;
}
.add-color-btn:hover {
  transform: scale(1.2);
}
.add-color-btn:active {
  transform: scale(0.9);
}

</style>
