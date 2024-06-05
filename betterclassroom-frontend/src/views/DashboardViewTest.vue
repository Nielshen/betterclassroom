<script setup>
import { onBeforeMount, ref } from 'vue'
import DashboardTable from '../components/DashboardTable.vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { io } from 'socket.io-client'

const route = useRoute()
const router = useRouter()

const courseId = route.params.courseId
const exerciseId = route.params.taskId /*Exercise ID*/

let tableOccupation = ref([])

const apiUrl = import.meta.env.VITE_API_PROD_URL

const loadCourse = async () => {
  try {
    const courseResponse = await axios.get(`${apiUrl}/course/${courseId}`)
    const currentCourse = courseResponse.data

    const courseStudentsResponse = await axios.get(`${apiUrl}/course/${courseId}/students`)
    const courseStudents = courseStudentsResponse.data

    const classroomResponse = await axios.get(`${apiUrl}/classroom/${currentCourse.classroom}`)
    const classroom = classroomResponse.data

    const tableCount = classroom.rows * classroom.tablesPerRow

    const tableOccupancy = Array(tableCount).fill().map(() => ({ student1: null, student2: null }))

    courseStudents.forEach((student) => {
      const tableIndex = student.table - 1
      console.log({ "tableIndex": tableIndex })
      if (tableIndex >= 0 && tableIndex < tableOccupancy.length) {
        const table = tableOccupancy[tableIndex]

        if (!table.student1) {
          table.student1 = student
        } else if (!table.student2) {
          table.student2 = student
        } else {
          console.error('Table is full')
        }
      }
    })

    tableOccupation.value = tableOccupancy || []
  } catch (error) {
    console.error('Error loading course data:', error)
  }
}

onBeforeMount(async () => {
  await loadCourse()
  initSockets()
  console.log("test")
  console.log({ tableOccupation: tableOccupation.value })
})


const initSockets = () => {
  const socket = io('ws://localhost:5000/student', {
    path: '/api/socket.io',
    transports: ['websocket']
  })

  socket.on('connect', () => {
    console.log('Connected to server')
  })

  socket.on('disconnect', () => {
    console.log('Disconnected from server')
  })

  socket.on('help', (data) => {
    console.log('Help requested', data.data)

    // Update the tableOccupation based on the received data
    const studentIndex = data.data.table - 1
    tableOccupation.value[studentIndex].student1.help_requested = data.data.help_requested;
    console.log(tableOccupation.value[studentIndex].student1)
  })

  socket.on('progress', (data) => {
    console.log('Progress updated', data.data)

    // Update the tableOccupation based on the received data
    const studentIndex = data.data.table - 1
    tableOccupation.value[studentIndex].student1.progress = data.data.progress;
    console.log(tableOccupation.value[studentIndex].student1)
  })
}

</script>
<template>
  <div>
    <div class="flex justify-end m-4">
      <button class="btn btn-warning">Beenden</button>
    </div>
    <div class="flex flex-row ">
      <div class="flex flex-col justify-center m-4">
        <div class="flex flex-row flex-wrap justify-center">
          <DashboardTable v-for="table in tableOccupation" :tableNumber="table.id" :table="table" />
        </div>
      </div>
    </div>
  </div>
</template>
