<script setup>
import { useRouter } from "vue-router"

const router = useRouter()

const newCourse = () => router.push("/createCourse")

const data = [
    {
        name: "Software Qualitätssicherung",
        raum: "O-201",
        count: 25
    },
    {
        name: "Web-Technologien",
        raum: "O-301",
        count: 14
    },
    {
        name: "Softwarearchitekturen",
        raum: "O-107",
        count: 20
    },
    {
        name: "Programmiertechnik 1",
        raum: "O-002",
        count: 32
    },
]

</script>

<template>
    <div class="overflow-x-auto">
        <div class="flex flex-col  justify-start items-start ">
        <table class="table-lg">
            <!-- head -->
            <thead>
                <tr>
                    <th>Kurs</th>
                    <th>Raum</th>
                    <th>Teilnehmer</th>
                </tr>
            </thead>
            <tbody v-for="e in data" >
                <!-- row 1 -->
                <tr class="bg-base-200">
                    <td>{{ e.name }}</td>
                    <td>{{ e.raum }}</td>
                    <td>{{ e.count }} Teilnehmende</td>
                    <td>
                    <div>
                    <button class="btn btn-accent mr-4 ">Bearbeiten</button>
                    <button class="btn btn-accent ">Starten</button>
                    </div>
                    </td>
                </tr>
            </tbody>
        </table>
        <button class="btn btn-accent mt-4" @click="newCourse" >Neuer Kurs</button>
        </div>
    </div>
</template>