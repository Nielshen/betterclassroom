<script setup>
import { ref } from 'vue'
import DashboardTable from '../components/DashboardTable.vue'
import axios from 'axios'
import { getApiUrl } from '@/utils/common'

const tableCount = ref(20)
/*
    Unsere parameter:
    class Course(BaseModel):
        id: str
        description: str
        exercises: List[Exercise] = Field(default_factory=list)
        participants: List[str] = Field(default_factory=list)
        classroom: str
        professor: int

    Auf eine Aufgabe klicken -> Dashboard mit Tischen soll angezeigt werden

    Aus participants Student herauslesen

    class Student(BaseModel):
        id: str
        table: int
        course: str
        progress: Dict[str, bool] = Field(default_factory=dict)
        help_requested: bool = False

*/

/* test parameter course*/
const course_id = "Web-Technologien"
const course_description = "Example description"
const course_exercises = ("Deployment mit Firebase", "test")
const participants = ("Anna", "Bedric")
const course_classroom = "O-201"
const course_professor = 1

/* test parameter participants / students */
const participant1_id = "Anna"
const participant1_table = 0
const participant1_course = "Web-Technologien"
const participant1_progress = ["20", false] /* [exercise_id, false/true] */
const participant1_help_requested = false

const participant2_id = "Bedric"
const participant2_table = 1
const participant2_course = "Web-Technologien"
const participant2_progress = ["100", true]
const participant2_help_requested = false

const rawUrl = getApiUrl()
const api_url = `http://${rawUrl}/api`

const helloApi = () => {
    axios.get(api_url)
        .then(response => {
            console.log(response.data)
        })
        .catch(error => {
            console.log(error)
        })
}

// helloApi()


</script>
<template>
    <div>
    </div>
</template>
