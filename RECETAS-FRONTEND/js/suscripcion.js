/* // Inicialización de la página de suscripción
document.addEventListener("DOMContentLoaded", () => {
  initializeSubscriptionPage()
})


function initializeSubscriptionPage() {
  updateSubscriptionInterface()
}

// Actualizar interfaz según estado de suscripción
function updateSubscriptionInterface() {
  const freeButton = document.getElementById("freeButton")
  const monthlyButton = document.getElementById("monthlyButton")
  const annualButton = document.getElementById("annualButton")

  if (!currentUser) {
    // Usuario no logueado
    if (monthlyButton) {
      monthlyButton.onclick = () => {
        showError("Debes iniciar sesión para suscribirte")
        setTimeout(() => {
          window.location.href = "login.html"
        }, 2000)
      }
    }

    if (annualButton) {
      annualButton.onclick = () => {
        showError("Debes iniciar sesión para suscribirte")
        setTimeout(() => {
          window.location.href = "login.html"
        }, 2000)
      }
    }
    return
  }

  // Usuario logueado - verificar estado de suscripción
  if (currentUser.tipo_suscripcion === "premium" && currentUser.suscripcion_activa) {
    // Usuario premium activo
    if (freeButton) {
      freeButton.textContent = "Plan Anterior"
      freeButton.className = "btn-plan"
    }

    if (monthlyButton) {
      monthlyButton.textContent = "Plan Actual"
      monthlyButton.className = "btn-plan current"
      monthlyButton.onclick = null
    }

    if (annualButton) {
      annualButton.textContent = "Cambiar a Anual"
      annualButton.className = "btn-plan premium"
      annualButton.onclick = () => selectPlan("anual")
    }
  } else {
    // Usuario gratuito
    if (freeButton) {
      freeButton.textContent = "Plan Actual"
      freeButton.className = "btn-plan current"
    }

    if (monthlyButton) {
      monthlyButton.onclick = () => selectPlan("mensual")
    }

    if (annualButton) {
      annualButton.onclick = () => selectPlan("anual")
    }
  }
}

// Seleccionar plan de suscripción
async function selectPlan(planType) {
  if (!currentUser) {
    showError("Debes iniciar sesión para suscribirte")
    setTimeout(() => {
      window.location.href = "login.html"
    }, 2000)
    return
  }

  if (currentUser.tipo_suscripcion === "premium" && currentUser.suscripcion_activa) {
    if (planType === "mensual") {
      showError("Ya tienes una suscripción premium activa")
      return
    }
  }

  // Mostrar confirmación
  const planNames = {
    mensual: "Premium Mensual ($9.99/mes)",
    anual: "Premium Anual ($79.99/año)",
  }

  if (
    !confirm(
      `¿Confirmas la suscripción al plan ${planNames[planType]}?\n\nEsta es una simulación - no se realizará ningún cobro real.`,
    )
  ) {
    return
  }

  try {
    // Mostrar loading
    const button =
      planType === "mensual" ? document.getElementById("monthlyButton") : document.getElementById("annualButton")

    if (button) {
      const originalText = button.textContent
      button.textContent = "Procesando..."
      button.disabled = true
    }

    const response = await fetch(`${API_BASE_URL}/suscripcion.php`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        action: "subscribe",
        usuario_id: currentUser.id,
        plan: planType,
      }),
    })

    const result = await response.json()

    if (result.success) {
      // Actualizar datos del usuario
      currentUser.tipo_suscripcion = "premium"
      currentUser.suscripcion_activa = true
      currentUser.fecha_vencimiento = result.fecha_vencimiento

      localStorage.setItem("currentUser", JSON.stringify(currentUser))
      updateUserInterface()
      updateSubscriptionInterface()

      showSuccess(`¡Suscripción ${planType} activada exitosamente! 🎉`)

      // Mostrar mensaje adicional
      setTimeout(() => {
        showSuccess("Ahora puedes ver todas las recetas completas paso a paso")
      }, 2000)
    } else {
      showError(result.message || "Error al procesar la suscripción")
    }
  } catch (error) {
    console.error("Error en suscripción:", error)
    showError("Error de conexión al procesar la suscripción")
  } finally {
    // Restaurar botón
    const button =
      planType === "mensual" ? document.getElementById("monthlyButton") : document.getElementById("annualButton")

    if (button) {
      button.disabled = false
      updateSubscriptionInterface()
    }
  }
}

// Hacer funciones globales
window.selectPlan = selectPlan

function showError(message) {
  alert(message)
}

function showSuccess(message) {
  alert(message)
}

function updateUserInterface() {
  // Implement user interface update logic here
}
 */

/*
let currentUser = JSON.parse(localStorage.getItem("currentUser") || "null")
*/

