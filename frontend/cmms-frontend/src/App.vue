<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/equipment">Equipment</router-link> |
      <router-link to="/parts">Parts</router-link> |
      <router-link to="/tasks">Tasks</router-link> |
      <router-link to="/schedules">Schedules</router-link>
      <router-link to="/dashboard">Dashboard</router-link>
    </nav>
    <router-view />
  </div>
</template>

<style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
  nav {
    padding: 10px;
  }
  nav a {
    margin: 0 10px;
    text-decoration: none;
    color: #42b983;
  }
  nav a.router-link-exact-active {
    color: #2c3e50;
    font-weight: bold;
  }
</style>

<script>
export default {
  name: 'App'
}
</script>