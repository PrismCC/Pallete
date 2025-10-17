<template>
  <div
      class="color-card"
      :style="{ borderColor: color.hex }"
      @click="$emit('click', color)"
  >
    <div class="color-preview" :style="{ backgroundColor: color.hex }"></div>
    <div class="color-info">
      <h2>{{ color.name }}</h2>
      <p class="hex-code">{{ color.hex }}</p>
      <p class="rgb-values">{{ color.r }} {{ color.g }} {{ color.b }}</p>
      <div class="tags-container">
        <span
            v-for="tag in color.tags"
            :key="tag"
            class="tag"
            :style="{
              backgroundColor: tagColors[tag] || '#f0f0f0',
              color: getTextColor(tagColors[tag])
            }"
        >
          {{ tag }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
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

const getTextColor = (hex) => {
  if (!hex) return '#666'
  const r = parseInt(hex.slice(1, 3), 16)
  const g = parseInt(hex.slice(3, 5), 16)
  const b = parseInt(hex.slice(5, 7), 16)
  return (r * 0.299 + g * 0.587 + b * 0.114) > 186 ? '#333' : '#666'
}

defineProps({
  color: {
    type: Object,
    required: true,
    validator: (value) => {
      return 'name' in value && 'hex' in value
    }
  }
})
defineEmits(['click'])
</script>

<style scoped>
.color-card {
  display: flex;
  border: 3px dotted;
  border-radius: 12px;
  padding: 1.2rem;
  background: #f5f5f5;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
  height: 100%;
  max-height: 120px;
}

.color-card:hover {
  transform: translateY(-4px);
}

.color-preview {
  width: 90px;
  height: 90px;
  border-radius: 8px;
  margin-right: 1.2rem;
  flex-shrink: 0;
}

.color-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  max-height: 100px;
}

h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.2em;
  color: #2c3e50;
}

.hex-code {
  color: #666;
  margin: 0.2rem 0;
  font-family: monospace;
}

.rgb-values {
  color: #888;
  margin: 0.2rem 0;
  font-size: 0.9em;
}

.tags-container {
  margin-top: auto;
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.tag {
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  border: 1px solid #ccc;
  font-size: 0.8em;
  white-space: nowrap;
}

@media (max-width: 480px) {
  .color-preview {
    width: 60px;
    height: 60px;
  }

  .color-card {
    padding: 0.8rem;
  }
}
</style>
