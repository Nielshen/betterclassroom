<script setup>
import axios from 'axios'
import { onBeforeMount, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getApiUrl } from '@/utils/common'
import { io } from 'socket.io-client';

const route = useRoute()
const router = useRouter()

const courseId = route.params.courseId
const taskId = route.params.taskId

const rawUrl = getApiUrl()
const api_url = `http://${rawUrl}/api`
const wsUrl = `ws://${rawUrl}/student`

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
const currentSubTaskId = ref('')
const isExerciseActive = ref(false)


const socket = io(wsUrl, {
  path: '/api/socket.io/student',
  transports: ['websocket']
})

const goBackToDashboard = () => {
  router.push(`/dashboard/${courseId}/${taskId}`)
}

const backToCourse = () => {
  router.push(`/createCourse/${courseId}`)
}

const loadExercises = async () => {
  try {
    const result = await axios.get(`${api_url}/course/${courseId}`)
    return result.data
  } catch (error) {
    console.log(error)
  }
}

const createExercise = async () => {
  const name = taskName.value
  if (!name) {
    alert("Keine Aufgaben-ID")
    return
  }
  try {
    const result = await axios.post(`${api_url}/course/${courseId}/exercise`, {
      name: name,
      description: taskDescription.value,
      exercises: subExercises.value.map((e) => ({ ...e, name: e.name }))
    })
    console.log(result)
    alert('Aufgabe erstellt')
    router.push(`/createCourse/${courseId}`)
  } catch (error) {
    console.log(error)
  }
}

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

const createSubTask = async () => {
  const name = subtaskName.value
  if (!name) {
    alert("Kein Unteraufgaben Titel")
    return
  }
  const description = subtask.value.replace(/\r?\n/g, '\\n')

  try {
    socket.emit("new_subexercise", {
      course: courseId,
      exercise: taskId,
      name: subtaskName.value,
      description: subtask.value
    }, (response) => {
      if (response.success) {
        subExercises.value.push({ id: response.success, name: name, description: description })
      } else {
        console.error('Fehler beim Erstellen der SubExercise:', response.error)
      }
    })
  } catch (error) {
    console.log(error)
  }
  subtaskName.value = ''
  subtask.value = ''
}

const selectSubTaskToEdit = async (subTaskId) => {
  if (!subTaskId) {
    alert("Keine Aufgaben-ID")
    return
  }
  const task = subExercises.value.find(subTask => subTask.id === subTaskId)
  subtaskName.value = task.name
  subtask.value = task.description.replace(/\\n/g, '\n')
  isEditing.value = true
  currentSubTaskId.value = subTaskId
}

const saveEditedSubTask = async () => {
  isEditing.value = false
  try {
    const subTaskExists = oldSubExercises.value.find(subExercise => subExercise.id === currentSubTaskId.value);
    subExercises.value = subExercises.value.map(subTask => {
      if (subTask.id === currentSubTaskId.value) {
        return { id: subTask.id, name: subtaskName.value, description: subtask.value }
      }
      return subTask
    })
    if (subTaskExists) {
      socket.emit('alter_subexercise',
        { course: courseId, exercise: taskId, subexercise: currentSubTaskId.value, name: subtaskName.value, description: subtask.value },
        function (response) {
          if (response.success) {
            alert("Änderungen gespeichert")
          } else
            console.error('Fehler beim Ändernn der SubExercise: ', response.error)
        }
      )
    }
    subtask.value = ''
    subtaskName.value = ''
  } catch (error) {
    console.error(error);
  }
}

const deleteSubTask = async (subTaskId) => {
  if (!subTaskId) {
    alert("Keine Aufgaben-ID")
    return
  }

  const subTaskExists = oldSubExercises.value.find(subExercise => subExercise.id === subTaskId);
  if (subTaskExists) {
    try {
      socket.emit("delete_subexercise", {
        course: courseId,
        exercise: taskId,
        subexercise: subTaskId
      }, function (response) {
        if (response.success) {
          alert("Unteraufgabe gelöscht")
        } else
          if (response.error) {
            console.error('Fehler beim Löschen der SubExercise:', response.error)
          }
      })
    } catch (error) {
      console.log(error);
    }
  }
  subExercises.value = subExercises.value.filter(subTask => subTask.id !== subTaskId)
}

const cancelChanges = async () => {
  isEditing.value = false
  subtask.value = ''
  subtaskName.value = ''
}

onBeforeMount(async () => {
  const oldTaskId = route.params.taskId

  if (oldTaskId) {
    const oldTask = await loadExercises(oldTaskId)
    if (oldTask) {
      const exercises = oldTask.exercises.find(e => e.id === taskId)
      oldSubExercises.value = exercises.exercises.map(e => {
        return { id: e.id, name: e.name, description: e.description }
      })
      subExercises.value = JSON.parse(JSON.stringify(oldSubExercises.value))
      taskName.value = exercises.name
      taskDescription.value = exercises.description
      title.value = 'Aufgabe bearbeiten'
      createButton.value = 'Speichern'
      exerciseButtonMethod.value = backToCourse
      isExerciseActive.value = exercises.is_active
    } else {
      console.error('loadOldTask hat keinen Wert zurückgegeben')
    }

  } else {
    title.value = 'Aufgabe erstellen'
    exerciseButtonMethod.value = createExercise
  }
})
</script>

<template>
  <div class="flex justify-center item-center">
    <div class="flex flex-col w-2/3">
      <div class="flex flex-row items-center justify-between">
        <h1 class="text-2xl my-10">{{ title }}</h1>
        <div>
          <button v-if="isExerciseActive" class="btn btn-secondary mr-4" @click="goBackToDashboard">Zurück zum
            Dashboard</button>
          <button v-if="route.params.taskId" class="btn btn-danger mr-2" @click="deleteTask(taskId)">Löschen</button>
        </div>
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
          <button class="btn btn-primary mr-2" @click="saveEditedSubTask">Speichern</button>
          <button class="btn" @click="cancelChanges">Abbrechen</button>
        </div>
        <table class="table table-zebra">
          <thead>
            <tr>
              <th>Titel</th>
              <th>Beschreibung</th>
              <th style="width: fit-content;">Aktionen</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in subExercises" :key="s.id">
              <td class="font-bold" style="width: 1%; white-space: nowrap;">{{ s.name }}</td>
              <td style="white-space: pre-line;">{{ s.description }}</td>
              <td style="text-align: right; width: 1%; white-space: nowrap;">
                <div class="inline-flex justify-end">
                  <button class="btn btn-xs btn-primary btn-square m-2"
                    @click="() => selectSubTaskToEdit(s.id)">✏️</button>
                  <button class="btn btn-xs btn-primary btn-square m-2" @click="() => deleteSubTask(s.id)">🗑️</button>
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
