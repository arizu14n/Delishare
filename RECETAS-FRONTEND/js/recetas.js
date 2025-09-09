// Variables específicas de recetas
let allRecipes = []
let allCategories = []
let filteredRecipes = []

// Variables para gestionar ingredientes e instrucciones
let ingredientsArray = [];
let instructionsArray = [];
let editingIngredientIndex = -1;
let editingInstructionIndex = -1;

// Function to show error messages
function showError(message) {
  const errorContainer = document.getElementById("errorContainer")
  if (errorContainer) {
    errorContainer.innerHTML = `<div class="error-message">${message}</div>`
  }
}

// Inicialización de la página de recetas
document.addEventListener("DOMContentLoaded", () => {
    initializeRecipesPage();
    setupRecipesEventListeners();
    setupStepByStepInputs(); // Añadir esta línea
    
    // Cancelar edición al hacer clic en el botón de cerrar
    const closeButtons = document.querySelectorAll('.close');
    closeButtons.forEach(button => {
        button.addEventListener('click', cancelEditing);
    });
});

// Hacer funciones globales
window.removeIngredient = removeIngredient;
window.removeInstruction = removeInstruction;
window.editIngredient = editIngredient;
window.editInstruction = editInstruction;

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

  // Validación en tiempo real para campos numéricos
  const recipePrepTimeInput = document.getElementById("recipePrepTime");
  const recipeServingsInput = document.getElementById("recipeServings");

  const validateNumericInput = (event, maxValue) => {
    let value = event.target.value.replace(/[^0-9]/g, '');
    if (value) {
      let numericValue = parseInt(value, 10);
      if (numericValue > maxValue) {
        value = maxValue.toString();
      }
    }
    event.target.value = value;
  };

  if (recipePrepTimeInput) {
    recipePrepTimeInput.addEventListener('input', (e) => {
      validateNumericInput(e, 240);
    });
  }

  if (recipeServingsInput) {
    recipeServingsInput.addEventListener('input', (e) => {
      validateNumericInput(e, 20);
    });
  }
}

