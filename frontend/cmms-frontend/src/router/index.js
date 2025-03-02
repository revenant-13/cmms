import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Equipment from '../components/Equipment.vue'
import Parts from '../components/Parts.vue'
import Tasks from '../components/Tasks.vue'
import Schedules from '../components/Schedules.vue'

const routes = [
  { path: '/', name: 'HomePage', component: Home },
  { path: '/equipment', name: 'EquipmentPage', component: Equipment },
  { path: '/parts', name: 'PartsPage', component: Parts },
  { path: '/tasks', name: 'TasksPage', component: Tasks },
  { path: '/schedules', name: 'SchedulesPage', component: Schedules }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router