<script setup>
import { ref } from 'vue'
import DashboardPerson from '../components/DashboardPerson.vue'


const roomRow = ref(5)
const roomCol = ref(4)

const  data = [
    {
        name: "Max Mustermann",
        seat: "C1",
        maxTasks: 5,
        finishedTasks: 3
    },
    {
        name: "Anna Schmidt",
        seat: "A2",
        maxTasks: 5,
        finishedTasks: 2
    },
    {
        name: "Johann Müller",
        seat: "B3",
        maxTasks: 5,
        finishedTasks: 4
    },
    {
        name: "Sophie Wagner",
        seat: "D4",
        maxTasks: 5,
        finishedTasks: 1
    },
    {
        name: "Felix Fischer",
        seat: "E5",
        maxTasks: 5,
        finishedTasks: 5
    },
    {
        name: "Laura Weber",
        seat: "F6",
        maxTasks: 5,
        finishedTasks: 3
    },
    {
        name: "Simon Schmitt",
        seat: "G7",
        maxTasks: 5,
        finishedTasks: 2
    },
    {
        name: "Lena Richter",
        seat: "H8",
        maxTasks: 5,
        finishedTasks: 4
    },
    {
        name: "David Becker",
        seat: "I9",
        maxTasks: 5,
        finishedTasks: 1
    },
    {
        name: "Emilia Koch",
        seat: "J10",
        maxTasks: 5,
        finishedTasks: 5
    },
    {
        name: "Julius Schulz",
        seat: "K11",
        maxTasks: 5,
        finishedTasks: 3
    },
    {
        name: "Hannah Meier",
        seat: "L12",
        maxTasks: 5,
        finishedTasks: 2
    },
    {
        name: "Nico Lehmann",
        seat: "M13",
        maxTasks: 5,
        finishedTasks: 4
    },
    {
        name: "Mia Herrmann",
        seat: "N14",
        maxTasks: 5,
        finishedTasks: 1
    },
    /*
    {
        name: "Tim Neumann",
        seat: "O15",
        maxTasks: 5,
        finishedTasks: 5
    },
    {
        name: "Lea Schwarz",
        seat: "P16",
        maxTasks: 5,
        finishedTasks: 3
    },
    {
        name: "Paula Zimmermann",
        seat: "Q17",
        maxTasks: 5,
        finishedTasks: 2
    },
    {
        name: "Jonas Richter",
        seat: "R18",
        maxTasks: 5,
        finishedTasks: 4
    },
    {
        name: "Lara Vogel",
        seat: "S19",
        maxTasks: 5,
        finishedTasks: 1
    },
    {
        name: "Tom Fuchs",
        seat: "T20",
        maxTasks: 5,
        finishedTasks: 5
    },
    {
        name: "Marie Kaiser",
        seat: "U21",
        maxTasks: 5,
        finishedTasks: 3
    },
    {
        name: "Kevin Werner",
        seat: "V22",
        maxTasks: 5,
        finishedTasks: 2
    },
    {
        name: "Sara Schäfer",
        seat: "W23",
        maxTasks: 5,
        finishedTasks: 4
    },
    {
        name: "Erik Lange",
        seat: "X24",
        maxTasks: 5,
        finishedTasks: 1
    },
    {
        name: "Carla Haas",
        seat: "Y25",
        maxTasks: 5,
        finishedTasks: 5
    },
    {
        name: "Tobias Krause",
        seat: "Z26",
        maxTasks: 5,
        finishedTasks: 3
    },
    {
        name: "Sarah Berger",
        seat: "AA27",
        maxTasks: 5,
        finishedTasks: 2
    },
    {
        name: "Alexander Lehmann",
        seat: "AB28",
        maxTasks: 5,
        finishedTasks: 4
    },
    {
        name: "Melanie Huber",
        seat: "AC29",
        maxTasks: 5,
        finishedTasks: 1
    },
    {
        name: "Benjamin Vogt",
        seat: "AD30",
        maxTasks: 5,
        finishedTasks: 5
    },
    {
        name: "Lisa Schulze",
        seat: "AE31",
        maxTasks: 5,
        finishedTasks: 3
    },
    {
        name: "Robin Lorenz",
        seat: "AF32",
        maxTasks: 5,
        finishedTasks: 2
    },
    {
        name: "Julia Frank",
        seat: "AG33",
        maxTasks: 5,
        finishedTasks: 4
    },
    {
        name: "Philipp Berger",
        seat: "AH34",
        maxTasks: 5,
        finishedTasks: 1
    },
    {
        name: "Luisa Voigt",
        seat: "AI35",
        maxTasks: 5,
        finishedTasks: 5
    },
    {
        name: "Christian Keller",
        seat: "AJ36",
        maxTasks: 5,
        finishedTasks: 3
    },
    {
        name: "Laura Möller",
        seat: "AK37",
        maxTasks: 5,
        finishedTasks: 2
    },
    {
        name: "Dominik Braun",
        seat: "AL38",
        maxTasks: 5,
        finishedTasks: 4
    },
    {
        name: "Vanessa Simon",
        seat: "AM39",
        maxTasks: 5,
        finishedTasks: 1
    },
    {
        name: "Marc Schuster",
        seat: "AN40",
        maxTasks: 5,
        finishedTasks: 5
    }
    */
];



</script>
<template>
<div class="flex flex-row">
   <div class="drawer lg:drawer-open ">
  <input id="my-drawer-2" type="checkbox" class="drawer-toggle" />
  <div class="drawer-content flex flex-col items-center justify-center">
    <label for="my-drawer-2" class="btn btn-primary drawer-button lg:hidden">Open drawer</label>
  
  </div> 
  <div class="drawer-side">
    <label for="my-drawer-2" aria-label="close sidebar" class="drawer-overlay"></label> 
    <ul class="menu p-4 w-80 min-h-full bg-base-200 text-base-content">
      <li><a>Kurse</a></li>
      <li><a>Aufgaben</a></li>
      <li><a>Studenten</a></li>
    </ul>
  
  </div>
</div>
<div class="flex flex-col justify-center">
    <div class="flex flex-row flex-wrap justify-start items-center static">
    <DashboardPerson v-for="e in data" :key="e" :name="e.name" :seat="e.seat" :maxTasks="e.maxTasks" :finishedTasks="e.finishedTasks" />
    </div>
</div>
</div>
</template>