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
    <div class="w-full flex justify-center">
        <div>
            <table class="table-lg">
                <thead>
                    <tr>
                        <th>Kurs</th>
                        <th>Raum</th>
                        <th>Teilnehmer</th>
                    </tr>
                </thead>
                <tbody v-for="e in courseData" :key="e">
                    <tr class="bg-base-200">
                        <td>{{ e._id }}</td>
                        <td>{{ e.classroom }}</td>
                        <td>{{ getTotalParticipants(e) }} Teilnehmende</td>
                        <td>
                            <div>
                                <button class="btn btn-primary" @click="editCourse(e)">Öffnen</button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
            <button class="btn btn-accent mt-4" @click="newCourse">Neuer Kurs</button>
        </div>
    </div>
</template>
