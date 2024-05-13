<script setup>

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
]

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
                <li><a href="/courses">Kurse</a></li>
                <li><a href="/tasks">Aufgaben</a></li>
                <li><a href="/dashboard">Studenten</a></li>
            </ul>

        </div>
    </div>
</template>