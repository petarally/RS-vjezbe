<template>
  <div class="reservations-view">
    <div class="header">
      <h1>Rezervacije</h1>
      <div class="header-actions">
        <div class="view-toggle">
          <button
            :class="['toggle-btn', { active: currentView === 'gantt' }]"
            @click="currentView = 'gantt'"
          >
            📊 Gantt pregled
          </button>
          <button
            :class="['toggle-btn', { active: currentView === 'list' }]"
            @click="currentView = 'list'"
          >
            📋 Lista
          </button>
        </div>
        <button class="btn-primary" @click="showAddForm = true">Nova rezervacija</button>
      </div>
    </div>

    <div v-if="showAddForm" class="modal" @click.self="showAddForm = false">
      <div class="modal-content">
        <ReservationForm @submit="handleAddReservation" @cancel="showAddForm = false" />
      </div>
    </div>

    <div v-if="showEditForm && editingReservation" class="modal" @click.self="closeEditForm">
      <div class="modal-content">
        <ReservationForm
          :reservation="editingReservation"
          :edit-mode="true"
          @submit="handleEditReservation"
          @cancel="closeEditForm"
        />
      </div>
    </div>

    <div v-if="loading" class="loading">Učitavanje rezervacija...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <!-- Gantt View -->
      <ReservationGantt
        v-if="currentView === 'gantt'"
        :reservations="reservations"
        :vehicles="vehicles"
        :customers="customers"
      />

      <!-- List View -->
      <div v-else-if="currentView === 'list'">
        <div v-if="reservations.length === 0" class="empty-state">
          <p>Nema rezervacija. Kliknite "Nova rezervacija" za dodavanje.</p>
        </div>
        <div v-else class="reservations-grid">
          <div v-for="reservation in reservations" :key="reservation.id" class="reservation-card">
            <div class="reservation-header">
              <h3>Rezervacija #{{ reservation.id }}</h3>
              <span class="status" :class="reservation.status">{{
                translateStatus(reservation.status || "")
              }}</span>
            </div>
            <div class="reservation-details">
              <p><strong>Kategorija:</strong> {{ translateCategory(reservation.category) }}</p>
              <p v-if="reservation.preferred_car_model">
                <strong>Preferirani model:</strong> {{ reservation.preferred_car_model }}
              </p>
              <p v-if="reservation.vehicle_id">
                <strong>Dodijeljeno vozilo:</strong> {{ getVehicleName(reservation.vehicle_id) }}
              </p>
              <p v-else>
                <strong>Vozilo:</strong> <span class="pending-text">Čeka se dodjela</span>
              </p>
              <p><strong>Korisnik:</strong> {{ getCustomerName(reservation.customer_id) }}</p>
              <p><strong>Datum preuzimanja:</strong> {{ formatDate(reservation.start_date) }}</p>
              <p><strong>Datum povrata:</strong> {{ formatDate(reservation.end_date) }}</p>
              <p><strong>Ukupna cijena:</strong> €{{ reservation.total_price?.toFixed(2) }}</p>
            </div>
            <div class="reservation-actions">
              <button class="btn-edit" @click="editReservation(reservation)">Uredi</button>
              <button
                class="btn-delete"
                @click="reservation.id && deleteReservation(reservation.id)"
              >
                Obriši
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import {
  reservationApi,
  vehicleApi,
  customerApi,
  type Reservation,
  type Vehicle,
  type Customer,
} from "@/services/api";
import ReservationForm from "@/components/ReservationForm.vue";
import ReservationGantt from "@/components/ReservationGantt.vue";

const reservations = ref<Reservation[]>([]);
const vehicles = ref<Vehicle[]>([]);
const customers = ref<Customer[]>([]);
const loading = ref(false);
const error = ref("");
const showAddForm = ref(false);
const showEditForm = ref(false);
const editingReservation = ref<Reservation | null>(null);
const currentView = ref<"gantt" | "list">("gantt");

const translateStatus = (status: string) => {
  const translations: Record<string, string> = {
    pending: "Na čekanju",
    confirmed: "Potvrđena",
    active: "Aktivna",
    completed: "Završena",
    cancelled: "Otkazana",
  };
  return translations[status] || status;
};

const translateCategory = (category: string) => {
  const translations: Record<string, string> = {
    economy: "Ekonomska",
    compact: "Kompaktna",
    suv: "SUV",
    luxury: "Luksuzna",
    van: "Kombi",
  };
  return translations[category] || category;
};

const getVehicleName = (vehicleId?: number) => {
  if (!vehicleId) return "Nije dodijeljeno";
  const vehicle = vehicles.value.find((v) => v.id === vehicleId);
  return vehicle ? `${vehicle.brand} ${vehicle.model}` : "Nepoznato";
};

