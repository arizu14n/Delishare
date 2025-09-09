// Configuración de la API
const API_BASE_URL = "http://127.0.0.1:5000"

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

// Verificar sesión de usuario
function checkUserSession() {
  const userData = localStorage.getItem("currentUser")
  if (userData) {
    try {
      currentUser = JSON.parse(userData)
      updateUserInterface()
    } catch (error) {
      console.error("Error al parsear datos de usuario:", error)
      localStorage.removeItem("currentUser")
    }
  }
}

// Actualizar interfaz según estado del usuario
function updateUserInterface() {
  const authButtons = document.getElementById("authButtons");
  const userMenu = document.getElementById("userMenu");
  const userName = document.getElementById("userName");
  const userBadge = document.getElementById("userBadge");

  if (currentUser && authButtons && userMenu) {
    authButtons.style.display = "none";
    userMenu.style.display = "flex";

    if (userName) {
      userName.textContent = currentUser.nombre;
    }

    if (userBadge) {
      if (
        currentUser.tipo_suscripcion === "premium" &&
        currentUser.suscripcion_activa
      ) {
        userBadge.textContent = "Premium";
        userBadge.className = "user-badge premium"; 
      } else {
        userBadge.textContent = "Gratuito";
        userBadge.className = "user-badge";
      }
    }
  } else if (authButtons && userMenu) {
    authButtons.style.display = "flex";
    userMenu.style.display = "none";
  }
}

// Cerrar sesión
function logout() {
  currentUser = null
  localStorage.removeItem("currentUser")
  updateUserInterface()

  Swal.fire({
    title: '¡Éxito!',
    text: 'Has cerrado sesión correctamente.',
    icon: 'success',
    showConfirmButton: false

  });

  // Redirigir al inicio
  setTimeout(() => {
    window.location.href = "inicio.html"
  }, 1500)
}

// Funciones de utilidad para mensajes
function showSuccess(message) {
  const alertDiv = document.createElement("div")
  alertDiv.className = "success-message"
  alertDiv.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`

  document.body.appendChild(alertDiv)

  setTimeout(() => {
    alertDiv.remove()
  }, 5000)
}

function showError(message) {
  const alertDiv = document.createElement("div")
  alertDiv.className = "error-message"
  alertDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`

  document.body.appendChild(alertDiv)

  setTimeout(() => {
    alertDiv.remove()
  }, 5000)
}

async function showConfirmation(title, text) {
  const result = await Swal.fire({
    title: title,
    text: text,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Sí, confirmar!',
    cancelButtonText: 'Cancelar'
  });
  return result.isConfirmed;
}

// Cerrar modal
function closeModal(modalId) {
  const modal = document.getElementById(modalId)
  if (modal) {
    modal.style.display = "none"
  }
}

// Hacer funciones globales
window.logout = logout
window.showSuccess = showSuccess
window.showError = showError
window.showConfirmation = showConfirmation
window.closeModal = closeModal
window.currentUser = currentUser