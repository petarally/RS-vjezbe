<template>
  <div class="gantt-container">
    <div class="gantt-header">
      <h2>Pregled dostupnosti vozila</h2>
      <div class="date-controls">
        <button @click="previousWeek" class="btn-nav">← Prethodni tjedan</button>
        <span class="current-period">{{ formatPeriod() }}</span>
        <button @click="nextWeek" class="btn-nav">Sljedeći tjedan →</button>
        <button @click="goToToday" class="btn-today">Danas</button>
      </div>
    </div>

    <!-- Statistics -->
    <div class="statistics">
      <div class="stat-card">
        <div class="stat-value">{{ stats.totalVehicles }}</div>
        <div class="stat-label">Ukupno vozila</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ stats.availableVehicles }}</div>
        <div class="stat-label">Dostupna vozila</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ stats.activeReservations }}</div>
        <div class="stat-label">Aktivne rezervacije</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ stats.utilizationRate }}%</div>
        <div class="stat-label">Iskorištenost</div>
      </div>
    </div>

    <!-- Gantt Chart -->
    <div class="gantt-wrapper">
      <div class="gantt-grid">
        <!-- Header Row with Dates -->
        <div class="gantt-header-row">
          <div class="category-header">Kategorija</div>
          <div class="dates-header">
            <div
              v-for="day in visibleDays"
              :key="day.date"
              class="date-cell"
              :class="{ today: isToday(day.date), weekend: day.isWeekend }"
            >
              <div class="day-name">{{ day.dayName }}</div>
              <div class="day-number">{{ day.dayNumber }}</div>
            </div>
          </div>
        </div>

        <!-- Category Rows -->
        <div v-for="category in categories" :key="category.value" class="category-group">
          <!-- Category Header Row -->
          <div class="category-header-row">
            <div class="category-cell category-title">
              <div class="category-name">{{ category.label }}</div>
              <div class="category-count">
                {{ getVehicleCount(category.value) }}
                {{ getVehicleCount(category.value) === 1 ? "vozilo" : "vozila" }}
              </div>
            </div>
            <div class="timeline category-timeline"></div>
          </div>

          <!-- Vehicle Rows within Category -->
          <div
            v-for="vehicle in getVehiclesInCategory(category.value)"
            :key="vehicle.id"
            class="vehicle-row"
          >
            <div class="vehicle-cell">
              <router-link :to="`/vehicles/${vehicle.id}`" class="vehicle-link">{{
                vehicle.registration_number
              }}</router-link>
            </div>
            <div class="timeline">
              <div
                v-for="day in visibleDays"
                :key="day.date"
                class="timeline-cell"
                :class="{ weekend: day.isWeekend, today: day.date && isToday(day.date) }"
              >
                <div
                  v-for="reservation in vehicle.id && day.date
                    ? getReservationsForVehicle(vehicle.id, day.date)
                    : []"
                  :key="reservation.id"
                  class="reservation-bar"
                  :style="day.date ? getReservationStyle(reservation, day.date) : {}"
                  :title="getReservationTooltip(reservation)"
                  @click="showReservationDetails(reservation)"
                >
                  <span class="reservation-text">{{ getReservationLabel(reservation) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Legend -->
    <div class="legend">
      <div class="legend-item">
        <span class="legend-color" style="background: #667eea"></span>
        <span>Potvrđena rezervacija</span>
      </div>
      <div class="legend-item">
        <span class="legend-color" style="background: #fbbf24"></span>
        <span>Na čekanju</span>
      </div>
      <div class="legend-item">
        <span class="legend-color" style="background: #10b981"></span>
        <span>Aktivna</span>
      </div>
      <div class="legend-item">
        <span class="legend-color" style="background: #6b7280"></span>
        <span>Završena</span>
      </div>
    </div>

    <!-- Reservation Details Modal -->
    <div v-if="selectedReservation" class="modal" @click.self="selectedReservation = null">
      <div class="modal-content reservation-details">
        <h3>Detalji rezervacije #{{ selectedReservation.id }}</h3>
        <div class="detail-row">
          <strong>Kategorija:</strong> {{ translateCategory(selectedReservation.category) }}
        </div>
        <div class="detail-row" v-if="selectedReservation.preferred_car_model">
          <strong>Preferirani model:</strong> {{ selectedReservation.preferred_car_model }}
        </div>
        <div class="detail-row" v-if="selectedReservation.vehicle_id">
          <strong>Dodijeljeno vozilo:</strong> {{ getVehicleName(selectedReservation.vehicle_id) }}
        </div>
        <div class="detail-row">
          <strong>Korisnik:</strong> {{ getCustomerName(selectedReservation.customer_id) }}
        </div>
        <div class="detail-row">
          <strong>Period:</strong> {{ formatDate(selectedReservation.start_date) }} -
          {{ formatDate(selectedReservation.end_date) }}
        </div>
        <div class="detail-row">
          <strong>Trajanje:</strong> {{ calculateDuration(selectedReservation) }} dana
        </div>
        <div class="detail-row">
          <strong>Cijena:</strong>
          {{
            (selectedReservation.total_price || 0).toLocaleString("de-DE", {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })
          }}
          €
        </div>
        <div class="detail-row">
          <strong>Status:</strong>
          <span :class="`status-badge ${selectedReservation.status}`">{{
            translateStatus(selectedReservation.status || "")
          }}</span>
        </div>
        <button class="btn-close" @click="selectedReservation = null">Zatvori</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import type { Reservation, Vehicle, Customer } from "@/services/api";

const props = defineProps<{
  reservations: Reservation[];
  vehicles: Vehicle[];
  customers: Customer[];
}>();

const categories = [
  { value: "economy", label: "Ekonomska" },
  { value: "compact", label: "Kompaktna" },
  { value: "suv", label: "SUV" },
  { value: "luxury", label: "Luksuzna" },
  { value: "van", label: "Kombi" },
];

const currentWeekStart = ref(new Date());
const selectedReservation = ref<Reservation | null>(null);
const DAYS_TO_SHOW = 14; // Show 2 weeks

// Initialize to start of current week
onMounted(() => {
  goToToday();
});

const visibleDays = computed(() => {
  const days = [];
  const start = new Date(currentWeekStart.value);

  for (let i = 0; i < DAYS_TO_SHOW; i++) {
    const date = new Date(start);
    date.setDate(start.getDate() + i);

    days.push({
      date: date.toISOString().split("T")[0],
      dayName: date.toLocaleDateString("hr-HR", { weekday: "short" }),
      dayNumber: date.getDate(),
      month: date.toLocaleDateString("hr-HR", { month: "short" }),
      isWeekend: date.getDay() === 0 || date.getDay() === 6,
    });
  }

  return days;
});

const stats = computed(() => {
  const totalVehicles = props.vehicles.length;
  const today = new Date().toISOString().split("T")[0];

  const activeReservations = props.reservations.filter(
    (r) => r.status === "active" || r.status === "confirmed"
  ).length;

  const availableVehicles = props.vehicles.filter((v) => {
    const hasActiveReservation = props.reservations.some(
      (r) =>
        r.vehicle_id === v.id &&
        (r.status === "active" || r.status === "confirmed") &&
        r.start_date &&
        r.end_date &&
        r.start_date <= today &&
        r.end_date >= today
    );
    return !hasActiveReservation && v.status !== "maintenance";
  }).length;

  const utilizationRate =
    totalVehicles > 0 ? Math.round((activeReservations / totalVehicles) * 100) : 0;

  return {
    totalVehicles,
    availableVehicles,
    activeReservations,
    utilizationRate,
  };
});

const getVehicleCount = (category: string) => {
  return props.vehicles.filter((v) => v.category === category && v.status !== "maintenance").length;
};

const getVehiclesInCategory = (category: string) => {
  return props.vehicles
    .filter((v) => v.category === category && v.status !== "maintenance")
    .sort((a, b) => a.brand.localeCompare(b.brand) || a.model.localeCompare(b.model));
};

const getReservationsForVehicle = (vehicleId: number, date: string) => {
  return props.reservations.filter((r) => {
    if (r.vehicle_id !== vehicleId) return false;
    if (r.status === "cancelled") return false;

    return r.start_date <= date && r.end_date >= date;
  });
};

const translateVehicleStatus = (status?: string) => {
  const translations: Record<string, string> = {
    available: "Dostupno",
    reserved: "Rezervirano",
    rented: "Iznajmljeno",
    maintenance: "Održavanje",
  };
  return translations[status || ""] || status;
};

const getReservationStyle = (reservation: Reservation, currentDate: string) => {
  const isStart = reservation.start_date === currentDate;
  const isEnd = reservation.end_date === currentDate;

  let backgroundColor = "#667eea"; // confirmed
  if (reservation.status === "pending") backgroundColor = "#fbbf24";
  if (reservation.status === "active") backgroundColor = "#10b981";
  if (reservation.status === "completed") backgroundColor = "#6b7280";

  return {
    backgroundColor,
    borderTopLeftRadius: isStart ? "4px" : "0",
    borderBottomLeftRadius: isStart ? "4px" : "0",
    borderTopRightRadius: isEnd ? "4px" : "0",
    borderBottomRightRadius: isEnd ? "4px" : "0",
  };
};

const getReservationLabel = (reservation: Reservation) => {
  const customer = props.customers.find((c) => c.id === reservation.customer_id);
  return customer ? `${customer.first_name} ${customer.last_name}` : `#${reservation.id}`;
};

const getReservationTooltip = (reservation: Reservation) => {
  const customer = getCustomerName(reservation.customer_id);
  const vehicle = reservation.vehicle_id
    ? getVehicleName(reservation.vehicle_id)
    : "Nije dodijeljeno";
  return `${customer}\n${vehicle}\n${reservation.start_date} - ${reservation.end_date}`;
};

const showReservationDetails = (reservation: Reservation) => {
  selectedReservation.value = reservation;
};

const isToday = (date: string) => {
  const today = new Date().toISOString().split("T")[0];
  return date === today;
};

const formatPeriod = () => {
  const start = visibleDays.value[0];
  const end = visibleDays.value[visibleDays.value.length - 1];
  if (!start || !end) return "";
  return `${start.dayNumber}. ${start.month} - ${end.dayNumber}. ${end.month}`;
};

const previousWeek = () => {
  const newDate = new Date(currentWeekStart.value);
  newDate.setDate(newDate.getDate() - 7);
  currentWeekStart.value = newDate;
};

const nextWeek = () => {
  const newDate = new Date(currentWeekStart.value);
  newDate.setDate(newDate.getDate() + 7);
  currentWeekStart.value = newDate;
};

const goToToday = () => {
  const today = new Date();
  const dayOfWeek = today.getDay();
  const diff = dayOfWeek === 0 ? -6 : 1 - dayOfWeek; // Start on Monday
  const monday = new Date(today);
  monday.setDate(today.getDate() + diff);
  currentWeekStart.value = monday;
};

const translateCategory = (category: string) => {
  const cat = categories.find((c) => c.value === category);
  return cat ? cat.label : category;
};

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

const getVehicleName = (vehicleId: number) => {
  const vehicle = props.vehicles.find((v) => v.id === vehicleId);
  return vehicle ? `${vehicle.brand} ${vehicle.model}` : "Nepoznato";
};

const getCustomerName = (customerId: number) => {
  const customer = props.customers.find((c) => c.id === customerId);
  return customer ? `${customer.first_name} ${customer.last_name}` : "Nepoznato";
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString("hr-HR");
};

const calculateDuration = (reservation: Reservation) => {
  const start = new Date(reservation.start_date);
  const end = new Date(reservation.end_date);
  const diffTime = Math.abs(end.getTime() - start.getTime());
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays || 1;
};
</script>

<style scoped>
.gantt-container {
  padding: 2rem;
  background: #f7fafc;
  min-height: 100vh;
}

.gantt-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

h2 {
  font-size: 2rem;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.date-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.btn-nav,
.btn-today {
  padding: 0.5rem 1rem;
  border: 1px solid #cbd5e0;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-nav:hover,
.btn-today:hover {
  background: #f7fafc;
  border-color: #667eea;
}

.btn-today {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
}

.current-period {
  font-weight: 600;
  color: #2d3748;
  min-width: 150px;
  text-align: center;
}

.statistics {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: #718096;
  font-size: 0.875rem;
  font-weight: 500;
}

.gantt-wrapper {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
  margin-bottom: 2rem;
}

.gantt-grid {
  min-width: 1200px;
}

.gantt-header-row {
  display: grid;
  grid-template-columns: 200px 1fr;
  border-bottom: 2px solid #e2e8f0;
  position: sticky;
  top: 0;
  background: white;
  z-index: 10;
}

.category-header {
  padding: 1rem;
  font-weight: 700;
  color: #2d3748;
  border-right: 2px solid #e2e8f0;
  display: flex;
  align-items: center;
}

.dates-header {
  display: grid;
  grid-template-columns: repeat(14, 1fr);
}

.date-cell {
  padding: 0.75rem 0.5rem;
  text-align: center;
  border-right: 1px solid #e2e8f0;
  min-width: 70px;
}

.date-cell.today {
  background: linear-gradient(180deg, #fef3c7 0%, #fef3c7 100%);
  font-weight: 700;
}

.date-cell.weekend {
  background: #f7fafc;
}

.day-name {
  font-size: 0.75rem;
  color: #718096;
  font-weight: 600;
  text-transform: uppercase;
}

.day-number {
  font-size: 1.125rem;
  font-weight: 600;
  color: #2d3748;
  margin-top: 0.25rem;
}

.gantt-row {
  display: grid;
  grid-template-columns: 200px 1fr;
  border-bottom: 1px solid #e2e8f0;
  min-height: 60px;
}

.gantt-row:hover {
  background: #f7fafc;
}

.category-header-row {
  display: grid;
  grid-template-columns: 200px 1fr;
  border-bottom: 2px solid #667eea;
  background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
  min-height: 50px;
  position: sticky;
  top: 0;
  z-index: 10;
}

.category-title {
  padding: 1rem;
  font-weight: 700;
  font-size: 1rem;
  color: #667eea;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.vehicle-row {
  display: grid;
  grid-template-columns: 200px 1fr;
  border-bottom: 1px solid #e2e8f0;
  min-height: 60px;
  background: white;
}

.vehicle-row:hover {
  background: #f7fafc;
}

.vehicle-cell {
  padding: 0.75rem 1rem;
  padding-left: 2rem;
  border-right: 2px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.25rem;
}

.vehicle-name {
  font-weight: 600;
  color: #2d3748;
  font-size: 0.9rem;
}

.vehicle-link {
  font-weight: 600;
  color: #667eea;
  font-size: 0.9rem;
  text-decoration: none;
  transition: color 0.2s;
}

.vehicle-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

.vehicle-details {
  font-size: 0.75rem;
  color: #718096;
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.vehicle-status {
  display: inline-block;
  padding: 0.125rem 0.5rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
}

.vehicle-status.available {
  background: #c6f6d5;
  color: #22543d;
}

.vehicle-status.reserved {
  background: #fef3c7;
  color: #92400e;
}

.vehicle-status.rented {
  background: #fed7d7;
  color: #742a2a;
}

.vehicle-status.maintenance {
  background: #e2e8f0;
  color: #4a5568;
}

.category-cell {
  padding: 1rem;
  border-right: 2px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.category-name {
  font-weight: 600;
  color: #2d3748;
  font-size: 1rem;
}

.category-count {
  font-size: 0.75rem;
  color: #718096;
  margin-top: 0.25rem;
}

.timeline {
  display: grid;
  grid-template-columns: repeat(14, 1fr);
  position: relative;
}

.timeline-cell {
  border-right: 1px solid #e2e8f0;
  padding: 0.5rem 0.25rem;
  position: relative;
  min-height: 60px;
}

.timeline-cell.weekend {
  background: #fafafa;
}

.timeline-cell.today {
  background: linear-gradient(180deg, rgba(254, 243, 199, 0.3) 0%, rgba(254, 243, 199, 0.3) 100%);
}

.reservation-bar {
  padding: 0.35rem 0.5rem;
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: all 0.2s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.reservation-bar:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
  z-index: 5;
}

.reservation-text {
  font-size: 0.7rem;
}

.legend {
  display: flex;
  gap: 2rem;
  justify-content: center;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #4a5568;
}

.legend-color {
  width: 20px;
  height: 12px;
  border-radius: 3px;
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
}

.modal-content.reservation-details {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.reservation-details h3 {
  margin: 0 0 1.5rem 0;
  color: #2d3748;
  font-size: 1.5rem;
}

.detail-row {
  padding: 0.75rem 0;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-row:last-of-type {
  border-bottom: none;
}

.detail-row strong {
  color: #4a5568;
  font-weight: 600;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
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

.btn-close {
  margin-top: 1.5rem;
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-close:hover {
  opacity: 0.9;
}
</style>
