// Variables específicas de inicio
let allCategories = [];

// Function to show error messages
function showError(message) {
  const errorContainer = document.getElementById("errorContainer")
  if (errorContainer) {
    errorContainer.textContent = message;
    errorContainer.style.display = "block";
  }
}

// Inicialización de la página de inicio
document.addEventListener("DOMContentLoaded", () => {
  initializeHomePage();
  setupHomeEventListeners();
});

async function initializeHomePage() {
  try {
    await loadCategories();
    await updateStats();
    displayFeaturedCategories();
  } catch (error) {
    console.error("Error al inicializar página de inicio:", error);
    showError("Error al cargar los datos iniciales");
  }
}

function setupHomeEventListeners() {
  // Búsqueda
  const searchBtn = document.getElementById("searchBtn");
  const searchInput = document.getElementById("searchInput");

  if (searchBtn) {
    searchBtn.addEventListener("click", handleSearch);
  }

  if (searchInput) {
    searchInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        handleSearch();
      }
    });
  }
}

// Actualizar estadísticas
async function updateStats() {
  try {
    // Cargar recetas para contar
    const response = await fetch(`${API_BASE_URL}/recetas/`)
    const recipes = await response.json()

    const totalRecipesEl = document.getElementById("totalRecipes")
    const totalCategoriesEl = document.getElementById("totalCategories")

    if (totalRecipesEl) {
      totalRecipesEl.textContent = Array.isArray(recipes) ? recipes.length : 0
    }

    if (totalCategoriesEl) {
      totalCategoriesEl.textContent = allCategories.length
    }
  } catch (error) {
    console.error("Error al actualizar estadísticas:", error)
  }
}

// Cargar categorías desde la API
async function loadCategories() {
  try {
    const response = await fetch(`${API_BASE_URL}/recetas/categorias`)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()

    if (Array.isArray(data)) {
      allCategories = data
    } else {
      console.error("Las categorías no son un array:", data)
    }
  } catch (error) {
    console.error("Error al cargar categorías:", error)
    showError("Error al cargar las categorías")
  }
}

// Mostrar categorías destacadas
function displayFeaturedCategories() {
  const categoriesGrid = document.getElementById("categoriesGrid");
  if (!categoriesGrid || allCategories.length === 0) return;

  categoriesGrid.innerHTML = allCategories
    .map(
      (category) => `
        <div class="category-card" onclick="filterByCategory(${category.id})">
            <div class="category-icon">
                <i class="${
                  category.icono ||
                  categoryIcons[category.nombre] ||
                  "fas fa-utensils"
                }"></i>
            </div>
            <div class="category-name">${category.nombre}</div>
            <div class="category-description">${
              category.descripcion || "Deliciosas recetas"
            }</div>
        </div>
    `
    )
    .join("");
}

// Filtrar por categoría (redirige a recetas)
function filterByCategory(categoryId) {
  localStorage.setItem("selectedCategory", categoryId);
  window.location.href = "recetas.html";
}

// Manejar búsqueda (redirige a recetas)
function handleSearch() {
  const searchInput = document.getElementById("searchInput");
  if (!searchInput) return;

  const searchTerm = searchInput.value.trim();
  if (searchTerm) {
    localStorage.setItem("searchTerm", searchTerm);
    window.location.href = "recetas.html";
  }
}

// Hacer funciones globales
window.filterByCategory = filterByCategory;
window.showError = showError; 