<script setup>
import { computed, onBeforeMount, ref } from 'vue'
import DashboardTable from '../components/DashboardTable.vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { io } from 'socket.io-client'
import QRCode from 'qrcode'
import { getApiUrl } from '@/utils/common'

const route = useRoute()
const router = useRouter()

const courseId = route.params.courseId
const exerciseId = route.params.taskId

const rawUrl = getApiUrl()
const api_url = `http://${rawUrl}/api`
const wsUrl = `ws://${rawUrl}/student`

let tableOccupation = ref([])
const courseLink = ref('')
const exerciseCount = ref(0)
const fullLink = computed(() => `http://${courseLink.value}`)
const showFullLink = ref(false)
const showNames = ref(true)


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
      const [tableNumber, side] = student.table.split('-')
      const tableIndex = parseInt(tableNumber) - 1
      
      if (tableIndex >= 0 && tableIndex < tableOccupancy.length) {
        const table = tableOccupancy[tableIndex]
        
        if (side === 'L' && !table.student1) {
          table.student1 = student
        } else if (side === 'R' && !table.student2) {
          table.student2 = student
        } else {
          console.error('Table side is already occupied. Student cannot be added:', table, student)
        }
      } else {
        console.error('Invalid table index:', tableIndex, 'for student:', student)
      }
    })

    tableOccupation.value = tableOccupancy
  } catch (error) {
    console.error('Error loading course data:', error)
  }
}

const handleStudentUpdate = (data) => {
  console.log('Handle student update', data)

  const tableNumber = parseInt(data.table.slice(0, -1), 10)
  const seatSide = data.table.slice(-1)

  const studentIndex = tableNumber - 1
  if (studentIndex < 0 || studentIndex >= tableOccupation.value.length) {
    console.error('Invalid table index')
    return
  }

  const table = tableOccupation.value[studentIndex]

  const studentKey = seatSide === 'L' ? 'student1' : 'student2'

  if (data.action === 'add') {
    if (!table[studentKey] || table[studentKey]._id === data._id) {
      table[studentKey] = data
    } else {
      console.error('All slots at table are full. Cannot add student:', data)
    }
  } else if (data.action === 'delete') {
    if (table[studentKey] && table[studentKey]._id === data._id) {
      table[studentKey] = null
    } else {
      console.error('Student not found at table:', data)
    }
  }
}

const updateStudentProperty = (data, property) => {
  console.log('Updating student property:', data, property)

  const tableNumber = parseInt(data.table.slice(0, -1), 10)
  const seatSide = data.table.slice(-1)

  const studentIndex = tableNumber - 1
  if (studentIndex < 0 || studentIndex >= tableOccupation.value.length) {
    console.error('Invalid table index')
    return
  }

  const table = tableOccupation.value[studentIndex]

  const studentKey = seatSide === 'L' ? 'student1' : 'student2'

  if (table[studentKey] && table[studentKey]._id === data._id) {
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

function copyToClipboard(text) {
  let copied = false;

  // Try using navigator.clipboard
  if (navigator.clipboard && window.isSecureContext) {
    console.log('Using navigator.clipboard')
    navigator.clipboard.writeText(text);
    copied = true;
  } else {
    // Fallback to execCommand
    console.log('Using execCommand')
    const textArea = document.createElement("textarea");
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.select();
    try {
      copied = document.execCommand('copy');
    } catch (err) {
      copied = false;
    }
    document.body.removeChild(textArea);
  }

  // If both methods failed, prompt user
  if (!copied) {
    window.prompt("Copy this link:", text);
  }

  return copied;
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

const toggleShowNames = () => {
  showNames.value = !showNames.value
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
  <div class="flex flex-col h-screen">

    <div class="flex m-4 justify-between sm:space-x-3">
      <div class="flex items-center text-sm sm:text-base">
        <div class="relative group mx-1">
          <button
            :href="fullLink"
            class="btn btn-danger hover:underline"
            @click="copyToClipboard(fullLink)"
            @mouseenter="showFullLink = true"
            @mouseleave="showFullLink = false"
          >
            Kurslink
          </button>
          <span
            v-if="showFullLink"
            class="sm:text-base absolute left-0 top-full mt-2 w-auto p-2 bg-gray-800 text-white text-xs rounded-md z-10 whitespace-nowrap"
          >
            {{ fullLink }}
          </span>
        </div>
        <button class="btn btn-danger ml-2" @click="generateQRCode">QR-Code</button>
      </div>
      <button class="btn btn-warning" @click="router.push(`/editTask/${courseId}/${exerciseId}`)">
        Aufgaben bearbeiten
      </button>
    </div>

    <div class="flex-grow flex flex-col">
      <div class="flex-grow container mx-auto px-4" style="max-width: 1300px;">
        <div class="grid grid-cols-4 gap-4 justify-center">
          <DashboardTable
            v-for="table in tableOccupation"
            :key="table.id"
            :exerciseCount="exerciseCount"
            :table="table"
            :tableNumber="table.id"
            :showNames="showNames"
            class="w-full max-w-[300px]"
          />
        </div>
          <div class="rounded-lg w-full h-[55px] mt-5 mb-5 bg-primary text-center text-white flex items-center justify-center">
            <p class="text-4xl">Tafel</p>
          </div>
      </div>

      <div class="flex justify-between items-center px-4 py-4">
        <button class="btn btn-danger" @click="toggleShowNames">Namen anzeigen</button>
        <button class="btn btn-warning" @click="closeCourse">Beenden</button>
      </div>
    </div>
    
  </div>
</template>