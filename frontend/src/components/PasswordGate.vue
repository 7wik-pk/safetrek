<!-- PasswordGate.vue -->
<template>
  <div class="gate">
    <h2>Enter Access Password</h2>
    <input v-model="input" type="password" placeholder="Password" @keydown.enter="validate" autofocus />
    <button @click="validate">Enter</button>
    <p v-if="error" class="error">Incorrect password</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const input = ref('')
const error = ref(false)
const correctPassword = "mS0ciety!"

function validate() {
  if (input.value === correctPassword) {
    sessionStorage.setItem('access_granted', 'true')
    window.location.reload()
  } else {
    error.value = true
  }
}
</script>

<style scoped>
.gate {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}
input {
  padding: 0.5rem;
  margin-top: 1rem;
}
button {
  margin-top: 1rem;
}
.error {
  color: red;
  margin-top: 0.5rem;
}
</style>
