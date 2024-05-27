<script setup>
import axios from 'axios'
import { onBeforeMount, ref } from 'vue'
import { v4 as uuidv4 } from 'uuid'
import { useRouter } from 'vue-router'
import { useRoute } from 'vue-router'

const route = useRoute()
const router = useRouter()



const loadOldCourse = async (id) => {
  try {
    const result = await axios.get(`${api_url}/course`)
    return result.data.filter(course => course._id === id)[0]
  } catch (error) {
    console.log(error)
  }
}

const title = ref('')
const courseName = ref('')
const courseDescription = ref('')
const courseRoom = ref('')
const createButton = ref('')

const api_url = import.meta.env.VITE_API_PROD_URL

const pushCourse = async ({ oldId, description, professor, classroom }) => {
  const id = oldId || uuidv4()
  try {
    const result = await axios.post(`${api_url}/course`, {
      id,
      professor,
      description,
      classroom
    })
    console.log(result)
  } catch (error) {
    console.log(error)
  }
}


const save = () => {
    if(courseName.value === '' || courseName.value === '') {
        alert('Bitte füllen Sie alle Felder aus')
        return
    }
    pushCourse({
        oldId: oldCourse ? oldCourse.id : null,
        description: courseName.value,
        professor: 'Prof. Dr. Max Mustermann',
        classroom: courseRoom.value
    })
    .then(() => {
        alert("Sucess")
        router.push('/courses')
    })
    .catch((err) => {
        alert("Error",err)
    })
}

const deleteCourse = () => {}

onBeforeMount(async () => {
  const oldCourseId = route.params.id
  if (oldCourseId) {
    const oldCourse = await loadOldCourse(oldCourseId)
    courseName.value = oldCourse.description
    courseRoom.value = oldCourse.classroom
    title.value = 'Kurs bearbeiten'
    createButton.value = 'Speichern'
  } else {
    title.value = 'Kurs erstellen'
    createButton.value = 'Erstellen'
  }

})
</script>

<template>
  <div class="flex flex-col w-2/3">
  <div class="flex flex-row items-center justify-between">
    <h1 class="text-2xl my-10">{{ title }}</h1>
    <button v-if="route.params.id" class="btn btn-danger" @click="deleteCourse">Löschen</button>
  </div>
    <input
      type="text"
      placeholder="Kursname"
      class="input input-bordered input-accent w-full max-w-xs my-5"
      v-model="courseName"
    />
    <input
      type="text"
      placeholder="Raum"
      class="input input-bordered input-accent w-full max-w-xs my-5"
      v-model="courseRoom"
    />
    <!--
    <textarea
      class="textarea textarea-accent my-5 overflow-auto"
      placeholder="Beschreibung des Kurs"
      style="min-height: 300px"
      v-model="courseDescription"
    ></textarea>
    -->
    <div class="flex w-1/2 justify-around">
    <button class="btn btn-primary" @click="save">{{ createButton }} </button>
    <button class="btn btn-warning" @click="router.push('/courses')">Abbrechen</button>
    </div>
  </div>
</template>