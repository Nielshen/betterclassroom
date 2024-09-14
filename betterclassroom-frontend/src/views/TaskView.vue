<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import { useDataStore } from '../stores/dataStore'
import { marked } from 'marked'

const emits = defineEmits(['idxChange', 'raisedHand'])
const dataStore = useDataStore()

const exercise = ref(dataStore.user.current_exercise ? dataStore.user.current_exercise : 0)

const questionAsked = computed(() => dataStore.user.help_requested)
const tasks = computed(() => dataStore.tasks)
const previousTasks = ref([])

const currentExerciseTitle = computed(() => {
  return tasks.value[exercise.value]?.name || 'Keine Aufgabe verfügbar'
})

watch(() => dataStore.user.current_exercise, (newVal) => {
  exercise.value = newVal
})

watch(tasks, (newTasks) => {
  if (newTasks.length === 0) {
    exercise.value = 0
    emits('idxChange', exercise.value)
  } else if (previousTasks.value.length > newTasks.length) {
    // A task was deleted
    const deletedIndex = previousTasks.value.findIndex((oldTask) => 
      !newTasks.some(newTask => newTask.id === oldTask.id)
    )
    
    if (deletedIndex <= exercise.value) {
      // If the deleted task was before or is the current one
      const currentTaskId = previousTasks.value[exercise.value]?.id
      const newIndex = newTasks.findIndex(task => task.id === currentTaskId)
      
      if (newIndex !== -1) {
        // The current task still exists, adjust the index
        exercise.value = newIndex
      } else {
        // The current task was deleted, move to the next available task
        exercise.value = Math.min(exercise.value, newTasks.length - 1)
      }
    }
    // If the deleted task was after the current one, no adjustment needed
  } else if (previousTasks.value.length < newTasks.length) {
    // A task was added, no need to change the current exercise
    console.log('New task added')
  }

  // Update previousTasks for the next change
  previousTasks.value = JSON.parse(JSON.stringify(newTasks))

  emits('idxChange', exercise.value)
}, { deep: true })

const nextTask = () => {
  if (tasks.value.length > 0) {
    let nextIndex = (exercise.value + 1) % tasks.value.length
    console.log('Next index:', nextIndex)
    exercise.value = nextIndex
    emits('idxChange', exercise.value)
  }
}

const previousTask = () => {
  if (tasks.value.length > 0) {
    let previousIndex = (exercise.value - 1 + tasks.value.length) % tasks.value.length
    console.log('Previous index:', previousIndex)
    exercise.value = previousIndex
    emits('idxChange', exercise.value)
  }
}

const finishExercise = (exercise) => {
  dataStore.updateUserField('current_exercise', exercise + 1)
  emits('idxChange', exercise + 1)
}

const toggleQuestion = () => {
  dataStore.updateUserField('help_requested', !dataStore.user.help_requested)
  emits('raisedHand')
}

onMounted(() => {
  exercise.value = dataStore.user.current_exercise ? dataStore.user.current_exercise : 0
  previousTasks.value = JSON.parse(JSON.stringify(tasks.value))
  emits('idxChange', exercise.value)
})

const renderMarkdown = (markdown) => {
  return marked(markdown)
}
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
                title="Hier klicken, um Hilfe anzufordern"
              >
                ✋🏼
              </button>
            </div>
            <p>
              <div v-if="tasks[exercise]">
                <div v-html="renderMarkdown(tasks[exercise].description)"></div>
              </div>
              <div v-else>Du hast alle Aufgaben bearbeitet.</div>
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
      <a v-else-if="exercise === tasks.length - 1" @click="finishExercise(exercise)" class="btn btn-circle btn-accent mr-4 text-xl text-checkmark font-semibold">✓</a>
      <a v-else class="btn btn-circle" style="visibility: hidden">❯</a>
    </div>
  </div>
</template>