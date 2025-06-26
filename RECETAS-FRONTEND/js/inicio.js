// Variables específicas de inicio
let allCategories = [];

// Function to show error messages
function showError(message) {
  const errorContainer = document.getElementById("errorContainer")
  if (errorContainer) {
    errorContainer.textContent = message;
    errorContainer.style.display = "block";
  }
} // Declare showError function here

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
    const response = await fetch(`${API_BASE_URL}/recetas.php`);
    const recipes = await response.json();

    const totalRecipesEl = document.getElementById("totalRecipes");
    const totalCategoriesEl = document.getElementById("totalCategories");

    if (totalRecipesEl) {
      totalRecipesEl.textContent = Array.isArray(recipes) ? recipes.length : 0;
    }

    if (totalCategoriesEl) {
      totalCategoriesEl.textContent = allCategories.length;
    }
  } catch (error) {
    console.error("Error al actualizar estadísticas:", error);
  }
}