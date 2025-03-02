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
          <li v-for="schedule in dueSchedules" :key="schedule.id">
            {{ schedule.task.description }} (Due: {{ schedule.due_date }})
          </li>
        </ul>
      </div>
      <div class="card">
        <h2>Completed Tasks</h2>
        <p>{{ completedSchedules.length }}</p>
        <ul>
          <li v-for="schedule in completedSchedules" :key="schedule.id">
            {{ schedule.task.description }} (Completed: {{ schedule.completion_date }})
          </li>
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
import axios from 'axios'

export default {
  name: 'DashboardPage',
  data() {
    return {
      tasks: [],
      schedules: [],
      csrfToken: null
    }
  },
  computed: {
    plannedTasks() {
      return this.tasks.filter(task => !this.schedules.some(s => s.task.id === task.id && s.status === 'completed'))
    },
    dueSchedules() {
      return this.schedules.filter(s => s.status === 'pending' && new Date(s.due_date) <= new Date())
    },
    completedSchedules() {
      return this.schedules.filter(s => s.status === 'completed')
    }
  },
  mounted() {
    this.fetchCsrfToken().then(() => {
      this.fetchTasks()
      this.fetchSchedules()
    })
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
        headers: { 'X-CSRFToken': this.csrfToken }
      })
        .then(response => {
          this.tasks = response.data
        })
        .catch(error => {
          console.error('Error fetching tasks:', error)
        })
    },
    fetchSchedules() {
      axios.get('http://localhost:8000/api/schedules/', {
        withCredentials: true,
        headers: { 'X-CSRFToken': this.csrfToken }
      })
        .then(response => {
          this.schedules = response.data
        })
        .catch(error => {
          console.error('Error fetching schedules:', error)
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