<template>
  <div class="parts">
    <h1>Parts Inventory</h1>
    <table v-if="parts.length">
      <thead>
        <tr>
          <th>Part Number</th>
          <th>Status</th>
          <th>Equipment</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="part in parts" :key="part.id">
          <td>{{ part.part_number }}</td>
          <td>{{ part.status }}</td>
          <td>{{ part.equipment ? part.equipment.name : 'None' }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>Loading parts...</p>
  </div>
</template>

<style scoped>
  .parts {
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
  name: 'PartsPage',
  data() {
    return {
      parts: [],
      csrfToken: null
    }
  },
  mounted() {
    this.fetchCsrfToken().then(() => this.fetchParts())
  },
  methods: {
    async fetchCsrfToken() {
      try {
        await axios.get('http://localhost:8000/api/parts/', { withCredentials: true })
        this.csrfToken = this.getCsrfToken()
      } catch (error) {
        console.error('Error fetching CSRF token:', error)
      }
    },
    fetchParts() {
      axios.get('http://localhost:8000/api/parts/', {
        withCredentials: true,
        headers: {
          'X-CSRFToken': this.csrfToken
        }
      })
        .then(response => {
          this.parts = response.data
        })
        .catch(error => {
          console.error('Error fetching parts:', error)
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