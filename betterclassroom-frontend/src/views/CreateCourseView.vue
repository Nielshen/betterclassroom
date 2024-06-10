<script setup>
import axios from 'axios'
import { onBeforeMount, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useRoute } from 'vue-router'
import { v4 as uuidv4 } from 'uuid'
import { getApiUrl } from '@/utils/common'


const route = useRoute()
const router = useRouter()

const rawUrl = getApiUrl()
const api_url = `http://${rawUrl}/api`

const courseId = route.params.courseId

const loadOldCourse = async (id) => {
  try {
    const result = await axios.get(`${api_url}/course`)
    return result.data.filter((course) => course._id === id)[0]
  } catch (error) {
    console.log(error)
  }
}

const loadProfessorId = async (professorName) => {
  try {
    const response = await axios.get(`${api_url}/professor?name=${professorName}`)
    if (response.data && response.data.length > 0) {
      return response.data[0]._id
    } else {
      return null
    }
  } catch (error) {
    console.error(error)
    return null
  }
}

const title = ref('')
const courseName = ref('')
const courseDescription = ref('')
const courseRoom = ref('')
const createButton = ref('')
const professorId = ref('') 
const tasks = ref([])

const pushCourse = async ({ oldId, description, professor, classroom }) => {
  const id = oldId || uuidv4()
  const professorId = await loadProfessorId(professor)
  try {
    const result = await axios.post(`${api_url}/course`, {
      id,
      professor: professorId,
      description,
      classroom
    })
    console.log(result)
  } catch (error) {
    console.log(error)
  }
}

const save = async () => {
  if (courseName.value === '' || courseRoom.value === '') {
    alert('Bitte füllen Sie alle Felder aus')
    return
  }
  const oldId = route.params.courseId || courseName.value
  console.log(route.params.courseId)
  console.log({ oldId })
  if (!oldId) {
    alert('Keine alte ID vorhanden')
    return
  }
  pushCourse({
    //oldId: route.params.id || courseName.value,
    oldId,
    description: courseName.value,
    professor: professorId.value,
    classroom: courseRoom.value
  })
    .then(() => {
      alert('Success')
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
    router.push('/courses')
    console.log(result)
  } catch (error) {
    console.log(error)
  }
}

const remove = async (courseId) => {
  if (!courseId) {
    alert("Keine Kurs-ID")
    return
  }
  try {
    await axios.delete(`${api_url}/course/${courseId}`)
      .then(() => {
        alert('Kurs gelöscht')
        router.push('/courses')
      })
  } catch (error) {
    alert('Fehler', error)
    console.log(error)
  }
}

onBeforeMount(async () => {
  const oldCourseId = route.params.courseId
  if (oldCourseId) {
    const oldCourse = await loadOldCourse(oldCourseId)
    tasks.value = oldCourse.exercises.map(e => ({ name: e.description, length: e.exercises.length, id: e.id }))
    courseName.value = oldCourse.description
    courseRoom.value = oldCourse.classroom
    title.value = 'Kurs bearbeiten'
    createButton.value = 'Speichern'
  } else {
    title.value = 'Kurs erstellen'
    createButton.value = 'Erstellen'
    professorId.value = await loadProfessorId('Prof. Dr. Eiglsperger')
  }
})

const createTask = (id) => {
  const courseId = route.params.courseId
  console.log({ courseId })
  router.push(`/createTask/${courseId}`)
}

const editTask = (taskid) => {
  const courseId = route.params.courseId
  router.push(`/editTask/${courseId}/${taskid}`)

}

const startTask = (taskId) => {
  console.log('Start task', taskId)
  const courseId = route.params.courseId
  const courseLink = `${window.location.host}/student/${courseId}/${taskId}`
  alert(`Kurs gestartet: ${courseLink}`)
  router.push(`/dashboard/${courseId}/${taskId}`)
}

</script>

<template>
  <div class="flex justify-center item-center">
    <div class="flex flex-col w-2/3">
      <div class="flex flex-row items-center justify-between">
        <h1 class="text-2xl my-10">{{ title }}</h1>
        <button v-if="route.params.courseId" class="btn btn-danger" @click="deleteCourse">Löschen</button>
      </div>
      <input type="text" placeholder="Kursname" class="input input-bordered input-accent w-full max-w-xs my-5"
        v-model="courseName" />
      <input type="text" placeholder="Raum" class="input input-bordered input-accent w-full max-w-xs my-5"
        v-model="courseRoom" />
      <div class="flex w-1/2 justify-around">
        <button class="btn btn-primary" @click="save">{{ createButton }} </button>
        <button class="btn btn-warning" @click="router.push('/courses')">Abbrechen</button>
        <button class="btn btn-primary" @click="createTask">Aufgaben erstellen</button>
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
              <td>{{ task.length }}</td>
              <button class="btn btn-sm btn-primary m-1" @click="editTask(task.id)">Bearbeiten</button>
              <button class="btn btn-sm btn-accent m-1" @click="startTask(task.id)">Starten</button>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>