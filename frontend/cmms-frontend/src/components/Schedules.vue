<template>
  <div class="schedules">
    <h1>Schedules</h1>
    <table>
      <thead>
        <tr>
          <th>Task</th>
          <th>Due Date</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="schedule in schedules" :key="schedule.id">
          <td>{{ schedule.task }}</td>
          <td>{{ schedule.due_date }}</td>
          <td>{{ schedule.status }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
  .schedules {
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
  name: 'SchedulesPage',
  data() {
    return {
      schedules: [
        { id: 1, task: 'Oil Change', due_date: '2025-03-03', status: 'pending' },
        { id: 2, task: 'Replace Capacitor', due_date: '2025-03-06', status: 'completed' }
      ]
    }
  }
}
</script>