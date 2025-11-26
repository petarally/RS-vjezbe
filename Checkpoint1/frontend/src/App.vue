<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <div class="app-wrapper">
    <nav class="navbar">
      <div class="nav-container">
        <RouterLink to="/" class="logo-link">
          <h1 class="logo">🚗 RentaCar</h1>
        </RouterLink>
        <div class="nav-links">
          <RouterLink to="/">Nadzorna ploča</RouterLink>
          <RouterLink to="/vehicles">Vozila</RouterLink>
          <RouterLink to="/customers">Korisnici</RouterLink>
          <RouterLink to="/reservations">Rezervacije</RouterLink>
        </div>
      </div>
    </nav>

    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-wrapper {
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.navbar {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-link {
  text-decoration: none;
}

.logo {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  transition: transform 0.3s ease;
}

.logo-link:hover .logo {
  transform: scale(1.05);
}

.nav-links {
  display: flex;
  gap: 0.5rem;
}

.nav-links a {
  color: #2c3e50;
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  position: relative;
}

.nav-links a:hover {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
}

.nav-links a.router-link-active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.main-content {
  min-height: calc(100vh - 88px);
  padding: 2rem;
}

@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .nav-links {
    width: 100%;
    justify-content: center;
    flex-wrap: wrap;
  }

  .nav-links a {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
}
</style>
