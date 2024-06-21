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


const title = ref('')
const courseName = ref('')
const courseDescription = ref('')
const courseRoom = ref('')
const createButton = ref('')
const professorId = ref('')
const tasks = ref([])
const isEditMode = ref('')

const pushCourse = async ({ oldId, description, professor, classroom }) => {
  const id = oldId || uuidv4()
  try {
    const result = await axios.post(`${api_url}/course`, {
      id,
      professor: professor,
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
  console.log(route.params.courseId)
  if (!route.params.courseId) { // Kurs existiert noch nicht
    pushCourse({
      oldId: courseName.value, // Kurs Name aus Input
      description: courseDescription.value,
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
  } else {
  // course exists do put
  try {
    await axios.put(`${api_url}/course/${courseName.value}`, {
      description: courseDescription.value,
      classroom: courseRoom.value
    })
  } catch (error) {
    console.log(error)
  }
  router.push('/courses')
  }
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
    console.log(oldCourse)
    tasks.value = oldCourse.exercises.map(e => ({ name: e.id, length: e.exercises.length, id: e.id }))
    console.log(tasks.value)
    courseName.value = oldCourse._id
    console.log(courseName.value)
    courseRoom.value = oldCourse.classroom
    title.value = 'Kurs bearbeiten'
    createButton.value = 'Speichern'
    courseDescription.value = oldCourse.description
    isEditMode.value = true
  } else {
    title.value = 'Kurs erstellen'
    createButton.value = 'Erstellen'
    professorId.value = 'Prof. Dr. Markus Eiglsperger'
    isEditMode.value = false
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

const startTask = async (taskId) => {
  console.log('Start task', taskId)
  const courseId = route.params.courseId
  const courseLink = `${window.location.host}/student/${courseId}/${taskId}`

  try {
    await axios.post(`${api_url}/course/${courseId}/exercise/${taskId}/start`)
    alert(`Kurs gestartet: ${courseLink}`)
    router.push(`/dashboard/${courseId}/${taskId}`)
  } catch (error) {
    console.error('Error starting the course:', error)
    alert('Fehler beim Starten des Kurses')
  }
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
      <div class="drawer drawer-end">
        <div class="mb-4">
          <label class="label">
            <span class="label-text">Raum</span>
          </label>
          <select class="select select-bordered w-full max-w-xs" v-model="courseRoom">
            <option disabled="disabled" selected="selected">Bitte wählen Sie einen Raum</option>
            <option>O-201</option>
            <option>O-301</option>
          </select>
        </div>

      </div>
      <textarea placeholder="Kursbeschreibung" class="textarea textarea-bordered w-full my-5 h-32"
        v-model="courseDescription"></textarea>
      <div class="flex w-full justify-start">
        <button class="btn btn-primary mr-4" @click="save">{{ createButton }} </button>
        <button class="btn btn-danger" @click="router.push('/courses')">Abbrechen</button>
        <button class="btn btn-primary ml-auto" v-if="isEditMode" @click="createTask">&#65291 Aufgabe erstellen</button>
      </div>
      <div v-if="isEditMode">
        <table class="table mt-8">
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
              <td class="text-right">
                <button class="btn btn-sm btn-danger m-1" @click="editTask(task.id)">Bearbeiten</button>
                <button class="btn btn-sm btn-accent m-1" @click="startTask(task.id)">Starten</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>