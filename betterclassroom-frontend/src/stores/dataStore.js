import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { getApiUrl } from '@/utils/common'
const rawUrl = getApiUrl()
const api_url = `http://${rawUrl}/api`
export const useDataStore = defineStore('dataStore', () => {
    const user = ref({})

    const isStudent = computed(() => user.value.role === 'student')
    const isLoggedIn = computed(() => !!user.value.role)

    const dashboardData = ref([])

    const saveStudent = async ({ id, table,courseId }) => {
        try{
            const result = await axios.post(`${api_url}/students`, { course: courseId, id, table })
            console.log(result)
            user.value = { id, table,  role: 'student' }
            localStorage.setItem('user', JSON.stringify(user.value))
            return true
        } catch(e){
            console.error(e)
            return false
        }

    }

    const initStudent = () => {
        user.value = { role: 'student' }
    }

    const deleteStudent = async () => {
        const oldId = user.value.id
        user.value = {}
        localStorage.removeItem('user')
        try{
            //const result = axios.delete(`${api_url}/students/${oldId}`)
        console.log({ user: !!user.value })
            return true
        } catch(e){
            console.error(e)
        console.log({ user: user.value })
            return false
        }
    }

    const checkUser = () => {
        console.log('checkUser')
        const userString = localStorage.getItem('user')
        if (userString) {
            user.value = JSON.parse(userString)
            return true
        }
        return false
    }


    return { user, isStudent, isLoggedIn, dashboardData ,saveStudent, deleteStudent, checkUser, initStudent}

})