<template>
    <div class="tasks">
      <h1>Tasks</h1>
      <table>
        <thead>
          <tr>
            <th>Description</th>
            <th>Frequency</th>
            <th>Equipment</th>
            <th>Assigned To</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in tasks" :key="task.id">
            <td>{{ task.description }}</td>
            <td>{{ task.frequency || 'One-Time' }}</td>
            <td>{{ task.equipment }}</td>
            <td>{{ task.assigned_to }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <style scoped>
    .tasks {
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }
    th, td {
      border: 1px solid #ddd;
      padding: 8px;
      text-align: left;
    }
    th {
      background-color: #f2f2f2;
    }
    tr:nth-child(even) {
      background-color: #f9f9f9;
    }
  </style>
  
  <script>
  export default {
    name: 'TasksPage',
    data() {
      return {
        tasks: [
          { id: 1, description: 'Oil Change', frequency: 'monthly', equipment: 'Main Generator', assigned_to: 'tech1' },
          { id: 2, description: 'Replace Capacitor', frequency: null, equipment: 'Pump System', assigned_to: 'tech2' }
        ]
      }
    }
  }
  </script>