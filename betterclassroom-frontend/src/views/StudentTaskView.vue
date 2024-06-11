<script setup>
import { onBeforeMount, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useRoute } from 'vue-router'
import TaskView from './TaskView.vue'
import axios from 'axios'
import { v4 as uuidv4 } from 'uuid'
import { getApiUrl } from '@/utils/common'


const route = useRoute()

const courseId = route.params.courseId
const exerciseId = route.params.taskId

const description = ref('')
const tasks = ref([])

const rawUrl = getApiUrl()
const api_url = `http://${rawUrl}/api`

const loadTasks = async () => {
  const response = await axios.get(`${api_url}/course/${courseId}/exercise`)
  const _tasks = response.data
  //console.log({ t: _tasks, exerciseId })
  const currentTask = _tasks.find((task) => task.id === exerciseId)
  //console.log({ currentTask })

  description.value = currentTask.description
  const exercises = currentTask.exercises.map((e) => e.description)
  //console.log(exercises)
  tasks.id = currentTask.exercises.map((e) => e.id)
  console.log(tasks.id)
  tasks.value = exercises
}

const changeIndex = async (index) => {
  const data = {
    current_exercise: index + 1
  }
  const response = await axios.post(`${api_url}/students/${studentName.value}/progress`, {
    ...data
  })
  console.log('Index changed', index + 1)
}

const raisedHand = async (value) => {
  console.log('Hand raised', value)
  const response = await axios.post(`${api_url}/students/${studentName.value}/help`, {})
  console.log(response)
}

const isAuth = ref(false)

const seat = ref('')
const studentName = ref('')

const studentAuth = async () => {
  const course = courseId
  try {
    const result = await axios.post(`${api_url}/students`, {
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

const width = ref(-1)
const height = ref(-1)

const loadClassroom = async () => {
  const { data } = await axios.get(`${api_url}/classroom`)
  //console.log({ classroomData: data })
  const course = await axios.get(`${api_url}/course`)
  const { classroom } = course.data.find((c) => c._id === courseId)
  const currentRoom = data.find((room) => room._id === classroom) || {}
  width.value = currentRoom.tablesPerRow * 2 || 8
  height.value = currentRoom.rows || 5
}

const clickOnSeat = (event) => {
  const id = event.target.id
  seat.value = id
}

const getSeat = (n, m, width, print = true) => {
  return (n * width + m) + 1
}

const w_ = computed(() => Array.from({ length: width.value }, (_, i) => i))
const h_ = computed(() => Array.from({ length: height.value }, (_, i) => i))


onBeforeMount(async () => {
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
          <input type="text" v-model="studentName" placeholder="Name" class="input input-bordered m-2 max-w-xs" />
          <input type="text" v-model="seat" placeholder="Sitzplatz" class="input input-bordered m-2 max-w-xs" />
        </div>
        <div class="border">
          <div class="flex flex-col justify-center items-center">
            <div class="rounded-lg w-full h-[55px] mt-5 mb-5 bg-primary text-center text-white">
              <p class="text-xl">Tafel</p>
            </div>
            <div v-for="n in h_" :key="n" class="flex flex-row justify-center">
              <div :id="getSeat(n, m, width, false)" v-for="m in w_" :key="m"
                class="rounded-lg w-[75px] h-[55px] bg-primary m-1 hover:bg-secondary hover:text-black text-l text-center text-white"
                @click="clickOnSeat">
                {{ getSeat(n, m, width) }}
              </div>
            </div>
          </div>
        </div>
        <button @click="studentAuth" class="btn btn-primary">Bestätigen</button>
      </div>
    </div>
    <div v-else class="h-full">
      <TaskView :tasks="tasks" @idxChange="changeIndex" @raisedHand="raisedHand" />
    </div>
  </div>
</template>