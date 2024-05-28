<script setup>
import axios from 'axios'
import { onBeforeMount, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useRoute } from 'vue-router'

const route = useRoute()
const router = useRouter()

const loadOldCourse = async (id) => {
  try {
    const result = await axios.get(`${api_url}/course`)
    return result.data.filter((course) => course._id === id)[0]
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
  const id = oldId || courseName.value
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
  if (courseName.value === '' || courseName.value === '') {
    alert('Bitte füllen Sie alle Felder aus')
    return
  }
  pushCourse({
    oldId: route.params.id || null,
    description: courseName.value,
    professor: 'Prof. Dr. Max Mustermann',
    classroom: courseRoom.value
  })
    .then(() => {
      alert('Sucess')
      router.push('/courses')
    })
    .catch((err) => {
      alert('Error', err)
    })
}

const deleteCourse = async (courseId) => {
  try {
    const courseId = route.params.courseId
    const result = await axios.delete(`${api_url}/course/${courseId}`)
    console.log(result)
  } catch (error) {
    console.log(error)
  }
}

const remove = (courseId) => {
  if (!courseId) {
    alert("No Course ID")
    return
  }
  deleteCourse(courseId)
    .then(() => {
      alert("Course deleted")
      router.push('/courses')
    })
    .catch((err) => {
      alert('Error', err)
    })
}

onBeforeMount(async () => {
  const oldCourseId = route.params.courseId
  if (oldCourseId) {
    const oldCourse = await loadOldCourse(oldCourseId)
    tasks.value = oldCourse.exercises.map(e => ({ name: e.description, length: e.exercises.length, id: e.id}))
    courseName.value = oldCourse.description
    courseRoom.value = oldCourse.classroom
    title.value = 'Kurs bearbeiten'
    createButton.value = 'Speichern'
  } else {
    title.value = 'Kurs erstellen'
    createButton.value = 'Erstellen'
  }
})

const createTask = (id) => {
  const courseId = route.params.courseId
  console.log({ courseId })
  router.push(`/createTask/${courseId}`)
}

const startTask = (taskId) => {
    console.log('Start task', taskId)
    const courseId = route.params.courseId
    const courseLink = `${window.location.host}/student/${courseId}/${taskId}`
    alert(`Kurs gestartet: ${courseLink}`)
    router.push(`/dashboard/${courseId}/${taskId}`)
}
const tasks = ref([])
</script>

<template>
  <div class="flex flex-col w-2/3">
  <div class="flex flex-row items-center justify-between">
    <h1 class="text-2xl my-10">{{ title }}</h1> 
    <button v-if="route.params.courseId" class="btn btn-danger" @click="deleteCourse">Löschen</button>
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
    <button class="btn btn-primary" @click="createTask" >Aufgaben erstellen</button>
    </div>
    <div>
    <table class="table">
      <thead>
        <tr>
        <th>Aufgabe</th>
        <th>Unteraufgaben</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in tasks">
          <td>{{ task.id }}</td>
          <td>{{ task.length  }}</td>
          <button class="btn btn-xs btn-primary mr-4">Bearbeiten</button>
          <button class="btn btn-xs btn-accent mr-4" @click="startTask(task.id)">Starten</button>
        </tr>
      </tbody>
      </table>
    </div>
  </div>
</template>