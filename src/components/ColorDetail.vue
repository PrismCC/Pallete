<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <!-- 左侧颜色展示区域 -->
      <div
          class="color-pane"
          :style="{ backgroundColor: color.hex, boxShadow: `inset 0 0 12px ${insetShadowColor}` }"
      ></div>
      <!-- 右侧信息展示区域 -->
      <div class="info-pane">
        <div class="top-buttons">
          <!-- 添加的垃圾桶按钮 -->
          <button
              v-if="color.custom"
              class="top-button delete-btn"
              @click.stop="confirmDelete"
          >
            🗑️
          </button>
          <!-- 加入配色组按钮 -->
          <button class="top-button add-to-palette-btn" @click.stop="handleAddToPalette">
            ➕<span class="add-text">加入配色组</span>
          </button>

          <button class="top-button favorite-btn" @click.stop="toggleFavorite(color.name)">
            <span :class="['star', { 'filled': isFavorite }]">{{ isFavorite ? '★' : '☆' }}</span>
          </button>
        </div>

        <h2>{{ color.name }}</h2>
        <div class="info-item">
          <span class="label">HEX:</span>
          <code class="value" @click.stop="copyHex">{{ color.hex }}</code>
        </div>
        <div class="info-item">
          <span class="label">RGB:</span>
          <code class="value" @click.stop="copyRgb">({{ color.r }}, {{ color.g }}, {{ color.b }})</code>
        </div>
        <span class="label">Tag:</span>
        <div class="info-item tags">
          <span
              v-for="tag in color.tags"
              :key="tag"
              class="tag"
              :style="{
              backgroundColor: tagColors[tag] || '#f0f0f0',
              color: '#666',
              borderColor: adjustBorderColor(tagColors[tag])
            }"
          >
            {{ tag }}
          </span>
        </div>
        <div class="info-item" v-if="color.introduction">
          <div class="label">简介</div>
          <p class="introduction">{{ color.introduction }}</p>
        </div>
        <div class="info-item" v-if="color.poetry">
          <blockquote class="poetry">{{ color.poetry }}</blockquote>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import {computed, inject} from 'vue'
const props = defineProps({
  color: Object
})
const favorites = inject('favorites')
const toggleFavorite = inject('toggleFavorite')
const emit = defineEmits(['close', 'toast', 'delete', 'addToPalette'])
const copyHex = () => {
  navigator.clipboard.writeText(props.color.hex)
      .then(() => emit('toast', 'HEX码已复制'))
      .catch(() => emit('toast', '复制失败'))
}
const copyRgb = () => {
  const rgbText = `rgb(${props.color.r}, ${props.color.g}, ${props.color.b})`
  navigator.clipboard.writeText(rgbText)
      .then(() => emit('toast', 'RGB值已复制'))
      .catch(() => emit('toast', '复制失败'))
}
// tag 颜色映射（与ColorCard保持同步）
const tagColors = inject('tagColors')
// 生成边框颜色（比背景色深15%）
const adjustBorderColor = (hex) => {
  if (!hex) return '#ccc'
  // 处理短 hex 代码 (如 #fff)
  const normalizedHex = hex.length === 4
    ? `#${hex[1]}${hex[1]}${hex[2]}${hex[2]}${hex[3]}${hex[3]}`
    : hex;

  // 解析为 RGB
  const r = parseInt(normalizedHex.substr(1, 2), 16);
  const g = parseInt(normalizedHex.substr(3, 2), 16);
  const b = parseInt(normalizedHex.substr(5, 2), 16);

  // 深色化并确保不小于 0
  return `rgb(${Math.max(0, r - 40)}, ${Math.max(0, g - 40)}, ${Math.max(0, b - 40)})`
}
// 生成内阴影颜色（降低亮度）
const insetShadowColor = computed(() => {
  // 处理短 hex 代码 (如 #fff)
  const normalizedHex = props.color.hex.length === 4
    ? `#${props.color.hex[1]}${props.color.hex[1]}${props.color.hex[2]}${props.color.hex[2]}${props.color.hex[3]}${props.color.hex[3]}`
    : props.color.hex;

  const r = parseInt(normalizedHex.substr(1, 2), 16);
  const g = parseInt(normalizedHex.substr(3, 2), 16);
  const b = parseInt(normalizedHex.substr(5, 2), 16);

  return `rgba(${r}, ${g}, ${b}, 0.3)`
})
const isFavorite = computed(() =>
    favorites.value.includes(props.color.name)
)
const handleAddToPalette = () => {
  emit('addToPalette', props.color)
  emit('toast', `${props.color.name} 已加入配色组`)
}

