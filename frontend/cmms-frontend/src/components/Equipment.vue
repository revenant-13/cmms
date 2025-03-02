<template>
    <div class="equipment">
      <h1>Equipment Hierarchy</h1>
      <ul v-if="equipment.length">
        <li v-for="item in equipment" :key="item.id">
          {{ item.name }} (Model: {{ item.model }}) {{ item.serial }}
          <ul v-if="item.children && item.children.length">
            <li v-for="child in item.children" :key="child.id">
              {{ child.name }} (Model: {{ child.model }}) {{ child.serial }}
            </li>
          </ul>
        </li>
      </ul>
      <p v-else>Loading equipment...</p>
    </div>
  </template>
  
  <style scoped>
    .equipment {
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
    }
    ul {
      list-style-type: none;
      padding-left: 20px;
    }
    li {
      margin: 5px 0;
    }
  </style>
  
  <script>
import axios from 'axios'

export default {
  name: 'EquipmentPage',
  data() {
    return {
      equipment: []
    }
  },
  mounted() {
    this.fetchEquipment()
  },
  methods: {
    fetchEquipment() {
      axios.get('http://127.0.0.1:8000/api/equipment/', {
        withCredentials: true,
        headers: {
          'X-CSRFToken': this.getCsrfToken()
        }
      })
        .then(response => {
          this.equipment = response.data
        })
        .catch(error => {
          console.error('Error fetching equipment:', error)
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