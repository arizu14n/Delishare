let allPlans = [];

function updateSubscriptionInterface() {
  // Esta función ahora se encarga de actualizar el estado de los botones de plan
  // basándose en si el usuario es premium o no.
  const freeButton = document.getElementById("freeButton");
  const monthlyButton = document.getElementById("monthlyButton");
  const annualButton = document.getElementById("annualButton");

  if (!currentUser) {
    // Usuario no logueado: todos los planes premium redirigen a login
    if (monthlyButton) monthlyButton.onclick = () => {
      showError("Acción requerida", "Debes iniciar sesión para suscribirte.");
      setTimeout(() => { window.location.href = "login.html"; }, 2000);
    };
    if (annualButton) annualButton.onclick = () => {
      showError("Acción requerida", "Debes iniciar sesión para suscribirte.");
      setTimeout(() => { window.location.href = "login.html"; }, 2000);
    };
    if (freeButton) {
      freeButton.textContent = "Plan Actual";
      freeButton.className = "btn-plan current";
    }
    return;
  }

  // Usuario logueado
  if (currentUser.tipo_suscripcion === "premium" && currentUser.suscripcion_activa) {
    // Usuario premium activo
    if (freeButton) {
      freeButton.textContent = "Plan Anterior";
      freeButton.className = "btn-plan";
    }
    // Encontrar el plan actual del usuario (mensual o anual)
    const currentPlan = allPlans.find(p => p.duracion_dias === (currentUser.fecha_vencimiento && (new Date(currentUser.fecha_vencimiento) - new Date(currentUser.fecha_suscripcion)) / (1000 * 60 * 60 * 24) > 30 ? 365 : 30));

    allPlans.forEach(plan => {
      const button = document.getElementById(plan.nombre.toLowerCase() + "Button");
      if (button) {
        if (currentPlan && plan.id === currentPlan.id) {
          button.textContent = "Plan Actual";
          button.className = "btn-plan current";
          button.onclick = null;
        } else {
          button.textContent = `Cambiar a ${plan.nombre}`;
          button.className = "btn-plan premium";
          button.onclick = () => selectPlan(plan.nombre.toLowerCase());
        }
      }
    });
  } else {
    // Usuario gratuito
    if (freeButton) {
      freeButton.textContent = "Plan Actual";
      freeButton.className = "btn-plan current";
    }
    allPlans.forEach(plan => {
      const button = document.getElementById(plan.nombre.toLowerCase() + "Button");
      if (button) {
        button.textContent = `Suscribirse ${plan.nombre}`;
        button.className = "btn-plan premium";
        button.onclick = () => selectPlan(plan.nombre.toLowerCase());
      }
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  updateUserInterface();
  initializeSubscriptionPage();
});

async function initializeSubscriptionPage() {
  await loadPlans(); // Cargar planes al inicializar
  updateSubscriptionInterface(); // Luego actualizar la interfaz
}

// Cargar planes desde la API
async function loadPlans() {
  try {
    const response = await fetch(`${API_BASE_URL}/suscripcion/planes`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    if (Array.isArray(data)) {
      allPlans = data;
      displayPlans(); // Mostrar los planes cargados
    } else {
      console.error("Los planes no son un array:", data);
    }
  } catch (error) {
    console.error("Error al cargar planes:", error);
    showError("Error", "No se pudieron cargar los planes de suscripción. Inténtalo de nuevo más tarde.");
  }
}

// Mostrar planes dinámicamente
function displayPlans() {
  const plansGrid = document.getElementById("plansGrid");
  if (!plansGrid) return;

  plansGrid.innerHTML = ""; // Limpiar planes existentes

  // Añadir el plan gratuito (siempre presente)
  plansGrid.innerHTML += `
        <div class="plan-card">
            <div class="plan-header">
                <h3>Gratuito</h3>
                <div class="plan-price">$0<span>/mes</span></div>
            </div>
            <div class="plan-features">
                <div class="feature"><i class="fas fa-check"></i> Ver ingredientes completos</div>
                <div class="feature"><i class="fas fa-check"></i> Primeros 2 pasos de preparación</div>
                <div class="feature"><i class="fas fa-times"></i> Preparación completa</div>
                <div class="feature"><i class="fas fa-times"></i> Recetas premium</div>
            </div>
            <button class="btn-plan current" id="freeButton">Plan Actual</button>
        </div>
    `;

  allPlans.forEach(plan => {
    const isFeatured = plan.nombre.toLowerCase() === "mensual"; // Marcar Mensual como destacado
    plansGrid.innerHTML += `
            <div class="plan-card ${isFeatured ? "featured" : ""}">
                ${isFeatured ? '<div class="plan-badge">Más Popular</div>' : ''}
                <div class="plan-header">
                    <h3>${plan.nombre}</h3>
                    <div class="plan-price">$${plan.precio}<span>/${plan.duracion_dias === 30 ? 'mes' : 'año'}</span></div>
                    ${plan.duracion_dias === 365 ? '<div class="plan-savings">Ahorra 33%</div>' : ''}
                </div>
                <div class="plan-features">
                    <div class="feature"><i class="fas fa-check"></i> Todo lo gratuito</div>
                    <div class="feature"><i class="fas fa-check"></i> Preparaciones completas paso a paso</div>
                    <div class="feature"><i class="fas fa-check"></i> Recetas premium exclusivas</div>
                    <div class="feature"><i class="fas fa-check"></i> Sin anuncios</div>
                    ${plan.duracion_dias === 365 ? '<div class="feature"><i class="fas fa-check"></i> Acceso prioritario a nuevas recetas</div><div class="feature"><i class="fas fa-check"></i> Recetas exclusivas de temporada</div><div class="feature"><i class="fas fa-check"></i> Soporte premium 24/7</div>' : ''}
                </div>
                <button class="btn-plan premium" id="${plan.nombre.toLowerCase()}Button" onclick="selectPlan('${plan.nombre.toLowerCase()}')">Suscribirse ${plan.nombre}</button>
            </div>
        `;
  });

  // Asegurarse de que los botones existan antes de llamar a updateSubscriptionInterface
  updateSubscriptionInterface();
}

// Seleccionar plan de suscripción
async function selectPlan(planName) {
  if (!currentUser) {
    showError("Acción requerida", "Debes iniciar sesión para suscribirte.");
    setTimeout(() => { window.location.href = "login.html"; }, 2000);
    return;
  }

  const selectedPlan = allPlans.find(p => p.nombre.toLowerCase() === planName);
  if (!selectedPlan) {
    showError("Error", "El plan seleccionado no fue encontrado.");
    return;
  }

  if (currentUser.tipo_suscripcion === "premium" && currentUser.suscripcion_activa) {
    // Lógica para cambiar de plan o si ya es premium
    if (selectedPlan.duracion_dias === (currentUser.fecha_vencimiento && (new Date(currentUser.fecha_vencimiento) - new Date(currentUser.fecha_suscripcion)) / (1000 * 60 * 60 * 24) > 30 ? 365 : 30)) {
      showInfo("Plan actual", "Ya tienes este plan premium activo.");
      return;
    }
  }

  // Mostrar confirmación
  const confirmed = await showConfirmation(
    `Confirmar Suscripción`,
    `Estás a punto de suscribirte al plan ${selectedPlan.nombre} por $${selectedPlan.precio}/${selectedPlan.duracion_dias === 30 ? 'mes' : 'año'}. Esta es una simulación y no se realizará ningún cobro real.`
  );

  if (!confirmed) {
    return;
  }

  try {
    // Mostrar loading
    const button = document.getElementById(selectedPlan.nombre.toLowerCase() + "Button");
    if (button) {
      const originalText = button.textContent;
      button.textContent = "Procesando...";
      button.disabled = true;
    }

    const response = await fetch(`${API_BASE_URL}/suscripcion/subscribe`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        usuario_id: currentUser.id,
        plan: selectedPlan.nombre.toLowerCase(), // Usar el nombre del plan (mensual/anual)
      }),
    });

    const result = await response.json();

    if (response.ok) {
      // Actualizar datos del usuario
      currentUser.tipo_suscripcion = "premium";
      currentUser.suscripcion_activa = true;
      currentUser.fecha_suscripcion = new Date().toISOString().slice(0, 10); // Fecha actual
      currentUser.fecha_vencimiento = result.fecha_vencimiento; // Viene del backend

      localStorage.setItem("currentUser", JSON.stringify(currentUser));
      updateUserInterface();
      updateSubscriptionInterface();

      showSuccess("¡Suscripción Activada!", `Tu suscripción al plan ${selectedPlan.nombre} está activa. ¡Disfruta de los beneficios! 🎉`);

      // Mostrar mensaje adicional
      setTimeout(() => {
        showInfo("¡Beneficios Desbloqueados!", "Ahora puedes ver todas las recetas completas paso a paso.");
      }, 2000);
    } else {
      showError("Error en la suscripción", result.error || "No se pudo procesar tu suscripción. Por favor, inténtalo de nuevo.");
    }
  } catch (error) {
    console.error("Error en suscripción:", error);
    showError("Error de conexión", "No se pudo conectar con el servidor para procesar la suscripción.");
  } finally {
    // Restaurar botón
    const button = document.getElementById(selectedPlan.nombre.toLowerCase() + "Button");
    if (button) {
      button.disabled = false;
      updateSubscriptionInterface();
    }
  }
}

// Hacer funciones globales
window.selectPlan = selectPlan;