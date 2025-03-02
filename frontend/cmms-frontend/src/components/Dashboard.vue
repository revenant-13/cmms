<template>
    <div class="dashboard">
      <h1>Dashboard</h1>
      <div class="summary">
        <div class="card">
          <h2>Planned Tasks</h2>
          <p>{{ plannedTasks.length }}</p>
          <ul>
            <li v-for="task in plannedTasks" :key="task.id">{{ task.description }}</li>
          </ul>
        </div>
        <div class="card">
          <h2>Due Schedules</h2>
          <p>{{ dueSchedules.length }}</p>
          <ul>
            <li v-for="schedule in dueSchedules" :key="schedule.id">{{ schedule.task }} (Due: {{ schedule.due_date }})</li>
          </ul>
        </div>
        <div class="card">
          <h2>Completed Tasks</h2>
          <p>{{ completedSchedules.length }}</p>
          <ul>
            <li v-for="schedule in completedSchedules" :key="schedule.id">{{ schedule.task }} (Completed: {{ schedule.completion_date }})</li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <style scoped>
    .dashboard {
      max-width: 1000px;
      margin: 0 auto;
      padding: 20px;
    }
    .summary {
      display: flex;
      justify-content: space-between;
      gap: 20px;
    }
    .card {
      flex: 1;
      border: 1px solid #ddd;
      padding: 15px;
      border-radius: 5px;
      background-color: #fff;
    }
    ul {
      list-style-type: none;
      padding: 0;
    }
    li {
      margin: 5px 0;
    }
  </style>
  
  <script>
  export default {
    name: 'DashboardPage',
    data() {
      return {
        plannedTasks: [
          { id: 1, description: 'Oil Change' },
          { id: 2, description: 'Inspect Belts' }
        ],
        dueSchedules: [
          { id: 1, task: 'Oil Change', due_date: '2025-03-03' },
          { id: 2, task: 'Inspect Belts', due_date: '2025-03-05' }
        ],
        completedSchedules: [
          { id: 3, task: 'Replace Capacitor', completion_date: '2025-03-01' }
        ]
      }
    }
  }
  </script>