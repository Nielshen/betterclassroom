<script setup>
import { onBeforeMount, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import TaskView from './TaskView.vue'
import axios from 'axios'
import { getApiUrl } from '@/utils/common'
import { io } from 'socket.io-client'
import { useDataStore } from '../stores/dataStore'

const dataStore = useDataStore()
const route = useRoute()

const courseId = route.params.courseId
const exerciseId = route.params.taskId

const rawUrl = getApiUrl()
const api_url = `http://${rawUrl}/api`
const wsUrl = `ws://${rawUrl}/student`

let socket = null

const description = ref('')
const isAuth = ref(false)
const seat = ref('')
const studentName = ref('')
const student_id = ref('')
const current_exercise = ref(0)
const help_requested = ref(false)
const width = ref(-1)
const height = ref(-1)
const w_ = computed(() => Array.from({ length: width.value }, (_, i) => i))
const h_ = computed(() => Array.from({ length: height.value }, (_, i) => i))

const loadTasks = async () => {
  const response = await axios.get(`${api_url}/course/${courseId}/exercise/${exerciseId}`)
  const exerciseData = response.data
  description.value = exerciseData.description
  dataStore.updateTasks(exerciseData)
}

const changeIndex = async (index) => {
  socket.emit(
    'update_progress',
    { id: dataStore.user.id, current_exercise: index},
    function (response) {
      if (response.error) {
        console.error('Fehler beim Aktualisieren des Fortschritts:', response.error)
      } else {
        console.log('Fortschritt erfolgreich aktualisiert:', response.success, index + 1)
        dataStore.updateUserField('current_exercise', index)
        current_exercise.value = index
      }
    }
  )
}

const raisedHand = async () => {
  socket.emit('help', { id: dataStore.user.id }, function (response) {
    if (response.error) {
      console.error(
        'Fehler beim Anfordern von Hilfe:',
        response.error,
        dataStore.user.id,
        dataStore.user.help_requested
      )
    } else {
      console.log(
        'Hilfe erfolgreich angefordert:',
        response.success,
        dataStore.user.id,
        dataStore.user.help_requested
      )
    }
  })
}

const studentAuth = () => {
  const studentData = {
    id: studentName.value,
    table: seat.value,
    course: courseId,
    exercise: exerciseId
  }
  socket.emit(
    'student_register',
    { course: courseId, exercise: exerciseId, student: studentName.value },
    function (response) {
      if (response.error) {
        console.error('Fehler beim Registrieren:', response.error)
      } else {
        console.log('Erfolgreich registriert:', response.success)
      }
    }
  )

  console.log('Emitting new_student', studentData)
  socket.emit('new_student', studentData, function (response) {
    if (response.error) {
      console.error('Fehler beim Hinzufügen des Studenten:', response.error)
      isAuth.value = false
    } else {
      console.log('Student erfolgreich hinzugefügt:', response.success)
      dataStore.saveStudentLocally(studentData)
      console.log('studentAuth: student_id ref:', dataStore.user.id)
      student_id.value = dataStore.user.id
      isAuth.value = true
    }
  })
}

const deleteStudent = () => {
  socket.emit('delete_student', { id: dataStore.user.id }, function (response) {
    if (response.error) {
      console.error('Fehler beim Löschen des Studenten:', response.error)
    } else {
      console.log('Student erfolgreich gelöscht:', response.success)
    }
    dataStore.deleteStudentLocally()
    isAuth.value = false
    student_id.value = ''
    help_requested.value = false
    current_exercise.value = 0
  })
}

const loadUser = () => {
  if (dataStore.checkUser()) {
    console.log('User is authenticated')
    const user = dataStore.readUser()
    if (Object.keys(user).length != 0) {
      console.log('Loaded user from sessionStorage:', user)
      student_id.value = user.id
      help_requested.value = user.help_requested
      current_exercise.value = user.current_exercise
      isAuth.value = true
      reregisterSocket()
    }
  } else {
    console.log('User not authenticated', isAuth.value)
    dataStore.initStudent()
    isAuth.value = false
  }
}

const loadClassroom = async () => {
  const { data } = await axios.get(`${api_url}/classroom`)
  const course = await axios.get(`${api_url}/course`)
  const { classroom } = course.data.find((c) => c._id === courseId)
  const currentRoom = data.find((room) => room._id === classroom) || {}
  width.value = currentRoom.tablesPerRow || 4
  height.value = currentRoom.rows || 5
}

const clickOnSeat = (event) => {
  const id = event.target.id
  seat.value = id
}

const getSeat = (n, m, width, print = true) => {
  return n * width + m + 1
}

const initSocket = () => {
  socket = io(wsUrl, {
    path: '/api/socket.io/student',
    transports: ['websocket']
  })

  socket.on('connect', () => {
    console.log('Connected to Socket')
  })

  socket.on('disconnect', () => {
    console.log('Disconnected from Socket')
  })

  socket.on('help', (data) => {
    console.log('Socket Event: Help requested', data.data.help_requested, data.data._id)
    dataStore.updateUserField('help_requested', data.data.help_requested)
  })

  socket.on('alter_subexercise', (data) => {
    console.log('Socket Event: Subexercise description updated', data.data)
    dataStore.alterTask(data.data.subexercise_id, data.data.name, data.data.description)
  })

  socket.on('new_subexercise', (data) => {
    console.log('Socket Event: New subexercise added', data.data)
    dataStore.addNewSubexercise(data.data)
  })

  socket.on('delete_subexercise', (data) => {
    console.log('Socket Event: Subexercise deleted', data.data)
    dataStore.deleteSubexercise(data.data.subexercise_id)
  })
}

const reregisterSocket = () => {
  socket.emit(
    'student_register',
    { course: courseId, exercise: exerciseId, student: student_id.value },
    function (response) {
      if (response.error) {
        console.error('Fehler beim Registrieren:', response.error)
      } else {
        console.log('Erfolgreich registriert:', response.success)
      }
    }
  )
}

onBeforeMount(async () => {
  initSocket()
  loadUser()
  await loadTasks()
  await loadClassroom()
})
</script>
<template>
  <div class="h-full">
    <div v-if="!isAuth">
      <div class="flex flex-col justify-center items-center mt-5">
        <div>
          <input
            type="text"
            v-model="studentName"
            placeholder="Name"
            class="input input-bordered m-2 max-w-xs"
          />
          <input
            type="text"
            v-model="seat"
            placeholder="Sitzplatz"
            class="input input-bordered m-2 max-w-xs"
          />
        </div>
        <div class="border">
          <div class="flex flex-col justify-center items-center">
            <div class="rounded-lg w-full h-[55px] mt-5 mb-5 bg-primary text-center text-white">
              <p class="text-xl">Tafel</p>
            </div>
            <div v-for="n in h_" :key="n" class="flex flex-row justify-center">
              <div
                :id="getSeat(n, m, width, false)"
                v-for="m in w_"
                :key="m"
                class="rounded-lg w-[200px] h-[55px] cursor-pointer bg-primary m-1 hover:bg-secondary hover:text-black text-l text-center text-white"
                @click="clickOnSeat"
              >
                {{ getSeat(n, m, width) }}
              </div>
            </div>
          </div>
        </div>
        <button @click="studentAuth" class="btn btn-primary">Bestätigen</button>
      </div>
    </div>
    <div v-else class="h-full">
      <div class="flex flex-row justify-between items-start my-2">
        <h1 class="text-base font-medium ml-6 mt-1">{{ dataStore.user.id }}</h1>
        <button v-if="isAuth" @click="deleteStudent" class="btn btn-primary mr-6 mt-1">Abmelden</button>
      </div>
      <TaskView v-if="isAuth" :key="student_id" @idxChange="changeIndex" @raisedHand="raisedHand" />
    </div>
  </div>
</template>