// Aplicar filtros
function applyFilters() {
  const categoryFilter = document.getElementById("categoryFilter")
  const difficultyFilter = document.getElementById("difficultyFilter")
  const typeFilter = document.getElementById("typeFilter")

  if (!categoryFilter || !difficultyFilter || !typeFilter) return

  const categoryValue = categoryFilter.value
  const difficultyValue = difficultyFilter.value
  const typeValue = typeFilter.value

  let filtered = [...allRecipes]

  if (categoryValue) {
    filtered = filtered.filter((recipe) => recipe.categoria_id == categoryValue)
  }

  if (difficultyValue) {
    filtered = filtered.filter((recipe) => recipe.dificultad === difficultyValue)
  }

  if (typeValue === "gratuitas") {
    filtered = filtered.filter((recipe) => !recipe.es_premium)
  } else if (typeValue === "premium") {
    filtered = filtered.filter((recipe) => recipe.es_premium)
  }

  displayRecipes(filtered)
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

// Cargar categorías
async function loadCategories() {
  try {
    const response = await fetch(`${API_BASE_URL}/recetas/categorias`)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()

    if (Array.isArray(data)) {
      allCategories = data
      populateCategorySelects()
      populateAddRecipeCategorySelect() 
    }
  } catch (error) {
    console.error("Error al cargar categorías:", error)
    showError("Error al cargar las categorías")
  }
}

// Poblar select de categorías para el formulario de añadir receta
function populateAddRecipeCategorySelect() {
  const recipeCategorySelect = document.getElementById("recipeCategory")
  if (!recipeCategorySelect) return

  recipeCategorySelect.innerHTML = "" // Limpiar opciones existentes

  allCategories.forEach((category) => {
    const option = new Option(category.nombre, category.id)
    recipeCategorySelect.appendChild(option)
  })
}

// Cargar recetas
async function loadRecipes() {
  try {
    showLoading()

    const response = await fetch(`${API_BASE_URL}/recetas/`)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()

    if (Array.isArray(data)) {
      allRecipes = data
      filteredRecipes = [...data]
      displayRecipes(allRecipes)
    } else {
      displayRecipes([])
    }
  } catch (error) {
    console.error("Error al cargar recetas:", error)
    showError("Error al cargar las recetas")
  }
}

// Mostrar loading
function showLoading() {
  const recipesGrid = document.getElementById("recipesGrid")
  if (recipesGrid) {
    recipesGrid.innerHTML = `
            <div class="loading">
                Cargando recetas...
            </div>
        `
  }
}

// Mostrar recetas
function displayRecipes(recipes) {
  const recipesGrid = document.getElementById("recipesGrid")

  if (!recipesGrid) return

  let recipesHtml = ""

  // Add "Add Recipe" card if user is premium
  if (currentUser && currentUser.tipo_suscripcion === "premium" && currentUser.suscripcion_activa) {
    recipesHtml += `
            <div class="recipe-card add-recipe-card" onclick="openAddRecipeModal()">
                <div class="recipe-image">
                    <i class="fas fa-plus"></i>
                </div>
                <div class="recipe-content">
                    <h3 class="recipe-title">Agregar Nueva Receta</h3>
                    <p class="recipe-description">Comparte tu creación culinaria con la comunidad.</p>
                </div>
            </div>
        `
  }

  if (recipes.length === 0 && (!currentUser || !currentUser.suscripcion_activa)) { // Modificado para usuarios no premium
    recipesGrid.innerHTML = `
            <div class="no-recipes">
                <i class="fas fa-utensils" style="font-size: 3rem; color: var(--gray-dark); margin-bottom: 1rem;"></i>
                <p>No se encontraron recetas</p>
            </div>
        `
    return
  }
  // Si no hay recetas pero el usuario es premium, solo muestra el botón de añadir receta
  if (recipes.length === 0 && currentUser && currentUser.tipo_suscripcion === "premium" && currentUser.suscripcion_activa) {
    recipesGrid.innerHTML = recipesHtml; // Solo el botón de agregar
    return;
  }


  recipesHtml += recipes
    .map(
      (recipe) => `
        <div class="recipe-card ${recipe.es_premium ? "premium" : ""}" onclick="showRecipeDetails(${recipe.id})">
            <div class="recipe-image">
                ${recipe.imagen_url ? `<img src="${DOMPurify.sanitize(recipe.imagen_url)}" alt="${DOMPurify.sanitize(recipe.titulo)}">` : `<i class="fas fa-utensils"></i>`}
            </div>
            <div class="recipe-content">
                <h3 class="recipe-title">${DOMPurify.sanitize(recipe.titulo)}</h3>
                <p class="recipe-description">${DOMPurify.sanitize(recipe.descripcion || "Sin descripción")}</p>
                <div class="recipe-meta">
                    <span><i class="fas fa-clock"></i> ${DOMPurify.sanitize(recipe.tiempo_preparacion || "N/A")} min</span>
                    <span><i class="fas fa-users"></i> ${DOMPurify.sanitize(recipe.porciones || "N/A")} porciones</span>
                </div>
                <div class="recipe-meta" style="margin-top: 0.5rem;">
                    <span class="recipe-difficulty difficulty-${(recipe.dificultad || "fácil").toLowerCase()}">
                        ${DOMPurify.sanitize(recipe.dificultad || "Fácil")}
                    </span>
                    <span><i class="fas fa-user"></i> ${DOMPurify.sanitize(recipe.autor || "Anónimo")}</span>
                </div>
            </div>
        </div>
    `,
    )
    .join("")

    recipesGrid.innerHTML = recipesHtml
}

// Procesar instrucciones para mostrar pasos limitados
function processInstructions(instructions, isPremium, userHasPremium) {
  const steps = instructions.split("\n").filter((step) => step.trim() !== "")

  if (!isPremium || userHasPremium) {
    // Mostrar todos los pasos
    return steps
      .map(
        (step, index) =>
          `<div class="instruction-step">
                <span class="step-number">${index + 1}</span>
                <span class="step-text">${DOMPurify.sanitize(step)}</span>
            </div>`,
      )
      .join("")
  } else {
    // Mostrar solo los primeros 2 pasos
    const visibleSteps = steps.slice(0, 2)
    const hiddenStepsCount = steps.length - 2

    let html = visibleSteps
      .map(
        (step, index) =>
          `<div class="instruction-step">
                <span class="step-number">${index + 1}</span>
                <span class="step-text">${DOMPurify.sanitize(step)}</span>
            </div>`,
      )
      .join("")

    if (hiddenStepsCount > 0) {
      html += `<div class="hidden-steps-notice">
                <i class="fas fa-lock"></i>
                <span>+${hiddenStepsCount} pasos más disponibles con suscripción Premium</span>
            </div>`
    }

    return html
  }
}

// Mostrar detalles de receta
async function showRecipeDetails(recipeId) {
  try {
    const response = await fetch(`${API_BASE_URL}/recetas/${recipeId}`)
    const recipe = await response.json()

    if (recipe.message) {
      showError("Receta no encontrada")
      return
    }

    const modalContent = document.getElementById("modalContent")
    if (!modalContent) return

    // Verificar permisos del usuario
    const userHasPremium = currentUser && currentUser.tipo_suscripcion === "premium" && currentUser.suscripcion_activa
    const canViewFullRecipe = !recipe.es_premium || userHasPremium

    modalContent.innerHTML = `
            <h2 class="modal-recipe-title">${DOMPurify.sanitize(recipe.titulo)}</h2>
            
            <div class="modal-recipe-meta">
                <div class="meta-item">
                    <span class="meta-label">Tiempo</span>
                    <span class="meta-value">${DOMPurify.sanitize(recipe.tiempo_preparacion || "N/A")} min</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Porciones</span>
                    <span class="meta-value">${DOMPurify.sanitize(recipe.porciones || "N/A")}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Dificultad</span>
                    <span class="meta-value">${DOMPurify.sanitize(recipe.dificultad || "Fácil")}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Autor</span>
                    <span class="meta-value">${DOMPurify.sanitize(recipe.autor || "Anónimo")}</span>
                </div>
            </div>
            
            ${recipe.descripcion ? `<p style="margin-bottom: 2rem; font-style: italic; color: var(--gray-dark);">${DOMPurify.sanitize(recipe.descripcion)}</p>` : ""}
            
            <div class="modal-section">
                <h3><i class="fas fa-list"></i> Ingredientes</h3>
                <div class="ingredients-list">${DOMPurify.sanitize(recipe.ingredientes)}</div>
            </div>
            
            <div class="modal-section">
                <h3><i class="fas fa-clipboard-list"></i> Preparación Paso a Paso</h3>
                <div class="instructions-container">
                    ${processInstructions(recipe.instrucciones, recipe.es_premium, userHasPremium)}
                </div>
                ${ 
                  !canViewFullRecipe
                    ? `
                    <div class="premium-preview">
                        <h4><i class="fas fa-crown"></i> Contenido Premium</h4>
                        <p>Esta receta requiere suscripción premium para ver todos los pasos de preparación.</p>
                        <div class="premium-actions">
                            <button class="btn-premium" onclick="closeModal('recipeModal'); window.location.href='suscripcion.html'">
                                <i class="fas fa-crown"></i> Ver Planes Premium
                            </button>
                            ${
                              !currentUser
                                ? `
                                <button class="btn-secondary" onclick="closeModal('recipeModal'); window.location.href='login.html'">
                                    <i class="fas fa-user"></i> Iniciar Sesión
                                </button>
                            `
                                : ""
                            }
                        </div>
                    </div>
                `
                    : ""
                }
            </div>
        `

    document.getElementById("recipeModal").style.display = "block"
  } catch (error) {
    console.error("Error al cargar detalles de la receta:", error)
    showError("Error al cargar los detalles de la receta")
  }
}

// Manejar búsqueda
async function handleSearch() {
  const searchInput = document.getElementById("searchInput")
  if (!searchInput) return

  const searchTerm = searchInput.value.trim()

  try {
    showLoading()

    const response = await fetch(`${API_BASE_URL}/recetas/?search=${encodeURIComponent(searchTerm)}`)
    const data = await response.json()

    if (Array.isArray(data)) {
      allRecipes = data
      filteredRecipes = [...data]
      displayRecipes(data)
    } else {
      displayRecipes([])
    }
  } catch (error) {
    console.error("Error en la búsqueda:", error)
    showError("Error al realizar la búsqueda")
  }
}

// Abrir modal para añadir nueva receta
function openAddRecipeModal() {
    if (currentUser && currentUser.tipo_suscripcion === "premium" && currentUser.suscripcion_activa) {
        document.getElementById("addRecipeModal").style.display = "block";
        document.getElementById("addRecipeForm").reset();
        populateAddRecipeCategorySelect();
        resetStepByStepInputs(); // Resetear las listas
        
        const recipeAuthorInput = document.getElementById("recipeAuthor");
        const recipeIsPremiumCheckbox = document.getElementById("recipeIsPremium");

        if (recipeAuthorInput && currentUser && currentUser.nombre) {
            recipeAuthorInput.value = currentUser.nombre;
        }

        if (recipeIsPremiumCheckbox && currentUser && currentUser.tipo_suscripcion === "premium" && currentUser.suscripcion_activa) {
            recipeIsPremiumCheckbox.checked = true;
        } else {
            recipeIsPremiumCheckbox.checked = false;
        }
    } else {
        showError("Debes ser usuario Premium para agregar recetas.");
    }
}

// Cerrar modal para añadir nueva receta
function closeAddRecipeModal() {
  document.getElementById("addRecipeModal").style.display = "none"
}

// Configurar event listeners para ingredientes e instrucciones
function setupStepByStepInputs() {
    const addIngredientBtn = document.getElementById("addIngredientBtn");
    const addInstructionBtn = document.getElementById("addInstructionBtn");
    const ingredientInput = document.getElementById("ingredientInput");
    const instructionInput = document.getElementById("instructionInput");
    
    if (addIngredientBtn && ingredientInput) {
        addIngredientBtn.addEventListener("click", addIngredient);
        ingredientInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                addIngredient();
            }
        });
    }
    
    if (addInstructionBtn && instructionInput) {
        addInstructionBtn.addEventListener("click", addInstruction);
        instructionInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                addInstruction();
            }
        });
    }
}

