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
    <div>
        <div class="radial-progress" :style="`--value: ${progress}`" role="progressbar">{{ finishedTasks }} / {{ maxTasks }}</div>
    </div>
</template>