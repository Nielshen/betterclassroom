<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();

const toCourses = () => router.push('/courses');
const toTasks = () => router.push('/tasks');
const toDashboard = () => router.push("/");

</script>

<template>
    <div class="drawer lg:drawer-open">
        <input id="my-drawer-2" type="checkbox" class="drawer-toggle" />
        <div class="drawer-content flex flex-col items-center">
            <label for="my-drawer-2" class="btn btn-primary drawer-button lg:hidden">Open drawer</label>
            <router-view></router-view>
        </div>
        <div class="drawer-side">
            <label for="my-drawer-2" aria-label="close sidebar" class="drawer-overlay"></label>
            <ul class="menu p-4 w-80 min-h-full bg-secondary text-base-content">
                <li><a @click="toCourses" >Kurse</a></li>
                <li> <a @click="toDashboard">Dashboard</a></li>
            </ul>

        </div>
    </div>
</template>