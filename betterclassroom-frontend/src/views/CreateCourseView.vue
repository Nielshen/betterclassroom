<script setup>

import { ref } from 'vue';

const { oldCourse } = defineProps({
    oldCourse: Object
});

const title = ref(oldCourse ? 'Kurs bearbeiten' : 'Kurs erstellen');
const courseName = ref(oldCourse ? oldCourse.courseName : '');
const courseDescription= ref(oldCourse ? oldCourse.courseDescription: '');

</script>

<template>
    <div class="flex flex-col w-2/3">
        <h1 class="text-2xl my-10">Kurs erstellen</h1>
        <input type="text" placeholder="Kursname" class="input input-bordered input-accent w-full max-w-xs my-5"
            v-model="courseName" />
        <textarea class="textarea textarea-accent my-5 overflow-auto" placeholder="Beschreibung des Kurs"
            style="min-height: 300px;" v-model="courseDescription"></textarea>
        <button class="btn btn-primary" @click="save">Erstellen</button>
    </div>
</template>