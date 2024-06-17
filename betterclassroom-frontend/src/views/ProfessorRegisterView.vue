<script setup>
import { onBeforeMount, ref, computed, watch } from 'vue'
import axios from 'axios'
import { getApiUrl } from '@/utils/common'
import { useRouter } from 'vue-router'

const router = useRouter()

const email = ref('')
const lastName = ref('')
const firstName = ref('')
const password1 = ref('')
const password2 = ref('')

const rawUrl = getApiUrl()
const professorApiUrl = `http://${rawUrl}/api/professor`

const register = async () => {
    const data = {
        email: email.value,
        last_name: lastName.value,
        first_name: firstName.value,
        password: password1.value,
        password2: password2.value
    }

    try {
        //const response = await axios.post(`${professorApiUrl}/register`, data)
        router.push("/courses")
    } catch(e) {

        console.error(e)
    
    }

    
}

</script>
<template>
  <div class="flex flex-col h-full my-10 p-4 items-center justify-between border-4 border-black ">
  <h1>Register as a Professor</h1>
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
          d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM12.735 14c.618 0 1.093-.561.872-1.139a6.002 6.002 0 0 0-11.215 0c-.22.578.254 1.139.872 1.139h9.47Z"
        />
      </svg>
      <input type="text" v-model="lastName" class="grow" placeholder="Vorname" />
    </label>
    <label class="input input-bordered flex items-center gap-2 my-2">
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
      <input type="text" v-model="firstName" class="grow" placeholder="Nachname" />
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
    <button @click="register"  class="btn btn-primary">Register</button>
  </div>
</template>