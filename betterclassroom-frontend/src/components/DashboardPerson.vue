<script setup>
import { defineProps, computed, ref } from 'vue'
const props = defineProps(
    {
        name: String,
        maxTasks: Number,
        raisedHand: Boolean,
        finishedTasks: Number,
    }
)

const studentName = ref(props.name)
const studentRaisedHand = ref(props.raisedHand)

const progress = computed(() => {
    return (props.finishedTasks / props.maxTasks) * 100
})
</script>

<template>
    <div>
        <p v-if="studentRaisedHand">👋</p>
        <p v-else>-</p>
        <div :class="['radial-progress', studentRaisedHand? 'text-error' : 'text-base-100']" :style="`--value: ${progress}`" role="progressbar">{{ finishedTasks }} / {{ maxTasks }}</div>
        <!-- <p>{{studentName}}</p> -->
    </div>
    
</template>