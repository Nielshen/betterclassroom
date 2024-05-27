<script setup>
import DashboardPerson from '../components/DashboardPerson.vue'
import { onBeforeMount, defineProps, computed, ref } from 'vue'

const props = defineProps({
  tableNumber: Number,
  table: {
    type: Object,
    required: true
  }
})

console.log(props.tableNumber)

const student1_finishedTasks = ref(0)
const student1_maxTasks = ref(0)
const student1_raisedHand = ref(false)
const student2_finishedTasks = ref(0)
const student2_maxTasks = ref(0)
const student2_raisedHand = ref(false)

const loadTable = async () => {
  if (props.table.student1) {
    student1_finishedTasks.value = props.table.student1.progress ? Object.values(props.table.student1.progress).filter(task => task).length : 0
    student1_maxTasks.value = props.table.student1.progress ? Object.keys(props.table.student1.progress).length : 0
    student1_raisedHand.value = props.table.student1.help_requested
    //console.log(props.table.student1)
  }

  if (props.table.student2) {
    student2_finishedTasks.value = props.table.student2.progress ? Object.values(props.table.student2.progress).filter(task => task).length : 0
    student2_maxTasks.value = props.table.student2.progress ? Object.keys(props.table.student2.progress).length : 0
    student2_raisedHand.value = props.table.student2.help_requested
    //console.log(props.table.student2)
  }
}

onBeforeMount(async () => {
  await loadTable()
})

</script>
<template>
<!-- 30 -> Base / 8 -> Anzahl Karten -->
<!-- 20 -> Base / 5 -> Anzahl Karten -->
  <div class="card w-[20rem] h-[8rem] overflow-hidden bg-primary text-primary-content my-2 mr-3">
    <div class="p-3">
      <div class="flex flex-row justify-between">
        <div class="mt-0" v-if="props.table.student1 != null">
          <DashboardPerson :finishedTasks="student1_finishedTasks" :maxTasks="student1_maxTasks" :raisedHand="student1_raisedHand"/>
          <!-- Seat is hardcoded, because not saved in database 
          :name="props.table.student1._id"
          :name="props.table.student2._id"
          -->
        </div>
        <div class="mt-0" v-if="props.table.student2 != null">
          <DashboardPerson :finishedTasks="student2_finishedTasks" :maxTasks="student2_maxTasks" :raisedHand="student2_raisedHand"/>
        </div>
      </div>
    </div>
  </div>
</template>

