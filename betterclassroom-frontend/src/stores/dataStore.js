import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
export const useDataStore = defineStore('dataStore', () => {
    const user = ref({})

    const isStudent = computed(() => user.value.role === 'student')
    const isLoggedIn = computed(() => !!user.value.role)

    const dashboardData = ref([])


    return { user, isStudent, isLoggedIn, dashboardData}

})