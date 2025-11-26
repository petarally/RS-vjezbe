<template>
  <div class="reservation-form">
    <h2>{{ editMode ? "Uredi rezervaciju" : "Nova rezervacija" }}</h2>
    <div class="form-content">
      <form @submit.prevent="handleSubmit">
        <!-- Category and Model Selection -->
        <div class="form-section">
          <h3 class="section-title">Vozilo</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="category">Kategorija *</label>
              <select
                id="category"
                v-model="reservation.category"
                required
                @change="onCategoryChange"
              >
                <option value="">Odaberite kategoriju</option>
                <option v-for="cat in categories" :key="cat.value" :value="cat.value">
                  {{ cat.label }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="preferred_car_model">Model automobila (opciono)</label>
              <select
                id="preferred_car_model"
                v-model="reservation.preferred_car_model"
                :disabled="!reservation.category || availableModels.length === 0"
                @change="checkAvailability"
              >
                <option value="">Bilo koji model</option>
                <option v-for="model in availableModels" :key="model.display" :value="model.model">
                  {{ model.display }} -
                  {{
                    model.daily_rate.toLocaleString("de-DE", {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    })
                  }}
                  €/dan
                </option>
              </select>
            </div>
          </div>
        </div>

        <!-- Customer Selection -->
        <div class="form-section">
          <h3 class="section-title">Korisnik</h3>
          <div class="form-group full-width">
            <label for="customer_id">Odaberite korisnika *</label>
            <select id="customer_id" v-model.number="reservation.customer_id" required>
              <option value="">Odaberite korisnika</option>
              <option v-for="customer in customers" :key="customer.id" :value="customer.id">
                {{ customer.first_name }} {{ customer.last_name }}
              </option>
            </select>
          </div>
        </div>

        <!-- Date Selection -->
        <div class="form-section">
          <h3 class="section-title">Period rezervacije</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="start_date">Datum preuzimanja *</label>
              <input
                id="start_date"
                v-model="reservation.start_date"
                type="date"
                :min="today"
                required
                @change="checkAvailability"
              />
            </div>

            <div class="form-group">
              <label for="end_date">Datum povrata *</label>
              <input
                id="end_date"
                v-model="reservation.end_date"
                type="date"
                :min="reservation.start_date || today"
                required
                @change="checkAvailability"
              />
            </div>
          </div>
        </div>

        <div v-if="availabilityMessage" class="availability-message" :class="availabilityClass">
          {{ availabilityMessage }}
        </div>

        <div v-if="availableModelsInfo.length > 0 && isAvailable" class="models-info">
          <strong>Dostupni modeli u ovoj kategoriji:</strong>
          <ul>
            <li v-for="model in availableModelsInfo" :key="model.display">
              {{ model.display }} - €{{ model.daily_rate }}/dan
            </li>
          </ul>
        </div>

        <div class="form-actions">
          <button type="button" class="btn-secondary" @click="$emit('cancel')">Odustani</button>
          <button type="submit" class="btn-primary" :disabled="!isAvailable">
            {{ editMode ? "Ažuriraj" : "Dodaj" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { customerApi, type Customer, type Reservation } from "@/services/api";

const props = defineProps<{
  reservation?: Reservation;
  editMode?: boolean;
}>();

const emit = defineEmits<{
  submit: [reservation: Reservation];
  cancel: [];
}>();

interface CarModel {
  brand: string;
  model: string;
  display: string;
  daily_rate: number;
}

const categories = [
  { value: "economy", label: "Ekonomska" },
  { value: "compact", label: "Kompaktna" },
  { value: "suv", label: "SUV" },
  { value: "luxury", label: "Luksuzna" },
  { value: "van", label: "Kombi" },
];

const customers = ref<Customer[]>([]);
const availableModels = ref<CarModel[]>([]);
const availableModelsInfo = ref<CarModel[]>([]);
const isAvailable = ref(true);
const availabilityMessage = ref("");

const today = new Date().toISOString().split("T")[0];

const reservation = ref<Reservation>({
  customer_id: props.reservation?.customer_id || 0,
  category: props.reservation?.category || "",
  preferred_car_model: props.reservation?.preferred_car_model || "",
  start_date: props.reservation?.start_date || "",
  end_date: props.reservation?.end_date || "",
  total_price: props.reservation?.total_price || 0,
  status: props.reservation?.status || "pending",
  vehicle_id: props.reservation?.vehicle_id,
});

const availabilityClass = computed(() => {
  return isAvailable.value ? "success" : "error";
});

const onCategoryChange = async () => {
  // Reset model selection when category changes
  reservation.value.preferred_car_model = "";
  availableModels.value = [];
  availableModelsInfo.value = [];
  availabilityMessage.value = "";

  if (reservation.value.category) {
    await loadModelsInCategory();
    await checkAvailability();
  }
};

const loadModelsInCategory = async () => {
  if (!reservation.value.category) return;

  try {
    const response = await fetch(
      `http://localhost:8000/api/categories/${reservation.value.category}/models`
    );
    const data = await response.json();
    availableModels.value = data.models || [];
  } catch (error) {
    console.error("Error loading models:", error);
    availableModels.value = [];
  }
};

const checkAvailability = async () => {
  if (reservation.value.category && reservation.value.start_date && reservation.value.end_date) {
    try {
      const params = new URLSearchParams({
        start_date: reservation.value.start_date,
        end_date: reservation.value.end_date,
      });

      if (reservation.value.preferred_car_model) {
        params.append("preferred_model", reservation.value.preferred_car_model);
      }

      const response = await fetch(
        `http://localhost:8000/api/categories/${reservation.value.category}/availability?${params}`
      );

      const data = await response.json();

      isAvailable.value = data.available;
      availableModelsInfo.value = data.available_models || [];

      if (data.available) {
        if (reservation.value.preferred_car_model) {
          availabilityMessage.value = `Odabrani model je dostupan za odabrane datume`;
        } else {
          availabilityMessage.value = `Dostupno ${
            availableModelsInfo.value.length
          } vozila u kategoriji ${getCategoryLabel(reservation.value.category)}`;
        }
      } else {
        availabilityMessage.value =
          "Nema dostupnih vozila u odabranoj kategoriji za odabrane datume";
      }
    } catch (error) {
      console.error("Error checking availability:", error);
      isAvailable.value = false;
      availabilityMessage.value = "Greška pri provjeri dostupnosti";
    }
  }
};

const getCategoryLabel = (value: string) => {
  const category = categories.find((c) => c.value === value);
  return category ? category.label : value;
};

onMounted(async () => {
  try {
    const customersData = await customerApi.getAll();
    customers.value = customersData;

    if (props.editMode && props.reservation) {
      if (reservation.value.category) {
        await loadModelsInCategory();
        await checkAvailability();
      }
    }
  } catch (error) {
    console.error("Error loading data:", error);
  }
});

const handleSubmit = () => {
  emit("submit", reservation.value);
};
</script>

<style scoped>
.reservation-form {
  max-width: 950px;
  margin: 0 auto;
  padding: 0;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  overflow: visible;
  display: flex;
  flex-direction: column;
  max-height: 85vh;
}

h2 {
  margin: 0;
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
  flex-shrink: 0;
  border-radius: 12px 12px 0 0;
}

.form-content {
  overflow-y: auto;
  overflow-x: visible;
  flex: 1;
  border-radius: 0 0 12px 12px;
}

form {
  padding: 2rem 2.5rem 2rem 2.5rem;
}

.form-section {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #f7fafc;
}

.form-section:last-of-type {
  border-bottom: none;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0 0 1rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #667eea;
  display: inline-block;
}

.form-group {
  margin-bottom: 0;
}

.form-group.full-width {
  width: 100%;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #4a5568;
  font-size: 0.875rem;
  letter-spacing: 0.3px;
}

input,
select {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1.5px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.9375rem;
  transition: all 0.2s ease;
  background: white;
  color: #2d3748;
}

select:disabled {
  background-color: #f7fafc;
  cursor: not-allowed;
  opacity: 0.6;
}

input:focus,
select:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.availability-message {
  padding: 1rem 1.25rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  font-size: 0.9375rem;
  font-weight: 600;
}

.availability-message.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.availability-message.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.models-info {
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, #f0f4ff 0%, #e8eeff 100%);
  border-radius: 8px;
  margin-bottom: 1.5rem;
  font-size: 0.9375rem;
  border: 1px solid #d1d9f5;
}

.models-info strong {
  display: block;
  margin-bottom: 0.75rem;
  color: #2d3748;
  font-size: 1rem;
}

.models-info ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.models-info li {
  padding: 0.5rem 0;
  color: #4a5568;
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
}

.models-info li:last-child {
  border-bottom: none;
}

.price-info {
  padding: 1rem;
  background: #f7fafc;
  border-radius: 6px;
  margin-bottom: 1.25rem;
  font-size: 1.1rem;
  color: #2d3748;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 2px solid #f7fafc;
}

button {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
  min-width: 120px;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background-color: #edf2f7;
  color: #4a5568;
  border: 1.5px solid #cbd5e0;
  min-width: 120px;
}

.btn-secondary:hover {
  background-color: #e2e8f0;
  border-color: #a0aec0;
  transform: translateY(-1px);
}
</style>
