<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();


const toStudent = () => router.push('/student');
const toProf = () => router.push('/prof');

</script>


<template>
  <div class="flex justify-center items-center">
    <button class="btn">Ich bin Student</button>
    <button class="btn">Ich bin Dozent</button>
  </div>
</template>
