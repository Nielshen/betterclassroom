<script setup>
import { ref } from 'vue'
import DashboardTable from '../components/DashboardTable.vue'
import axios from 'axios'

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

const api_url = import.meta.env.VITE_API_PROD_URL

const helloApi = () => {
    axios.get(api_url )
    .then(response => {
        console.log(response.data)
    })
    .catch(error => {
        console.log(error)
    })
}

helloApi()


</script>
<template>
<div>
<div class="flex justify-end m-4">
    <button class="btn btn-warning">Beenden</button>
    </div>
    <div class="flex flex-row ">
        <div class="flex flex-col justify-center m-4">
            <div class="flex flex-row flex-wrap justify-center">
                <DashboardTable v-for="e in tableCount" />
            </div>
        </div>
    </div>
    </div>
</template>
