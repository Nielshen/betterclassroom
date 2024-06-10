<script setup>
import axios from 'axios'
import { onBeforeMount, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { v4 as uuidv4 } from 'uuid'
import { getApiUrl } from '@/utils/common'

const route = useRoute()
const router = useRouter()

const loadOldTask = async (id) => {
  try {
    const result = await axios.get(`${api_url}/course`)
    return result.data.filter((course) => course._id === courseId)[0]
  } catch (error) {
    console.log(error)
  }
}

const courseId = route.params.courseId
const taskId = route.params.taskid // Verwende taskid statt taskId

const title = ref('Aufgabe erstellen')
const taskName = ref('')
const taskDescription = ref('')
const subtask = ref('')
const subExercises = ref([])
const createButton = ref('Erstellen')
const exerciseButtonMethod = ref('')

const rawUrl = getApiUrl()
const api_url = `http://${rawUrl}/api`

const createSubTask = () => {
  const id = uuidv4()
  subExercises.value.push({ id: id, description: subtask.value })
  subtask.value = ''
}

const createExercise = async () => {
  const id = taskName.value || uuidv4()
  try {
    const result = await axios.post(`${api_url}/course/${courseId}/exercise`, {
      id: id,
      description: taskDescription.value,
      exercises: subExercises.value.map((e) => ({ ...e, id: uuidv4() }))
    })
    alert('Aufgabe erstellt')
    router.push(`/createCourse/${courseId}`)
  } catch (error) {
    console.log(error)
  }
}

const editExercise = async () => {
  const id = taskName.value || uuidv4()
  try {
    const result1 = await axios.delete(`${api_url}/course/${courseId}/exercise/${taskId}`)
    const result = await axios.post(`${api_url}/course/${courseId}/exercise`, {
      id: id,
      description: taskDescription.value,
      exercises: subExercises.value.map((e) => ({ ...e, id: uuidv4() }))
    })
    alert('Aufgabe bearbeitet')
    router.push(`/createCourse/${courseId}`)
  } catch (error) {
    console.log(error)
  }
}

onBeforeMount(async () => {
  const oldTaskId = route.params.taskid
  if (oldTaskId) {
    const oldTask = await loadOldTask(oldTaskId)
    if (oldTask) {
      const exercises = oldTask.exercises.find(e => e.id === taskId).exercises
      subExercises.value = exercises.map(e => {
        return { id: e.id, description: e.description }
      })
      taskName.value = oldTask.exercises.find(e => e.id === taskId)?.id
      taskDescription.value = oldTask.exercises.find(e => e.id === taskId)?.description
      title.value = 'Aufgabe bearbeiten'
      createButton.value = 'Speichern'
      exerciseButtonMethod.value = editExercise

    } else {
      console.error('loadOldTask hat keinen Wert zurückgegeben')
    }

  } else {
    title.value = 'Aufgabe erstellen'
    exerciseButtonMethod.value = createExercise
  }
})

const deleteTask = async (taskId) => {
  if (!taskId) {
    alert("Keine Aufgaben-ID")
    return
  }
  try {
    const result = await axios.delete(`${api_url}/course/${courseId}/exercise/${taskId}`)
    alert("Aufgabe gelöscht")
    router.push(`/createCourse/${courseId}`)
  } catch (error) {
    alert('Fehler', error)
  }
}

const deleteSubTask = async (subTaskId) => {
  if (!subTaskId) {
    alert("Keine Aufgaben-ID")
    return
  }
  try {
    const result = await axios.delete(`${api_url}/course/${courseId}/exercise/${taskId}/${subTaskId}`)
    alert("Aufgabe gelöscht")
    subExercises.value = subExercises.value.filter(subTask => subTask.id !== subTaskId)
  } catch (error) {
    alert('Fehler', error)
  }
}
</script>

<template>
  <div class="flex flex-col w-2/3">
    <div class="flex flex-row items-center justify-between">
      <h1 class="text-2xl my-10">{{ title }}</h1>
      <button v-if="route.params.taskid" class="btn btn-danger" @click="() => deleteTask(taskId)">Löschen</button>
    </div>
    <input type="text" placeholder="Aufgabenname" class="input input-bordered input-accent w-full max-w-xs my-5"
      v-model="taskName" />
    <textarea class="textarea textarea-accent my-5 overflow-auto" placeholder="Beschreibung der Aufgabe"
      style="min-height: 100px;" v-model="taskDescription"></textarea>
    <div class="overflow-x-auto w-full">
      <div class="flex items-center">
        <textarea class="textarea textarea-accent my-5 overflow-auto flex-grow" placeholder="Unteraufgabe einfügen"
          style="min-height: 200px;" v-model="subtask"></textarea>
        <button class="btn btn-accent btn-circle btn-xl ml-10 mr-10 text-xl" @click="createSubTask">&#65291</button>
      </div>
      <table class="table table-zebra">
        <tbody>
          <tr v-for="s in subExercises" :key="s.id">
            <td>{{ s.description }} </td>
            <button class="btn btn-xs btn-primary btn-square mt-2 mr-2 float-right"
              @click="() => deleteSubTask(s.id)">🗑️</button>
          </tr>
        </tbody>
      </table>
    </div>
    <button class="btn btn-primary mt-5" @click="exerciseButtonMethod">{{ createButton }}</button>
  </div>
</template>
