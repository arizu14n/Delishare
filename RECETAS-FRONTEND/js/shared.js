// Configuración de la API
const API_BASE_URL = "http://localhost/prueba/recetas-api/api/endpoints"

// Variables globales compartidas
let currentUser = null

// Iconos para categorías
const categoryIcons = {
  Desayunos: "fas fa-coffee",
  Almuerzos: "fas fa-hamburger",
  Cenas: "fas fa-moon",
  Postres: "fas fa-ice-cream",
  Bebidas: "fas fa-glass-cheers",
  Aperitivos: "fas fa-cheese",
  Vegetarianas: "fas fa-leaf",
  Veganas: "fas fa-seedling",
}

// Inicialización común
document.addEventListener("DOMContentLoaded", () => {
  checkUserSession()
})