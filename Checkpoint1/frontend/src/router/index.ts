import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/vehicles",
      name: "vehicles",
      component: () => import("../views/VehiclesView.vue"),
    },
    {
      path: "/customers",
      name: "customers",
      component: () => import("../views/CustomersView.vue"),
    },
    {
      path: "/reservations",
      name: "reservations",
      component: () => import("../views/ReservationsView.vue"),
    },
    {
      path: "/vehicles/:id",
      name: "vehicle-details",
      component: () => import("../views/VehicleStatsView.vue"),
    },
  ],
});

export default router;
