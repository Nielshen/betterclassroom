<script setup>
import { defineProps, computed, ref } from 'vue'
const props = defineProps(
    {
        name: String,
        seat: String,
        maxTasks: Number,
        raisedHand: Boolean,
        finishedTasks: Number,
    }
)

const raisedHand = ref(props.raisedHand)

const progress = computed(() => {
    return (props.finishedTasks / props.maxTasks) * 100
})
</script>

<template>
    <div>
        <div :class="['radial-progress', raisedHand ? 'text-error' : 'text-base-100']" :style="`--value: ${progress}`" role="progressbar">{{ finishedTasks }} / {{ maxTasks }}</div>
    </div>
</template>