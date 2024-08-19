<script setup>
import DashboardPerson from '../components/DashboardPerson.vue'
import { onBeforeMount, defineProps, computed, ref, watch } from 'vue'

const props = defineProps({
  tableNumber: Number,
  table: {
    type: Object,
    required: true
  },
  exerciseCount: Number
})

const student1_finishedTasks = ref(0)
const student1_maxTasks = ref(0)
const student1_raisedHand = ref(false)
const student2_finishedTasks = ref(0)
const student2_maxTasks = ref(0)
const student2_raisedHand = ref(false)

const loadTable = async () => {
  if (props.table.student1) {
    student1_finishedTasks.value = props.table.student1.current_exercise || 1
    student1_maxTasks.value = props.exerciseCount
    student1_raisedHand.value = props.table.student1.help_requested
  }

  if (props.table.student2) {
    student2_finishedTasks.value = props.table.student2.current_exercise || 1
    student2_maxTasks.value = props.exerciseCount
    student2_raisedHand.value = props.table.student2.help_requested
  }
}

onBeforeMount(async () => {
  await loadTable()
})

watch(
  () => props.table,
  (newTable, oldTable) => {
    console.log('Table changed')
    console.log(newTable)
    loadTable()
  },
  { deep: true }
)
</script>
<template>
  <div
    class="card w-full sm:w-[13rem] md:w-[14rem] lg:w-[15rem] xl:w-[17rem] h-[7rem] overflow-hidden bg-primary text-primary-content my-2 mr-3"
  >
    <div class="pl-3 pr-3">
      <div class="flex flex-row justify-between">
        <div class="mt-0" v-if="props.table.student2 != null">
          <DashboardPerson
            :name="props.table.student2._id"
            :finishedTasks="student2_finishedTasks"
            :maxTasks="student2_maxTasks"
            :raisedHand="student2_raisedHand"
          />
        </div>
        <div class="mt-0" v-if="props.table.student1 != null">
          <DashboardPerson
            :name="props.table.student1._id"
            :finishedTasks="student1_finishedTasks"
            :maxTasks="student1_maxTasks"
            :raisedHand="student1_raisedHand"
          />
        </div>
      </div>
    </div>
  </div>
</template>
