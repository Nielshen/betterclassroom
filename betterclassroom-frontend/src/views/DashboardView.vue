<script setup>
import { ref } from 'vue'
import DashboardTable from '../components/DashboardTable.vue'
import axios from 'axios'

const tableCount = ref(20)
/*
    Hier direkt DashboardPersonen auflösen und pro DashboardTable 2 personen dem <DashboardTable> weitergeben?
*/
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