// Añadir ingrediente a la lista
function addIngredient() {
    const ingredientInput = document.getElementById("ingredientInput");
    const addIngredientBtn = document.getElementById("addIngredientBtn");
    const ingredient = DOMPurify.sanitize(ingredientInput.value.trim());
    
    if (!ingredient) return;
    
    if (editingIngredientIndex >= 0) {
        // Modo edición
        ingredientsArray[editingIngredientIndex] = ingredient;
        editingIngredientIndex = -1;
        addIngredientBtn.innerHTML = '<i class="fas fa-plus"></i> Agregar';
    } else {
        // Modo agregar
        ingredientsArray.push(ingredient);
    }
    
    updateIngredientsList();
    ingredientInput.value = "";
    ingredientInput.focus();
}

// Añadir instrucción a la lista
function addInstruction() {
    const instructionInput = document.getElementById("instructionInput");
    const addInstructionBtn = document.getElementById("addInstructionBtn");
    const instruction = DOMPurify.sanitize(instructionInput.value.trim());
    
    if (!instruction) return;
    
    if (editingInstructionIndex >= 0) {
        // Modo edición
        instructionsArray[editingInstructionIndex] = instruction;
        editingInstructionIndex = -1;
        addInstructionBtn.innerHTML = '<i class="fas fa-plus"></i> Agregar';
    } else {
        // Modo agregar
        instructionsArray.push(instruction);
    }
    
    updateInstructionsList();
    instructionInput.value = "";
    instructionInput.focus();
}

