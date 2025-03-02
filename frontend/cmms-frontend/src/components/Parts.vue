<template>
    <div class="parts">
      <h1>Parts Inventory</h1>
      <table>
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
            <td>{{ part.equipment }}</td>
          </tr>
        </tbody>
      </table>
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
  export default {
    name: 'PartsPage',
    data() {
      return {
        parts: [
          { id: 1, part_number: 'P001', status: 'Active', equipment: 'Main Generator' },
          { id: 2, part_number: 'P002', status: 'Inactive', equipment: 'Cooling Fan' },
          { id: 3, part_number: 'P003', status: 'Active', equipment: 'Pump System' }
        ]
      }
    }
  }
  </script>