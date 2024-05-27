<script setup>
import { onBeforeMount, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useRoute } from 'vue-router'
import TaskView from './TaskView.vue'
import axios from 'axios'
import { v4 as uuidv4 } from 'uuid'

const route = useRoute()

const courseId = route.params.courseId
const exerciseId = route.params.taskId

const description = ref('')
const tasks = ref([])

const apiUrl = import.meta.env.VITE_API_PROD_URL
const loadTasks = async () => {
  const response = await axios.get(`${apiUrl}/course/${courseId}/exercise`)
  const _tasks = response.data
  console.log({ t: _tasks, exerciseId })
  const currentTask = _tasks.find((task) => task.id === exerciseId)
  console.log({ currentTask })

  description.value = currentTask.description
  const exercises = currentTask.exercises.map((e) => e.description)
  console.log(exercises)
  tasks.value = exercises
}

const changeIndex = async (index) => {
  const data = {}
  for (let i = 0; i < tasks.value.length; i++) {
    data[`Aufgabe${i + 1}`] = i <= index
  }
  const response = await axios.post(`${apiUrl}/students/${studentName.value}/progress`, {
    ...data
  })
  console.log('Index changed', index + 1)
}

const raisedHand = async (value) => {
  console.log('Hand raised', value)
  const response = await axios.post(`${apiUrl}/students/${studentName.value}/help`, {})
  console.log(response)
}

const isAuth = ref(false)

const seat = ref('')
const studentName = ref('')

const studentAuth = async () => {
  const course = courseId
  try {
    const result = await axios.post(`${apiUrl}/students`, {
      course,
      id: studentName.value,
      table: seat.value
    })
    console.log(result)
    localStorage.setItem('studentId', studentName.value)
  } catch (error) {
    console.log(error)
  }
  isAuth.value = true
}

const loadUser = () => {
  localStorage.getItem('studentId') ? (isAuth.value = true) : (isAuth.value = false)
  studentName.value = localStorage.getItem('studentId') || null
}

const width = ref(4)
const height = ref(10)

const loadClassroom = async () => {
  const { data } = await axios.get(`${apiUrl}/classroom`)
  console.log({ classroomData: data })
  const course = await axios.get(`${apiUrl}/course`)
  const { classroom } = course.data.find((c) => c._id === courseId)
  const currentRoom = data.find((room) => room._id === classroom) || {}
  width.value = currentRoom.tablesPerRow || 4
  height.value = currentRoom.rows || 10
}

const clickOnSeat = (event) => {
  const id = event.target.id
  seat.value = id
}

onBeforeMount(async () => {
  loadUser()
  await loadTasks()
  await loadClassroom()
})
</script>
<template>
  <div>
    <div v-if="!isAuth">
      <input type="text" v-model="studentName" placeholder="Name..." class="input" />
      <input type="text" v-model="seat" placeholder="Sitzplatz.." class="input" />
      <div class="border">
        <div class="flex flex-col justify-center items-center">
          <div class="flex  justify-end w-3/4">
            <div
              class="rounded-lg w-[30px] h-[20px] bg-primary m-[2px] hover:bg-secondary text-s text-center text-white"
            ></div>
          </div>
          <div v-for="n in width" :key="n" class="flex">
            <div
              :id="n * width + m"
              v-for="m in height"
              :key="m"
              class="rounded-lg w-[30px] h-[20px] bg-primary m-[2px] hover:bg-secondary text-s text-center text-white"
              @click="clickOnSeat"
            >
              {{ n * width + m }}
            </div>
          </div>
        </div>
      </div>
      <button @click="studentAuth" class="btn btn-primary">Bestätigen</button>
    </div>
    <div v-else>
      <TaskView :tasks="tasks" @idxChange="changeIndex" @raisedHand="raisedHand" />
    </div>
  </div>
</template>