<template>
  <div class="customers-view">
    <div class="header">
      <h1>Korisnici</h1>
      <button class="btn-primary" @click="showAddForm = true">Dodaj korisnika</button>
    </div>

    <div v-if="showAddForm" class="modal" @click.self="showAddForm = false">
      <div class="modal-content">
        <CustomerForm @submit="handleAddCustomer" @cancel="showAddForm = false" />
      </div>
    </div>

    <div v-if="showEditForm && editingCustomer" class="modal" @click.self="closeEditForm">
      <div class="modal-content">
        <CustomerForm
          :customer="editingCustomer"
          :edit-mode="true"
          @submit="handleEditCustomer"
          @cancel="closeEditForm"
        />
      </div>
    </div>

    <div v-if="loading" class="loading">Učitavanje korisnika...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="table-container">
      <table class="customers-table">
        <thead>
          <tr>
            <th>Ime i prezime</th>
            <th>Email</th>
            <th>Telefon</th>
            <th>OIB</th>
            <th>Vozačka dozvola</th>
            <th>Grad</th>
            <th>Akcije</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="customer in customers" :key="customer.id" class="customer-row">
            <td class="customer-name">{{ customer.first_name }} {{ customer.last_name }}</td>
            <td>{{ customer.email }}</td>
            <td>{{ customer.phone }}</td>
            <td class="oib">{{ customer.oib }}</td>
            <td class="license">{{ customer.drivers_license }}</td>
            <td>{{ customer.city || "-" }}</td>
            <td class="actions">
              <button class="btn-edit" @click="editCustomer(customer)">Uredi</button>
              <button class="btn-delete" @click="customer.id && deleteCustomer(customer.id)">
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
import { customerApi, type Customer } from "../services/api";
import CustomerForm from "../components/CustomerForm.vue";

const customers = ref<Customer[]>([]);
const loading = ref(false);
const error = ref("");
const showAddForm = ref(false);
const showEditForm = ref(false);
const editingCustomer = ref<Customer | null>(null);

const loadCustomers = async () => {
  loading.value = true;
  error.value = "";
  try {
    customers.value = await customerApi.getAll();
  } catch (err) {
    error.value = "Failed to load customers";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const handleAddCustomer = async (customer: Customer) => {
  try {
    await customerApi.create(customer);
    showAddForm.value = false;
    await loadCustomers();
  } catch (err) {
    error.value = "Failed to add customer";
    console.error(err);
  }
};

const editCustomer = (customer: Customer) => {
  editingCustomer.value = { ...customer };
  showEditForm.value = true;
};

const handleEditCustomer = async (customer: Customer) => {
  if (!editingCustomer.value?.id) return;

  try {
    await customerApi.update(editingCustomer.value.id, customer);
    showEditForm.value = false;
    editingCustomer.value = null;
    await loadCustomers();
  } catch (err) {
    error.value = "Failed to update customer";
    console.error(err);
  }
};

const closeEditForm = () => {
  showEditForm.value = false;
  editingCustomer.value = null;
};

const deleteCustomer = async (id: number) => {
  if (confirm("Jeste li sigurni da želite obrisati ovog korisnika?")) {
    try {
      await customerApi.delete(id);
      await loadCustomers();
    } catch (err) {
      error.value = "Failed to delete customer";
      console.error(err);
    }
  }
};

onMounted(() => {
  loadCustomers();
});
</script>

<style scoped>
.customers-view {
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
}

.modal-content {
  width: auto;
  max-height: 90vh;
  overflow-y: auto;
}

.loading,
.error {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
  color: white;
}

.error {
  color: #ff6b6b;
}

.table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
}

.customers-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.customers-table thead {
  background-color: #f8f9fa;
  border-bottom: 2px solid #dee2e6;
}

.customers-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #495057;
  white-space: nowrap;
}

.customers-table tbody tr {
  border-bottom: 1px solid #dee2e6;
  transition: background-color 0.2s;
}

.customers-table tbody tr:hover {
  background-color: #f8f9fa;
}

.customers-table td {
  padding: 1rem;
}

.customer-name {
  font-weight: 500;
  color: #2c3e50;
}

.oib,
.license {
  font-family: monospace;
  font-size: 0.9rem;
  color: #495057;
}

.actions {
  display: flex;
  gap: 0.5rem;
  white-space: nowrap;
}

.btn-edit,
.btn-delete {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-edit {
  background: #3498db;
  color: white;
}

.btn-edit:hover {
  background: #2980b9;
}

.btn-delete {
  background: #e74c3c;
  color: white;
}

.btn-delete:hover {
  background: #c0392b;
}
</style>
