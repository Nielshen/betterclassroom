<script setup>
import { defineProps, computed, ref, watch } from 'vue'
import { getApiUrl } from '@/utils/common'
import { io } from 'socket.io-client'

const props = defineProps({
  name: String,
  maxTasks: Number,
  raisedHand: Boolean,
  finishedTasks: Number,
  showNames: Boolean
})

const rawUrl = getApiUrl()
const api_url = `http://${rawUrl}/api`
const wsUrl = `ws://${rawUrl}/student`

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

const socket = io(wsUrl, {
  path: '/api/socket.io/student',
  transports: ['websocket'],
  reconnectio: true,
  reconnectionAttempts: 500,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
  randomizationFactor: 0.5
})

const removeHelp = async () => {
  socket.emit('help', { id: studentName.value }, function (response) {
    if (response.error) {
      console.error('Error removing help:', response.error)
    } else {
      console.log('Removed help:', response.success)
    }
  })
}
</script>

<template>
  <div v-if="showNames"  class="flex flex-col items-center w-full">
    <div class="flex items-center justify-center w-full mb-2 relative">
      <button 
        v-if="studentRaisedHand" 
        class="absolute left-2 text-base"
      >👋</button>
      <span class="text-base font-medium text-center truncate max-w-[80%]">{{ studentName }}</span>
    </div>
    <div
      :class="['radial-progress', studentRaisedHand ? 'text-error' : 'text-base-100', 'font-semibold']"
      :style="`--value: ${progress}; --size: 4.5rem; --thickness: 7px;`"
      role="progressbar"
    >
      {{ finishedTasks }} / {{ maxTasks }}
    </div>
  </div>
  <div v-else>
    <p v-if="studentRaisedHand"><button @click="removeHelp">👋</button></p>
    <p v-else><br></p>
    <div
      :class="['radial-progress', studentRaisedHand ? 'text-error' : 'text-base-100', 'font-semibold']"
      :style="`--value: ${progress}`"
      role="progressbar"
    >
      <div class="tooltip tooltip-secondary" :data-tip="`${studentName}`">
        {{ finishedTasks }} / {{ maxTasks }}
      </div>
    </div>
  </div>

</template>