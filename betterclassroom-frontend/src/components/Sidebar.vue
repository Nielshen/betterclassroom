<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();
</script>

<template>
    <div class="drawer lg:drawer-open ">
        <input id="my-drawer-2" type="checkbox" class="drawer-toggle" />
        <div class="drawer-content flex flex-col items-center">
            <label for="my-drawer-2" class="btn btn-primary drawer-button lg:hidden">Open drawer</label>
            <router-view></router-view>
        </div>
        <div class="drawer-side">
            <label for="my-drawer-2" aria-label="close sidebar" class="drawer-overlay"></label>
            <ul class="menu p-4 w-80 min-h-full bg-base-200 text-base-content">
                <li><a @click="router.push('/courses')">Kurse</a></li>
                <li><a @click="router.push('/createtasks')">Aufgaben</a></li>
                <li><a @click="router.push('/students')">Studenten</a></li>
            </ul>

        </div>
    </div>
</template>