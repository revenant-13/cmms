<template>
    <div class="equipment">
      <h1>Equipment Hierarchy</h1>
      <ul>
        <li v-for="item in equipment" :key="item.id">
          {{ item.name }} (Model: {{ item.model }})
          <ul v-if="item.children && item.children.length">
            <li v-for="child in item.children" :key="child.id">
              {{ child.name }} (Model: {{ child.model }})
            </li>
          </ul>
        </li>
      </ul>
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
  export default {
    name: 'EquipmentPage',
    data() {
      return {
        equipment: [
          {
            id: 1,
            name: 'Main Generator',
            model: 'XG-500',
            children: [
              { id: 2, name: 'Cooling Fan', model: 'CF-200' },
              { id: 3, name: 'Control Panel', model: 'CP-100' }
            ]
          },
          {
            id: 4,
            name: 'Pump System',
            model: 'PS-300',
            children: []
          }
        ]
      }
    }
  }
  </script>