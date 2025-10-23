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
/* 更新后的完整样式 */
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1001;
  display: flex;
  flex-direction: column;
  gap: 10px;
  /* 添加容器过渡 */
  transition: all 0.3s;
}
.toast-item {
  min-width: 100px;
  background: rgba(255, 255, 255, 0.95);
  padding: 12px 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  font-size: 14px;
  border: 1px solid #eee;
  backdrop-filter: blur(5px);
  /* 修复层级问题 */
  transform: translateZ(0);
  will-change: transform, opacity;
}
/* 优化后的层级动画 */
.toast-enter-active {
  transition:
      transform 0.6s cubic-bezier(0.18, 0.89, 0.32, 1.28),
      opacity 0.6s ease-out;
  z-index: 1; /* 新进入的层级置顶 */
}
.toast-leave-active {
  transition:
      transform 0.4s cubic-bezier(0.6, -0.3, 0.74, 0.05),
      opacity 0.3s ease-in;
  z-index: 0; /* 离开的层级降低 */
}
/* 关键修复点：移除绝对定位 */
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(120%) translateZ(0); /* 保持3D加速 */
}
/* 动态顺序过渡 */
.toast-move {
  transition:
      transform 0.6s cubic-bezier(0.18, 0.89, 0.32, 1.28),
      opacity 0.6s ease-out;
}
/* 消除移动动画残留 */
.toast-leave-active ~ .toast-item {
  transition:
      transform 0.6s cubic-bezier(0.18, 0.89, 0.32, 1.28),
      opacity 0.6s ease-out;
}
</style>
