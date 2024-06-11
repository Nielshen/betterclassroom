<script setup>
import { defineProps, computed, ref, watch } from 'vue'
import { getApiUrl } from '@/utils/common'
import axios from 'axios'
const props = defineProps({
  name: String,
  maxTasks: Number,
  raisedHand: Boolean,
  finishedTasks: Number
})

const rawUrl = getApiUrl()
const api_url = `http://${rawUrl}/api`

const studentName = ref(props.name)
const studentRaisedHand = ref(props.raisedHand)
const studentFinishedTasks = ref(props.finishedTasks)
const studentMaxTasks = ref(props.maxTasks)

const progress = computed(() => {
  return (studentFinishedTasks.value / studentMaxTasks.value) * 100
})

watch(
  () => props.raisedHand,
  (newVal) => {
    studentRaisedHand.value = newVal
  }
)

watch(
  () => props.finishedTasks,
  (newVal) => {
    studentFinishedTasks.value = newVal
  }
)

watch(
  () => props.maxTasks,
  (newVal) => {
    studentMaxTasks.value = newVal
  }
)

const removeHelp = async () => {
  await axios.post(`${api_url}/students/${studentName.value}/help`, {})
}
</script>

<template>
  <div>
    <p v-if="studentRaisedHand"><button @click="removeHelp">👋</button></p>
    <p v-else>-</p>
    <div
      :class="['radial-progress', studentRaisedHand ? 'text-error' : 'text-base-100']"
      :style="`--value: ${progress}`"
      role="progressbar"
    >
      <div class="tooltip tooltip-secondary" :data-tip="`${studentName}`">
        {{ finishedTasks }} / {{ maxTasks }}
      </div>
    </div>
    <!-- <p>{{studentName}}</p> -->
  </div>
</template>