// Actualizar lista visual de ingredientes
function updateIngredientsList() {
    const ingredientsList = document.getElementById("ingredientsList");
    const recipeIngredients = document.getElementById("recipeIngredients");
    
    if (!ingredientsList) return;
    
    ingredientsList.innerHTML = ingredientsArray.map((ingredient, index) => `
        <div class="list-item">
            <span class="item-number">${index + 1}.</span>
            <span class="item-text">${ingredient}</span>
            <div class="item-actions">
                <button type="button" class="btn-edit-item" onclick="editIngredient(${index})">
                    <i class="fas fa-edit"></i>
                </button>
                <button type="button" class="btn-remove-item" onclick="removeIngredient(${index})">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
    `).join("");
    
    // Actualizar campo oculto con todos los ingredientes unidos por saltos de línea
    if (recipeIngredients) {
        recipeIngredients.value = ingredientsArray.join("\n");
    }
}

// Actualizar lista visual de instrucciones
function updateInstructionsList() {
    const instructionsList = document.getElementById("instructionsList");
    const recipeInstructions = document.getElementById("recipeInstructions");
    
    if (!instructionsList) return;
    
    instructionsList.innerHTML = instructionsArray.map((instruction, index) => `
        <div class="list-item">
            <span class="item-number">Paso ${index + 1}:</span>
            <span class="item-text">${instruction}</span>
            <div class="item-actions">
                <button type="button" class="btn-edit-item" onclick="editInstruction(${index})">
                    <i class="fas fa-edit"></i>
                </button>
                <button type="button" class="btn-remove-item" onclick="removeInstruction(${index})">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
    `).join("");
    
    // Actualizar campo oculto con todas las instrucciones unidas por saltos de línea
    if (recipeInstructions) {
        recipeInstructions.value = instructionsArray.join("\n");
    }
}

