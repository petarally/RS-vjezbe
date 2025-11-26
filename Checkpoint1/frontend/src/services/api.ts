const API_BASE_URL = "http://localhost:8000/api";

export interface Vehicle {
  id?: number;
  brand: string;
  model: string;
  year: number;
  category: string;
  registration_number: string;
  daily_rate: number;
  mileage?: number;
  status?: string;
  fuel_type?: string;
  transmission?: string;
  seats?: number;
  // Registration & Compliance
  registration_expiry?: string | null;
  last_inspection_date?: string | null;
  next_inspection_due?: string | null;
  // Insurance
  insurance_company?: string | null;
  insurance_policy_number?: string | null;
  insurance_expiry?: string | null;
  insurance_premium?: number | null;
  // Ownership/Leasing
  ownership_type?: string | null;
  lease_company?: string | null;
  lease_start_date?: string | null;
  lease_end_date?: string | null;
  lease_monthly_payment?: number | null;
  // Maintenance
  last_service_date?: string | null;
  next_service_due?: string | null;
  service_interval_km?: number | null;
}

export interface Customer {
  id?: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  oib: string;
  drivers_license: string;
  city?: string;
}

export interface Reservation {
  id?: number;
  vehicle_id?: number;
  customer_id: number;
  category: string;
  preferred_car_model?: string;
  start_date: string;
  end_date: string;
  total_price?: number;
  status?: string;
}

export interface DamageReport {
  id?: number;
  vehicle_id: number;
  reservation_id?: number | null;
  report_date: string;
  description: string;
  severity: string;
  repair_cost?: number | null;
  repaired: boolean;
  repair_date?: string | null;
  notes?: string | null;
}

export interface MaintenanceRecord {
  id?: number;
  vehicle_id: number;
  service_date: string;
  service_type: string;
  mileage_at_service?: number | null;
  cost?: number | null;
  performed_by?: string | null;
  description?: string | null;
  next_service_km?: number | null;
}

export interface CarMakesResponse {
  count: number;
  results: string[];
}

export interface CarModelsResponse {
  make: string;
  count: number;
  results: string[];
}

// Vehicle API
export const vehicleApi = {
  async getAll(): Promise<Vehicle[]> {
    const response = await fetch(`${API_BASE_URL}/vehicles`);
    if (!response.ok) throw new Error("Failed to fetch vehicles");
    return response.json();
  },

  async getById(id: number): Promise<Vehicle> {
    const response = await fetch(`${API_BASE_URL}/vehicles/${id}`);
    if (!response.ok) throw new Error("Failed to fetch vehicle");
    return response.json();
  },

  async create(vehicle: Vehicle): Promise<Vehicle> {
    const response = await fetch(`${API_BASE_URL}/vehicles`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(vehicle),
    });
    if (!response.ok) throw new Error("Failed to create vehicle");
    return response.json();
  },

  async update(id: number, vehicle: Vehicle): Promise<Vehicle> {
    const response = await fetch(`${API_BASE_URL}/vehicles/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(vehicle),
    });
    if (!response.ok) throw new Error("Failed to update vehicle");
    return response.json();
  },

  async delete(id: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/vehicles/${id}`, {
      method: "DELETE",
    });
    if (!response.ok) throw new Error("Failed to delete vehicle");
  },

  async checkAvailability(id: number, startDate: string, endDate: string): Promise<boolean> {
    const response = await fetch(
      `${API_BASE_URL}/vehicles/${id}/availability?start_date=${startDate}&end_date=${endDate}`
    );
    if (!response.ok) throw new Error("Failed to check availability");
    const data = await response.json();
    return data.available;
  },
};

// Customer API
export const customerApi = {
  async getAll(): Promise<Customer[]> {
    const response = await fetch(`${API_BASE_URL}/customers`);
    if (!response.ok) throw new Error("Failed to fetch customers");
    return response.json();
  },

  async getById(id: number): Promise<Customer> {
    const response = await fetch(`${API_BASE_URL}/customers/${id}`);
    if (!response.ok) throw new Error("Failed to fetch customer");
    return response.json();
  },

  async create(customer: Customer): Promise<Customer> {
    const response = await fetch(`${API_BASE_URL}/customers`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(customer),
    });
    if (!response.ok) throw new Error("Failed to create customer");
    return response.json();
  },

  async update(id: number, customer: Customer): Promise<Customer> {
    const response = await fetch(`${API_BASE_URL}/customers/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(customer),
    });
    if (!response.ok) throw new Error("Failed to update customer");
    return response.json();
  },

  async delete(id: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/customers/${id}`, {
      method: "DELETE",
    });
    if (!response.ok) throw new Error("Failed to delete customer");
  },
};

// Reservation API
export const reservationApi = {
  async getAll(): Promise<Reservation[]> {
    const response = await fetch(`${API_BASE_URL}/reservations`);
    if (!response.ok) throw new Error("Failed to fetch reservations");
    return response.json();
  },

  async getById(id: number): Promise<Reservation> {
    const response = await fetch(`${API_BASE_URL}/reservations/${id}`);
    if (!response.ok) throw new Error("Failed to fetch reservation");
    return response.json();
  },

  async create(reservation: Reservation): Promise<Reservation> {
    const response = await fetch(`${API_BASE_URL}/reservations`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(reservation),
    });
    if (!response.ok) throw new Error("Failed to create reservation");
    return response.json();
  },

  async update(id: number, reservation: Reservation): Promise<Reservation> {
    const response = await fetch(`${API_BASE_URL}/reservations/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(reservation),
    });
    if (!response.ok) throw new Error("Failed to update reservation");
    return response.json();
  },

  async delete(id: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/reservations/${id}`, {
      method: "DELETE",
    });
    if (!response.ok) throw new Error("Failed to delete reservation");
  },
};

// Car Makes and Models Autocomplete API
export const carAutocompleteApi = {
  async getMakes(query?: string): Promise<string[]> {
    const url = query
      ? `${API_BASE_URL}/car-makes?q=${encodeURIComponent(query)}`
      : `${API_BASE_URL}/car-makes`;

    const response = await fetch(url);
    if (!response.ok) throw new Error("Failed to fetch car makes");
    const data: CarMakesResponse = await response.json();
    return data.results;
  },

  async getModels(make: string, query?: string): Promise<string[]> {
    const url = query
      ? `${API_BASE_URL}/car-makes/${encodeURIComponent(make)}/models?q=${encodeURIComponent(
          query
        )}`
      : `${API_BASE_URL}/car-makes/${encodeURIComponent(make)}/models`;

    const response = await fetch(url);
    if (!response.ok) throw new Error("Failed to fetch car models");
    const data: CarModelsResponse = await response.json();
    return data.results;
  },
};
