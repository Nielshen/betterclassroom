<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  tasks: {
    type: Array,
    required: true
  }
});

const emits = defineEmits(['idxChange', 'raisedHand'])

const index = ref(0)

const nextTask = () => {
  index.value = (index.value + 1) % props.tasks.length
  emits('idxChange', index.value)
}

const previousTask = () => {
  index.value = (index.value - 1 + props.tasks.length) % props.tasks.length
  emits('idxChange', index.value)
}

const questionAsked = ref(false)

const toggleQuestion = () => {
  questionAsked.value = !questionAsked.value
  emits('raisedHand', questionAsked.value)
}
</script>

<template>
  <div class="carousel w-full h-full">
    <div id="slide1" class="carousel-item relative w-full">
      <div class="mx-20">
        <h1 class="text-2xl my-10">Aufgabe {{ index + 1 }} / {{ props.tasks.length }}</h1>
        <p>
          {{ props.tasks[index] }}
        </p>
      </div>
      <div class="absolute flex justify-between transform -translate-y-1/2 left-5 right-5 top-1/2">
        <a @click="previousTask" class="btn btn-circle btn-accent">❮</a>
        <a @click="nextTask" class="btn btn-circle btn-accent">❯</a>
      </div>
      <button
        @click="toggleQuestion"
        :class="['btn', 'btn-accent', 'm-4', 'text-2xl', !questionAsked && 'btn-outline']"
      >
        ✋🏼
      </button>
    </div>
  </div>
</template>