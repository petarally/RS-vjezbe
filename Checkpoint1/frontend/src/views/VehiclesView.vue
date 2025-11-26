<template>
  <div class="vehicles-view">
    <div class="header">
      <h1>Vozila</h1>
      <button class="btn-primary" @click="showAddForm = true">Dodaj vozilo</button>
    </div>

    <div v-if="showAddForm" class="modal" @click.self="showAddForm = false">
      <div class="modal-content">
        <VehicleForm @submit="handleAddVehicle" @cancel="showAddForm = false" />
      </div>
    </div>

    <div v-if="showEditForm && editingVehicle" class="modal" @click.self="closeEditForm">
      <div class="modal-content">
        <VehicleForm
          :vehicle="editingVehicle"
          :edit-mode="true"
          @submit="handleEditVehicle"
          @cancel="closeEditForm"
        />
      </div>
    </div>

    <div v-if="loading" class="loading">Učitavanje vozila...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="table-container">
      <table class="vehicles-table">
        <thead>
          <tr>
            <th>Vozilo</th>
            <th>Godina</th>
            <th>Kategorija</th>
            <th>Registracija</th>
            <th>Kilometraža</th>
            <th>Gorivo</th>
            <th>Mjenjač</th>
            <th>Dnevna cijena</th>
            <th>Status</th>
            <th>Akcije</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="vehicle in vehicles" :key="vehicle.id" class="vehicle-row">
            <td class="vehicle-name">
              <router-link :to="`/vehicles/${vehicle.id}`" class="vehicle-link">
                {{ vehicle.brand }} {{ vehicle.model }}
              </router-link>
            </td>
            <td>{{ vehicle.year }}</td>
            <td>{{ translateCategory(vehicle.category || "") }}</td>
            <td class="registration">{{ vehicle.registration_number }}</td>
            <td>{{ vehicle.mileage?.toLocaleString("de-DE") || "-" }} km</td>
            <td>{{ translateFuelType(vehicle.fuel_type || "") }}</td>
            <td>{{ translateTransmission(vehicle.transmission || "") }}</td>
            <td class="price">{{ formatPrice(vehicle.daily_rate) }}</td>
            <td>
              <span class="status-badge" :class="vehicle.status">{{
                translateStatus(vehicle.status || "")
              }}</span>
            </td>
            <td class="actions">
              <button class="btn-edit" @click="editVehicle(vehicle)">Uredi</button>
              <button class="btn-delete" @click="vehicle.id && deleteVehicle(vehicle.id)">
                Obriši
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { vehicleApi, type Vehicle } from "@/services/api";
import VehicleForm from "@/components/VehicleForm.vue";

const vehicles = ref<Vehicle[]>([]);
const loading = ref(false);
const error = ref("");
const showAddForm = ref(false);
const showEditForm = ref(false);
const editingVehicle = ref<Vehicle | null>(null);

const translateStatus = (status: string) => {
  const translations: Record<string, string> = {
    available: "Dostupno",
    rented: "Iznajmljeno",
    maintenance: "U servisu",
  };
  return translations[status] || status;
};

const translateCategory = (category: string) => {
  const translations: Record<string, string> = {
    economy: "Ekonomična",
    compact: "Kompaktna",
    sedan: "Sedan",
    suv: "SUV",
    luxury: "Luksuzna",
    van: "Kombi",
  };
  return translations[category] || category;
};

const translateFuelType = (fuelType: string) => {
  const translations: Record<string, string> = {
    petrol: "Benzin",
    diesel: "Dizel",
    electric: "Električno",
    hybrid: "Hibrid",
  };
  return translations[fuelType] || fuelType;
};

const translateTransmission = (transmission: string) => {
  const translations: Record<string, string> = {
    manual: "Ručni",
    automatic: "Automatski",
  };
  return translations[transmission] || transmission;
};

