<template>
  <div class="equipment">
    <div class="header">
      <h1>Equipment Hierarchy</h1>
      <button @click="toggleForm" class="toggle-btn">
        {{ showForm ? 'Hide Form' : 'Add Equipment' }}
      </button>
    </div>
    <equipment-form
      v-if="showForm"
      :equipment="editingEquipment"
      :equipment-list="flattenedEquipment"
      :vendor-list="vendorList"
      :error="errorMessage"
      @save="saveEquipment"
      @cancel="cancelEdit"
    />
    <div class="controls">
      <filter-controls
        v-model:search-query="searchQuery"
        v-model:filter-location="filterLocation"
        v-model:filter-manufacturer="filterManufacturer"
        :vendors="vendorList"
        @update:search-query="filterEquipment"
        @update:filter-location="filterEquipment"
        @update:filter-manufacturer="filterEquipment"
      />
    </div>
    <ul v-if="filteredEquipment.length" class="equipment-list">
      <equipment-node v-for="item in filteredEquipment" :key="item.id" :item="item" @edit="editEquipment" @delete="deleteEquipment" />
    </ul>
    <p v-else>No equipment found</p>
  </div>
</template>

<style scoped>
.equipment {
  max-width: 1000px;
  margin: 0 auto;
  padding: 10px;
}
.header {
  display: flex;
  justify-content: center; /* Center the entire header content */
  align-items: center;
  margin-bottom: 10px;
  position: relative; /* Allow absolute positioning of button */
}
.header h1 {
  margin: 0;
  font-size: 1.5em;
  text-align: center; /* Ensure text is centered */
}
.toggle-btn {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 6px 12px;
  cursor: pointer;
  border-radius: 4px;
  position: absolute; /* Position button on the right */
  right: 0;
}
.toggle-btn:hover {
  background-color: #2c3e50;
}
.controls {
  display: flex;
  justify-content: center; /* Center the filter controls */
  margin-bottom: 10px;
}
.equipment-list {
  list-style-type: none;
  padding-left: 10px;
}
.equipment-list li {
  margin: 2px 0;
}
</style>

<script>
import { reactive } from 'vue'
import EquipmentNode from './EquipmentNode.vue'
import FilterControls from './FilterControls.vue'
import EquipmentForm from './EquipmentForm.vue'
import { fetchCsrfToken, fetchData, saveData, deleteData } from '../utils/api.js'

export default {
  name: 'EquipmentPage',
  components: {
    EquipmentNode,
    FilterControls,
    EquipmentForm
  },
  setup() {
    const state = reactive({
      equipment: [],
      filteredEquipment: [],
      vendorList: [],
      csrfToken: null,
      searchQuery: '',
      filterLocation: '',
      filterManufacturer: '',
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
      errorMessage: '',
      showForm: false
    })

    return state
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
      this.csrfToken = await fetchCsrfToken()
    },
    async fetchEquipment() {
      try {
        const data = await fetchData('equipment', this.csrfToken)
        this.equipment = data.filter(item => item.is_active)
        this.filteredEquipment = this.equipment.filter(item => !item.parent)
        console.log('Fetched equipment:', this.equipment)
        console.log('Initial filteredEquipment:', this.filteredEquipment)
        console.log('Initial filteredEquipment children check:', this.filteredEquipment.map(item => ({
          id: item.id,
          name: item.name,
          children: item.children ? item.children.map(child => ({
            id: child.id,
            name: child.name,
            parent: child.parent,
            children: child.children ? child.children.length : 0
          })) : []
        })))
        this.filterEquipment()
      } catch (error) {
        // Error logged in fetchData
      }
    },
    async fetchVendors() {
      try {
        this.vendorList = await fetchData('vendors', this.csrfToken)
      } catch (error) {
        // Error logged in fetchData
      }
    },
    filterEquipment() {
      const query = this.searchQuery.toLowerCase()
      const filterRecursive = (items) => {
        return items.map(item => {
          const matchesName = query ? item.name.toLowerCase().includes(query) : true
          const matchesLocation = this.filterLocation ? item.location_status === this.filterLocation : true
          const matchesManufacturer = this.filterManufacturer ? 
            (item.manufacturer && item.manufacturer.id === parseInt(this.filterManufacturer)) : true
          const itemMatches = matchesName && matchesLocation && matchesManufacturer
          let filteredChildren = []
          if (item.children && item.children.length) {
            filteredChildren = filterRecursive(item.children)
            item.children = filteredChildren
          }
          if (itemMatches || filteredChildren.length > 0) {
            return { ...item }
          }
          return null
        }).filter(item => item !== null)
      }
      this.filteredEquipment = filterRecursive(this.equipment.filter(item => !item.parent))
      console.log('Filtered equipment after filter:', this.filteredEquipment)
    },
    async saveEquipment(equipmentData) {
      try {
        await this.fetchCsrfToken()
        console.log('saveEquipment called, editingEquipment:', this.editingEquipment)
        const isEdit = !!this.editingEquipment && this.editingEquipment.id
        console.log('isEdit:', isEdit)
        const dataToSend = isEdit ? { ...equipmentData, id: this.editingEquipment.id } : { ...equipmentData, id: undefined }
        console.log('Sending equipment data:', JSON.stringify(dataToSend))
        const response = await saveData('equipment', dataToSend, this.csrfToken, isEdit)
        console.log('Response:', response)
        this.fetchEquipment()
        this.showForm = false
        this.resetForm()
      } catch (error) {
        console.error('Save equipment failed:', error)
        this.errorMessage = 'Failed to save equipment. Please try again.'
      }
    },
    async deleteEquipment(equipmentId) {
      if (confirm('Are you sure you want to delete this equipment? This will also delete its children.')) {
        try {
          await this.fetchCsrfToken()
          await deleteData('equipment', equipmentId, this.csrfToken)
          this.fetchEquipment()
        } catch (error) {
          this.errorMessage = 'Failed to delete equipment. Please try again.'
        }
      }
    },
    editEquipment(item) {
      console.log('Editing item:', item)
      this.editingEquipment = { ...item }
      console.log('After editEquipment, editingEquipment set to:', this.editingEquipment)
      this.showForm = true
    },
    cancelEdit() {
      this.resetForm()
      this.showForm = false
    },
    resetForm() {
      console.log('Resetting form')
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
    toggleForm() {
      this.showForm = !this.showForm
      if (!this.showForm) {
        this.resetForm()
      } else if (!this.editingEquipment) {
        this.resetForm()
      }
    }
  }
}
</script>