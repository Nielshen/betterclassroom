<script setup>
import { ref, watch, watchEffect, onBeforeMount } from 'vue'

import { useDataStore } from '../stores/dataStore'

const props = defineProps({
  current_exercise: Number,
  help_requested: Boolean,
  tasks: {
    type: Array,
    required: true
  }
})

const emits = defineEmits(['idxChange', 'raisedHand'])

const index = ref(0)
const questionAsked = ref(props.help_requested)
const dataStore = useDataStore()

const exercise = ref(props.current_exercise)
watch(
  () => props.help_requested,
  (newVal) => {
    questionAsked.value = newVal
  }
)

watch(
  () => props.current_exercise,
  (newVal) => {
    exercise.value = newVal
  }
)

const nextTask = () => {
  // index.value = (index.value + 1) % props.tasks.length
  let nextIndex = (exercise.value + 1) % props.tasks.length;
  if (props.tasks[nextIndex]) { // Überprüfen, ob der Index gültig ist
    exercise.value = nextIndex;
    console.log('exercise', exercise.value);
    emits('idxChange', exercise.value);
  }
}

const previousTask = () => {
  // index.value = (index.value - 1 + props.tasks.length) % props.tasks.length
  let previousIndex = (exercise.value - 1 + props.tasks.length) % props.tasks.length;
  if (props.tasks[previousIndex]) { // Überprüfen, ob der Index gültig ist
    exercise.value = previousIndex;
    console.log('exercise', exercise.value);
    emits('idxChange', exercise.value);
  }
}

const toggleQuestion = () => {
  dataStore.updateUserField('help_requested', !dataStore.user.help_requested)
  // questionAsked.value = dataStore.user.help_requested;
  emits('raisedHand')
  questionAsked.value = !questionAsked.value
}

watchEffect(() => {
  console.log('Aktuelle Aufgabe:', props.tasks[exercise.value]);
});


</script>

<
<template>
  <div class="w-full h-full">
    <div class="carousel h-full w-full">
      <div id="slide1" class="carousel-item relative justify-center item-center w-full h-full">
        <div class="flex w-3/4 h-[580px] w-[850px]">
          <div class="mx-20 w-full">
            <div class="flex justify-between">
              <h1 class="text-2xl my-10">Aufgabe {{ exercise + 1 }} / {{ props.tasks.length }}</h1>
              <button
                @click="toggleQuestion"
                :class="['btn', 'btn-accent', 'text-2xl', !questionAsked && 'btn-outline']"
              >
                ✋🏼
              </button>
            </div>
            <p>
              <div v-html="props.tasks[exercise] ? props.tasks[exercise].replace(/(\\n|\n)/g, '<br><br>') : 'Laden...'"></div>
              <!-- <div v-html="props.tasks[exercise].replace(/(\\n|\n)/g, '<br><br>')"></div> -->
            </p>
          </div>
        </div>
      </div>
    </div>
    <div class="absolute flex justify-between transform -translate-y-1/2 left-1 right-1 top-1/2">
      <a v-if="exercise > 0" @click="previousTask" class="btn btn-circle btn-accent ml-4">❮</a>
      <a v-else class="btn btn-circle" style="visibility: hidden">❮</a>
      <a
        v-if="exercise < props.tasks.length - 1"
        @click="nextTask"
        class="btn btn-circle btn-accent mr-4"
        >❯</a
      >
    </div>
  </div>
</template>