const formatPrice = (price: number | undefined) => {
  if (!price) return "0,00 €";
  return (
    price.toLocaleString("de-DE", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " €"
  );
};

const loadVehicles = async () => {
  loading.value = true;
  error.value = "";
  try {
    vehicles.value = await vehicleApi.getAll();
  } catch (err) {
    error.value = "Failed to load vehicles";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const handleAddVehicle = async (vehicle: Vehicle) => {
  try {
    await vehicleApi.create(vehicle);
    showAddForm.value = false;
    await loadVehicles();
  } catch (err) {
    error.value = "Failed to add vehicle";
    console.error(err);
  }
};

const editVehicle = (vehicle: Vehicle) => {
  editingVehicle.value = { ...vehicle };
  showEditForm.value = true;
};

const handleEditVehicle = async (vehicle: Vehicle) => {
  if (!editingVehicle.value?.id) return;

  try {
    await vehicleApi.update(editingVehicle.value.id, vehicle);
    showEditForm.value = false;
    editingVehicle.value = null;
    await loadVehicles();
  } catch (err) {
    error.value = "Failed to update vehicle";
    console.error(err);
  }
};

const closeEditForm = () => {
  showEditForm.value = false;
  editingVehicle.value = null;
};

const deleteVehicle = async (id: number) => {
  if (confirm("Jeste li sigurni da želite obrisati ovo vozilo?")) {
    try {
      await vehicleApi.delete(id);
      await loadVehicles();
    } catch (err) {
      error.value = "Failed to delete vehicle";
      console.error(err);
    }
  }
};

onMounted(() => {
  loadVehicles();
});
</script>

<style scoped>
.vehicles-view {
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

h1 {
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
  font-size: 1rem;
  font-weight: 600;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.5);
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

.loading,
.error {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.error {
  color: #e74c3c;
}

.vehicles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.vehicle-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.vehicle-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.vehicle-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #2d3748;
}

.vehicle-link {
  color: #667eea;
  text-decoration: none;
  transition: all 0.2s;
}

.vehicle-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

.status {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.status.available {
  background-color: #d4edda;
  color: #155724;
}

.status.rented {
  background-color: #fff3cd;
  color: #856404;
}

.status.maintenance {
  background-color: #f8d7da;
  color: #721c24;
}

.vehicle-details {
  margin-bottom: 1rem;
}

.vehicle-details p {
  margin: 0.5rem 0;
  color: #555;
}

.vehicle-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-edit,
.btn-delete {
  flex: 1;
  padding: 0.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-edit {
  background-color: #3498db;
  color: white;
}

.btn-edit:hover {
  background-color: #2980b9;
}

.btn-delete {
  background-color: #e74c3c;
  color: white;
}

.btn-delete:hover {
  background-color: #c0392b;
}

.table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
}

.vehicles-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.vehicles-table thead {
  background-color: #f8f9fa;
  border-bottom: 2px solid #dee2e6;
}

.vehicles-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #495057;
  white-space: nowrap;
}

.vehicles-table tbody tr {
  border-bottom: 1px solid #dee2e6;
  transition: background-color 0.2s;
}

.vehicles-table tbody tr:hover {
  background-color: #f8f9fa;
}

.vehicles-table td {
  padding: 1rem;
}

.vehicle-name {
  font-weight: 500;
}

.registration {
  font-family: monospace;
  font-size: 0.9rem;
  color: #495057;
}

.price {
  font-weight: 600;
  color: #28a745;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
  white-space: nowrap;
}

.status-badge.available {
  background-color: #d4edda;
  color: #155724;
}

.status-badge.rented {
  background-color: #fff3cd;
  color: #856404;
}

.status-badge.maintenance {
  background-color: #f8d7da;
  color: #721c24;
}

.actions {
  display: flex;
  gap: 0.5rem;
  white-space: nowrap;
}

.actions .btn-edit,
.actions .btn-delete {
  flex: initial;
  padding: 0.5rem 1rem;
}
</style>
