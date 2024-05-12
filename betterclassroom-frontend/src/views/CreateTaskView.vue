<script setup>

import { ref } from 'vue';

const { oldTasks } = defineProps({
    oldTasks: Object
});

const title = ref(oldTasks ? 'Aufgabe bearbeiten' : 'Aufgaben erstellen');
const taskName = ref(oldTasks ? oldTasks.taskName : '');
const taskDescription = ref(oldTasks ? oldTasks.taskDescription : '');

</script>

<template>
    <div class="flex flex-col w-2/3">
        <h1 class="text-2xl my-10">Aufgaben erstellen</h1>
        <input type="text" placeholder="Aufgabenname" class="input input-bordered input-accent w-full max-w-xs my-5"
            v-model="taskName" />
        <textarea class="textarea textarea-accent my-5 overflow-auto" placeholder="Beschreibung der Aufgabe"
            style="min-height: 300px;" v-model="taskDescription"></textarea>
        <button class="btn btn-primary" @click="save">Erstellen</button>
    </div>
</template>