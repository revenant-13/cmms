<template>
  <div class="parts">
    <h1>Parts Inventory</h1>
    <div class="form">
      <h2>{{ editingPart ? 'Edit Part' : 'Add New Part' }}</h2>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <form @submit.prevent="savePart">
        <input v-model="newPart.part_number" placeholder="Part Number" required />
        <input v-model="newPart.status" placeholder="Status" required />
        <select v-model="newPart.equipment" multiple>
          <option v-for="equip in equipmentList" :key="equip.id" :value="equip.id">
            {{ equip.name }}
          </option>
        </select>
        <button type="submit">{{ editingPart ? 'Update' : 'Add' }}</button>
        <button v-if="editingPart" type="button" @click="cancelEdit">Cancel</button>
      </form>
    </div>
    <table v-if="parts.length">
      <thead>
        <tr>
          <th>Part Number</th>
          <th>Status</th>
          <th>Equipment</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="part in parts" :key="part.id">
          <td>{{ part.part_number }}</td>
          <td>{{ part.status }}</td>
          <td>{{ part.equipment_details && part.equipment_details.length ? part.equipment_details.map(e => e.name).join(', ') : 'None' }}</td>
          <td><button @click="editPart(part)">Edit</button></td>
        </tr>
      </tbody>
    </table>
    <p v-else>Loading parts...</p>
  </div>
</template>

<style scoped>
  .parts {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
  }
  .form {
    margin-bottom: 20px;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  input, select, button {
    margin: 5px 0;
    padding: 8px;
    width: 100%;
    box-sizing: border-box;
  }
  select[multiple] {
    height: 100px;
  }
  button {
    background-color: #42b983;
    color: white;
    border: none;
    cursor: pointer;
  }
  button:hover {
    background-color: #2c3e50;
  }
  .error {
    color: red;
    margin-bottom: 10px;
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
      equipmentList: [],
      csrfToken: null,
      newPart: {
        part_number: '',
        status: '',
        equipment: []
      },
      editingPart: null,
      errorMessage: ''
    }
  },
  mounted() {
    this.fetchCsrfToken().then(() => {
      this.fetchEquipment()
      this.fetchParts()
    })
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
        headers: { 'X-CSRFToken': this.csrfToken }
      })
        .then(response => {
          this.parts = response.data
        })
        .catch(error => {
          console.error('Error fetching parts:', error)
        })
    },
    fetchEquipment() {
      axios.get('http://localhost:8000/api/equipment/', {
        withCredentials: true,
        headers: { 'X-CSRFToken': this.csrfToken }
      })
        .then(response => {
          this.equipmentList = response.data
        })
        .catch(error => {
          console.error('Error fetching equipment:', error)
        })
    },
    async savePart() {
      this.errorMessage = ''
      try {
        await this.fetchCsrfToken()
        const partData = { ...this.newPart }
        console.log('Sending part data:', partData)
        if (!partData.equipment.length) delete partData.equipment

        if (this.editingPart) {
          const response = await axios.put(`http://localhost:8000/api/parts/${this.editingPart.id}/`, partData, {
            withCredentials: true,
            headers: { 'X-CSRFToken': this.csrfToken }
          }).catch(error => {
            if (error.response && error.response.status === 400) {
              throw { response: error.response }
            }
            throw error
          })
          console.log('PUT response:', response.data)
        } else {
          await axios.post('http://localhost:8000/api/parts/', partData, {
            withCredentials: true,
            headers: { 'X-CSRFToken': this.csrfToken }
          })
        }
        this.fetchParts()
        this.resetForm()
      } catch (error) {
        if (error.response && error.response.status === 400) {
          this.errorMessage = error.response.data.detail || 'Invalid part data.'
        } else {
          console.error('Error saving part:', error)
          this.errorMessage = 'Failed to save part. Please try again.'
        }
      }
    },
    editPart(part) {
      this.editingPart = part
      this.newPart = {
        part_number: part.part_number,
        status: part.status,
        equipment: part.equipment_details ? part.equipment_details.map(e => e.id) : []
      }
    },
    resetForm() {
      this.newPart = { part_number: '', status: '', equipment: [] }
      this.editingPart = null
      this.errorMessage = ''
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