<script setup>
import { ref, shallowRef, onMounted, onBeforeUnmount } from 'vue'
import { defineAsyncComponent } from 'vue'

const Desktop = defineAsyncComponent(() => import('@/Desktop.vue'))
const Mobile = defineAsyncComponent(() => import('@/Mobile.vue'))

const currentComponent = shallowRef(Desktop)

const updateComponent = () => {
  console.log(window.innerWidth)
  currentComponent.value = window.innerWidth <= 800 ? Mobile : Desktop
}

onMounted(() => {
  updateComponent()
  window.addEventListener('resize', updateComponent)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateComponent)
})

</script>

<template>
  <component :is="currentComponent" />
</template>