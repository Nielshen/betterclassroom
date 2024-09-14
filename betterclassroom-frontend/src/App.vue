<script setup>
import Navbar from './components/Navbar.vue'
import Sidebar from './components/Sidebar.vue'
</script>

<template>
  <Navbar />
  <Sidebar />
  <notifications width="300px" position="top center" :duration="2000" :speed="300" classes="my-notification" />
</template>

<style>
.my-notification {
  margin: 80px 0;
  padding: 10px;
  font-size: 14px;
  font-weight: 600;
  border-radius: 0; /* Remove border radius to make it square */
  opacity: 0.9;
}

.my-notification.success {
  background-color: #4CAF50;
  border-left: 5px solid #2E7D32;
}

.my-notification.error {
  background-color: #F44336;
  border-left: 5px solid #D32F2F;
}

.my-notification.warn {
  background-color: #FFC107;
  border-left: 5px solid #FFA000;
}

.my-notification.info {
  background-color: #2196F3;
  border-left: 5px solid #1976D2;
}
</style>