function updateUserInterface () {
  const authButtons = document.getElementById("authButtons")
  const userMenu    = document.getElementById("userMenu")
  const userNameEl  = document.getElementById("userName")
  const userBadgeEl = document.getElementById("userBadge")

  if (currentUser) {
    // Oculta botones de login/registro
    if (authButtons) authButtons.style.display = "none"
    // Muestra menú de usuario
    if (userMenu)    userMenu.style.display    = "flex"

    if (userNameEl)  userNameEl.textContent  = currentUser.nombre || "Usuario"
    if (userBadgeEl) userBadgeEl.textContent = currentUser.tipo_suscripcion === "premium"
      ? "⭐ Premium"
      : "Free"
  } else {
    // Usuario no logueado
    if (authButtons) authButtons.style.display = "flex"
    if (userMenu)    userMenu.style.display    = "none"
  }
}

function updateSubscriptionInterface () {
  initializeSubscriptionPage()    
}

document.addEventListener("DOMContentLoaded", () => {
  updateUserInterface()         
  initializeSubscriptionPage()
})

async function initializeSubscriptionPage () {
  const freeButton    = document.getElementById("freeButton")
  const monthlyButton = document.getElementById("monthlyButton")
  const annualButton  = document.getElementById("annualButton")

  // 👇 Evita reventar si no hay usuario
  if (currentUser && currentUser.tipo_suscripcion === "premium" && currentUser.suscripcion_activa) {
    // Usuario premium activo
    if (freeButton) {
      freeButton.textContent = "Plan Anterior"
      freeButton.className = "btn-plan"
    }

    if (monthlyButton) {
      monthlyButton.textContent = "Plan Actual"
      monthlyButton.className = "btn-plan current"
      monthlyButton.onclick = null
    }

    if (annualButton) {
      annualButton.textContent = "Cambiar a Anual"
      annualButton.className = "btn-plan premium"
      annualButton.onclick = () => selectPlan("anual")
    }
  } else {
    if (freeButton) {
      freeButton.textContent = "Plan Actual"
      freeButton.className = "btn-plan current"
    }

    if (monthlyButton) {
      monthlyButton.onclick = () => selectPlan("mensual")
    }

    if (annualButton) {
      annualButton.onclick = () => selectPlan("anual")
    }
  }
}


// Seleccionar plan de suscripción
async function selectPlan(planType) {
  if (!currentUser) {
    showError("Debes iniciar sesión para suscribirte")
    setTimeout(() => {
      window.location.href = "login.html"
    }, 2000)
    return
  }

  if (currentUser.tipo_suscripcion === "premium" && currentUser.suscripcion_activa) {
    if (planType === "mensual") {
      showError("Ya tienes una suscripción premium activa")
      return
    }
  }

  // Mostrar confirmación
  const planNames = {
    mensual: "Premium Mensual ($9.99/mes)",
    anual: "Premium Anual ($79.99/año)",
  }

  if (
    !confirm(
      `¿Confirmas la suscripción al plan ${planNames[planType]}?\n\nEsta es una simulación - no se realizará ningún cobro real.`
    )
  ) {
    return
  }

  try {
    // Mostrar loading
    const button =
      planType === "mensual" ? document.getElementById("monthlyButton") : document.getElementById("annualButton")

    if (button) {
      const originalText = button.textContent
      button.textContent = "Procesando..."
      button.disabled = true
    }

    const response = await fetch(`${API_BASE_URL}/suscripcion.php`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        action: "subscribe",
        usuario_id: currentUser.id,
        plan: planType,
      }),
    })

    const result = await response.json()

    if (result.success) {
      // Actualizar datos del usuario
      currentUser.tipo_suscripcion = "premium"
      currentUser.suscripcion_activa = true
      currentUser.fecha_vencimiento = result.fecha_vencimiento

      localStorage.setItem("currentUser", JSON.stringify(currentUser))
      updateUserInterface()
      updateSubscriptionInterface()

      showSuccess(`¡Suscripción ${planType} activada exitosamente! 🎉`)

      // Mostrar mensaje adicional
      setTimeout(() => {
        showSuccess("Ahora puedes ver todas las recetas completas paso a paso")
      }, 2000)
    } else {
      showError(result.message || "Error al procesar la suscripción")
    }
  } catch (error) {
    console.error("Error en suscripción:", error)
    showError("Error de conexión al procesar la suscripción")
  } finally {
    // Restaurar botón
    const button =
      planType === "mensual" ? document.getElementById("monthlyButton") : document.getElementById("annualButton")

    if (button) {
      button.disabled = false
      updateSubscriptionInterface()
    }
  }
}

// Hacer funciones globales
window.selectPlan = selectPlan

function showError(message) {
  alert(message)
}

function showSuccess(message) {
  alert(message)
}


