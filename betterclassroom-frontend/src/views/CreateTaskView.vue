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
    console.log(result)
    return result.data.filter((course) => course._id === courseId)[0]
  } catch (error) {
    console.log(error)
  }
}

const courseId = route.params.courseId
const taskId = route.params.taskid // Verwende taskid statt taskId

console.log(route.params)

const title = ref('Aufgabe erstellen')
const taskName = ref('')
const taskDescription = ref('')
const subtask = ref('')
const subExercises = ref([])

const api_url = import.meta.env.VITE_API_PROD_URL

const createSubExercise = () => {
  subExercises.value.push({ description: subtask.value })
  console.log(subExercises.value) 
  subtask.value = ''
}

const createExercise = async () => {
  const id = taskId || uuidv4()
  console.log(taskDescription.value)
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
      subExercises.value = oldTask.exercises.map(e => ({ description: e.description, id: e.id }))
      taskName.value = oldTask.exercises.find(e => e.id === taskId)?.id
      console.log(oldTask.exercises.map(e => e.id))
      taskDescription.value = oldTask.exercises.find(e => e.id === taskId)?.description
      console.log(oldTask.exercises.map(e => e.description))
      title.value = 'Aufgabe bearbeiten'
    } else {
      console.error('loadOldTask hat keinen Wert zurückgegeben')
    }

  } else {
    title.value = 'Aufgabe erstellen'
  }
})

const deleteTask = async (taskId) => {
  try {
    const taskId = route.params.taskid
    const result = await axios.delete(`${api_url}/course/${courseId}/exercise/${taskId}`)
    console.log(result)
  } catch (error) {
    console.log(error)
  }
}

const remove = async (taskId) => {
  if (!taskId) {
    alert("No Task ID")
    return
  }
  try {
    await deleteTask(taskId)
    alert("Task deleted")
    router.push(`/courses/${courseId}`)
  } catch (err) {
    alert('Error', err)
  }
}

const deleteSubTask = async (taskId) => {
  /** 
  try {
    const taskId = route.params.taskid
    const result = await axios.delete(`${api_url}/course/${courseId}/exercise/${taskId}`)
    console.log(result)
  } catch (error) {
    console.log(error)
  }
  */
}

const removeSubTask = async (taskId) => {
  if (!taskId) {
    alert("No Task ID")
    return
  }
  try {
    await deleteTask(taskId)
    alert("Task deleted")
    router.push(`/courses/${courseId}`)
  } catch (err) {
    alert('Error', err)
  }
}
</script>

<template>
  <div class="flex flex-col w-2/3">
    <div class="flex flex-row items-center justify-between">
      <h1 class="text-2xl my-10">{{ title }}</h1>
      <button v-if="route.params.taskid" class="btn btn-danger" @click="deleteTask">Löschen</button>
    </div>
    <input type="text" placeholder="Aufgabenname" class="input input-bordered input-accent w-full max-w-xs my-5"
      v-model="taskName" />
    <textarea class="textarea textarea-accent my-5 overflow-auto" placeholder="Beschreibung der Aufgabe"
      style="min-height: 300px;" v-model="taskDescription"></textarea>
    <div class="overflow-x-auto">
      <input type="text" placeholder="Unteraufgabe" class="input input-bordered input-accent w-full max-w-xs my-5"
        v-model="subtask" />
      <table class="table">
        <tbody>
          <tr v-for="s in subExercises" :key="s.id">
            <td>{{ s.description }} </td>
            <button class="btn btn-xs btn-square mt-2" @click="deleteSubTask">🗑️</button>
          </tr>
        </tbody>
      </table>
    </div>
    <button class="btn btn-primary mb-4" @click="createSubExercise">Unteraufgabe hinzufügen</button>
    <button class="btn btn-primary" @click="createExercise">Erstellen</button>
  </div>
</template>
