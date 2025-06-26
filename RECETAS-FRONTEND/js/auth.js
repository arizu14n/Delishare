document.addEventListener("DOMContentLoaded", () => {
  setupAuthEventListeners();

  const savedUser = localStorage.getItem("currentUser");
  if (savedUser) {
    console.log("Ya hay un usuario logueado.");
    alert("Ya tienes una sesión iniciada");
  }
});

function setupAuthEventListeners() {
  const loginForm = document.getElementById("loginForm");
  const registerForm = document.getElementById("registerForm");

  if (loginForm) {
    loginForm.addEventListener("submit", handleLogin);
  }

  if (registerForm) {
    registerForm.addEventListener("submit", handleRegister);
  }
}

// Manejar login
async function handleLogin(e) {
  e.preventDefault();

  const email = document.getElementById("loginEmail").value.trim();
  const password = document.getElementById("loginPassword").value.trim();

  if (!email || !password) {
    alert("Por favor completa todos los campos");
    return;
  }

  const submitButton = e.target.querySelector('button[type="submit"]');
  const originalText = submitButton.textContent;

  try {
    submitButton.textContent = "Iniciando sesión...";
    submitButton.disabled = true;

    const response = await fetch(`${API_BASE_URL}/auth.php`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        action: "login",
        email: email,
        password: password,
      }),
    });

    const result = await response.json();

    if (result.success) {
      localStorage.setItem("currentUser", JSON.stringify(result.user));
      document.getElementById("overlay").style.display = "flex";

      setTimeout(() => {
        window.location.href = "inicio.html";
      }, 1500);
    } else {
      alert(result.message || "Error al iniciar sesión");
    }
  } catch (error) {
    console.error("Error en login:", error);
    alert("Error de conexión. Verifica que el servidor esté funcionando.");
  } finally {
    submitButton.textContent = originalText;
    submitButton.disabled = false;
  }
}

// Manejar registro
async function handleRegister(e) {
  e.preventDefault();
  hideMessages();

  const nombre = document.getElementById("registerName").value.trim();
  const email = document.getElementById("registerEmail").value.trim();
  const password = document.getElementById("registerPassword").value.trim();

  if (!nombre || !email || !password) {
    alert("Por favor completa todos los campos.");
    return;
  }

  if (password.length < 6) {
    alert("La contraseña debe tener al menos 6 caracteres.");
    return;
  }

  const submitButton = e.target.querySelector('button[type="submit"]');
  const originalText = submitButton.textContent;

  try {
    submitButton.textContent = "Creando cuenta...";
    submitButton.disabled = true;

    const response = await fetch(`${API_BASE_URL}/auth.php`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        action: "register",
        nombre: nombre,
        email: email,
        password: password,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      if (response.status === 409) {
        alert(errorData?.message || "Este correo ya está registrado.");
      } else {
        alert(errorData?.message || "Error al crear la cuenta.");
      }
      return;
    }

    const result = await response.json();

    if (result.success) {
      localStorage.setItem("currentUser", JSON.stringify(result.user));

      alert("¡Cuenta creada exitosamente! Redirigiendo a tu inicio...");
      setTimeout(() => {
        window.location.href = "inicio.html";
      }, 2000);
    } else {
      alert(result.message || "Error desconocido.");
    }
  } catch (error) {
    console.error("Error en registro:", error);
    alert("Error de conexión. Verifica que el servidor esté funcionando.");
  } finally {
    submitButton.textContent = originalText;
    submitButton.disabled = false;
  }
}

// Funciones auxiliares
function showError(message) {
  const errorElement = document.getElementById("error");
  if (errorElement) {
    errorElement.textContent = message;
    errorElement.style.display = "block";
    setTimeout(() => (errorElement.style.display = "none"), 4000);
  }
}

function showSuccess(message) {
  const successElement = document.getElementById("success");
  if (successElement) {
    successElement.textContent = message;
    successElement.style.display = "block";
    setTimeout(() => (successElement.style.display = "none"), 4000);
  }
}

function hideMessages() {
  ["error", "success"].forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.style.display = "none";
  });
}
