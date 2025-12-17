<template>
  <div v-if="show" class="modal-overlay" @click.self="close">
    <div class="add-color-modal">
      <h2>添加自定义颜色</h2>
      <div class="form-group">
        <label>颜色名称</label>
        <input v-model="customColor.name" type="text" placeholder="输入颜色名称">
      </div>
      <div class="form-group">
        <label>HEX 值</label>
        <div class="color-input">
          <input
              v-model="customColor.hex"
              type="text"
              placeholder="#FFFFFF"
              :style="{ backgroundColor: validHexColor }"
          >
          <input
              v-model="customColor.hex"
              type="color"
              class="color-picker"
          >
        </div>
      </div>
      <div class="form-group">
        <label>选择标签</label>
        <div class="tags-container">
          <span
              v-for="tag in tagOrder"
              :key="tag"
              class="tag"
              :style="{
              backgroundColor: selectedTags.includes(tag) ? tagColors[tag] : '#f0f0f0',
              border: selectedTags.includes(tag) ? '1px solid #7f7f7f' : '1px solid #e0e0e0'
            }"
              @click="toggleTag(tag)"
          >
            {{ tag }}
          </span>
        </div>
      </div>
      <div class="form-actions">
        <button class="cancel" @click="close">取消</button>
        <button class="confirm" @click="saveColor" :disabled="!isFormValid">添加</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  show: Boolean,
  tagOrder: Array,
  tagColors: Object
})

const emit = defineEmits(['close', 'save'])

const customColor = ref({
  name: '',
  hex: '',
  tags: []
})

const selectedTags = ref([])

const validHexColor = computed(() => {
  const hexRegex = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/
  return hexRegex.test(customColor.value.hex) ? customColor.value.hex : '#ffffff'
})

const isFormValid = computed(() => {
  return customColor.value.name.trim() &&
      /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/.test(customColor.value.hex) &&
      selectedTags.value.length > 0
})

const toggleTag = (tag) => {
  const index = selectedTags.value.indexOf(tag)
  if (index === -1) {
    selectedTags.value.push(tag)
  } else {
    selectedTags.value.splice(index, 1)
  }
}

const saveColor = () => {
  // 确保HEX值格式正确
  let hex = customColor.value.hex
  if (hex.length === 4) { // 如 #fff
    hex = '#' + hex[1] + hex[1] + hex[2] + hex[2] + hex[3] + hex[3]
  }

  // 将HEX转换为RGB
  const r = parseInt(hex.substr(1, 2), 16)
  const g = parseInt(hex.substr(3, 2), 16)
  const b = parseInt(hex.substr(5, 2), 16)

  const newColor = {
    ...customColor.value,
    hex: hex.toUpperCase(),
    r,
    g,
    b,
    tags: [...selectedTags.value],
    custom: true // 标记为自定义颜色
  }

  emit('save', newColor)
  resetForm()
  close()
}

const resetForm = () => {
  customColor.value = { name: '', hex: '', tags: [] }
  selectedTags.value = []
}

const close = () => {
  emit('close')
  resetForm()
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
  z-index: 2000;
}

.add-color-modal {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

h2 {
  margin-top: 0;
  color: #333;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #555;
}

input[type="text"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box;
}

.color-input {
  display: flex;
  align-items: center;
  gap: 10px;
}

.color-picker {
  height: 42px;
  width: 50px;
  padding: 0;
  border: none;
  cursor: pointer;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 0.5rem;
}

.tag {
  padding: 0.4rem 0.8rem;
  border-radius: 16px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

button {
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

button.cancel {
  background-color: #f5f5f5;
}

button.cancel:hover {
  background-color: #e0e0e0;
}

button.confirm {
  background-color: #4a9dff;
  color: white;
}

button.confirm:hover {
  background-color: #3a8def;
}

button.confirm:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
