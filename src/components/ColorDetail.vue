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
        <h2>{{ color.name }}</h2>
        <div class="info-item">
          <span class="label">HEX:</span>
          <code class="value">{{ color.hex }}</code>
        </div>
        <div class="info-item">
          <span class="label">RGB:</span>
          <code class="value">RGB({{ color.r }}, {{ color.g }}, {{ color.b }})</code>
        </div>
        <div class="info-item tags">
          <span class="label">标签:</span>
          <span
              v-for="tag in color.tags"
              :key="tag"
              class="tag"
              :style="{
              backgroundColor: tagColors[tag] || '#f0f0f0',
              color: getTextColor(tagColors[tag]),
              borderColor: adjustBorderColor(tagColors[tag])
            }"
          >
            {{ tag }}
          </span>
        </div>
        <div class="info-item" v-if="color.introduction">
          <div class="label">颜色介绍</div>
          <p class="introduction">{{ color.introduction }}</p>
        </div>
        <div class="info-item" v-if="color.poetry">
          <div class="label">相关诗句</div>
          <blockquote class="poetry">{{ color.poetry }}</blockquote>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  color: {
    type: Object,
    required: true
  }
})

defineEmits(['close'])

// tag 颜色映射（与ColorCard保持同步）
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

// 生成边框颜色（比背景色深15%）
const adjustBorderColor = (hex) => {
  if (!hex) return '#ccc'
  const rgb = hex.slice(1, 7).match(/.{2}/g)
  return `rgb(${rgb.map(x => Math.max(0, parseInt(x, 16) - 40)).join(',')})`
}

// 文字颜色计算（与ColorCard一致）
const getTextColor = (hex) => {
  if (!hex) return '#666'
  const r = parseInt(hex.slice(1, 3), 16)
  const g = parseInt(hex.slice(3, 5), 16)
  const b = parseInt(hex.slice(5, 7), 16)
  return (r * 0.299 + g * 0.587 + b * 0.114) > 186 ? '#333' : '#666'
}

// 生成内阴影颜色（降低亮度）
const insetShadowColor = computed(() => {
  const rgb = props.color.hex.slice(1, 7).match(/.{2}/g)
  return `rgba(${rgb.map(x => parseInt(x, 16)).join(',')}, 0.3)`
})
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

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  align-items: center;
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
</style>
