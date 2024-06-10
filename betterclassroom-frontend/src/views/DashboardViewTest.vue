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


const rawUrl = getApiUrl()
const api_url = `http://${rawUrl}/api`
const wsUrl = `ws://${rawUrl}/student`


const loadCourse = async () => {
  try {
    const courseResponse = await axios.get(`${api_url}/course/${courseId}`)
    const currentCourse = courseResponse.data

    const courseStudentsResponse = await axios.get(`${api_url}/course/${courseId}/students`)
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

onBeforeMount(async () => {
  await loadCourse()
  initSockets()
  console.log({ tableOccupation: tableOccupation.value })
  courseLink.value = `${window.location.host}/student/${courseId}/${exerciseId}`
})

const handleNewStudent = (data) => {
  const studentIndex = data.table - 1;
  if (studentIndex < 0 || studentIndex >= tableOccupation.value.length) {
    console.error('Invalid table index');
    return;
  }

  const table = tableOccupation.value[studentIndex]
  const studentKey = ['student1', 'student2'].find(key => table[key]?._id === data.id)

  if (studentKey) {
    table[studentKey] = data;
  } else {
    const emptyKey = ['student1', 'student2'].find(key => !table[key])
    if (emptyKey) {
      table[emptyKey] = data;
    } else {
      console.error('All slots at table are full. Cannot add student:', data)
    }
  }
};

const updateStudentProperty = (data, property) => {
  const studentIndex = data.table - 1;
  if (studentIndex < 0 || studentIndex >= tableOccupation.value.length) {
    console.error('Invalid table index');
    return;
  }

  const table = tableOccupation.value[studentIndex]
  const studentKey = ['student1', 'student2'].find(key => table[key]?._id === data.id)
  if (studentKey) {
    table[studentKey][property] = data[property]
  } else {
    console.error(`Updating student failed: Student not found for property ${property}`)
  }
};

const initSockets = () => {
  const socket = io(wsUrl, {
    path: '/api/socket.io/student',
    transports: ['websocket']
  });

  socket.on('connect', () => console.log('Connected to server'));
  socket.on('disconnect', () => console.log('Disconnected from server'));
  socket.on('help', data => updateStudentProperty(data.data, 'help_requested'));
  socket.on('progress', data => updateStudentProperty(data.data, 'progress'));
  socket.on('student', data => handleNewStudent(data.data));

};

const copyLink = () => {
  navigator.clipboard.writeText(courseLink.value).then(() => {
    console.log('Kurslink wurde in die Zwischenablage kopiert.');
  }).catch(err => {
    console.error('Fehler beim Kopieren des Kurslinks: ', err);
  });
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
    await axios.post(`${api_url}/course/${courseId}/close`)
    alert('Kurs wurde geschlossen und alle Studenten wurden abgemeldet.')
    router.push('/courses')
  } catch (error) {
    console.error('Error closing course:', error)
  }
}
</script>
<template>
  <div>
    <div class="flex justify-end m-4">
      <div class="flex items-center">
        Kurslink für Student*innen:&nbsp;<a :href="courseLink">{{ courseLink }}</a>
        <button class="btn btn-danger ml-2" @click="copyLink">Kopieren</button>
        <button class="btn btn-danger ml-2" @click="generateQRCode">QR-Code</button>
      </div>
      <button class="btn btn-warning" @click="closeCourse">Beenden</button>
    </div>
    <div class="flex flex-row">
      <div class="flex flex-col justify-center m-4">
        <div class="flex flex-row flex-wrap justify-center">
          <DashboardTable v-for="table in tableOccupation" :tableNumber="table.id" :table="table" />
        </div>
      </div>
    </div>
  </div>
</template>
