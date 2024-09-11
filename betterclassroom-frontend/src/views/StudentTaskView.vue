<script setup>
import {computed, onBeforeMount, ref} from 'vue'
import {useRoute} from 'vue-router'
import TaskView from './TaskView.vue'
import axios from 'axios'
import {getApiUrl} from '@/utils/common'
import {io} from 'socket.io-client'
import {useDataStore} from '../stores/dataStore'

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
const classroomId = ref('')

const width = ref(-1)
const height = ref(-1)

const w_ = computed(() => Array.from({length: width.value}, (_, i) => i))
const h_ = computed(() => Array.from({length: height.value}, (_, i) => i))

const loadTasks = async () => {
  const response = await axios.get(`${api_url}/course/${courseId}/exercise/${exerciseId}`)
  const exerciseData = response.data
  description.value = exerciseData.description
  dataStore.updateTasks(exerciseData)
}

const changeIndex = async (index) => {
  socket.emit(
      'update_progress',
      {id: dataStore.user.id, current_exercise: index},
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
  socket.emit('help', {id: dataStore.user.id}, function (response) {
    if (response.error) {
      console.error('Fehler beim Anfordern von Hilfe:', response.error)
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
  if (studentName.value === '' || seat.value === '') {
    console.error('Name oder Sitzplatz nicht ausgefüllt')
    alert('Bitte füllen Sie alle Felder aus')
    return
  }

  socket.emit(
      'student_register',
      {course: courseId, exercise: exerciseId, student: studentName.value},
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
      alert("Student with this name already exists")
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
  socket.emit('delete_student', {id: dataStore.user.id}, function (response) {
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
    if (Object.keys(user).length !== 0) {
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
  try {
    const {data: courses} = await axios.get(`${api_url}/course`)
    const course = courses.find((c) => c._id === courseId)

    if (course && course.classroom) {
      const {data: classroom} = await axios.get(`${api_url}/classroom/${course.classroom}`)
      classroomId.value = classroom._id
      width.value = classroom.tablesPerRow
      height.value = classroom.rows
    } else {
      console.error('Classroom ID not found in the course')
    }
  } catch (error) {
    console.error('Error loading classroom:', error)
  }
}


const clickOnSeat = async (event) => {
  const id = event.target.id.split('-');
  const tableId = id[0];
  const seatSide = id[1];

  seat.value = id.join('-');
  console.log(classroomId.value, tableId, seatSide);

  try {
    const getResponse = await axios.get(`${api_url}/classroom/${classroomId.value}/table/${tableId}/${seatSide}/occupied`);
    console.log('getResponse:', getResponse.data);
    const isOccupied = getResponse.data.occupied;

    if (isOccupied === true) {
      alert(`The seat on ${seatSide} side of table ${tableId} is already occupied.`);
    } else {
      const putResponse = await axios.post(`${api_url}/classroom/${classroomId.value}/table/${tableId}/${seatSide}`, {
        occupied: true
      });
      console.log('putResponse:', putResponse.data);
    }
  } catch (error) {
    console.error("Test test test Error updating seat status:", error);
  }
}

const getSeat = (n, m, seat) => {
  return `${n * width.value + m + 1}-${seat}`
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
      {course: courseId, exercise: exerciseId, student: student_id.value},
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
  await loadClassroom()
  await loadTasks()
})
</script>

<template>
  <div class="h-full">
    <div v-if="!isAuth">
      <div class="flex flex-col justify-center items-center mt-5">
        <div>
          <input
              v-model="studentName"
              class="input input-bordered m-2 max-w-xs"
              placeholder="Name"
              type="text"
          />
          <input
              v-model="seat"
              class="input input-bordered m-2 max-w-xs"
              placeholder="Sitzplatz"
              type="text"
          />
        </div>
        <div class="border">
          <div class="flex flex-col justify-center items-center">
            <div class="rounded-lg w-full h-[55px] mt-5 mb-5 bg-primary text-center text-white">
              <p class="text-xl">Tafel</p>
            </div>
            <div v-for="n in h_" :key="n" class="flex flex-row justify-center">
              <div
                  v-for="m in w_"
                  :key="m"
                  class="relative rounded-lg w-[200px] h-[80px] bg-primary text-white text-center m-2 p-2"
              >
                <div
                    :id="getSeat(n, m, 'L')"
                    class="absolute top-1/2 left-4 transform -translate-y-1/2 w-[60px] h-[40px] border border-gray-300 rounded-md bg-transparent cursor-pointer hover:bg-gray-200"
                    @click="clickOnSeat"
                ></div>
                <div
                    :id="getSeat(n, m, 'R')"
                    class="absolute top-1/2 right-4 transform -translate-y-1/2 w-[60px] h-[40px] border border-gray-300 rounded-md bg-transparent cursor-pointer hover:bg-gray-200"
                    @click="clickOnSeat"
                ></div>
              </div>
            </div>
          </div>
        </div>
        <button class="btn btn-primary" @click="studentAuth">Bestätigen</button>
      </div>
    </div>
    <div v-else class="h-full">
      <div class="flex flex-row justify-between items-start my-2">
        <h1 class="text-base font-medium ml-6 mt-1">{{ dataStore.user.id }}</h1>
        <button v-if="isAuth" class="btn btn-primary mr-6 mt-1" @click="deleteStudent">Abmelden</button>
      </div>
      <TaskView v-if="isAuth" :key="student_id" @idxChange="changeIndex" @raisedHand="raisedHand"/>
    </div>
  </div>
</template>

