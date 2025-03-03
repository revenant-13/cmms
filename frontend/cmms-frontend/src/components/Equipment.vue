<template>
  <div class="equipment">
    <h1>Equipment Hierarchy</h1>
    <div class="search">
      <input v-model="searchQuery" placeholder="Search equipment by name" @input="filterEquipment" id="search" name="search" />
    </div>
    <div class="form">
      <h2>{{ editingEquipment ? 'Edit Equipment' : 'Add New Equipment' }}</h2>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <form @submit.prevent="saveEquipment">
        <input v-model="newEquipment.name" placeholder="Name" required id="name" name="name" />
        <input v-model="newEquipment.model" placeholder="Model" id="model" name="model" />
        <input v-model="newEquipment.serial" placeholder="Serial Number" id="serial" name="serial" />
        <textarea v-model="newEquipment.description" placeholder="Description"></textarea>
        <select v-model="newEquipment.location_status" required id="location_status" name="location_status">
          <option value="in-house">In-House</option>
          <option value="off-site">Off-Site</option>
        </select>
        <select v-model="newEquipment.parent" id="parent" name="parent">
          <option value="">No Parent</option>
          <option v-for="equip in flattenedEquipment" :key="equip.id" :value="equip.id">
            {{ equip.name }}
          </option>
        </select>
        <select v-model="newEquipment.manufacturer" id="manufacturer" name="manufacturer">
          <option value="">No Manufacturer</option>
          <option v-for="vendor in vendorList" :key="vendor.id" :value="vendor.id">
            {{ vendor.name }}
          </option>
        </select>
        <button type="submit">{{ editingEquipment ? 'Update' : 'Add' }}</button>
        <button v-if="editingEquipment" type="button" @click="cancelEdit">Cancel</button>
      </form>
    </div>
    <ul v-if="filteredEquipment.length">
      <li v-for="item in filteredEquipment" :key="item.id">
        {{ item.name }} (Model: {{ item.model }}) {{ item.serial }} - {{ item.description || 'No description' }}
        <button @click="editEquipment(item)">Edit</button>
        <button @click="deleteEquipment(item.id)" class="delete-btn">Delete</button>
        <ul v-if="item.children && item.children.length">
          <li v-for="child in item.children" :key="child.id">
            {{ child.name }} (Model: {{ child.model }}) {{ child.serial }} - {{ child.description || 'No description' }}
            <button @click="editEquipment(child)">Edit</button>
            <button @click="deleteEquipment(child.id)" class="delete-btn">Delete</button>
          </li>
        </ul>
      </li>
    </ul>
    <p v-else>No equipment found</p>
  </div>
</template>

