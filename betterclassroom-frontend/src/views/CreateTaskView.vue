<script setup>
import axios from 'axios'
import { onBeforeMount, ref } from 'vue'
import { useRoute } from 'vue-router'
import { v4 as uuidv4 } from 'uuid'

const route = useRoute()

const courseId = route.params.courseId

console.log(route.params)

const { oldTasks } = defineProps({
  oldTasks: Object
})

const title = ref('Aufgabe erstellen')
const taskName = ref('')
const taskDescription = ref('')
const subtask = ref('')

const createSubExercise = () => {
  subExercises.value.push({ description: subtask.value })
  subtask.value = ''
}

const api_url = import.meta.env.VITE_API_PROD_URL

const createExercise = async () => {
  const id = null || taskName.value
  try {
    const result = await axios.post(`${api_url}/course/${courseId}/exercise`, {
      id: id,
      description: taskDescription.value,
      exercises: subExercises.value.map((e) => ({ ...e, id: uuidv4() }))
    })
    alert('Aufgabe erstellt')
  } catch (error) {
    console.log(error)
  }
}

const loadOldTasks = async () => {
  const result = await axios.get(`${api_url}/course/${courseId}/exercise`)
  const data = result.data[0]
  taskName.value = data.id
  taskDescription.value = data.description
  subExercises.value = data.exercises
}

const subExercises = ref([])
onBeforeMount(async () => {})
</script>

<template>
  <div class="flex flex-col w-2/3">
    <h1 class="text-2xl my-10">Aufgaben erstellen</h1>
    <input
      type="text"
      placeholder="Aufgabenname"
      class="input input-bordered input-accent w-full max-w-xs my-5"
      v-model="taskName"
    />
    <textarea class="textarea textarea-accent my-5 overflow-auto" placeholder="Beschreibung der Aufgabe" 
    style="min-height: 300px;" v-model="taskDescription"></textarea>
    <div class="overflow-x-auto">
      <input
        type="text"
        placeholder="Unteraufgabe"
        class="input input-bordered input-accent w-full max-w-xs my-5"
        v-model="subtask"
      />
      <table class="table">
        <tbody>
          <tr v-for="s in subExercises" :key="s">
            {{
              s.description
            }}
          </tr>
        </tbody>
      </table>
    </div>
    <button class="btn btn-primary" @click="createSubExercise">Unteraufgabe hinzufügen</button>
    <button class="btn btn-primary" @click="createExercise">Erstellen</button>
  </div>
</template>