const getCustomerName = (customerId: number) => {
  const customer = customers.value.find((c) => c.id === customerId);
  return customer ? `${customer.first_name} ${customer.last_name}` : "Nepoznato";
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString("hr-HR");
};

const loadReservations = async () => {
  loading.value = true;
  error.value = "";
  try {
    const [reservationsData, vehiclesData, customersData] = await Promise.all([
      reservationApi.getAll(),
      vehicleApi.getAll(),
      customerApi.getAll(),
    ]);

    reservations.value = reservationsData;
    vehicles.value = vehiclesData;
    customers.value = customersData;
  } catch (err) {
    error.value = "Greška pri učitavanju rezervacija";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const handleAddReservation = async (reservation: Reservation) => {
  try {
    await reservationApi.create(reservation);
    showAddForm.value = false;
    await loadReservations();
  } catch (err) {
    error.value = err instanceof Error ? err.message : "Greška pri dodavanju rezervacije";
    console.error(err);
  }
};

const editReservation = (reservation: Reservation) => {
  editingReservation.value = { ...reservation };
  showEditForm.value = true;
};

const handleEditReservation = async (reservation: Reservation) => {
  if (!editingReservation.value?.id) return;

  try {
    await reservationApi.update(editingReservation.value.id, reservation);
    showEditForm.value = false;
    editingReservation.value = null;
    await loadReservations();
  } catch (err) {
    error.value = "Greška pri ažuriranju rezervacije";
    console.error(err);
  }
};

const closeEditForm = () => {
  showEditForm.value = false;
  editingReservation.value = null;
};

const deleteReservation = async (id: number) => {
  if (confirm("Jeste li sigurni da želite obrisati ovu rezervaciju?")) {
    try {
      await reservationApi.delete(id);
      await loadReservations();
    } catch (err) {
      error.value = "Greška pri brisanju rezervacije";
      console.error(err);
    }
  }
};

onMounted(() => {
  loadReservations();
});
</script>

<style scoped>
.reservations-view {
  padding: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.view-toggle {
  display: flex;
  gap: 0.5rem;
  background: white;
  padding: 0.25rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.toggle-btn {
  padding: 0.5rem 1rem;
  border: none;
  background: transparent;
  color: #4a5568;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.toggle-btn:hover {
  background: #f7fafc;
}

.toggle-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
}

h1 {
  font-size: 2rem;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.625rem 1.25rem;
  border-radius: 0.5rem;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: opacity 0.2s;
}

.btn-primary:hover {
  opacity: 0.9;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  overflow-y: auto;
  padding: 2rem 0;
}

.modal-content {
  background: white;
  border-radius: 0.5rem;
  max-height: 90vh;
  overflow-y: auto;
}

.loading,
.error,
.empty-state {
  text-align: center;
  padding: 2rem;
  color: #4a5568;
}

.error {
  color: #f56565;
}

.reservations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.reservation-card {
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.2s;
}

.reservation-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.reservation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.reservation-header h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
}

.status {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status.active {
  background: #c6f6d5;
  color: #22543d;
}

.status.completed {
  background: #bee3f8;
  color: #2c5282;
}

.status.cancelled {
  background: #fed7d7;
  color: #742a2a;
}

.reservation-details {
  margin-bottom: 1rem;
}

.reservation-details p {
  margin: 0.5rem 0;
  color: #4a5568;
  font-size: 0.875rem;
}

.reservation-details strong {
  color: #2d3748;
  font-weight: 600;
}

.reservation-actions {
  display: flex;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.btn-edit,
.btn-delete {
  flex: 1;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: opacity 0.2s;
}

.btn-edit {
  background: #667eea;
  color: white;
}

.btn-edit:hover {
  opacity: 0.9;
}

.btn-delete {
  background: #f56565;
  color: white;
}

.btn-delete:hover {
  opacity: 0.9;
}

.pending-text {
  color: #718096;
  font-style: italic;
}
</style>

<style scoped>
.reservations-view {
  max-width: 1400px;
  margin: 0 auto;
}

.header {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h1 {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.btn-primary {
  padding: 0.75rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.5);
}

.placeholder-text {
  text-align: center;
  padding: 3rem;
  color: #666;
  font-size: 1.2rem;
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

.coming-soon {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  text-align: center;
  max-width: 500px;
}

.coming-soon h2 {
  margin-bottom: 1rem;
  color: #2d3748;
}

.coming-soon p {
  margin-bottom: 2rem;
  color: #718096;
  font-size: 1.1rem;
}

.reservations-view > p {
  background: white;
  padding: 3rem;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  text-align: center;
  font-size: 1.2rem;
  color: #666;
}
</style>
