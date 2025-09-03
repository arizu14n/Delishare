/**
 * Muestra una notificación de éxito.
 * @param {string} title - El título de la alerta.
 * @param {string} text - El texto del cuerpo de la alerta.
 */
function showSuccess(title, text) {
  Swal.fire({
    icon: 'success',
    title: title,
    text: text,
    confirmButtonColor: '#3085d6'
  });
}

/**
 * Muestra una notificación de error.
 * @param {string} title - El título de la alerta.
 * @param {string} text - El texto del cuerpo de la alerta.
 */
function showError(title, text) {
  Swal.fire({
    icon: 'error',
    title: title,
    text: text,
    confirmButtonColor: '#d33'
  });
}

/**
 * Muestra una notificación de información.
 * @param {string} title - El título de la alerta.
 * @param {string} text - El texto del cuerpo de la alerta.
 */
function showInfo(title, text) {
  Swal.fire({
    icon: 'info',
    title: title,
    text: text,
    confirmButtonColor: '#3085d6'
  });
}

/**
 * Muestra un diálogo de confirmación.
 * @param {string} title - El título de la alerta.
 * @param {string} text - El texto del cuerpo de la alerta.
 * @returns {Promise<boolean>} - Resuelve a true si el usuario confirma, false en caso contrario.
 */
async function showConfirmation(title, text) {
  const { isConfirmed } = await Swal.fire({
    title: title,
    text: text,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Sí, confirmar',
    cancelButtonText: 'Cancelar'
  });
  return isConfirmed;
}