<script setup>
import { onBeforeMount, ref } from 'vue'
import DashboardTable from '../components/DashboardTable.vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const courseId = route.params.courseId
const exerciseId = route.params.taskId /*Exercise ID*/

const tableCount = 20 /* Count of table is hardcoded as 20 / 5 rows, 4 tables per row, when it's variable and in DB, find out how much tables are in this room*/
const tableOccupation = ref([])

const apiUrl = import.meta.env.VITE_API_PROD_URL

const loadCourse = async () => {
  try {
    /* Get our current course */
    const courseResponse = await axios.get(`${apiUrl}/course`)
    const _course = courseResponse.data

    const currentCourse = _course.find((course) => course._id === courseId)
    if (!currentCourse) {
      console.error('Course not found')
      return
    }
    //console.log(currentCourse)

    const participants = currentCourse.participants
    //console.log(participants)

    /* Get all students */
    const studentsResponse = await axios.get(`${apiUrl}/students`)
    const _students = studentsResponse.data
    const relevantStudents = _students.filter((student) => student.course === courseId)
    //console.log(relevantStudents)

    const tableOccupancy = Array(tableCount).fill().map(() => ({ student1: null, student2: null }))

    relevantStudents.forEach((student) => {
      const studentTable = tableOccupancy[student.table - 1]
      if (studentTable ? studentTable.student1 === null : null) {
        studentTable.student1 = student
      } else if (studentTable ? studentTable.student2 === null : null) {
        studentTable.student2 = student
      }
    })

    tableOccupation.value = tableOccupancy
    //console.log(tableOccupation.value)
  } catch (error) {
    console.error('Error loading course data:', error)
  }
}

onBeforeMount(async () => {
  await loadCourse()
})


</script>
<template>
  <div>
    <div class="flex justify-end m-4">
      <button class="btn btn-warning">Beenden</button>
    </div>
    <div class="flex flex-row">
      <div class="flex flex-col justify-center m-4">
        <div class="flex flex-row flex-wrap justify-center">
          <DashboardTable v-for="table in tableOccupation" :tableNumber="table.id" :table="table" />
        </div>
      </div>
    </div>
  </div>
</template>
