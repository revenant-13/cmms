<template>
  <div class="tasks">
    <h1>Tasks</h1>
    <table v-if="tasks.length">
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
          <td>{{ task.equipment.name }}</td>
          <td>{{ task.assigned_to ? task.assigned_to.username : 'Unassigned' }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>Loading tasks...</p>
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
import axios from 'axios'

export default {
  name: 'TasksPage',
  data() {
    return {
      tasks: [],
      csrfToken: null
    }
  },
  mounted() {
    this.fetchCsrfToken().then(() => this.fetchTasks())
  },
  methods: {
    async fetchCsrfToken() {
      try {
        await axios.get('http://localhost:8000/api/tasks/', { withCredentials: true })
        this.csrfToken = this.getCsrfToken()
      } catch (error) {
        console.error('Error fetching CSRF token:', error)
      }
    },
    fetchTasks() {
      axios.get('http://localhost:8000/api/tasks/', {
        withCredentials: true,
        headers: {
          'X-CSRFToken': this.csrfToken
        }
      })
        .then(response => {
          this.tasks = response.data
        })
        .catch(error => {
          console.error('Error fetching tasks:', error)
        })
    },
    getCsrfToken() {
      const name = 'csrftoken'
      let cookieValue = null
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim()
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
            break
          }
        }
      }
      return cookieValue
    }
  }
}
</script>