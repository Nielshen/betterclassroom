<script setup>
import { onBeforeMount, ref } from 'vue'
import DashboardTable from '../components/DashboardTable.vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { io } from 'socket.io-client'
import QRCode from 'qrcode'
import { getApiUrl } from '@/utils/common'

const route = useRoute()
const router = useRouter()

const courseId = route.params.courseId
const exerciseId = route.params.taskId /*Exercise ID*/

let tableOccupation = ref([])
const courseLink = ref('')
const exerciseCount = ref(0)

const rawUrl = getApiUrl()
const api_url = `http://${rawUrl}/api`
const wsUrl = `ws://${rawUrl}/student`

const fetchExercisesCount = async () => {
  try {
    const response = await axios.get(`${api_url}/course/${courseId}/exercise/${exerciseId}`)
    console.log('fetchExercises:', response.data)
    exerciseCount.value = response.data.length
  } catch (error) {
    console.error('Error fetching exercises count:', error)
  }
}

const loadCourse = async () => {
  try {
    const courseResponse = await axios.get(`${api_url}/course/${courseId}`)
    const currentCourse = courseResponse.data

    const courseStudentsResponse = await axios.get(
      `${api_url}/course/${courseId}/exercise/${exerciseId}/students`
    )
    const courseStudents = courseStudentsResponse.data

    const classroomResponse = await axios.get(`${api_url}/classroom/${currentCourse.classroom}`)
    const classroom = classroomResponse.data

    const tableCount = classroom.rows * classroom.tablesPerRow

    const tableOccupancy = Array(tableCount)
      .fill()
      .map(() => ({ student1: null, student2: null }))

    courseStudents.forEach((student) => {
      const tableIndex = student.table - 1
      if (tableIndex >= 0 && tableIndex < tableOccupancy.length) {
        const table = tableOccupancy[tableIndex]

        if (!table.student1) {
          table.student1 = student
        } else if (!table.student2) {
          table.student2 = student
        } else {
          console.error('Table is full. Student cannot be added:', table, student)
        }
      }
    })

    tableOccupation.value = tableOccupancy || []
  } catch (error) {
    console.error('Error loading course data:', error)
  }
}

const handleStudentUpdate = (data) => {
  console.log('Handle student update', data)
  const studentIndex = data.table - 1
  if (studentIndex < 0 || studentIndex >= tableOccupation.value.length) {
    console.error('Invalid table index')
    return
  }

  const table = tableOccupation.value[studentIndex]

  if (data.action === 'add') {
    const studentKey = ['student1', 'student2'].find(
      (key) => !table[key] || table[key]._id === data._id
    )

    if (studentKey) {
      table[studentKey] = data
    } else {
      console.error('All slots at table are full. Cannot add student:', data)
    }
  } else if (data.action === 'delete') {
    const studentKey = ['student1', 'student2'].find((key) => table[key]?._id === data._id)
    if (studentKey) {
      table[studentKey] = null
    } else {
      console.error('Student not found at table:', data)
    }
  }
}

const updateStudentProperty = (data, property) => {
  console.log('Updating student property:', data, property)
  const studentIndex = data.table - 1
  if (studentIndex < 0 || studentIndex >= tableOccupation.value.length) {
    console.error('Invalid table index')
    return
  }

  const table = tableOccupation.value[studentIndex]
  const studentKey = ['student1', 'student2'].find(
    (key) => table[key] && table[key]._id === data._id
  )
  if (studentKey) {
    table[studentKey][property] = data[property]
  } else {
    console.error(`Updating student failed: Student not found for property ${property}`)
  }
}

const initSockets = () => {
  const socket = io(wsUrl, {
    path: '/api/socket.io/student',
    transports: ['websocket']
  })

  socket.emit(
    'dashboard_register',
    { course: courseId, exercise: exerciseId },
    function (response) {
      if (response.error) {
        console.error('Fehler beim Registrieren:', response.error)
      } else {
        console.log('Erfolgreich registriert:', response.success)
      }
    }
  )

  socket.on('connect', () => console.log('Connected to server'))
  socket.on('disconnect', () => console.log('Disconnected from server'))
  socket.on('help', (data) => updateStudentProperty(data.data, 'help_requested'))
  socket.on('progress', (data) => updateStudentProperty(data.data, 'current_exercise'))
  socket.on('student', (data) => handleStudentUpdate(data.data))
}

const generateQRCode = async () => {
  try {
    const qrCodeDataURL = await QRCode.toDataURL(courseLink.value)
    const qrCodeWindow = window.open()
    qrCodeWindow.document.write(`
      <html>
        <head>
          <title>${exerciseId}</title>
        </head>
        <body style="display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
          <img src="${qrCodeDataURL}" style="width: 250px; height: 250px;">
        </body>
      </html>
    `)
  } catch (err) {
    console.error(err)
  }
}
const closeCourse = async () => {
  try {
    await axios.delete(`${api_url}/course/${courseId}/exercise/${exerciseId}/students`)
    await axios.post(`${api_url}/course/${courseId}/exercise/${exerciseId}/close`)
    tableOccupation.value = []
    alert('Kurs wurde geschlossen und alle Studenten wurden abgemeldet.')
    router.push('/courses')
  } catch (error) {
    console.error('Error closing course:', error)
  }
}

onBeforeMount(async () => {
  await fetchExercisesCount()
  await loadCourse()
  console.log({ tableOccupation: tableOccupation.value })
  courseLink.value = `${window.location.host}/student/${courseId}/${exerciseId}`
  initSockets()
})
</script>
<template>
  <div class="flex flex-col min-h-screen max-h-screen">
    <div class="flex m-4 justify-between sm:space-x-3">
      <div class="flex items-center text-sm sm:text-base">
        Kurslink für Student*innen:&nbsp;<a :href="'http://' + courseLink">{{
          'http://' + courseLink
        }}</a>
        <button class="btn btn-danger ml-2" @click="generateQRCode">QR-Code</button>
      </div>
      <button class="btn btn-warning" @click="router.push(`/editTask/${courseId}/${exerciseId}`)">
        Aufgaben bearbeiten
      </button>
    </div>

    <div class="flex overflow-auto flex-row justify-center">
      <div class="flex flex-col justify-center m-4">
        <div
          class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-1 justify-items-center mx-auto"
        >
          <DashboardTable
            v-for="table in tableOccupation"
            :key="table.id"
            :exerciseCount="exerciseCount"
            :table="table"
            :tableNumber="table.id"
            class="w-full max-w-[18rem] h-[7rem] overflow-hidden bg-primary text-primary-content my-2 mr-3"
          />
        </div>
        <div
          class="rounded-lg w-full h-[55px] mt-5 mb-5 bg-primary text-center text-white flex items-center justify-center"
        >
          <p class="text-4xl">Tafel</p>
        </div>
      </div>
    </div>
    <div class="flex justify-end m-4">
      <button class="btn btn-warning" @click="closeCourse">Beenden</button>
    </div>
  </div>
</template>
