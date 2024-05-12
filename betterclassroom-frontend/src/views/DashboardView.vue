<script setup>
import { ref } from 'vue'
import DashboardTable from '../components/DashboardTable.vue'

const tableCount = ref(20)
/*
    Hier direkt DashboardPersonen auflösen und pro DashboardTable 2 personen dem <DashboardTable> weitergeben?
*/
const data = [
    {
        name: "Max Mustermann",
        seat: "C1",
        maxTasks: 5,
        finishedTasks: 3
    },
    {
        name: "Max Mustermann",
        seat: "C1",
        maxTasks: 5,
        finishedTasks: 3
    },
    {
        name: "Max Mustermann",
        seat: "C1",
        maxTasks: 5,
        finishedTasks: 3
    },
    {
        name: "Max Mustermann",
        seat: "C1",
        maxTasks: 5,
        finishedTasks: 3
    },
];

</script>
<template>
    <div class="flex flex-row">
        <div class="flex flex-col justify-center m-4">
            <div class="flex flex-row flex-wrap justify-center">
                <DashboardTable v-for="e in tableCount" />
            </div>
        </div>
    </div>
</template>