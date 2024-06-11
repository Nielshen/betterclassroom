<script setup>
import { useRouter } from 'vue-router'
import { useDataStore } from '../stores/dataStore'
const dataStore = useDataStore()

const router = useRouter()

const toCourses = () => router.push('/courses')
const toTasks = () => router.push('/tasks')
const toDashboard = () => router.push('/')
</script>

<template>
<div>
    <div v-if="!dataStore.isStudent" class="drawer lg:drawer-open">
        <input id="my-drawer-2" type="checkbox" class="drawer-toggle" />
        <div class="drawer-content">
            <label for="my-drawer-2" class="btn btn-primary drawer-button lg:hidden">Open drawer</label>
            <router-view></router-view>
        </div>
        <div class="drawer-side">
            <label for="my-drawer-2" aria-label="close sidebar" class="drawer-overlay"></label>
            <ul class="menu p-4 w-80 min-h-full bg-secondary text-base-content">
                <li><a @click="toCourses" >Kurse</a></li>
                <li><a @click="toDashboard">Dashboard</a></li>
            </ul>
        </div>
    </div>
    <div v-else>
    <router-view></router-view>
    </div>
</div>
</template>