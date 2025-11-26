<template>
  <div class="vehicle-form">
    <h2>{{ editMode ? "Uredi vozilo" : "Dodaj novo vozilo" }}</h2>
    <div class="form-content">
      <form @submit.prevent="handleSubmit">
        <!-- Vehicle Identity -->
        <div class="form-row">
          <div class="form-group">
            <label for="brand">Marka *</label>
            <input
              id="brand"
              v-model="searchBrand"
              type="text"
              @input="handleBrandSearch"
              placeholder="Unesite za pretragu (npr. Toyota)..."
              list="brands-list"
              required
              autocomplete="off"
            />
            <datalist id="brands-list">
              <option v-for="brand in filteredBrands" :key="brand" :value="brand">
                {{ brand }}
              </option>
            </datalist>
          </div>

          <div class="form-group">
            <label for="model">Model *</label>
            <input
              id="model"
              v-model="searchModel"
              type="text"
              @input="handleModelSearch"
              placeholder="Unesite za pretragu (npr. Camry)..."
              list="models-list"
              :disabled="!vehicle.brand"
              required
              autocomplete="off"
            />
            <datalist id="models-list">
              <option v-for="model in filteredModels" :key="model" :value="model">
                {{ model }}
              </option>
            </datalist>
          </div>
        </div>

        <div class="form-row-3">
          <div class="form-group">
            <label for="year">Godina *</label>
            <input
              id="year"
              v-model.number="vehicle.year"
              type="number"
              min="1900"
              :max="new Date().getFullYear() + 1"
              required
            />
          </div>

          <div class="form-group">
            <label for="category">Kategorija *</label>
            <select id="category" v-model="vehicle.category" required>
              <option value="">Odaberite kategoriju</option>
              <option value="economy">Ekonomična</option>
              <option value="compact">Kompaktna</option>
              <option value="sedan">Sedan</option>
              <option value="suv">SUV</option>
              <option value="luxury">Luksuzna</option>
              <option value="van">Kombi</option>
            </select>
          </div>

          <div class="form-group">
            <label for="registration">Registarska oznaka *</label>
            <input
              id="registration"
              v-model="vehicle.registration_number"
              type="text"
              placeholder="npr. ZG-1234-AB"
              required
            />
          </div>
        </div>

        <!-- Specifications -->
        <div class="form-row-3">
          <div class="form-group">
            <label for="fuel_type">Gorivo</label>
            <select id="fuel_type" v-model="vehicle.fuel_type">
              <option value="">Odaberite gorivo</option>
              <option value="petrol">Benzin</option>
              <option value="diesel">Dizel</option>
              <option value="electric">Električno</option>
              <option value="hybrid">Hibrid</option>
            </select>
          </div>

          <div class="form-group">
            <label for="transmission">Mjenjač</label>
            <select id="transmission" v-model="vehicle.transmission">
              <option value="">Odaberite mjenjač</option>
              <option value="manual">Ručni</option>
              <option value="automatic">Automatski</option>
            </select>
          </div>

          <div class="form-group">
            <label for="seats">Sjedala</label>
            <input id="seats" v-model.number="vehicle.seats" type="number" min="2" max="15" />
          </div>
        </div>

        <!-- Pricing & Availability -->
        <div class="form-row-3">
          <div class="form-group">
            <label for="daily_rate">Dnevna cijena (€) *</label>
            <input
              id="daily_rate"
              v-model.number="vehicle.daily_rate"
              type="number"
              min="0"
              step="0.01"
              required
            />
          </div>

          <div class="form-group">
            <label for="mileage">Kilometraža (km)</label>
            <input id="mileage" v-model.number="vehicle.mileage" type="number" min="0" />
          </div>

          <div class="form-group">
            <label for="status">Status</label>
            <select id="status" v-model="vehicle.status">
              <option value="available">Dostupno</option>
              <option value="rented">Iznajmljeno</option>
              <option value="maintenance">U servisu</option>
            </select>
          </div>
        </div>

        <!-- Registration & Compliance -->
        <h3 class="section-title">Registracija i tehnički pregled</h3>
        <div class="form-row-3">
          <div class="form-group">
            <label for="registration_expiry">Istek registracije</label>
            <input id="registration_expiry" v-model="vehicle.registration_expiry" type="date" />
          </div>

          <div class="form-group">
            <label for="last_inspection_date">Zadnji tehnički pregled</label>
            <input id="last_inspection_date" v-model="vehicle.last_inspection_date" type="date" />
          </div>

          <div class="form-group">
            <label for="next_inspection_due">Sljedeći tehnički pregled</label>
            <input id="next_inspection_due" v-model="vehicle.next_inspection_due" type="date" />
          </div>
        </div>

        <!-- Insurance -->
        <h3 class="section-title">Osiguranje</h3>
        <div class="form-row">
          <div class="form-group">
            <label for="insurance_company">Osiguravajuća kuća</label>
            <input
              id="insurance_company"
              v-model="vehicle.insurance_company"
              type="text"
              placeholder="npr. Croatia osiguranje"
            />
          </div>

          <div class="form-group">
            <label for="insurance_policy_number">Broj police</label>
            <input
              id="insurance_policy_number"
              v-model="vehicle.insurance_policy_number"
              type="text"
              placeholder="npr. POL-123456"
            />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="insurance_expiry">Istek osiguranja</label>
            <input id="insurance_expiry" v-model="vehicle.insurance_expiry" type="date" />
          </div>

          <div class="form-group">
            <label for="insurance_premium">Godišnja premija (€)</label>
            <input
              id="insurance_premium"
              v-model.number="vehicle.insurance_premium"
              type="number"
              min="0"
              step="0.01"
              placeholder="0.00"
            />
          </div>
        </div>

        <!-- Ownership/Leasing -->
        <h3 class="section-title">Vlasništvo</h3>
        <div class="form-row-3">
          <div class="form-group">
            <label for="ownership_type">Tip vlasništva</label>
            <select id="ownership_type" v-model="vehicle.ownership_type">
              <option value="">Odaberite tip</option>
              <option value="owned">Vlasništvo</option>
              <option value="leased">Leasing</option>
              <option value="financed">Financirano</option>
            </select>
          </div>

          <div class="form-group">
            <label for="lease_company">Leasing kuća</label>
            <input
              id="lease_company"
              v-model="vehicle.lease_company"
              type="text"
              placeholder="npr. Raiffeisen leasing"
              :disabled="vehicle.ownership_type !== 'leased'"
            />
          </div>

          <div class="form-group">
            <label for="lease_monthly_payment">Mjesečna rata (€)</label>
            <input
              id="lease_monthly_payment"
              v-model.number="vehicle.lease_monthly_payment"
              type="number"
              min="0"
              step="0.01"
              placeholder="0.00"
              :disabled="vehicle.ownership_type !== 'leased'"
            />
          </div>
        </div>

        <div class="form-row" v-if="vehicle.ownership_type === 'leased'">
          <div class="form-group">
            <label for="lease_start_date">Početak leasinga</label>
            <input id="lease_start_date" v-model="vehicle.lease_start_date" type="date" />
          </div>

          <div class="form-group">
            <label for="lease_end_date">Kraj leasinga</label>
            <input id="lease_end_date" v-model="vehicle.lease_end_date" type="date" />
          </div>
        </div>

        <!-- Maintenance -->
        <h3 class="section-title">Održavanje</h3>
        <div class="form-row-3">
          <div class="form-group">
            <label for="last_service_date">Zadnji servis</label>
            <input id="last_service_date" v-model="vehicle.last_service_date" type="date" />
          </div>

          <div class="form-group">
            <label for="next_service_due">Sljedeći servis</label>
            <input id="next_service_due" v-model="vehicle.next_service_due" type="date" />
          </div>

          <div class="form-group">
            <label for="service_interval_km">Interval servisa (km)</label>
            <input
              id="service_interval_km"
              v-model.number="vehicle.service_interval_km"
              type="number"
              min="0"
              placeholder="npr. 15000"
            />
          </div>
        </div>

        <div class="form-actions">
          <button type="button" class="btn-secondary" @click="$emit('cancel')">Cancel</button>
          <button type="submit" class="btn-primary">
            {{ editMode ? "Ažuriraj" : "Dodaj" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import { carAutocompleteApi, type Vehicle } from "@/services/api";

const props = defineProps<{
  vehicle?: Vehicle;
  editMode?: boolean;
}>();

const emit = defineEmits<{
  submit: [vehicle: Vehicle];
  cancel: [];
}>();

const vehicle = ref<Vehicle>({
  brand: props.vehicle?.brand || "",
  model: props.vehicle?.model || "",
  year: props.vehicle?.year || new Date().getFullYear(),
  category: props.vehicle?.category || "",
  registration_number: props.vehicle?.registration_number || "",
  daily_rate: props.vehicle?.daily_rate || 0,
  mileage: props.vehicle?.mileage || 0,
  status: props.vehicle?.status || "available",
  fuel_type: props.vehicle?.fuel_type || "",
  transmission: props.vehicle?.transmission || "",
  seats: props.vehicle?.seats || 5,
  // Registration & Compliance
  registration_expiry: props.vehicle?.registration_expiry || null,
  last_inspection_date: props.vehicle?.last_inspection_date || null,
  next_inspection_due: props.vehicle?.next_inspection_due || null,
  // Insurance
  insurance_company: props.vehicle?.insurance_company || null,
  insurance_policy_number: props.vehicle?.insurance_policy_number || null,
  insurance_expiry: props.vehicle?.insurance_expiry || null,
  insurance_premium: props.vehicle?.insurance_premium || null,
  // Ownership/Leasing
  ownership_type: props.vehicle?.ownership_type || null,
  lease_company: props.vehicle?.lease_company || null,
  lease_start_date: props.vehicle?.lease_start_date || null,
  lease_end_date: props.vehicle?.lease_end_date || null,
  lease_monthly_payment: props.vehicle?.lease_monthly_payment || null,
  // Maintenance
  last_service_date: props.vehicle?.last_service_date || null,
  next_service_due: props.vehicle?.next_service_due || null,
  service_interval_km: props.vehicle?.service_interval_km || null,
});

const searchBrand = ref(props.vehicle?.brand || "");
const searchModel = ref(props.vehicle?.model || "");
const filteredBrands = ref<string[]>([]);
const filteredModels = ref<string[]>([]);
const brandSearchTimeout = ref<number | null>(null);
const modelSearchTimeout = ref<number | null>(null);

onMounted(async () => {
  // Load initial brand suggestions if editing
  if (props.vehicle?.brand) {
    try {
      vehicle.value.brand = props.vehicle.brand;
      searchBrand.value = props.vehicle.brand;
      // Load brands based on the existing brand
      filteredBrands.value = await carAutocompleteApi.getMakes(props.vehicle.brand);

      // Load models for the brand
      filteredModels.value = await carAutocompleteApi.getModels(props.vehicle.brand);
    } catch (error) {
      console.error("Error loading car data:", error);
    }
  }
});

const handleBrandSearch = async () => {
  vehicle.value.brand = searchBrand.value;

  // Clear the previous timeout
  if (brandSearchTimeout.value) {
    clearTimeout(brandSearchTimeout.value);
  }

  // Reset models when brand changes
  vehicle.value.model = "";
  searchModel.value = "";
  filteredModels.value = [];

  // If search is empty, clear suggestions
  if (!searchBrand.value || searchBrand.value.length < 2) {
    filteredBrands.value = [];
    return;
  }

  // Debounce the API call
  brandSearchTimeout.value = window.setTimeout(async () => {
    try {
      filteredBrands.value = await carAutocompleteApi.getMakes(searchBrand.value);

      // If there's an exact match, load models for it
      const exactMatch = filteredBrands.value.find(
        (b) => b.toLowerCase() === searchBrand.value.toLowerCase()
      );
      if (exactMatch) {
        vehicle.value.brand = exactMatch;
        filteredModels.value = await carAutocompleteApi.getModels(exactMatch);
      }
    } catch (error) {
      console.error("Error searching brands:", error);
      filteredBrands.value = [];
    }
  }, 300);
};

const handleModelSearch = async () => {
  vehicle.value.model = searchModel.value;

  // Clear the previous timeout
  if (modelSearchTimeout.value) {
    clearTimeout(modelSearchTimeout.value);
  }

  // Can't search models without a brand
  if (!vehicle.value.brand) {
    filteredModels.value = [];
    return;
  }

  // If search is empty, clear suggestions
  if (!searchModel.value || searchModel.value.length < 2) {
    filteredModels.value = [];
    return;
  }

  // Debounce the API call
  modelSearchTimeout.value = window.setTimeout(async () => {
    try {
      filteredModels.value = await carAutocompleteApi.getModels(
        vehicle.value.brand,
        searchModel.value
      );
    } catch (error) {
      console.error("Error searching models:", error);
      filteredModels.value = [];
    }
  }, 300);
};

const handleSubmit = () => {
  emit("submit", vehicle.value);
};
</script>

<style scoped>
.vehicle-form {
  max-width: 1100px;
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
  padding: 1.25rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 1.4rem;
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
  padding: 1.5rem 2rem 1.5rem 2rem;
}

.section-title {
  font-size: 1rem;
  font-weight: 600;
  color: #667eea;
  margin: 1.5rem 0 1rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e2e8f0;
}

.section-title:first-of-type {
  margin-top: 1rem;
}

.form-group {
  margin-bottom: 0;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
  margin-bottom: 1.25rem;
}

.form-row-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
  margin-bottom: 1.25rem;
}

label {
  display: block;
  margin-bottom: 0.4rem;
  font-weight: 600;
  color: #4a5568;
  font-size: 0.8125rem;
  letter-spacing: 0.3px;
}

input,
select {
  width: 100%;
  padding: 0.6rem 0.75rem;
  border: 1.5px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.875rem;
  transition: all 0.2s ease;
  background: white;
  color: #2d3748;
}

input:focus,
select:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.08);
}

input:disabled {
  background-color: #f7fafc;
  cursor: not-allowed;
  opacity: 0.6;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
  padding-top: 1.25rem;
  border-top: 1px solid #e2e8f0;
}

button {
  padding: 0.6rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background-color: #edf2f7;
  color: #4a5568;
}

.btn-secondary:hover {
  background-color: #e2e8f0;
}
</style>