// 删除确认
const confirmDelete = () => {
  emit('delete', props.color)
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(3px);
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 780px;
  max-height: 80vh;
  display: flex;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.color-pane {
  flex: 0 0 50%;
  min-height: 300px;
  transition: background-color 0.3s;
}

.info-pane {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
  background: linear-gradient(to bottom, #fafafa, #fff 15%);
  position: relative;
}

.favorite-btn {
  background: none;
  border: none;
  cursor: pointer;
}

/* 添加平滑的缩放过渡 */
.star {
  font-size: 28px;
  display: inline-block;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform-origin: center;
}

h2 {
  margin: 0 0 1.5rem;
  color: #2c3e50;
  font-size: 1.8em;
  position: relative;
  padding-bottom: 0.5rem;
}

h2::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 40px;
  height: 2px;
  background: #ddd;
}

.info-item {
  margin: 1.2rem 0;
}

.label {
  display: block;
  font-weight: 600;
  color: #444;
  margin-bottom: 0.6rem;
  font-size: 0.95em;
}

.value {
  color: #666;
  font-family: 'Fira Code', monospace;
  background: #f5f5f5;
  padding: 0.2em 0.4em;
  border-radius: 4px;
}

.value:hover {
  cursor: pointer;
  background: #e0e0e0;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  align-items: center;
  margin-top: 0.4rem;
}

.tag {
  font-size: 0.85em;
  padding: 0.3em 0.8em;
  border-radius: 1em;
  border: 1px solid;
  line-height: 1.2;
}

.introduction {
  color: #444;
  line-height: 1.8;
  margin: 0.5rem 0;
  font-size: 0.92em;
}

.poetry {
  margin: 0.8rem 0;
  padding-left: 1.2rem;
  border-left: 3px solid #eee;
  color: #666;
  font-style: italic;
  line-height: 1.6;
}

@media (max-width: 600px) {
  .modal-content {
    flex-direction: column;
    max-height: 90vh;
  }

  .color-pane {
    flex: none;
    height: 200px;
  }

  .info-pane {
    overflow-y: visible;
  }
}

/* 添加顶部按钮容器 */
.top-buttons {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 10px;
  z-index: 10;
}
.top-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  border-radius: 4px;
}
.favorite-btn {
  color: #FFD700; /* 黄色 */
}
.favorite-btn:hover .star {
  transform: scale(1.2);
  filter: brightness(1.1);
}
.favorite-btn:active .star {
  transform: scale(0.9);
}
.delete-btn:hover {
  background-color: #ffe6e6;
  transform: scale(1.1);
}
.delete-btn:active {
  transform: scale(0.9);
}
/* 调整收藏按钮位置 */

/* Add to palette button styles */
.add-to-palette-btn {
  color: #667eea; /* 紫色 */
}

.add-to-palette-btn:hover {
  background-color: #f0f0ff; /* 淡紫色背景 */
  transform: scale(1.1);
}

.add-to-palette-btn:active {
  transform: scale(0.9);
}

/* 加入配色组文字样式 - 默认隐藏 */
.add-text {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: #667eea;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.3s;
  z-index: 10;
  margin-top: 4px;
}

/* 鼠标悬浮时显示文字 */
.add-to-palette-btn:hover .add-text {
  opacity: 1;
}
</style>
