<script setup>
import DashboardPerson from '../components/DashboardPerson.vue'
import { defineProps, computed } from 'vue'

const tableNumber = 2

const props = defineProps(
    {
        name: String,
        seat: String,
        maxTasks: Number,
        finishedTasks: Number
    }
)


const data = [
    {
        name: "Max Mustermann",
        seat: "C1",
        maxTasks: 5,
        finishedTasks: 3
    },
];

</script>
<template>
<!-- 30 -> Base / 8 -> Anzahl Karten -->
<!-- 20 -> Base / 5 -> Anzahl Karten -->
  <div class="card w-[20rem] h-[8rem] overflow-hidden bg-primary text-primary-content my-2 mr-3">
    <div class="p-3">
      <div class="flex flex-row justify-between">
        <div class="mt-4">
          <DashboardPerson v-for="e in data" :key="e" :name="e.name" :seat="e.seat" :maxTasks="e.maxTasks" :finishedTasks="e.finishedTasks" />
        </div>
        <div class="mt-4">
          <DashboardPerson v-for="e in data" :raisedHand="true"  :key="e" :name="e.name" :seat="e.seat" :maxTasks="e.maxTasks" :finishedTasks="e.finishedTasks" />
        </div>
      </div>
    </div>
  </div>
</template>

