// Variables específicas de recetas
let allRecipes = []
let allCategories = []
let filteredRecipes = []

// Function to show error messages
function showError(message) {
  const errorContainer = document.getElementById("errorContainer")
  if (errorContainer) {
    errorContainer.innerHTML = `<div class="error-message">${message}</div>`
  }
}

// Inicialización de la página de recetas
document.addEventListener("DOMContentLoaded", () => {
  initializeRecipesPage()
  setupRecipesEventListeners()
})

async function initializeRecipesPage() {
  try {
    await loadCategories() 
    await loadRecipes() 

    // Verificar si hay filtros guardados
    checkSavedFilters()
  } catch (error) {
    console.error("Error al inicializar página de recetas:", error)
    showError("Error al cargar los datos")
  }
}

function setupRecipesEventListeners() {
  // Búsqueda
  const searchBtn = document.getElementById("searchBtn")
  const searchInput = document.getElementById("searchInput")

  if (searchBtn) {
    searchBtn.addEventListener("click", handleSearch)
  }

  if (searchInput) {
    searchInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        handleSearch()
      }
    })
  }