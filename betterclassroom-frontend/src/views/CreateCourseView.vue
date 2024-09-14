<script setup>
import axios from 'axios'
import { onBeforeMount, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useRoute } from 'vue-router'
import { getApiUrl } from '@/utils/common'
import { notify } from "@kyvg/vue3-notification"

const route = useRoute()
const router = useRouter()

const rawUrl = getApiUrl()
const api_url = `http://${rawUrl}/api`

const courseId = route.params.courseId

const title = ref('')
const courseName = ref('')
const courseDescription = ref('')
const courseRoom = ref('')
const createButton = ref('')
const professorId = ref('')
const tasks = ref([])
const isEditMode = ref('')

const loadCourse = async (id) => {
  try {
    const result = await axios.get(`${api_url}/course/${id}`)
    return result.data
  } catch (error) {
    console.log(error)
  }
}

const pushCourse = async ({ name, description, professor, classroom }) => {
  try {
    const result = await axios.post(`${api_url}/course`, {
      name,
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
    notify({type: "warn", text: "Bitte füllen Sie alle Felder aus"})
    return
  }
  if (!courseId) {
    pushCourse({
      name: courseName.value,
      description: courseDescription.value,
      professor: professorId.value,
      classroom: courseRoom.value
    })
      .then(() => {
        notify({type: "success", text: "Kurs erfolgreich erstellt"})
        router.push('/courses')
      })
      .catch((err) => {
        notify({type: "error", text: "Fehler beim Erstellen vom Kurs", err})
      })
  } else {
    try {
      await axios.put(`${api_url}/course/${courseId}`, {
        name: courseName.value,
        description: courseDescription.value,
        classroom: courseRoom.value
      })
    } catch (error) {
      console.log(error)
    }
    router.push('/courses')
  }
}

const deleteCourse = async () => {
  try {
    const result = await axios.delete(`${api_url}/course/${courseId}`)
    router.push('/courses')
    console.log(result)
  } catch (error) {
    console.log(error)
  }
}


onBeforeMount(async () => {
  if (courseId) {
    title.value = 'Kurs bearbeiten'
    createButton.value = 'Speichern'
    isEditMode.value = true

    const oldCourse = await loadCourse(courseId)
    courseName.value = oldCourse.name
    tasks.value = oldCourse.exercises.map(e => ({ name: e.name, length: e.exercises.length, id: e.id, is_active: e.is_active }))
    courseRoom.value = oldCourse.classroom
    courseDescription.value = oldCourse.description
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

const editTask = (taskId) => {
  const courseId = route.params.courseId
  router.push(`/editTask/${courseId}/${taskId}`)

}

const startTask = async (taskId) => {
  console.log('Start task', taskId)
  const courseLink = `${window.location.host}/student/${courseId}/${taskId}`

  try {
    await axios.post(`${api_url}/course/${courseId}/exercise/${taskId}/start`)
    notify({type: "success", text: `"Kurs gestartet: " ${courseLink}`})
    router.push(`/dashboard/${courseId}/${taskId}`)
  } catch (error) {
    console.error('Error starting the course:', error)
    notify({type: "error", text: "Fehler beim Starten des Kurses"})
  }
}

const goBackToDashboard = (taskId) => {
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
              <td>{{ task.name }}</td>
              <td>{{ task.length }}</td>
              <td class="text-right">
                <button class="btn btn-sm btn-danger m-1 w-24" @click="editTask(task.id)">Bearbeiten</button>
                <button v-if="!task.is_active" class="btn btn-sm btn-accent m-1 w-24" @click="startTask(task.id)">Starten</button>
                <button v-else class="btn btn-sm btn-secondary m-1 w-24" @click="goBackToDashboard(task.id)">Dashboard</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>