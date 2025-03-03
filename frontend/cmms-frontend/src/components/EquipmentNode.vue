<template>
    <li>
      {{ item.name }} (Model: {{ item.model }}) {{ item.serial }} - 
      {{ item.description || 'No description' }} 
      [Parent: {{ item.parent_details ? item.parent_details.name : 'None' }}, 
      Manufacturer: {{ item.manufacturer_details ? item.manufacturer_details.name : 'None' }}]
      <button @click="$emit('edit', item)">Edit</button>
      <button @click="$emit('delete', item.id)" class="delete-btn">Delete</button>
      <ul v-if="item.children && item.children.length">
        <equipment-node v-for="child in item.children" :key="child.id" :item="child" @edit="$emit('edit', $event)" @delete="$emit('delete', $event)" />
      </ul>
    </li>
  </template>
  
  <script>
  export default {
    name: 'EquipmentNode',
    props: {
      item: {
        type: Object,
        required: true
      }
    }
  }
  </script>
  
  <style scoped>
  button {
    background-color: #42b983;
    color: white;
    border: none;
    padding: 3px 8px;
    margin-left: 10px;
    cursor: pointer;
  }
  button:hover {
    background-color: #2c3e50;
  }
  .delete-btn {
    background-color: #e74c3c;
  }
  .delete-btn:hover {
    background-color: #c0392b;
  }
  ul {
    list-style-type: none;
    padding-left: 20px;
  }
  li {
    margin: 5px 0;
  }
  </style>