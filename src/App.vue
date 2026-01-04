<template>
  <h1 class="vertical-title">中国传统色卡</h1>

  <!-- 右上角折纸翻页按钮 -->
  <div class="page-fold"
       @click="activeTab = activeTab === 'library' ? 'palette' : 'library'">
  </div>

  <div class="container">
    <!-- 颜色库标签内容 -->
    <div v-if="activeTab === 'library'">
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

    <!-- 配色组标签内容 -->
    <div v-else-if="activeTab === 'palette'">
      <div class="palette-container">
        <div class="palette-header">
          <h3>当前配色组</h3>
          <div class="palette-controls">
            <input type="text" placeholder="配色组名称..." class="palette-name-input" />
            <button class="palette-save-btn" @click="handleSavePalette">💾 保存</button>
            <button class="palette-load-btn" @click="handleLoadPalette">📂 加载</button>
            <button class="palette-clear-btn" @click="currentPalette = []">🗑️ 清空</button>
          </div>
        </div>

        <!-- 配色条显示 -->
        <div class="palette-colors-strip">
          <div
            v-for="(color, index) in currentPalette"
            :key="index"
            class="palette-color-block"
            :style="{ backgroundColor: color.hex }"
            @mouseover="activeColorIndex = index"
            @click="copyHex(color.hex, color.name)"
          >
            <div class="color-hover-info">{{ color.hex }}</div>
          </div>
        </div>

        <!-- 颜色信息列表 -->
        <div class="palette-colors-list" :draggable="true">
          <div
            v-for="(color, index) in currentPalette"
            :key="index"
            class="palette-color-item"
            draggable="true"
            @dragstart="handleDragStart(index)"
            @dragover.prevent
            @drop="handleDrop(index)"
          >
            <div class="color-preview" :style="{ backgroundColor: color.hex }"></div>
            <div class="color-info">
              <div class="color-name">{{ color.name }}</div>
              <div class="color-tags">
                <span
                  v-for="tag in color.tags"
                  :key="tag"
                  class="tag"
                  :style="{
                    backgroundColor: tagColors[tag] || '#f0f0f0',
                    color: isTagDark(tagColors[tag]) ? '#fff' : '#666'
                  }"
                >{{ tag }}</span>
              </div>
              <div class="color-values">
                <span class="rgb">RGB: ({{ color.r }}, {{ color.g }}, {{ color.b }})</span>
                <span class="hex">{{ color.hex }}</span>
              </div>
            </div>
            <div class="color-drag-handle">⠿</div>
            <button
              class="color-delete-btn"
              @click.stop="handleDeleteFromPalette(index)"
            >
              🗑️
            </button>
          </div>

          <div v-if="currentPalette.length === 0" class="empty-palette">
            <p>配色组为空，请从颜色库添加颜色</p>
          </div>
        </div>
      </div>
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
        @addToPalette="handleAddToPalette"
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

  <!-- 加载配色组模态框 -->
  <transition name="modal">
    <div class="modal-overlay fixed" v-if="showLoadModal" @click.self="showLoadModal = false">
      <div class="modal-content palette-select-modal fixed-modal"
         ref="loadModal">
        <div class="modal-header" @mousedown="handleModalMouseDown">
          <h3>选择已保存的配色组</h3>
          <button class="close-btn" @click="showLoadModal = false">×</button>
        </div>
        <div class="palette-list-container">
          <div
            v-for="(palette, index) in savedPalettes"
            :key="index"
            class="saved-palette-item"
          >
            <div class="palette-item-header">
              <h4 class="palette-item-name">{{ palette.name }}</h4>
              <div class="palette-item-actions">
                <span class="palette-item-count">{{ palette.colors.length }} 种颜色</span>
                <button
                  class="palette-delete-btn"
                  @click.stop="handleDeleteSavedPalette(index)"
                  title="删除配色组"
                >
                  🗑️
                </button>
              </div>
            </div>
            <div class="palette-item-colors">
              <div
                v-for="(color, colorIndex) in palette.colors.slice(0, 5)"
                :key="colorIndex"
                class="palette-item-color-preview"
                :style="{ backgroundColor: color.hex }"
                title="点击加载配色组"
                @click="selectPalette(palette)"
              ></div>
              <div v-if="palette.colors.length > 5" class="more-colors-indicator" @click="selectPalette(palette)">
                +{{ palette.colors.length - 5 }}
              </div>
            </div>
            <div class="palette-item-date" @click="selectPalette(palette)">
              {{ new Date(palette.createdAt).toLocaleString('zh-CN') }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>
<script setup>
import { computed, onMounted, provide, ref, reactive } from 'vue'

// 用于加载配色组的模态框
const showLoadModal = ref(false)
const savedPalettes = ref([])
const loadModal = ref(null)
let isDragging = false
let startX = 0
let startY = 0
let initialModalX = 0
let initialModalY = 0

// 模态框拖动事件处理
const handleModalMouseDown = (e) => {
  if (loadModal.value) {
    isDragging = true
    startX = e.clientX
    startY = e.clientY
    initialModalX = loadModal.value.offsetLeft
    initialModalY = loadModal.value.offsetTop

    // 将模态框定位改为fixed
    loadModal.value.style.position = 'fixed'
    loadModal.value.style.margin = '0'

    // 添加事件监听器
    document.addEventListener('mousemove', handleModalMouseMove)
    document.addEventListener('mouseup', handleModalMouseUp)
  }
}

const handleModalMouseMove = (e) => {
  if (isDragging && loadModal.value) {
    const deltaX = e.clientX - startX
    const deltaY = e.clientY - startY
    loadModal.value.style.left = `${initialModalX + deltaX}px`
    loadModal.value.style.top = `${initialModalY + deltaY}px`
  }
}

const handleModalMouseUp = () => {
  isDragging = false
  // 移除事件监听器
  document.removeEventListener('mousemove', handleModalMouseMove)
  document.removeEventListener('mouseup', handleModalMouseUp)
}

import ColorCard from './components/ColorCard.vue'
import ColorDetail from './components/ColorDetail.vue'
import ToastMessage from './components/ToastMessage.vue'
import AddCustomColor from './components/AddCustomColor.vue'

// 当前选中的标签页
const activeTab = ref('library') // 'library' 或 'palette'
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
// 配色组功能
// 当前配色组
const currentPalette = ref([])

// 用于颜色块悬停效果的变量
const activeColorIndex = ref(null)

// 处理将颜色加入配色组
const handleAddToPalette = (color) => {
  // 检查颜色是否已在配色组中
  const isColorInPalette = currentPalette.value.some(item => item.name === color.name && item.custom === (color.custom || false))
  if (!isColorInPalette) {
    currentPalette.value.push({ ...color })
  }
}

// 用于拖拽排序的变量
const draggedItemIndex = ref(null)

// 处理拖拽开始
const handleDragStart = (index) => {
  draggedItemIndex.value = index
}

// 处理放置
const handleDrop = (targetIndex) => {
  if (draggedItemIndex.value !== null) {
    const temp = [...currentPalette.value]
    // 从原位置移除
    const [draggedItem] = temp.splice(draggedItemIndex.value, 1)
    // 插入到新位置
    temp.splice(targetIndex, 0, draggedItem)
    // 更新当前配色组
    currentPalette.value = temp
    draggedItemIndex.value = null
  }
}

// 保存配色组到localStorage
const handleSavePalette = () => {
  const paletteName = document.querySelector('.palette-name-input').value || '默认配色组'
  const palette = {
    name: paletteName,
    colors: [...currentPalette.value],
    createdAt: new Date().toISOString()
  }

  // 获取已保存的配色组
  const savedPalettes = JSON.parse(localStorage.getItem('savedPalettes') || '[]')

  // 检查是否已存在同名配色组
  const existingIndex = savedPalettes.findIndex(p => p.name === paletteName)
  if (existingIndex !== -1) {
    // 更新现有配色组
    savedPalettes[existingIndex] = palette
  } else {
    // 添加新配色组
    savedPalettes.push(palette)
  }

  // 保存到localStorage
  localStorage.setItem('savedPalettes', JSON.stringify(savedPalettes))
  addToast(`${paletteName} 已保存`)
}

// 从配色组删除颜色
const handleDeleteFromPalette = (index) => {
  currentPalette.value.splice(index, 1)
}

// 判断标签颜色是否为深色（用于决定文字颜色）
const isTagDark = (hex) => {
  if (!hex) return false
  // 处理短 hex 代码 (如 #fff)
  const normalizedHex = hex.length === 4
    ? `#${hex[1]}${hex[1]}${hex[2]}${hex[2]}${hex[3]}${hex[3]}`
    : hex;

  const r = parseInt(normalizedHex.substr(1, 2), 16)
  const g = parseInt(normalizedHex.substr(3, 2), 16)
  const b = parseInt(normalizedHex.substr(5, 2), 16)

  // 使用 luminance 公式判断
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
  return luminance < 0.5
}

// 加载配色组
const handleLoadPalette = () => {
  // 获取已保存的配色组
  const saved = JSON.parse(localStorage.getItem('savedPalettes') || '[]')
  savedPalettes.value = saved

  if (saved.length === 0) {
    addToast('没有已保存的配色组')
    return
  }

  // 显示模态框
  showLoadModal.value = true
}

// 选择配色组
const selectPalette = (palette) => {
  // 更新当前配色组
  currentPalette.value = [...palette.colors]

  // 填充配色组名称到输入框
  const input = document.querySelector('.palette-name-input')
  if (input) {
    input.value = palette.name
  }

  // 关闭模态框
  showLoadModal.value = false

  // 显示提示
  addToast(`${palette.name} 已加载`)
}

// 删除已保存的配色组
const handleDeleteSavedPalette = (index) => {
  // 获取当前已保存的配色组
  let saved = JSON.parse(localStorage.getItem('savedPalettes') || '[]')

  // 获取要删除的配色组名称
  const paletteName = saved[index].name

  // 从数组中删除该配色组
  saved.splice(index, 1)

  // 保存回localStorage
  localStorage.setItem('savedPalettes', JSON.stringify(saved))

  // 更新savedPalettes ref
  savedPalettes.value = [...saved]

  // 显示提示
  addToast(`${paletteName} 已删除`)
}

// 复制hex值功能
const copyHex = (hex, colorName) => {
  navigator.clipboard.writeText(hex)
      .then(() => addToast(`${colorName} 的 HEX码已复制`))
      .catch(() => addToast('复制失败'))
}

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

/* 收藏按钮 */
.favorite-filter-btn {
  font-size: 1.4em;
  padding: 0.1em 0.3em;
  line-height: 1;
  border-radius: 8px;
  display: inline-block;
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

/* 右上角折纸翻页按钮 */
.page-fold {
  position: fixed;
  top: 0;
  right: 0;
  width: 0;
  height: 0;
  /* 创建三角形折纸效果 */
  border-top: 80px solid #e5e7eb; /* 折纸颜色 */
  border-left: 80px solid transparent;
  cursor: pointer;
  z-index: 999;
  /* 阴影效果，增强立体感 */
  box-shadow:
    -2px 2px 4px rgba(0, 0, 0, 0.1), /* 外部阴影 */
    inset 0 -1px 1px rgba(255, 255, 255, 0.8); /* 内部高光 */
  transition: transform 0.2s ease, border-color 0.2s ease;
}

/* 悬停效果 */
.page-fold:hover {
  /* 折纸向上翻起的效果 */
  transform: translateY(-4px) translateX(-4px);
  /* 颜色变浅 */
  border-top-color: #d1d5db;
  /* 增强阴影 */
  box-shadow:
    4px 4px 8px rgba(0, 0, 0, 0.15),
    inset -1px 0 1px rgba(255, 255, 255, 0.8);
}

/* 点击效果 */
.page-fold:active {
  transform: translateY(0) translateX(0);
  //border-top-color: #9ca3af;
  box-shadow:
    -2px 2px 4px rgba(0, 0, 0, 0.2),
    inset 0 -1px 1px rgba(255, 255, 255, 0.8);
}

/* 扩展点击区域 */
.page-fold::after {
  content: '';
  position: absolute;
  top: 0;
  right: -80px;
  width: 120px;
  height: 120px;
  background: transparent;
  cursor: pointer;
  z-index: 1000;
}

/* Palette styles */
.palette-container {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-top: 1rem;
}

.palette-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.palette-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.5em;
}

.palette-controls {
  display: flex;
  gap: 0.8rem;
  align-items: center;
  flex-wrap: wrap;
}

.palette-name-input {
  padding: 0.6rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 0.9em;
  min-width: 200px;
}

.palette-save-btn,
.palette-load-btn,
.palette-clear-btn {
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9em;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.palette-save-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.palette-load-btn {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.palette-clear-btn {
  background: #ff6b6b;
  color: white;
}

.palette-save-btn:hover,
.palette-load-btn:hover,
.palette-clear-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.palette-save-btn:active,
.palette-load-btn:active,
.palette-clear-btn:active {
  transform: translateY(0);
}

/* Palette colors strip */
.palette-colors-strip {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  padding: 2rem 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  min-height: 80px;
  align-items: center;
  justify-content: flex-start;
  overflow: visible;
  position: relative;
  z-index: 1;
}

.palette-color-block {
  flex: 0 0 80px;
  height: 80px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.palette-color-block:hover {
  flex: 0 0 120px;
  height: 120px;
  margin: -20px 0;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  z-index: 10;
}

.color-hover-info {
  position: absolute;
  bottom: -30px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  font-size: 0.8em;
  font-family: monospace;
  opacity: 0;
  transition: opacity 0.3s ease;
  white-space: nowrap;
}

.palette-color-block:hover .color-hover-info {
  opacity: 1;
}

/* Palette colors list */
.palette-colors-list {
  margin-top: 2rem;
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1rem;
}

.palette-color-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: white;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  cursor: grab;
}

.palette-color-item:active {
  cursor: grabbing;
}

.palette-color-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateX(4px);
}

.color-preview {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  flex-shrink: 0;
}

.color-info {
  flex: 1;
  min-width: 0;
}

.color-name {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.3rem;
}

.color-tags {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.3rem;
}

.color-tags .tag {
  padding: 0.2rem 0.6rem;
  border-radius: 1rem;
  font-size: 0.75em;
  background: #e0e0e0;
  color: #666;
}

.color-values {
  font-size: 0.85em;
  color: #666;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  font-family: monospace;
}

.color-drag-handle {
  font-size: 1.5em;
  color: #999;
  cursor: grab;
  user-select: none;
}

.color-drag-handle:active {
  cursor: grabbing;
}

.color-delete-btn {
  background: none;
  color: #666; /* 灰色 */
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  font-size: 0.9em;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
}

.color-delete-btn:hover {
  background: #f5f5f5; /* 浅灰色背景 */
  color: #ff6b6b; /* 悬停时变为红色 */
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.color-delete-btn:active {
  transform: scale(0.95);
}

.empty-palette {
  text-align: center;
  padding: 4rem 2rem;
  color: #999;
  font-size: 1.1em;
}

.empty-palette p {
  margin: 0;
}

/* Modal overlay fixed position */
.modal-overlay.fixed {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;
  background-color: rgba(0, 0, 0, 0.5); /* 添加半透明背景 */
  display: flex; /* 使用flexbox居中 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}

/* Modal content fixed position */
.modal-content.fixed-modal {
  margin: auto;
  position: relative;
  z-index: 1001;
}

/* Palette select modal styles */
.palette-select-modal {
  width: 90%;
  max-width: 600px;
  max-height: 70vh;
  overflow-y: auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5em;
  color: #999;
  cursor: pointer;
  padding: 0.2rem;
  width: 30px;
  height: 30px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: #f5f5f5;
  color: #666;
}

.palette-list-container {
  padding: 1.5rem;
}

.saved-palette-item {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.saved-palette-item:hover {
  background: #e9ecef;
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.palette-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
}

.palette-item-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.palette-delete-btn {
  background: none;
  color: #999;
  border: none;
  font-size: 1.1em;
  cursor: pointer;
  padding: 0.3rem;
  border-radius: 4px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.palette-delete-btn:hover {
  background: #ff6b6b;
  color: white;
  transform: scale(1.1);
}

.palette-item-name {
  margin: 0;
  color: #2c3e50;
  font-size: 1.1em;
  font-weight: 600;
}

.palette-item-count {
  color: #999;
  font-size: 0.85em;
}

.palette-item-colors {
  display: flex;
  gap: 0.3rem;
  margin-bottom: 0.8rem;
}

.palette-item-color-preview {
  width: 40px;
  height: 40px;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.more-colors-indicator {
  width: 40px;
  height: 40px;
  border-radius: 6px;
  background: #ddd;
  color: #666;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8em;
  font-weight: 600;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.palette-item-date {
  color: #999;
  font-size: 0.8em;
}

</style>
