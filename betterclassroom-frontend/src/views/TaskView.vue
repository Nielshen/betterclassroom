<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  help_requested: Boolean,
  tasks: {
    type: Array,
    required: true
  }
})

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

const questionAsked = ref(props.help_requested)

const toggleQuestion = () => {
  questionAsked.value = !questionAsked.value
  emits('raisedHand', questionAsked.value)
}

watch(
  () => props.help_requested,
  console.log('Property help changed:', props.help_requested),
  (newVal) => {
    questionAsked.value = newVal
  }
)


</script>

<template>
  <div class="w-full h-full">
    <div class="carousel h-full w-full">
      <div id="slide1" class="carousel-item relative justify-center item-center w-full h-full ">
        <div class="flex w-2/3 h-[580px] w-[850px]">
          <div class="mx-20 w-2/3">
            <h1 class="text-2xl my-10">Aufgabe {{ index + 1 }} / {{ props.tasks.length }}</h1>
            <p>
              <div v-html="props.tasks[index].replace(/\\n/g, '<br><br>')"></div>
            </p>
          </div>
        </div> <!-- Add closing div tag here -->
        <button @click="toggleQuestion"
          :class="['btn', 'btn-accent', 'text-2xl', !questionAsked && 'btn-outline']">
          ✋🏼
        </button>
      </div>
    </div>
    <div class="absolute flex justify-between transform -translate-y-1/2 left-1 right-1 top-1/2">
      <a v-if="index > 0" @click="previousTask" class="btn btn-circle btn-accent ml-4">❮</a>
      <a v-else class="btn btn-circle" style="visibility: hidden;">❮</a>
      <a v-if="index < props.tasks.length - 1" @click="nextTask" class="btn btn-circle btn-accent mr-4">❯</a>
    </div>
  </div>
</template>
