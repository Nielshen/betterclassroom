import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useDataStore = defineStore('dataStore', () => {
  const user = ref({})
  const tasks = ref([])
  const dashboardData = ref([])

  const isStudent = computed(() => user.value.role === 'student')
  const isProfessor = computed(() => user.value.role === 'professor')
  const isLoggedIn = computed(() => !!user.value.role)

  const initStudent = () => {
    user.value = { role: 'student' }
  }

  const saveStudentLocally = ({ id, table }) => {
    try {
      user.value = { id, table, role: 'student', help_requested: false, current_exercise: 0 }
      console.log('User value', user.value)
      sessionStorage.setItem('user', JSON.stringify(user.value))
      console.log('Lokale Benutzerdaten gespeichert:', user.value)
      return true
    } catch (e) {
      console.error('Error saving student to local storage: ', e)
      return false
    }
  }

  const saveProfessorLocally = ({ id, firstName, lastName, email}) => {
    try {
      user.value = { id, firstName, lastName, email, role: 'professor' }
      console.log('User value', user.value)
      sessionStorage.setItem('user', JSON.stringify(user.value))
      console.log('Lokale Benutzerdaten gespeichert:', user.value)
      return true
    } catch (e) {
      console.error('Error saving professor to local storage: ', e)
      return false
    }
  }

  const checkUser = () => {
    const userString = sessionStorage.getItem('user')
    console.log('Check user: ', userString)
    if (userString) {
      user.value = JSON.parse(userString)
      return true
    }
    return false
  }

  const checkProfessor = () => {
    const profString = sessionStorage.getItem('user')
    console.log('Check professor: ', profString)
    if (profString) {
      user.value = JSON.parse(profString)
      return true
    }
    return false
  }

  const updateUserField = (fieldName, fieldValue) => {
    if (fieldName in user.value && typeof fieldValue === typeof user.value[fieldName]) {
      user.value[fieldName] = fieldValue
      const updatedUser = { ...user.value, [fieldName]: fieldValue }
      sessionStorage.setItem('user', JSON.stringify(updatedUser))
      console.log(`Updated ${fieldName} in user data:`, updatedUser)
    } else {
      console.error(`Error: Type mismatch or invalid field ${fieldName}`)
    }
  }

  const readUser = () => {
    console.log('Reading user from sessionStorage')
    const user = JSON.parse(sessionStorage.getItem('user'))
    if (user) {
      return user
    } else {
      console.error('No user found in sessionStorage')
      return {}
    }
  }

  const readProfessor = () => {
    console.log('Reading professor from sessionStorage')
    const professor = JSON.parse(sessionStorage.getItem('user'))
    if (professor) {
      return professor
    } else {
      console.error('No professor found in sessionStorage')
      return {}
    }
  }

  const deleteStudentLocally = () => {
    user.value = {}
    sessionStorage.removeItem('user')
    console.log({ user: !!user.value })
  }

  const deleteProfessorLocally = () => {
    user.value = {}
    sessionStorage.removeItem('user')
    console.log({ user: !!user.value })
  }

  const updateTasks = (newTasks) => {
    tasks.value = newTasks
  }

  const alterTask = (exerciseId, newName, newDescription) => {
    const taskIndex = tasks.value.findIndex((task) => task.id === exerciseId)
    if (taskIndex !== -1) {
      tasks.value[taskIndex].description = newDescription
      tasks.value[taskIndex].name = newName
    } else {
      console.error(`Exercise with id ${exerciseId} not found`)
    }
  }

  const addNewSubexercise = (newSubexercise) => {
    if (newSubexercise && newSubexercise.id && newSubexercise.name && newSubexercise.description) {
      tasks.value = [...tasks.value, newSubexercise]
    } else {
      console.error('Attempted to add invalid subexercise:', newSubexercise)
    }
  }

  const deleteSubexercise = (subexerciseId) => {
    const index = tasks.value.findIndex((task) => task.id === subexerciseId)
    if (index !== -1) {
      tasks.value.splice(index, 1)
      console.log(`Subexercise with id ${subexerciseId} has been deleted`)
    } else {
      console.error(`Subexercise with id ${subexerciseId} not found`)
    }
  }

  const getTasks = computed(() => tasks.value)

  return {
    user,
    tasks: getTasks,
    isStudent,
    isProfessor,
    isLoggedIn,
    dashboardData,
    initStudent,
    saveStudentLocally,
    saveProfessorLocally,
    checkUser,
    checkProfessor,
    updateUserField,
    readUser,
    deleteStudentLocally,
    deleteProfessorLocally,
    updateTasks,
    alterTask,
    addNewSubexercise,
    deleteSubexercise
  }
})
