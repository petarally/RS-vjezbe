<template>
  <div class="customer-form">
    <h2>{{ editMode ? "Uredi korisnika" : "Dodaj novog korisnika" }}</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-row">
        <div class="form-group">
          <label for="first_name">Ime *</label>
          <input id="first_name" v-model="customer.first_name" type="text" required />
        </div>

        <div class="form-group">
          <label for="last_name">Prezime *</label>
          <input id="last_name" v-model="customer.last_name" type="text" required />
        </div>
      </div>

      <div class="form-group">
        <label for="email">Email *</label>
        <input id="email" v-model="customer.email" type="email" required />
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="phone">Telefon *</label>
          <input
            id="phone"
            v-model="customer.phone"
            type="tel"
            placeholder="npr. +385 91 234 5678"
            required
          />
        </div>

        <div class="form-group">
          <label for="oib">OIB *</label>
          <input
            id="oib"
            v-model="customer.oib"
            type="text"
            maxlength="11"
            pattern="[0-9]{11}"
            placeholder="11 digits"
            required
          />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="drivers_license">Driver's License *</label>
          <input id="drivers_license" v-model="customer.drivers_license" type="text" required />
        </div>

        <div class="form-group">
          <label for="city">City</label>
          <input id="city" v-model="customer.city" type="text" />
        </div>
      </div>

      <div class="form-actions">
        <button type="button" class="btn-secondary" @click="$emit('cancel')">Cancel</button>
        <button type="submit" class="btn-primary">
          {{ editMode ? "Update" : "Add" }} Customer
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import type { Customer } from "../services/api";

const props = defineProps<{
  customer?: Customer;
  editMode?: boolean;
}>();

const emit = defineEmits<{
  submit: [customer: Customer];
  cancel: [];
}>();

const customer = ref<Customer>({
  first_name: props.customer?.first_name || "",
  last_name: props.customer?.last_name || "",
  email: props.customer?.email || "",
  phone: props.customer?.phone || "",
  oib: props.customer?.oib || "",
  drivers_license: props.customer?.drivers_license || "",
  city: props.customer?.city || "",
});

const handleSubmit = () => {
  emit("submit", customer.value);
};
</script>

<style scoped>
.customer-form {
  max-width: 950px;
  margin: 0 auto;
  padding: 0;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

h2 {
  margin: 0;
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
}

form {
  padding: 2rem 2.5rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.25rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #4a5568;
  font-size: 0.875rem;
  letter-spacing: 0.3px;
}

input {
  width: 100%;
  padding: 0.7rem 0.875rem;
  border: 1.5px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  background: white;
  color: #2d3748;
}

input:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.08);
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
}

button {
  padding: 0.65rem 1.75rem;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
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
