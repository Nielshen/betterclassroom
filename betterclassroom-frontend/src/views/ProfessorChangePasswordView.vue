<script setup>
import { onBeforeMount, ref, computed, watch } from 'vue'
import axios from 'axios'
import { getApiUrl } from '@/utils/common'
import { useDataStore } from '../stores/dataStore'

const { saveProfessorLocally,deleteProfessorLocally } = useDataStore()

const email = ref('')
const password1 = ref('')
const password2 = ref('')

const rawUrl = getApiUrl()
const professorApiUrl = `http://${rawUrl}/api/professor`


const saveLocally = (data) => {
  localStorage.setItem('user', JSON.stringify(data))
}



const requestChangePassword = async ({ email, password}) => {
  try {
    const data = {
      email: email,
      password: password,
    }
    const apiUrl = getApiUrl() + "/api/professor/reset_Password"
    console.log({
      apiUrl, data
    })
    const response = await axios.post(apiUrl, data)
    if (response.status !== 200) {
      console.error("Register failed", response)
      return
    }
    console.log("Response", response)
    saveProfessorLocally(data)
  } catch (e) {
    console.error(e)
  }
}


const  resetPassword = async () => {
  if (password1.value !== password2.value) {
    console.error("Passwords do not match")
    return
  }
  const data = {
    email: email.value,
    password: password1.value,
  }

  try {
    await requestChangePassword(data)
  } catch (e) {
    console.error(e)
  }
}
</script>
<template>
  <div class="flex flex-col items-center justify-center border-black">
    <div
      class="flex flex-col w-[400px] h-full my-10 p-8 justify-between border-2 shadow-2xl rounded-xl"
    >
      <h1 class="text-2xl">Better Classroom</h1>
      <h1 class="text-xl font-bold mb-10">Neues Passwort erstellen</h1>
      <label class="input input-bordered flex items-center gap-2 my-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          fill="currentColor"
          class="w-4 h-4 opacity-70"
        >
          <path
            d="M2.5 3A1.5 1.5 0 0 0 1 4.5v.793c.026.009.051.02.076.032L7.674 8.51c.206.1.446.1.652 0l6.598-3.185A.755.755 0 0 1 15 5.293V4.5A1.5 1.5 0 0 0 13.5 3h-11Z"
          />
          <path
            d="M15 6.954 8.978 9.86a2.25 2.25 0 0 1-1.956 0L1 6.954V11.5A1.5 1.5 0 0 0 2.5 13h11a1.5 1.5 0 0 0 1.5-1.5V6.954Z"
          />
        </svg>
        <input type="text" v-model="email" class="grow" placeholder="Email" />
      </label>
      <label class="input input-bordered flex items-center gap-2 my-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          fill="currentColor"
          class="w-4 h-4 opacity-70"
        >
          <path
            fill-rule="evenodd"
            d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z"
            clip-rule="evenodd"
          />
        </svg>
        <input type="password" v-model="password1" class="grow" value="password" />
      </label>
      <label class="input input-bordered flex items-center gap-2 my-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          fill="currentColor"
          class="w-4 h-4 opacity-70"
        >
          <path
            fill-rule="evenodd"
            d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z"
            clip-rule="evenodd"
          />
        </svg>
        <input type="password" v-model="password2" class="grow" value="password" />
      </label>
      <button @click="resetPassword" class="btn btn-primary mt-3">Passwort ändern</button>
    </div>
  </div>
</template>