// Editar ingrediente
function editIngredient(index) {
    const ingredientInput = document.getElementById("ingredientInput");
    const addIngredientBtn = document.getElementById("addIngredientBtn");
    
    ingredientInput.value = ingredientsArray[index];
    editingIngredientIndex = index;
    addIngredientBtn.innerHTML = '<i class="fas fa-save"></i> Guardar';
    ingredientInput.focus();
}

// Editar instrucción
function editInstruction(index) {
    const instructionInput = document.getElementById("instructionInput");
    const addInstructionBtn = document.getElementById("addInstructionBtn");
    
    instructionInput.value = instructionsArray[index];
    editingInstructionIndex = index;
    addInstructionBtn.innerHTML = '<i class="fas fa-save"></i> Guardar';
    instructionInput.focus();
}

// Eliminar ingrediente
function removeIngredient(index) {
    ingredientsArray.splice(index, 1);
    
    // Si estábamos editando y eliminamos el elemento editado, cancelar edición
    if (editingIngredientIndex === index) {
        editingIngredientIndex = -1;
        const addIngredientBtn = document.getElementById("addIngredientBtn");
        const ingredientInput = document.getElementById("ingredientInput");
        
        addIngredientBtn.innerHTML = '<i class="fas fa-plus"></i> Agregar';
        ingredientInput.value = "";
    }
    
    updateIngredientsList();
}

// Eliminar instrucción
function removeInstruction(index) {
    instructionsArray.splice(index, 1);
    
    // Si estábamos editando y eliminamos el elemento editado, cancelar edición
    if (editingInstructionIndex === index) {
        editingInstructionIndex = -1;
        const addInstructionBtn = document.getElementById("addInstructionBtn");
        const instructionInput = document.getElementById("instructionInput");
        
        addInstructionBtn.innerHTML = '<i class="fas fa-plus"></i> Agregar';
        instructionInput.value = "";
    }
    
    updateInstructionsList();
}

// Limpiar listas al abrir el modal
function resetStepByStepInputs() {
    ingredientsArray = [];
    instructionsArray = [];
    editingIngredientIndex = -1;
    editingInstructionIndex = -1;
    
    updateIngredientsList();
    updateInstructionsList();
    
    const ingredientInput = document.getElementById("ingredientInput");
    const instructionInput = document.getElementById("instructionInput");
    const addIngredientBtn = document.getElementById("addIngredientBtn");
    const addInstructionBtn = document.getElementById("addInstructionBtn");
    
    if (ingredientInput) ingredientInput.value = "";
    if (instructionInput) instructionInput.value = "";
    if (addIngredientBtn) addIngredientBtn.innerHTML = '<i class="fas fa-plus"></i> Agregar';
    if (addInstructionBtn) addInstructionBtn.innerHTML = '<i class="fas fa-plus"></i> Agregar';
}

