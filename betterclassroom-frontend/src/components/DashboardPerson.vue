<script setup>
import { defineProps, computed, ref, watch } from 'vue'
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
const studentFinishedTasks = ref(props.finishedTasks)
const studentMaxTasks = ref(props.maxTasks)

const progress = computed(() => {
    return (studentFinishedTasks.value / studentMaxTasks.value) * 100
})

watch(() => props.raisedHand, (newVal) => {
    studentRaisedHand.value = newVal
})

watch(() => props.finishedTasks, (newVal) => {
    studentFinishedTasks.value = newVal
})


</script>

<template>
    <div>
        <p v-if="studentRaisedHand">👋</p>
        <p v-else>-</p>
        <div :class="['radial-progress', studentRaisedHand ? 'text-error' : 'text-base-100']"
            :style="`--value: ${progress}`" role="progressbar">{{ finishedTasks }} / {{ maxTasks }}</div>
        <!-- <p>{{studentName}}</p> -->
    </div>

</template>