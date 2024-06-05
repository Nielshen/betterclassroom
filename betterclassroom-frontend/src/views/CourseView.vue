<script setup>
import { onBeforeMount, ref } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"

const router = useRouter()

const api_url = import.meta.env.VITE_API_PROD_URL

const courseData = ref([])

const fetchCourses = async () => {
    const result = await axios.get(`${api_url}/course`)
    const data = result.data
    courseData.value = data
}


onBeforeMount(async () => {
    await fetchCourses()
})


const newCourse = () => router.push("/createCourse")
const editCourse = (e) => {
    const id = e._id
    router.push(`/createCourse/${id}`)
}

</script>

<template>
    <div class="overflow-x-auto">
        <div class="flex flex-col  justify-start items-start ">
            <table class="table-lg">
                <!-- head -->
                <thead>
                    <tr>
                        <th>Kurs</th>
                        <th>Raum</th>
                        <th>Teilnehmer</th>
                    </tr>
                </thead>
                <tbody v-for="e in courseData">
                    <!-- row 1 -->
                    <tr class="bg-base-200">
                        <td>{{ e.description }}</td>
                        <td>{{ e.classroom }}</td>
                        <td>{{ e.participants.length }} Teilnehmende</td>
                        <td>
                            <div>
                                <button class="btn btn-primary mr-4 " @click="editCourse(e)">Öffnen</button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
            <button class="btn btn-accent mt-4" @click="newCourse">Neuer Kurs</button>
        </div>
    </div>
</template>