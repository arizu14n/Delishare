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
  // Filtros
  const categoryFilter = document.getElementById("categoryFilter")
  const difficultyFilter = document.getElementById("difficultyFilter")
  const typeFilter = document.getElementById("typeFilter")

  if (categoryFilter) {
    categoryFilter.addEventListener("change", applyFilters)
  }

  if (difficultyFilter) {
    difficultyFilter.addEventListener("change", applyFilters)
  }

  if (typeFilter) {
    typeFilter.addEventListener("change", applyFilters)
  }

  // Formulario de añadir receta
  const addRecipeForm = document.getElementById("addRecipeForm")
  if (addRecipeForm) {
    addRecipeForm.addEventListener("submit", submitNewRecipe)
  }
}

// Verificar filtros guardados desde otras páginas
function checkSavedFilters() {
  const selectedCategory = localStorage.getItem("selectedCategory")
  const searchTerm = localStorage.getItem("searchTerm")

  if (selectedCategory) {
    const categoryFilter = document.getElementById("categoryFilter")
    if (categoryFilter) {
      categoryFilter.value = selectedCategory
      applyFilters()
    }
    localStorage.removeItem("selectedCategory")
  }

  if (searchTerm) {
    const searchInput = document.getElementById("searchInput")
    if (searchInput) {
      searchInput.value = searchTerm
      handleSearch()
    }
    localStorage.removeItem("searchTerm")
  }
}

// Poblar select de categorías para filtros
function populateCategorySelects() {
  const categoryFilter = document.getElementById("categoryFilter")

  if (!categoryFilter) return

  categoryFilter.innerHTML = '<option value="">Todas las categorías</option>'

  allCategories.forEach((category) => {
    const option = new Option(category.nombre, category.id)
    categoryFilter.appendChild(option)
  })
}