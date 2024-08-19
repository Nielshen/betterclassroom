<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import { useDataStore } from '../stores/dataStore'

const emits = defineEmits(['idxChange', 'raisedHand'])
const dataStore = useDataStore()

const exercise = ref(dataStore.user.current_exercise ? dataStore.user.current_exercise - 1 : 0)

const questionAsked = computed(() => dataStore.user.help_requested)
const tasks = computed(() => {
  console.log('Tasks computed property called, current value:', dataStore.tasks)
  return dataStore.tasks
})

const currentExerciseTitle = computed(() => {
  return tasks.value[exercise.value]?.name || 'Keine Aufgabe verfügbar'
})

watch(() => dataStore.user.current_exercise, (newVal) => {
  exercise.value = newVal - 1
})

watch(tasks, (newTasks, oldTasks) => {
  console.log('Tasks watcher triggered')
  console.log('New tasks:', newTasks)
  console.log('Old tasks:', oldTasks)
  
  if (newTasks.length === 1) {
    exercise.value = 0
    emits('idxChange', exercise.value)
  } else if (newTasks.length > oldTasks.length) {
    console.log('New task added, navigation controls updated')
  } else if (newTasks.length < oldTasks.length) {
    console.log('Task deleted, adjusting current exercise if necessary')
    if (exercise.value >= newTasks.length) {
      // If the current exercise is now out of bounds, adjust it
      exercise.value = newTasks.length - 1
      emits('idxChange', exercise.value)
    } else if (exercise.value > 0) {
      // If the deleted task was before the current one, we need to shift back
      const oldTask = oldTasks[exercise.value]
      const newIndex = newTasks.findIndex(task => task.id === oldTask.id)
      if (newIndex !== -1) {
        exercise.value = newIndex
        emits('idxChange', exercise.value)
      }
    }
  }
}, { deep: true })

const nextTask = () => {
  if (tasks.value.length > 0) {
    let nextIndex = (exercise.value + 1) % tasks.value.length
    exercise.value = nextIndex
    emits('idxChange', exercise.value)
  }
}

const previousTask = () => {
  if (tasks.value.length > 0) {
    let previousIndex = (exercise.value - 1 + tasks.value.length) % tasks.value.length
    exercise.value = previousIndex
    emits('idxChange', exercise.value)
  }
}

const toggleQuestion = () => {
  dataStore.updateUserField('help_requested', !dataStore.user.help_requested)
  emits('raisedHand')
}

onMounted(() => {
  exercise.value = dataStore.user.current_exercise ? dataStore.user.current_exercise - 1 : 0
  emits('idxChange', exercise.value)
})
</script>

<template>
  <div class="w-full h-full">
    <div class="carousel h-full w-full">
      <div id="slide1" class="carousel-item relative justify-center item-center w-full h-full">
        <div class="flex w-3/4 h-[580px] w-[850px]">
          <div class="mx-20 w-full">
            <div class="flex justify-between items-center">
              <h1 class="text-2xl my-10">{{ currentExerciseTitle }}</h1>
              <button
                @click="toggleQuestion"
                :class="['btn', 'btn-accent', 'text-2xl', !questionAsked && 'btn-outline']"
              >
                ✋🏼
              </button>
            </div>
            <p>
              <div v-if="tasks[exercise]">
                <div v-html="tasks[exercise].description.replace(/(\\n|\n)/g, '<br><br>')"></div>
              </div>
              <div v-else>Laden...</div>
            </p>
          </div>
        </div>
      </div>
    </div>
    <div class="absolute flex justify-between transform -translate-y-1/2 left-1 right-1 top-1/2">
      <a v-if="tasks.length > 1 && exercise > 0" @click="previousTask" class="btn btn-circle btn-accent ml-4">❮</a>
      <a v-else class="btn btn-circle" style="visibility: hidden">❮</a>
      <a
        v-if="tasks.length > 1 && exercise < tasks.length - 1"
        @click="nextTask"
        class="btn btn-circle btn-accent mr-4"
      >❯</a>
      <a v-else class="btn btn-circle" style="visibility: hidden">❯</a>
    </div>
  </div>
</template>