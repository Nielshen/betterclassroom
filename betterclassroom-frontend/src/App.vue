<script setup>
import axios from 'axios'
import { ref } from 'vue'

const students = ref([])

const fetchStudents = async () => {
  try {
    // const response = await axios.get('http://better-classroom.com:8088/api/students')
    const response = await axios.get('http://better-classroom.com:8088/api/students')
    console.log("Daten empfangen:", response.data);
    students.value = response.data
  } catch (error) {
    console.error("Error fetching students:", error)
  }
}
</script>

<template>
  <button @click="fetchStudents">Get Students</button>
  <ul>
    <!-- Loop -->
    <li v-for="student in students" :key="student.id">{{ student.name }}</li>
  </ul>
</template>

<style scoped>
button {
  margin: 20px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
</style>
