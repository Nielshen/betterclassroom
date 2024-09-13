<script setup>
import { onBeforeMount, ref, computed, watch } from 'vue'
import axios from 'axios'
import { getApiUrl } from '@/utils/common'
import { useRouter } from 'vue-router'
import { useDataStore } from '../stores/dataStore'

const router = useRouter()

const { saveProfessorLocally,deleteProfessorLocally } = useDataStore()

const email = ref('')
const lastName = ref('')
const firstName = ref('')
const password1 = ref('')
const password2 = ref('')

const rawUrl = getApiUrl()
const api_url = `http://${rawUrl}/api`


const requestRegister = async ({ email, last_name, first_name, password}) => {
 try{
    const data = {
      id: email,
      lastName: last_name,
      firstName: first_name,
      password: password,
    }
    const apiUrl = api_url + "/professor"
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

const register = async () => {
  if (password1.value !== password2.value) {
    console.error("Passwords do not match")
    return
  }
  const data = {
    email: email.value,
    last_name: lastName.value,
    first_name: firstName.value,
    password: password1.value,
  }

  try {
    await requestRegister(data)
    router.push('/courses')
  } catch (e) {
    console.error(e)
  }
}

onBeforeMount(() => {
  deleteProfessorLocally()
}) 
</script>
<template>
<div class="flex flex-col items-center">
  <div class="flex flex-col h-full w-[400px] my-10 p-6 items-left justify-between rounded-xl shadow-2xl shadow-bg-primaryl hover:shadow-cyan-500/50">
    <h1 class="text-2xl">Better Classroom</h1>
    <h1 class="text-xl font-bold mb-10">Registrierung</h1>

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
    <div class="flex gap-2 my-3">
      <label class="input input-bordered flex items-center gap-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          fill="currentColor"
          class="w-4 h-4 opacity-70"
        >
          <path
            d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM12.735 14c.618 0 1.093-.561.872-1.139a6.002 6.002 0 0 0-11.215 0c-.22.578.254 1.139.872 1.139h9.47Z"
          />
        </svg>
        <input type="text" v-model="lastName" class="grow w-1/2" placeholder="Vorname" />
      </label>
      <label class="input input-bordered flex items-center gap-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          fill="currentColor"
          class="w-4 h-4 opacity-70"
        >
          <path
            d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM12.735 14c.618 0 1.093-.561.872-1.139a6.002 6.002 0 0 0-11.215 0c-.22.578.254 1.139.872 1.139h9.47Z"
          />
        </svg>
        <input type="text" v-model="firstName" class="grow w-1/2" placeholder="Nachname" />
      </label>
    </div>
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
    <button @click="register" class="btn btn-primary my-4">Registrieren</button>
  </div>
</div>
</template>