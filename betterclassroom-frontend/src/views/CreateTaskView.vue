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
    console.log(result.data)
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
const subtaskName = ref('')
const subExercises = ref([])
const oldSubExercises = ref([])
const createButton = ref('Erstellen')
const exerciseButtonMethod = ref('')
const isEditing = ref(false)

let currentSubTaskId = null

const api_url = import.meta.env.VITE_API_PROD_URL

const createSubTask = () => {
  const id = subtaskName.value || uuidv4()
  subExercises.value.push({ id: id, description: subtask.value })
  subtaskName.value = ''
  subtask.value = ''
}

const createExercise = async () => {
  const id = taskName.value || uuidv4()
  try {
    const result = await axios.post(`${api_url}/course/${courseId}/exercise`, {
      id: id,
      description: taskDescription.value.replace(/\n/g, '\\n'),
      exercises: subExercises.value.map((e) => ({ ...e, id: e.id }))
    })
    console.log(result)
    alert('Aufgabe erstellt')
    router.push(`/createCourse/${courseId}`)
  } catch (error) {
    console.log(error)
  }
}

const editExercise = async () => {
  for (let subExercise of subExercises.value) {
    // Zugriff auf die subTaskId
    const subTaskId = subExercise.id;
    const existingSubExercise = oldSubExercises.value.find(oldSubExercise => oldSubExercise.id === subTaskId)
    console.log(existingSubExercise)
    if (!existingSubExercise) { // Entfernen Sie .data
      try {
        const result = await axios.post(`${api_url}/course/${courseId}/exercise/${taskId}`, {
          id: subExercise.id,
          description: subExercise.description.replace(/\n/g, '\\n')
        })
        console.log(result)
      } catch (error) {
        console.log(error)
      }
    }
  }
  try {
    const result = await axios.put(`${api_url}/course/${courseId}/exercise/${taskId}`, {
      description: taskDescription.value.replace(/\n/g, '\\n'),
    })
    console.log(result)
    alert('Aufgabe bearbeitet')
    router.push(`/createCourse/${courseId}`)
  } catch (error) {
    console.log(error)
  }
}

const editSubTask = async (subTaskId) => {
  if (!subTaskId) {
    alert("Keine Aufgaben-ID")
    return
  }
  const task = subExercises.value.find(subTask => subTask.id === subTaskId)
  subtaskName.value = task.id
  subtask.value = task.description
  isEditing.value = true
  currentSubTaskId = subTaskId
}

const saveChanges = async () => {
  isEditing.value = false
  try {
    const result = await axios.put(`${api_url}/course/${courseId}/exercise/${taskId}/${currentSubTaskId}`, {
      description: subtask.value.replace(/\n/g, '\\n')
    })
    alert("Änderungen gespeichert")
    subExercises.value = subExercises.value.map(subTask => {
      if (subTask.id === currentSubTaskId) {
        return { id: subTask.id, description: subtask.value }
      }
      return subTask
    })
  } catch (error) {
    subExercises.value = subExercises.value.map(subTask => {
      if (subTask.id === currentSubTaskId) {
        return { id: subTask.id, description: subtask.value }
      }
      return subTask
    })
  }
}

const cancelChanges = async () => {
  isEditing.value = false
  subtask.value = ''
  subtaskName.value = ''
}

onBeforeMount(async () => {
  const oldTaskId = route.params.taskid
  if (oldTaskId) {
    const oldTask = await loadOldTask(oldTaskId)
    if (oldTask) {
      const exercises = oldTask.exercises.find(e => e.id === taskId)
      console.log(exercises)
      oldSubExercises.value = exercises.exercises.map(e => {
        return { id: e.id, description: e.description }
      })
      subExercises.value = JSON.parse(JSON.stringify(oldSubExercises.value))
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
    subExercises.value.pop();
  }
}

const deleteSubTask = async (subTaskId) => {
  if (!subTaskId) {
    alert("Keine Aufgaben-ID")
    return
  }
  try {
    try {
      const result = await axios.delete(`${api_url}/course/${courseId}/exercise/${taskId}/${subTaskId}`)
      alert("Aufgabe gelöscht")
      subExercises.value = subExercises.value.filter(subTask => subTask.id !== subTaskId)
    } catch (error) {
      subExercises.value.pop();
    }
  } catch (error) {
    console.log(error)
  }
}
</script>

<template>
  <div class="flex justify-center item-center">
    <div class="flex flex-col w-2/3">
      <div class="flex flex-row items-center justify-between">
        <h1 class="text-2xl my-10">{{ title }}</h1>
        <button v-if="route.params.taskid" class="btn btn-danger" @click="deleteTask(taskId)">Löschen</button>
      </div>
      <input type="text" placeholder="Aufgabenname" class="input input-bordered input-accent w-full max-w-xs my-5"
        v-model="taskName" />
      <textarea class="textarea textarea-accent my-5 overflow-auto" placeholder="Beschreibung der Aufgabe"
        style="min-height: 100px;" v-model="taskDescription"></textarea>
      <div class="overflow-x-auto w-full">
        <h2 class="text-xl my-5">Unteraufgaben</h2>
        <input type="text" placeholder="Unteraufgabentitel" class="input input-md input-bordered input-accent w-full"
          v-model="subtaskName" />
        <div class="flex items-center">
          <textarea class="textarea textarea-accent my-5 overflow-auto flex-grow"
            placeholder="Beschreibung der Unteraufgabe" style="min-height: 200px;" v-model="subtask"></textarea>
        </div>
        <button class="btn btn-accent mb-5 float-right" v-if="!isEditing" @click="createSubTask">&#65291 Unteraufgabe
          hinzufügen</button>
        <div class="mb-4" v-if="isEditing">
          <button class="btn btn-primary mr-2" @click="saveChanges">Speichern</button>
          <button class="btn" @click="cancelChanges">Abbrechen</button>
        </div>
        <table class="table table-zebra">
          <thead>
            <tr>
              <th>Titel</th>
              <th>Beschreibung</th>
              <th>Aktionen</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in subExercises" :key="s.id">
              <td class="font-bold">{{ s.id }}</td>
              <td>{{ s.description }} </td>
              <td style="text-align: right;">
                <div class="flex justify-end">
                  <button class="btn btn-xs btn-primary btn-square mt-2 mr-2"
                    @click="() => editSubTask(s.id)">✏️</button>
                  <button class="btn btn-xs btn-primary btn-square mt-2" @click="() => deleteSubTask(s.id)">🗑️</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <button class="btn btn-primary mt-10" @click="exerciseButtonMethod">{{ createButton }}</button>
    </div>
  </div>
</template>
