import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
export const useDataStore = defineStore('dataStore', () => {
    const user = ref({})

    const isStudent = computed(() => user.value.role === 'student')
    const isLoggedIn = computed(() => !!user.value.role)

    const dashboardData = ref([])

    const saveStudent = ({ id, table }) => {
        user.value = { id, table,  role: 'student' }
        localStorage.setItem('user', JSON.stringify(user.value))
    }

    const initStudent = () => {
        user.value = { role: 'student' }
    }

    const deleteStudent = () => {
        user.value = {}
        localStorage.removeItem('user')
    }

    const checkUser = () => {
        const userString = localStorage.getItem('user')
        if (userString) {
            user.value = JSON.parse(userString)
            return true
        }
        return false
    }


    return { user, isStudent, isLoggedIn, dashboardData ,saveStudent, deleteStudent, checkUser, initStudent}

})