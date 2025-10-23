<template>
  <transition-group
      name="toast"
      tag="div"
      class="toast-container"
  >
    <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast-item"
    >
      {{ toast.message }}
    </div>
  </transition-group>
</template>

<script setup>
defineProps({
  toasts: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1001;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.toast-item {
  background: rgba(255, 255, 255, 0.95);
  padding: 12px 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.5s ease;
  font-size: 14px;
  border: 1px solid #eee;
  backdrop-filter: blur(5px);
}
</style>