// Cancelar edición si se hace clic fuera o se cierra el modal
function cancelEditing() {
    const addIngredientBtn = document.getElementById("addIngredientBtn");
    const addInstructionBtn = document.getElementById("addInstructionBtn");
    const ingredientInput = document.getElementById("ingredientInput");
    const instructionInput = document.getElementById("instructionInput");
    
    if (editingIngredientIndex >= 0) {
        editingIngredientIndex = -1;
        addIngredientBtn.innerHTML = '<i class="fas fa-plus"></i> Agregar';
        ingredientInput.value = "";
    }
    
    if (editingInstructionIndex >= 0) {
        editingInstructionIndex = -1;
        addInstructionBtn.innerHTML = '<i class="fas fa-plus"></i> Agregar';
        instructionInput.value = "";
    }
}


// Enviar nueva receta
async function submitNewRecipe(event) {
  event.preventDefault()

  const recipeTitle = DOMPurify.sanitize(document.getElementById("recipeTitle").value.trim());
  const recipeDescription = DOMPurify.sanitize(document.getElementById("recipeDescription").value.trim());
  const recipeIngredients = DOMPurify.sanitize(document.getElementById("recipeIngredients").value.trim());
const recipeInstructions = DOMPurify.sanitize(document.getElementById("recipeInstructions").value.trim());
  const recipePrepTime = DOMPurify.sanitize(document.getElementById("recipePrepTime").value.trim());
  const recipeServings = DOMPurify.sanitize(document.getElementById("recipeServings").value.trim());
  const recipeDifficulty = DOMPurify.sanitize(document.getElementById("recipeDifficulty").value);
  const recipeCategory = DOMPurify.sanitize(document.getElementById("recipeCategory").value);
  const recipeImageUrl = DOMPurify.sanitize(document.getElementById("recipeImageUrl").value.trim());
  const recipeAuthor = DOMPurify.sanitize(document.getElementById("recipeAuthor").value.trim());
  const recipeIsPremium = document.getElementById("recipeIsPremium").checked;

  if (!recipeTitle || !recipeIngredients || !recipeInstructions || !recipePrepTime || !recipeServings || !recipeAuthor) {
    showError("Por favor, completa todos los campos obligatorios.")
    return
  }

  // Validación para tiempo_preparacion
  if (!/^\d+$/.test(recipePrepTime) || parseInt(recipePrepTime, 10) <= 0) {
    showError("El tiempo de preparación debe ser un número entero positivo.");
    return;
  }
  if (parseInt(recipePrepTime, 10) > 240) {
    showError("El tiempo de preparación no puede ser mayor a 240 minutos.");
    return;
  }

  // Validación para porciones
  if (!/^\d+$/.test(recipeServings) || parseInt(recipeServings, 10) <= 0) {
    showError("Las porciones deben ser un número entero positivo.");
    return;
  }
  if (parseInt(recipeServings, 10) > 20) {
    showError("Las porciones no pueden ser mayores a 20.");
    return;
  }

  const newRecipeData = {
    titulo: recipeTitle,
    descripcion: recipeDescription,
    ingredientes: recipeIngredients,
    instrucciones: recipeInstructions,
    tiempo_preparacion: parseInt(recipePrepTime),
    porciones: parseInt(recipeServings),
    dificultad: recipeDifficulty,
    categoria_id: parseInt(recipeCategory),
    imagen_url: recipeImageUrl,
    autor: recipeAuthor
  }

  try {
    const response = await fetch(`${API_BASE_URL}/recetas/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newRecipeData),
    })

    if (response.ok) {  
      const result = await response.json(); 
      console.log("Respuesta del servidor:", result); 

      showSuccess("¡Nueva receta guardada!") 
      document.getElementById("addRecipeForm").reset() 
      closeAddRecipeModal() 
      await loadRecipes() 
    } else {
      const errorResult = await response.json();
      showError(errorResult.message || "Error al agregar la receta. Por favor, inténtalo de nuevo.")
    }
  } catch (error) {
    console.error("Error al enviar nueva receta:", error)
    showError("Error de conexión al agregar la receta.")
  }
}

// Hacer funciones globales
window.showRecipeDetails = showRecipeDetails
window.showError = showError // Make showError function global
window.openAddRecipeModal = openAddRecipeModal
window.closeAddRecipeModal = closeAddRecipeModal
