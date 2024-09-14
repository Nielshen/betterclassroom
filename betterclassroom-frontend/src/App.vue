<script setup>
import axios from 'axios'
import { ref } from 'vue'
import Navbar from './components/Navbar.vue'
import Sidebar from './components/Sidebar.vue'

const students = ref([])

const fetchStudents = async () => {
  try {
    const response = await axios.get('http://better-classroom.com:8088/api/students')
    console.log("Daten empfangen:", response.data);
    students.value = response.data
  } catch (error) {
    console.error("Error fetching students:", error)
  }
}
</script>

<template>
  <Navbar />
  <Sidebar />
  <notifications width="350px" position="top center" classes="my-notification" />
</template>

