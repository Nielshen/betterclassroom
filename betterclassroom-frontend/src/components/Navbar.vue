<script setup>
import { useRouter } from 'vue-router'
import { useDataStore } from '@/stores/dataStore'
import { computed } from 'vue'

const router = useRouter()
const dataStore = useDataStore()


const isLoggedIn = computed(() => dataStore.user.role === 'professor')

const logout = async () => {
  dataStore.deleteProfessorLocally()
  router.push('/login')
}

const toDashboard = () => {
  if (dataStore.isProfessor) {
    router.push('/courses')
  } else {
  }
}
</script>

<template>
  <div class="navbar bg-neutral">
    <div class="flex-1">
      <a class="btn btn-primary text-xl" @click="toDashboard">BetterClassroom</a>
    </div>
    <div class="flex-none gap-2">
      <div class="dropdown dropdown-end">
        <ul
          tabindex="0"
          class="mt-3 z-[1] p-2 shadow menu menu-sm dropdown-content bg-secondary rounded-box w-52"
        >
          <li><a>Profile</a></li>
          <li><a>Settings</a></li>
          <li><a>Logout</a></li>
          <hr />
          <label class="cursor-pointer grid place-items-center m-2">
            <input
              type="checkbox"
              value="synthwave"
              class="toggle theme-controller bg-primary row-start-1 col-start-1 col-span-2"
            />
            <svg
              class="col-start-1 row-start-1 stroke-accent fill-accent"
              xmlns="http://www.w3.org/2000/svg"
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <circle cx="12" cy="12" r="5" />
              <path
                d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"
              />
            </svg>
            <svg
              class="col-start-2 row-start-1 stroke-neutral fill-neutral"
              xmlns="http://www.w3.org/2000/svg"
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
            </svg>
          </label>
        </ul>
      </div>
    </div>
    <!--<button v-if="dataStore.isLoggedIn" @click="logout" class="btn btn-secondary">Logout</button>-->
    <button v-if="isLoggedIn" @click="logout" class="btn btn-primary">Logout</button>
  </div>
</template>