import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useDataStore = defineStore('dataStore', () => {
  const user = ref({})
  const isStudent = computed(() => user.value.role === 'student')
  const isLoggedIn = computed(() => !!user.value.role)
  const dashboardData = ref([])

  const initStudent = () => {
    user.value = { role: 'student' }
  }

  const saveStudentLocally = ({ id, table, course }) => {
    try {
      user.value = { id, table, role: 'student', help_requested: false, current_exercise: 1 }
      console.log('User value', user.value)
      localStorage.setItem('user', JSON.stringify(user.value))
      console.log('Lokale Benutzerdaten gespeichert:', user.value)
      return true
    } catch (e) {
      console.error('Error saving student to local storage: ', e)
      return false
    }
  }

  const checkUser = () => {
    const userString = localStorage.getItem('user')
    console.log('Check user: ', userString)
    if (userString) {
      user.value = JSON.parse(userString)
      return true
    }
    return false
  }

  const updateUserField = (fieldName, fieldValue) => {
    if (fieldName in user.value && typeof fieldValue === typeof user.value[fieldName]) {
      user.value[fieldName] = fieldValue // Directly update the reactive property
      localStorage.setItem('user', JSON.stringify(user.value)) // Update local storage to sync
      console.log(`Updated ${fieldName} in user data:`, user.value)
    } else {
      console.error(`Error: Type mismatch or invalid field ${fieldName}`)
    }
  }

  const readUser = () => {
    console.log('Reading user from localStorage')
    const user = JSON.parse(localStorage.getItem('user'))
    if (user) {
      return user
    } else {
      console.error('No user found in localStorage')
      return {}
    }
  }

  const deleteStudentLocally = () => {
    user.value = {}
    localStorage.removeItem('user')
    console.log({ user: !!user.value })
  }

  return {
    user,
    isStudent,
    isLoggedIn,
    dashboardData,
    initStudent,
    saveStudentLocally,
    checkUser,
    updateUserField,
    readUser,
    deleteStudentLocally
  }
})