<style scoped>
  .equipment {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
  }
  .search, .form {
    margin-bottom: 20px;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  .search input, .form input, .form select, .form textarea {
    width: 100%;
    padding: 8px;
    margin: 5px 0;
    box-sizing: border-box;
  }
  .form textarea {
    height: 100px;
  }
  .form button {
    background-color: #42b983;
    color: white;
    border: none;
    padding: 8px 15px;
    margin: 5px 5px 0 0;
    cursor: pointer;
  }
  .form button:hover {
    background-color: #2c3e50;
  }
  .error {
    color: red;
    margin-bottom: 10px;
  }
  ul {
    list-style-type: none;
    padding-left: 20px;
  }
  li {
    margin: 5px 0;
  }
  li button {
    margin-left: 10px;
    background-color: #42b983;
    color: white;
    border: none;
    padding: 3px 8px;
    cursor: pointer;
  }
  li button:hover {
    background-color: #2c3e50;
  }
  .delete-btn {
    background-color: #e74c3c;
  }
  .delete-btn:hover {
    background-color: #c0392b;
  }
</style>

<script>
import axios from 'axios'

export default {
  name: 'EquipmentPage',
  data() {
    return {
      equipment: [],
      filteredEquipment: [],
      vendorList: [],
      csrfToken: null,
      searchQuery: '',
      newEquipment: {
        name: '',
        model: '',
        serial: '',
        description: '',
        location_status: 'in-house',
        parent: '',
        manufacturer: ''
      },
      editingEquipment: null,
      errorMessage: ''
    }
  },
  computed: {
    flattenedEquipment() {
      const seenIds = new Set()
      const flatten = (items) => {
        let flat = []
        items.forEach(item => {
          if (!seenIds.has(item.id) && (!this.editingEquipment || item.id !== this.editingEquipment.id)) {
            seenIds.add(item.id)
            flat.push({ id: item.id, name: item.name })
          }
          if (item.children && item.children.length) {
            flat = flat.concat(flatten(item.children))
          }
        })
        return flat
      }
      return flatten(this.equipment)
    }
  },
  mounted() {
    this.fetchCsrfToken().then(() => {
      this.fetchVendors()
      this.fetchEquipment()
    })
  },
  methods: {
    async fetchCsrfToken() {
      try {
        await axios.get('http://localhost:8000/api/equipment/', { withCredentials: true })
        this.csrfToken = this.getCsrfToken()
      } catch (error) {
        console.error('Error fetching CSRF token:', error)
      }
    },
    fetchEquipment() {
      axios.get('http://localhost:8000/api/equipment/', {
        withCredentials: true,
        headers: { 'X-CSRFToken': this.csrfToken }
      })
        .then(response => {
          this.equipment = response.data
          this.filteredEquipment = response.data.filter(item => !item.parent)
          this.filterEquipment()
        })
        .catch(error => {
          console.error('Error fetching equipment:', error)
        })
    },
    fetchVendors() {
      axios.get('http://localhost:8000/api/vendors/', {
        withCredentials: true,
        headers: { 'X-CSRFToken': this.csrfToken }
      })
        .then(response => {
          this.vendorList = response.data
        })
        .catch(error => {
          console.error('Error fetching vendors:', error)
        })
    },
    filterEquipment() {
      const query = this.searchQuery.toLowerCase()
      if (!query) {
        this.filteredEquipment = this.equipment.filter(item => !item.parent)
        return
      }
      const filterRecursive = (items) => {
        return items.map(item => {
          const matches = item.name.toLowerCase().includes(query)
          const filteredChildren = item.children && item.children.length ? filterRecursive(item.children) : []
          if ((matches && !item.parent) || filteredChildren.length) {
            return { ...item, children: filteredChildren }
          }
          return null
        }).filter(item => item !== null)
      }
      this.filteredEquipment = filterRecursive(this.equipment)
    },
    async saveEquipment() {
      try {
        await this.fetchCsrfToken()
        const equipmentData = { ...this.newEquipment }
        console.log('Sending equipment data:', equipmentData)
        if (!equipmentData.parent) delete equipmentData.parent
        if (!equipmentData.manufacturer) delete equipmentData.manufacturer

        if (this.editingEquipment) {
          await axios.put(`http://localhost:8000/api/equipment/${this.editingEquipment.id}/`, equipmentData, {
            withCredentials: true,
            headers: { 'X-CSRFToken': this.csrfToken }
          })
        } else {
          await axios.post('http://localhost:8000/api/equipment/', equipmentData, {
            withCredentials: true,
            headers: { 'X-CSRFToken': this.csrfToken }
          })
        }
        this.fetchEquipment()
        this.resetForm()
      } catch (error) {
        console.error('Error saving equipment:', error)
        if (error.response) console.log('Response data:', error.response.data)
        this.errorMessage = 'Failed to save equipment. Please try again.'
      }
    },
    async deleteEquipment(equipmentId) {
      if (confirm('Are you sure you want to delete this equipment? This will also delete its children.')) {
        try {
          await this.fetchCsrfToken()
          await axios.delete(`http://localhost:8000/api/equipment/${equipmentId}/`, {
            withCredentials: true,
            headers: { 'X-CSRFToken': this.csrfToken }
          })
          this.fetchEquipment()
        } catch (error) {
          console.error('Error deleting equipment:', error)
          this.errorMessage = 'Failed to delete equipment. Please try again.'
        }
      }
    },
    editEquipment(item) {
      console.log('Editing item:', item)
      this.editingEquipment = item
      this.newEquipment = {
        name: item.name,
        model: item.model,
        serial: item.serial,
        description: item.description || '',
        location_status: item.location_status,
        parent: item.parent ? item.parent.id : '',
        manufacturer: item.manufacturer ? item.manufacturer.id : ''
      }
    },
    resetForm() {
      this.newEquipment = { 
        name: '', 
        model: '', 
        serial: '', 
        description: '', 
        location_status: 'in-house', 
        parent: '', 
        manufacturer: '' 
      }
      this.editingEquipment = null
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