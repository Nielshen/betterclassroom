<script setup>
import axios from 'axios'
import { onBeforeMount, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { v4 as uuidv4 } from 'uuid'

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

const api_url = import.meta.env.VITE_API_PROD_URL

const createSubExercise = () => {
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

onBeforeMount(async () => {
  const oldTaskId = route.params.taskid
  if (oldTaskId) {
    const oldTask = await loadOldTask(oldTaskId)
    if (oldTask) {
      const exercises = oldTask.exercises.find(e => e.id === taskId).exercises
      subExercises.value = exercises.map(e => {
        const innerArray = e.innerArray;
        return { id: e.id, description: e.description }
      })      
      taskName.value = oldTask.exercises.find(e => e.id === taskId)?.id
      taskDescription.value = oldTask.exercises.find(e => e.id === taskId)?.description
      title.value = 'Aufgabe bearbeiten'
    } else {
      console.error('loadOldTask hat keinen Wert zurückgegeben')
    }

  } else {
    title.value = 'Aufgabe erstellen'
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

// TODO: Implement deleteSubTask
const deleteSubTask = async (subTaskId) => {
  try {
    // Abrufen der Übung
    const response = await axios.get(`${api_url}/course/${courseId}/exercise/${taskId}`)
    const exercise = response.data

    // Finden und Entfernen des Subtasks
    const index = exercise.subTasks.findIndex(subTask => subTask.id === subTaskId)
    if (index !== -1) {
      exercise.subTasks.splice(index, 1)
    }

    // Aktualisieren der Übung auf dem Server
    await axios.put(`${api_url}/course/${courseId}/exercise/${taskId}`, exercise)

    alert("Subtask gelöscht")
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
      style="min-height: 300px;" v-model="taskDescription"></textarea>
    <div class="overflow-x-auto">
      <input type="text" placeholder="Unteraufgabe" class="input input-bordered input-accent w-2/3 my-5"
        v-model="subtask" />
      <table class="table">
        <tbody>
          <tr v-for="s in subExercises" :key="s.id">
            <td>{{ s.description }} </td>
            <button class="btn btn-xs btn-square mt-2" @click="() => deleteSubTask(s.id)">🗑️</button>
          </tr>
        </tbody>
      </table>
    </div>
    <button class="btn btn-primary mb-4" @click="createSubExercise">Unteraufgabe hinzufügen</button>
    <button class="btn btn-primary" @click="createExercise">{{ createButton }}</button>
  </div>
</template>
