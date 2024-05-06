<script setup>
import { defineProps, computed } from 'vue'
const props = defineProps(
    {
        name: String,
        seat: String,
        maxTasks: Number,
        finishedTasks: Number
    }
)

const progress = computed(() => {
    return (props.finishedTasks / props.maxTasks) * 100
})
</script>
<template>
<!-- 30 -> Base / 8 -> Anzahl Karten -->
<!-- 20 -> Base / 5 -> Anzahl Karten -->
  <div class="card w-[15rem] h-[8rem] overflow-hidden bg-primary text-primary-content my-2 mr-3">
    <div class="p-3">
      <div class="flex flex-row justify-between">
        <div class="mt-4">
          <h2 class="card-title text-lg">{{ seat }}</h2>
          <h2 class="card-title">{{ name }}</h2>
        </div>
        <div>
          <div class="radial-progress" :style="`--value: ${progress}`" role="progressbar">{{ progress }}%</div>
          <!--<h2>{{ finishedTasks }} / {{ maxTasks }}</h2>-->
        </div>
      </div>
    </div>
  </div>
</template>

