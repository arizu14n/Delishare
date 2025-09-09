document.addEventListener("DOMContentLoaded", () => {
  setupAuthEventListeners();

  const savedUser = localStorage.getItem("currentUser");
  if (savedUser) {
    showInfo("Sesión ya iniciada", "Ya tienes una sesión activa. Serás redirigido a la página de inicio.");    
    setTimeout(() => { window.location.href = "inicio.html"; }, 2000);
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
    Swal.fire({
        title: '¡Error!',
        text: 'Por favor, completa tu email y contraseña.',
        icon: 'error',
        showConfirmButton: true
      });
    return;
  }

  const submitButton = e.target.querySelector('button[type="submit"]');
  const originalText = submitButton.textContent;

  try {
    Swal.fire({
            title: 'Iniciando sesión',
            text: 'Por favor, espere...',
            icon: 'info',
            showConfirmButton: false,
            allowOutsideClick: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    });

    const result = await response.json();

    if (response.ok) {
      localStorage.setItem("currentUser", JSON.stringify(result.user));
      Swal.fire({
        title: '¡Bienvenido!',
        text: 'Has iniciado sesión correctamente.',
        icon: 'success',
        timer: 1500,
        showConfirmButton: false,
        willClose: () => {
          window.location.href = "inicio.html";
        }
      });
    } else {
      Swal.fire({
        title: '¡Error!',
        text: 'Email o contraseña incorrectos.',
        icon: 'error',
        showConfirmButton: true
      });
    }
  } catch (error) {
    console.error("Error en login:", error);
    Swal.fire({
        title: '¡Error!',
        text: 'No se pudo conectar con el servidor. Por favor, inténtalo más tarde.',
        icon: 'error',
        showConfirmButton: true
      });
  } finally {
    submitButton.textContent = originalText;
    submitButton.disabled = false;
  }
}

// Manejar registro
async function handleRegister(e) {
  e.preventDefault();


  const nombre = DOMPurify.sanitize(document.getElementById("registerName").value.trim());
  const email = DOMPurify.sanitize(document.getElementById("registerEmail").value.trim());
  const password = DOMPurify.sanitize(document.getElementById("registerPassword").value.trim());

  if (!nombre || !email || !password) {
    Swal.fire({
        title: '¡Campos incompletos!',
        text: 'Por favor, completa todos los campos para registrarte.',
        icon: 'error',
        showConfirmButton: true
      });
    return;
  }

  // Validación de contraseña con RegEx como pide la consigna
  const passwordRegex = /^[a-zA-Z0-9!@#$%^&*]{8,20}$/;
  if (!passwordRegex.test(password)) {
    Swal.fire({
        title: '¡Contraseña no válida!',
        text: 'La contraseña debe tener entre 8 y 20 caracteres, sin espacios. Puede incluir letras, números y los símbolos !@#$%^&*',
        icon: 'error',
        showConfirmButton: true
      });
    return;
  }

  const submitButton = e.target.querySelector('button[type="submit"]');
  const originalText = submitButton.textContent;

  try {
    Swal.fire({
            title: 'Creando cuenta',
            text: 'Por favor, espere...',
            icon: 'info',
            showConfirmButton: false,
            allowOutsideClick: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        nombre: nombre,
        email: email,
        password: password,
      }),
    });

    const result = await response.json();

    if (response.ok) {
      localStorage.setItem("currentUser", JSON.stringify(result.user));
      Swal.fire({
        title: '¡Cuenta Creada!',
        text: 'Tu cuenta ha sido creada exitosamente. Serás redirigido a la página de inicio.',
        icon: 'success',
        timer: 2000,
        showConfirmButton: false,
        willClose: () => {
          window.location.href = "inicio.html";
        }
      });
    } else {
      Swal.fire({
        title: 'Error en el registro',
        text: result.error || "No se pudo crear la cuenta. Inténtalo de nuevo.",
        icon: 'error',
        showConfirmButton: true
      });
    }
  } catch (error) {
    console.error("Error en registro:", error);
    Swal.fire({
        title: '¡Error de conexión!',
        text: 'No se pudo conectar con el servidor. Por favor, inténtalo más tarde.',
        icon: 'error',
        showConfirmButton: true
      });
  } finally {
    submitButton.textContent = originalText;
    submitButton.disabled = false;
  } 
}
