<template>
  <div class="vehicle-stats-container">
    <div class="header">
      <button class="btn-back" @click="goBack">← Natrag</button>
      <h1 v-if="vehicle">Statistika: {{ vehicle.brand }} {{ vehicle.model }}</h1>
    </div>

    <div v-if="!vehicle" class="loading">Učitavanje podataka...</div>

    <div v-else class="content">
      <!-- Vehicle Overview Card -->
      <div class="stats-card overview-card">
        <div class="card-header">
          <h2>Pregled vozila</h2>
          <div class="quick-actions">
            <button class="btn-add" @click="showEditRegistration = true">📄 Registracija</button>
            <button class="btn-add" @click="showEditInsurance = true">🛡️ Osiguranje</button>
          </div>
        </div>
        <div class="overview-grid">
          <div class="overview-item">
            <span class="label">Registracija</span>
            <span class="value">{{ vehicle.registration_number }}</span>
          </div>
          <div class="overview-item">
            <span class="label">Kategorija</span>
            <span class="value">{{ translateCategory(vehicle.category) }}</span>
          </div>
          <div class="overview-item">
            <span class="label">Status</span>
            <span class="value">
              <span class="status-badge" :class="vehicle.status">
                {{ translateStatus(vehicle.status) }}
              </span>
            </span>
          </div>
          <div class="overview-item">
            <span class="label">Kilometraža</span>
            <span class="value">{{ vehicle.mileage?.toLocaleString() || 0 }} km</span>
          </div>
        </div>
      </div>

      <!-- Key Metrics -->
      <div class="metrics-row">
        <div class="metric-card">
          <div class="metric-icon">📊</div>
          <div class="metric-value">{{ stats.totalReservations }}</div>
          <div class="metric-label">Ukupno rezervacija</div>
        </div>

        <div class="metric-card">
          <div class="metric-icon">✅</div>
          <div class="metric-value">{{ stats.completedReservations }}</div>
          <div class="metric-label">Završene rezervacije</div>
        </div>

        <div class="metric-card">
          <div class="metric-icon">💰</div>
          <div class="metric-value">{{ formatPrice(stats.totalRevenue) }}</div>
          <div class="metric-label">Ukupna zarada</div>
        </div>

        <div class="metric-card">
          <div class="metric-icon">📅</div>
          <div class="metric-value">{{ stats.totalDaysRented }}</div>
          <div class="metric-label">Dana iznajmljeno</div>
        </div>
      </div>

      <!-- Revenue & Utilization -->
      <div class="stats-row">
        <div class="stats-card">
          <h2>Prihod po mjesecima</h2>
          <div v-if="stats.monthlyRevenue.length > 0" class="chart-container">
            <div class="bar-chart">
              <div v-for="month in stats.monthlyRevenue" :key="month.month" class="bar-item">
                <div class="bar-wrapper">
                  <div
                    class="bar"
                    :style="{
                      height: `${(month.revenue / maxMonthlyRevenue) * 100}%`,
                    }"
                  ></div>
                </div>
                <div class="bar-label">{{ month.month }}</div>
                <div class="bar-value">
                  {{ month.revenue.toLocaleString("de-DE", { maximumFractionDigits: 0 }) }} €
                </div>
              </div>
            </div>
          </div>
          <div v-else class="no-data">Nema podataka o prihodima</div>
        </div>

        <div class="stats-card">
          <h2>Korištenje vozila</h2>
          <div class="utilization-stats">
            <div class="util-item">
              <div class="util-label">Stopa korištenja</div>
              <div class="util-value">{{ stats.utilizationRate.toFixed(1) }}%</div>
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: `${stats.utilizationRate}%` }"></div>
              </div>
            </div>

            <div class="util-item">
              <div class="util-label">Prosječno dana po rezervaciji</div>
              <div class="util-value">{{ stats.avgDaysPerReservation.toFixed(1) }}</div>
            </div>

            <div class="util-item">
              <div class="util-label">Prosječna zarada po danu</div>
              <div class="util-value">{{ formatPrice(stats.avgRevenuePerDay) }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Maintenance & Damage Stats -->
      <div class="stats-row">
        <div class="stats-card">
          <div class="card-header">
            <h2>Održavanje</h2>
            <button class="btn-add" @click="showAddMaintenance = true">+ Dodaj servis</button>
          </div>
          <div class="maintenance-stats">
            <div class="stat-row">
              <span class="stat-label">Ukupno servisa:</span>
              <span class="stat-value">{{ stats.totalMaintenanceRecords }}</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Ukupni troškovi servisa:</span>
              <span class="stat-value">{{ formatPrice(stats.totalMaintenanceCost) }}</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Zadnji servis:</span>
              <span class="stat-value">{{
                vehicle.last_service_date ? formatDate(vehicle.last_service_date) : "N/A"
              }}</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Sljedeći servis:</span>
              <span class="stat-value" :class="{ expired: isExpired(vehicle.next_service_due) }">{{
                vehicle.next_service_due ? formatDate(vehicle.next_service_due) : "N/A"
              }}</span>
            </div>
          </div>
        </div>

        <div class="stats-card">
          <div class="card-header">
            <h2>Oštećenja</h2>
            <button class="btn-add" @click="showAddDamage = true">+ Prijavi štetu</button>
          </div>
          <div class="damage-stats">
            <div class="stat-row">
              <span class="stat-label">Ukupno prijava:</span>
              <span class="stat-value">{{ stats.totalDamageReports }}</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Nepopravljeno:</span>
              <span class="stat-value">{{ stats.unrepairedDamages }}</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Ukupni troškovi popravka:</span>
              <span class="stat-value">{{ formatPrice(stats.totalRepairCost) }}</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Posljednja šteta:</span>
              <span class="stat-value">{{
                stats.lastDamageDate ? formatDate(stats.lastDamageDate) : "N/A"
              }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="stats-card">
        <h2>Nedavna aktivnost</h2>
        <div v-if="recentReservations.length > 0" class="activity-list">
          <div
            v-for="reservation in recentReservations"
            :key="reservation.id"
            class="activity-item"
          >
            <div class="activity-icon">🚗</div>
            <div class="activity-details">
              <div class="activity-title">{{ getCustomerName(reservation.customer_id) }}</div>
              <div class="activity-date">
                {{ formatDate(reservation.start_date) }} - {{ formatDate(reservation.end_date) }}
              </div>
            </div>
            <div class="activity-status">
              <span class="status-badge" :class="reservation.status">
                {{ translateReservationStatus(reservation.status || "") }}
              </span>
            </div>
            <div class="activity-price">{{ formatPrice(reservation.total_price || 0) }}</div>
          </div>
        </div>
        <div v-else class="no-data">Nema nedavnih aktivnosti</div>
      </div>
    </div>

    <!-- Modals -->
    <div v-if="showAddMaintenance" class="modal" @click.self="showAddMaintenance = false">
      <div class="modal-content">
        <h2>Dodaj servisni zapis</h2>
        <form @submit.prevent="handleAddMaintenance">
          <div class="form-group">
            <label>Vrsta servisa *</label>
            <select v-model="maintenanceForm.service_type" required>
              <option value="oil_change">Zamjena ulja</option>
              <option value="tire_change">Zamjena guma</option>
              <option value="brake_service">Servis kočnica</option>
              <option value="general_inspection">Opći pregled</option>
              <option value="repair">Popravak</option>
              <option value="other">Ostalo</option>
            </select>
          </div>
          <div class="form-group">
            <label>Opis</label>
            <textarea v-model="maintenanceForm.description" rows="3"></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Datum servisa *</label>
              <input type="date" v-model="maintenanceForm.service_date" required />
            </div>
            <div class="form-group">
              <label>Kilometraža *</label>
              <input type="number" v-model.number="maintenanceForm.mileage_at_service" required />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Trošak (€) *</label>
              <input type="number" step="0.01" v-model.number="maintenanceForm.cost" required />
            </div>
            <div class="form-group">
              <label>Izvršio</label>
              <input type="text" v-model="maintenanceForm.performed_by" />
            </div>
          </div>
          <div class="form-group">
            <label>Sljedeći servis (km)</label>
            <input type="number" v-model.number="maintenanceForm.next_service_km" />
          </div>
          <div class="form-actions">
            <button type="button" class="btn-cancel" @click="showAddMaintenance = false">
              Odustani
            </button>
            <button type="submit" class="btn-submit">Spremi</button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showAddDamage" class="modal" @click.self="showAddDamage = false">
      <div class="modal-content">
        <h2>Prijavi štetu</h2>
        <form @submit.prevent="handleAddDamage">
          <div class="form-group">
            <label>Ozbiljnost *</label>
            <select v-model="damageForm.severity" required>
              <option value="minor">Manja</option>
              <option value="moderate">Umjerena</option>
              <option value="major">Veća</option>
            </select>
          </div>
          <div class="form-group">
            <label>Opis oštećenja *</label>
            <textarea v-model="damageForm.description" rows="4" required></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Datum prijave *</label>
              <input type="date" v-model="damageForm.report_date" required />
            </div>
            <div class="form-group">
              <label>Procjena troška (€)</label>
              <input type="number" step="0.01" v-model.number="damageForm.repair_cost" />
            </div>
          </div>
          <div class="form-group">
            <label>Povezana rezervacija</label>
            <select v-model="damageForm.reservation_id">
              <option :value="null">Nema</option>
              <option v-for="res in reservations" :key="res.id" :value="res.id">
                Rezervacija #{{ res.id }} ({{ formatDate(res.start_date) }})
              </option>
            </select>
          </div>
          <div class="form-actions">
            <button type="button" class="btn-cancel" @click="showAddDamage = false">
              Odustani
            </button>
            <button type="submit" class="btn-submit">Spremi</button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showEditRegistration" class="modal" @click.self="showEditRegistration = false">
      <div class="modal-content">
        <h2>Ažuriraj podatke o registraciji</h2>
        <form @submit.prevent="handleUpdateRegistration">
          <div class="form-group">
            <label>Broj registracije *</label>
            <input type="text" v-model="registrationForm.registration_number" required />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Datum isteka registracije</label>
              <input type="date" v-model="registrationForm.registration_expiry" />
            </div>
            <div class="form-group">
              <label>Datum sledećeg tehničkog</label>
              <input type="date" v-model="registrationForm.technical_inspection_due" />
            </div>
          </div>
          <div class="form-actions">
            <button type="button" class="btn-cancel" @click="showEditRegistration = false">
              Odustani
            </button>
            <button type="submit" class="btn-submit">Spremi</button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showEditInsurance" class="modal" @click.self="showEditInsurance = false">
      <div class="modal-content">
        <h2>Ažuriraj podatke o osiguranju</h2>
        <form @submit.prevent="handleUpdateInsurance">
          <div class="form-group">
            <label>Osiguravajuća kuća</label>
            <input type="text" v-model="insuranceForm.insurance_provider" />
          </div>
          <div class="form-group">
            <label>Broj polise</label>
            <input type="text" v-model="insuranceForm.insurance_policy_number" />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Datum isteka osiguranja</label>
              <input type="date" v-model="insuranceForm.insurance_expiry" />
            </div>
            <div class="form-group">
              <label>Godišnja premija (€)</label>
              <input type="number" step="0.01" v-model.number="insuranceForm.insurance_premium" />
            </div>
          </div>
          <div class="form-actions">
            <button type="button" class="btn-cancel" @click="showEditInsurance = false">
              Odustani
            </button>
            <button type="submit" class="btn-submit">Spremi</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const formatPrice = (price: number) => {
  return (
    price.toLocaleString("de-DE", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " €"
  );
};

import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import type {
  Vehicle,
  Reservation,
  Customer,
  DamageReport,
  MaintenanceRecord,
} from "@/services/api";

const API_BASE_URL = "http://localhost:8000/api";

const route = useRoute();
const router = useRouter();

const vehicle = ref<Vehicle | null>(null);
const reservations = ref<Reservation[]>([]);
const customers = ref<Customer[]>([]);
const damageReports = ref<DamageReport[]>([]);
const maintenanceRecords = ref<MaintenanceRecord[]>([]);

const showAddMaintenance = ref(false);
const showAddDamage = ref(false);
const showEditRegistration = ref(false);
const showEditInsurance = ref(false);

const maintenanceForm = ref({
  vehicle_id: 0,
  service_type: "oil_change",
  description: "",
  service_date: new Date().toISOString().split("T")[0],
  mileage_at_service: 0,
  cost: 0,
  performed_by: "",
  next_service_km: null as number | null,
});

const damageForm = ref({
  vehicle_id: 0,
  reservation_id: null as number | null,
  description: "",
  severity: "minor",
  report_date: new Date().toISOString().split("T")[0],
  repair_cost: 0,
  repaired: false,
  repair_date: null as string | null,
});

const registrationForm = ref({
  registration_number: "",
  registration_expiry: null as string | null,
  technical_inspection_due: null as string | null,
});

const insuranceForm = ref({
  insurance_provider: null as string | null,
  insurance_policy_number: null as string | null,
  insurance_expiry: null as string | null,
  insurance_premium: null as number | null,
});

const categories = [
  { value: "economy", label: "Ekonomska" },
  { value: "compact", label: "Kompaktna" },
  { value: "suv", label: "SUV" },
  { value: "luxury", label: "Luksuzna" },
  { value: "van", label: "Kombi" },
];

const vehicleReservations = computed(() => {
  return reservations.value.filter((r) => r.vehicle_id === vehicle.value?.id);
});

const recentReservations = computed(() => {
  return vehicleReservations.value
    .sort((a, b) => new Date(b.start_date).getTime() - new Date(a.start_date).getTime())
    .slice(0, 10);
});

const stats = computed(() => {
  const completed = vehicleReservations.value.filter((r) => r.status === "completed");
  const totalRevenue = completed.reduce((sum, r) => sum + (r.total_price || 0), 0);
  const totalDays = completed.reduce((sum, r) => {
    const start = new Date(r.start_date);
    const end = new Date(r.end_date);
    return sum + Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
  }, 0);

  // Monthly revenue (last 12 months)
  const monthlyRevenue: { month: string; revenue: number }[] = [];
  const now = new Date();
  for (let i = 11; i >= 0; i--) {
    const date = new Date(now.getFullYear(), now.getMonth() - i, 1);
    const monthName = date.toLocaleDateString("hr-HR", { month: "short" });
    const monthRevenue = completed
      .filter((r) => {
        const resDate = new Date(r.start_date);
        return (
          resDate.getMonth() === date.getMonth() && resDate.getFullYear() === date.getFullYear()
        );
      })
      .reduce((sum, r) => sum + (r.total_price || 0), 0);
    monthlyRevenue.push({ month: monthName, revenue: monthRevenue });
  }

  // Utilization rate (percentage of days rented in last 365 days)
  const utilizationRate = (totalDays / 365) * 100;

  // Maintenance stats
  const totalMaintenanceCost = maintenanceRecords.value.reduce((sum, m) => sum + (m.cost || 0), 0);

  // Damage stats
  const unrepairedDamages = damageReports.value.filter((d) => !d.repaired).length;
  const totalRepairCost = damageReports.value.reduce((sum, d) => sum + (d.repair_cost || 0), 0);
  const lastDamageDate =
    damageReports.value.length > 0
      ? damageReports.value.sort(
          (a, b) => new Date(b.report_date).getTime() - new Date(a.report_date).getTime()
        )[0].report_date
      : null;

  return {
    totalReservations: vehicleReservations.value.length,
    completedReservations: completed.length,
    totalRevenue,
    totalDaysRented: totalDays,
    avgDaysPerReservation: completed.length > 0 ? totalDays / completed.length : 0,
    avgRevenuePerDay: totalDays > 0 ? totalRevenue / totalDays : 0,
    monthlyRevenue,
    utilizationRate: utilizationRate > 100 ? 100 : utilizationRate,
    totalMaintenanceRecords: maintenanceRecords.value.length,
    totalMaintenanceCost,
    totalDamageReports: damageReports.value.length,
    unrepairedDamages,
    totalRepairCost,
    lastDamageDate,
  };
});

const maxMonthlyRevenue = computed(() => {
  return Math.max(...stats.value.monthlyRevenue.map((m) => m.revenue), 1);
});

const fetchData = async () => {
  const vehicleId = route.params.id;

  try {
    const [vehicleRes, reservationsRes, customersRes, damageRes, maintenanceRes] =
      await Promise.all([
        fetch(`${API_BASE_URL}/vehicles/${vehicleId}`).then((r) => r.json()),
        fetch(`${API_BASE_URL}/reservations`).then((r) => r.json()),
        fetch(`${API_BASE_URL}/customers`).then((r) => r.json()),
        fetch(`${API_BASE_URL}/damage-reports?vehicle_id=${vehicleId}`).then((r) => r.json()),
        fetch(`${API_BASE_URL}/maintenance-records?vehicle_id=${vehicleId}`).then((r) => r.json()),
      ]);

    vehicle.value = vehicleRes;
    reservations.value = reservationsRes;
    customers.value = customersRes;
    damageReports.value = damageRes;
    maintenanceRecords.value = maintenanceRes;

    // Populate forms with current vehicle data
    registrationForm.value = {
      registration_number: vehicleRes.registration_number || "",
      registration_expiry: vehicleRes.registration_expiry || null,
      technical_inspection_due: vehicleRes.technical_inspection_due || null,
    };

    insuranceForm.value = {
      insurance_provider: vehicleRes.insurance_provider || null,
      insurance_policy_number: vehicleRes.insurance_policy_number || null,
      insurance_expiry: vehicleRes.insurance_expiry || null,
      insurance_premium: vehicleRes.insurance_premium || null,
    };
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

const goBack = () => {
  router.back();
};

const translateCategory = (category: string) => {
  const cat = categories.find((c) => c.value === category);
  return cat ? cat.label : category;
};

const translateStatus = (status?: string) => {
  const translations: Record<string, string> = {
    available: "Dostupno",
    reserved: "Rezervirano",
    rented: "Iznajmljeno",
    maintenance: "Održavanje",
  };
  return translations[status || ""] || status;
};

const translateReservationStatus = (status: string) => {
  const translations: Record<string, string> = {
    pending: "Na čekanju",
    confirmed: "Potvrđena",
    active: "Aktivna",
    completed: "Završena",
    cancelled: "Otkazana",
  };
  return translations[status] || status;
};

const getCustomerName = (customerId: number) => {
  const customer = customers.value.find((c) => c.id === customerId);
  return customer ? `${customer.first_name} ${customer.last_name}` : "Nepoznato";
};

const formatDate = (dateString: string | null) => {
  if (!dateString) return null;
  const date = new Date(dateString);
  return date.toLocaleDateString("hr-HR");
};

const isExpired = (dateString: string | null) => {
  if (!dateString) return false;
  const date = new Date(dateString);
  const today = new Date();
  return date < today;
};

const handleAddMaintenance = async () => {
  try {
    maintenanceForm.value.vehicle_id = vehicle.value?.id || 0;
    const response = await fetch(`${API_BASE_URL}/maintenance-records`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(maintenanceForm.value),
    });
    if (response.ok) {
      showAddMaintenance.value = false;
      await fetchData();
      // Reset form
      maintenanceForm.value = {
        vehicle_id: 0,
        service_type: "oil_change",
        description: "",
        service_date: new Date().toISOString().split("T")[0],
        mileage_at_service: 0,
        cost: 0,
        performed_by: "",
        next_service_km: null,
      };
    }
  } catch (err) {
    console.error("Failed to add maintenance record:", err);
    alert("Greška pri dodavanju servisnog zapisa");
  }
};

const handleAddDamage = async () => {
  try {
    damageForm.value.vehicle_id = vehicle.value?.id || 0;
    const response = await fetch(`${API_BASE_URL}/damage-reports`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(damageForm.value),
    });
    if (response.ok) {
      showAddDamage.value = false;
      await fetchData();
      // Reset form
      damageForm.value = {
        vehicle_id: 0,
        reservation_id: null,
        description: "",
        severity: "minor",
        report_date: new Date().toISOString().split("T")[0],
        repair_cost: 0,
        repaired: false,
        repair_date: null,
      };
    }
  } catch (err) {
    console.error("Failed to add damage report:", err);
    alert("Greška pri dodavanju prijave štete");
  }
};

const handleUpdateRegistration = async () => {
  try {
    const updateData = {
      ...vehicle.value,
      registration_number: registrationForm.value.registration_number,
      registration_expiry: registrationForm.value.registration_expiry,
      technical_inspection_due: registrationForm.value.technical_inspection_due,
    };

    const response = await fetch(`${API_BASE_URL}/vehicles/${vehicle.value?.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updateData),
    });

    if (response.ok) {
      showEditRegistration.value = false;
      await fetchData();
    }
  } catch (err) {
    console.error("Failed to update registration:", err);
    alert("Greška pri ažuriranju registracije");
  }
};

const handleUpdateInsurance = async () => {
  try {
    const updateData = {
      ...vehicle.value,
      insurance_provider: insuranceForm.value.insurance_provider,
      insurance_policy_number: insuranceForm.value.insurance_policy_number,
      insurance_expiry: insuranceForm.value.insurance_expiry,
      insurance_premium: insuranceForm.value.insurance_premium,
    };

    const response = await fetch(`${API_BASE_URL}/vehicles/${vehicle.value?.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updateData),
    });

    if (response.ok) {
      showEditInsurance.value = false;
      await fetchData();
    }
  } catch (err) {
    console.error("Failed to update insurance:", err);
    alert("Greška pri ažuriranju osiguranja");
  }
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.vehicle-stats-container {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  background: #f7fafc;
  min-height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.btn-back {
  padding: 0.75rem 1.5rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-back:hover {
  background: #f7fafc;
  border-color: #667eea;
}

h1 {
  font-size: 2rem;
  font-weight: bold;
  color: #2d3748;
  margin: 0;
}

h2 {
  font-size: 1.25rem;
  color: #2d3748;
  margin: 0 0 1.5rem 0;
  font-weight: 600;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.stats-card,
.overview-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
}

.overview-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.overview-item .label {
  font-size: 0.875rem;
  color: #718096;
  font-weight: 500;
}

.overview-item .value {
  font-size: 1.25rem;
  color: #2d3748;
  font-weight: 600;
}

.metrics-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.metric-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.metric-icon {
  font-size: 2.5rem;
  margin-bottom: 0.75rem;
}

.metric-value {
  font-size: 2rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.metric-label {
  font-size: 0.875rem;
  color: #718096;
  font-weight: 500;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.chart-container {
  height: 250px;
  display: flex;
  align-items: flex-end;
}

.bar-chart {
  display: flex;
  gap: 0.75rem;
  width: 100%;
  align-items: flex-end;
  height: 100%;
}

.bar-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
}

.bar-wrapper {
  flex: 1;
  width: 100%;
  display: flex;
  align-items: flex-end;
  padding-bottom: 0.5rem;
}

.bar {
  width: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px 4px 0 0;
  min-height: 5px;
  transition: all 0.3s;
}

.bar-item:hover .bar {
  opacity: 0.8;
}

.bar-label {
  font-size: 0.75rem;
  color: #718096;
  margin-top: 0.25rem;
  font-weight: 500;
}

.bar-value {
  font-size: 0.75rem;
  color: #2d3748;
  font-weight: 600;
  margin-top: 0.25rem;
}

.utilization-stats {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.util-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.util-label {
  font-size: 0.875rem;
  color: #718096;
  font-weight: 500;
}

.util-value {
  font-size: 1.5rem;
  color: #2d3748;
  font-weight: 700;
}

.progress-bar {
  height: 12px;
  background: #e2e8f0;
  border-radius: 6px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s;
}

.maintenance-stats,
.damage-stats {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #e2e8f0;
}

.stat-row:last-child {
  border-bottom: none;
}

.stat-label {
  color: #718096;
  font-weight: 500;
}

.stat-value {
  color: #2d3748;
  font-weight: 600;
}

.expired {
  color: #dc2626;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f7fafc;
  border-radius: 8px;
  transition: all 0.2s;
}

.activity-item:hover {
  background: #edf2f7;
}

.activity-icon {
  font-size: 1.5rem;
}

.activity-details {
  flex: 1;
}

.activity-title {
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 0.25rem;
}

.activity-date {
  font-size: 0.875rem;
  color: #718096;
}

.activity-price {
  font-size: 1.125rem;
  font-weight: 700;
  color: #667eea;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.available {
  background: #c6f6d5;
  color: #22543d;
}

.status-badge.reserved {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.rented {
  background: #fed7d7;
  color: #742a2a;
}

.status-badge.maintenance {
  background: #e2e8f0;
  color: #4a5568;
}

.status-badge.pending {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.confirmed {
  background: #dbeafe;
  color: #1e40af;
}

.status-badge.active {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.completed {
  background: #e5e7eb;
  color: #374151;
}

.status-badge.cancelled {
  background: #fee;
  color: #991b1b;
}

.no-data {
  text-align: center;
  padding: 2rem;
  color: #718096;
  font-style: italic;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #718096;
  font-size: 1.25rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.card-header h2 {
  margin: 0;
}

.quick-actions {
  display: flex;
  gap: 0.5rem;
}

.quick-actions .btn-add {
  font-size: 0.875rem;
  padding: 0.5rem 1rem;
}

.btn-add {
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 600;
  transition: background 0.2s;
}

.btn-add:hover {
  background: #5a67d8;
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
  padding: 2rem;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-content h2 {
  margin: 0 0 1.5rem 0;
  color: #2d3748;
}

.form-group {
  margin-bottom: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #4a5568;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.95rem;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-cancel,
.btn-submit {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel {
  background: #e2e8f0;
  color: #4a5568;
}

.btn-cancel:hover {
  background: #cbd5e0;
}

.btn-submit {
  background: #667eea;
  color: white;
}

.btn-submit:hover {
  background: #5a67d8;
}
</style>
