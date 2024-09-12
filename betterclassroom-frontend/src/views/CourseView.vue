<script setup>
import { onBeforeMount, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { getApiUrl } from '@/utils/common'

const router = useRouter()

const rawUrl = getApiUrl()
const api_url = `http://${rawUrl}/api`

const courseData = ref([])

const fetchCourses = async () => {
    const result = await axios.get(`${api_url}/course`)
    const data = result.data
    courseData.value = data
    console.log(courseData.value)
}

onBeforeMount(async () => {
    await fetchCourses()
})

const newCourse = () => router.push('/createCourse')

const editCourse = (e) => {
    const id = e._id
    router.push(`/createCourse/${id}`)
}

function getTotalParticipants(course) {
    if (!course.exercises || !Array.isArray(course.exercises)) {
        return 0
    }

    const totalParticipants = course.exercises.reduce((sum, exercise) => {
        if (exercise.participants && Array.isArray(exercise.participants)) {
            return sum + exercise.participants.length
        }
        return sum
    }, 0)

    return totalParticipants
}
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="course in courseData" :key="course.id" class="bg-white rounded-lg shadow-md overflow-hidden transition-transform duration-300 hover:shadow-lg hover:-translate-y-1">
        <div class="p-6">
          <h3 class="text-xl font-semibold mb-2">{{ course.name }}</h3>
          <p class="text-gray-600 mb-4">Raum: {{ course.classroom }}</p>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-500">{{ getTotalParticipants(course) }} Teilnehmende</span>
            <button @click="editCourse(course)" class="btn btn-base bg-gray-700 text-white hover:bg-gray-600">Öffnen</button>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow-md overflow-hidden transition-transform duration-300 hover:shadow-lg hover:-translate-y-1 flex items-center justify-center">
        <button @click="newCourse" class="p-6 w-full h-full text-center">
          <span class="text-2xl font-semibold text-teal-600">+</span>
          <p class="mt-2 text-lg font-semibold text-teal-600">Neuer Kurs</p>
        </button>
      </div>
    </div>
  </div>
</template>
