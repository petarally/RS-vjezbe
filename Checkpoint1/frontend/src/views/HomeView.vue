<script setup lang="ts">
import { ref, onMounted } from "vue";
import { vehicleApi, customerApi, reservationApi } from "@/services/api";
import VehicleForm from "@/components/VehicleForm.vue";
import CustomerForm from "@/components/CustomerForm.vue";
import ReservationForm from "@/components/ReservationForm.vue";
import type { Vehicle, Customer, Reservation } from "@/services/api";

const stats = ref({
  totalVehicles: 0,
  availableVehicles: 0,
  totalCustomers: 0,
  activeReservations: 0,
});

const loading = ref(true);
const showVehicleForm = ref(false);
const showCustomerForm = ref(false);
const showReservationForm = ref(false);

const loadStats = async () => {
  try {
    const [vehicles, customers, reservations] = await Promise.all([
      vehicleApi.getAll(),
      customerApi.getAll(),
      reservationApi.getAll(),
    ]);

    stats.value = {
      totalVehicles: vehicles.length,
      availableVehicles: vehicles.filter((v) => v.status === "available").length,
      totalCustomers: customers.length,
      activeReservations: reservations.filter((r) => r.status === "active").length,
    };
  } catch (error) {
    console.error("Error loading stats:", error);
  } finally {
    loading.value = false;
  }
};

const handleAddVehicle = async (vehicle: Vehicle) => {
  try {
    await vehicleApi.create(vehicle);
    showVehicleForm.value = false;
    loadStats();
  } catch (error) {
    console.error("Error adding vehicle:", error);
    alert("Greška pri dodavanju vozila");
  }
};

const handleAddCustomer = async (customer: Customer) => {
  try {
    await customerApi.create(customer);
    showCustomerForm.value = false;
    loadStats();
  } catch (error) {
    console.error("Error adding customer:", error);
    alert("Greška pri dodavanju korisnika");
  }
};

const handleAddReservation = async (reservation: Reservation) => {
  try {
    await reservationApi.create(reservation);
    showReservationForm.value = false;
    loadStats();
  } catch (error) {
    console.error("Error adding reservation:", error);
    alert("Greška pri dodavanju rezervacije");
  }
};

onMounted(async () => {
  loadStats();
});
</script>

<template>
  <div class="dashboard">
    <div class="welcome-section">
      <h1>Dobrodošli u RentaCar</h1>
      <p>Učinkovito upravljajte svojim poslom najma vozila</p>
    </div>

    <div v-if="loading" class="loading">Učitavanje nadzorne ploče...</div>

    <div v-else class="stats-grid">
      <div class="stat-card vehicles">
        <div class="stat-icon">🚗</div>
        <div class="stat-content">
          <h3>Ukupno vozila</h3>
          <p class="stat-number">{{ stats.totalVehicles }}</p>
        </div>
      </div>

      <div class="stat-card available">
        <div class="stat-icon">✅</div>
        <div class="stat-content">
          <h3>Dostupno</h3>
          <p class="stat-number">{{ stats.availableVehicles }}</p>
        </div>
      </div>

      <div class="stat-card customers">
        <div class="stat-icon">👥</div>
        <div class="stat-content">
          <h3>Korisnici</h3>
          <p class="stat-number">{{ stats.totalCustomers }}</p>
        </div>
      </div>

      <div class="stat-card reservations">
        <div class="stat-icon">📋</div>
        <div class="stat-content">
          <h3>Aktivne rezervacije</h3>
          <p class="stat-number">{{ stats.activeReservations }}</p>
        </div>
      </div>
    </div>

    <div class="quick-actions">
      <h2>Brze akcije</h2>
      <div class="actions-grid">
        <button @click="showVehicleForm = true" class="action-card">
          <span class="action-icon">🚗</span>
          <span class="action-text">Dodaj vozilo</span>
        </button>
        <button @click="showCustomerForm = true" class="action-card">
          <span class="action-icon">👤</span>
          <span class="action-text">Dodaj korisnika</span>
        </button>
        <button @click="showReservationForm = true" class="action-card">
          <span class="action-icon">📅</span>
          <span class="action-text">Nova rezervacija</span>
        </button>
      </div>
    </div>

    <!-- Modals -->
    <div v-if="showVehicleForm" class="modal" @click.self="showVehicleForm = false">
      <div class="modal-content">
        <VehicleForm @submit="handleAddVehicle" @cancel="showVehicleForm = false" />
      </div>
    </div>

    <div v-if="showCustomerForm" class="modal" @click.self="showCustomerForm = false">
      <div class="modal-content">
        <CustomerForm @submit="handleAddCustomer" @cancel="showCustomerForm = false" />
      </div>
    </div>

    <div v-if="showReservationForm" class="modal" @click.self="showReservationForm = false">
      <div class="modal-content">
        <ReservationForm @submit="handleAddReservation" @cancel="showReservationForm = false" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

.welcome-section {
  background: white;
  padding: 2rem 2.5rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  text-align: center;
}

.welcome-section h1 {
  font-size: 1.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.welcome-section p {
  font-size: 1rem;
  color: #718096;
}

.loading {
  text-align: center;
  padding: 2rem;
  font-size: 1rem;
  color: white;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.25rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  gap: 1.25rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.stat-icon {
  font-size: 2.5rem;
  line-height: 1;
}

.stat-content h3 {
  font-size: 0.75rem;
  color: #718096;
  margin-bottom: 0.35rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #2d3748;
  margin: 0;
}

.quick-actions {
  background: white;
  padding: 1.5rem 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.quick-actions h2 {
  margin-bottom: 1.25rem;
  color: #2d3748;
  font-size: 1.25rem;
  font-weight: 600;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.action-card {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 10px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
  border: none;
  cursor: pointer;
  width: 100%;
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.action-icon {
  font-size: 1.75rem;
}

.action-text {
  font-size: 0.95rem;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
  overflow-y: auto;
}

.modal-content {
  width: auto;
  max-height: none;
  overflow: visible;
}

@media (max-width: 768px) {
  .welcome-section h1 {
    font-size: 1.5rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }
}
</style>
