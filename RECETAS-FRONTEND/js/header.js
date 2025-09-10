// header.js - Script para inyectar el header global
document.addEventListener('DOMContentLoaded', function() {
    // Crear el elemento header
    const header = document.createElement('header');
    header.className = 'header';
    header.innerHTML = `
        <nav class="navbar">
            <div class="nav-container">
                <h1 class="logo">
                    <a href="inicio.html" class="logo-link">
                        <img src="Imagenes/Logo.png" alt="Logo Delishare">
                    </a>
                    Delishare
                </h1>
                <div class="nav-menu">
                    <a href="inicio.html" class="nav-link" id="navInicio">Inicio</a>
                    <a href="recetas.html" class="nav-link" id="navRecetas">Recetas</a>
                    <a href="suscripcion.html" class="nav-link" id="navSuscripcion">Suscripción</a>
                    <div class="auth-buttons" id="authButtons">
                        <button class="btn-login" onclick="window.location.href='login.html'">Iniciar Sesión</button>
                        <button class="btn-register" onclick="window.location.href='registrar.html'">Registrarse</button>
                    </div>
                </div>
                <div class="user-menu" id="userMenu" style="display: none;">
                    <span class="user-name" id="userName"></span>
                    <span class="user-badge" id="userBadge"></span>
                    <button class="btn-logout" onclick="logout()">Cerrar Sesión</button>
                </div>
            </div>
        </nav>
    `;
    
    // Insertar el header al principio del body
    document.body.insertBefore(header, document.body.firstChild);
    
    // Marcar como activo el enlace correspondiente a la página actual
    highlightCurrentPage();
    
    // Verificar estado de autenticación
    checkAuthStatus();
});

// Función para resaltar la página actual en el menú
function highlightCurrentPage() {
    const currentPage = window.location.pathname.split('/').pop();
    const pageIds = {
        'inicio.html': 'navInicio',
        'recetas.html': 'navRecetas',
        'suscripcion.html': 'navSuscripcion',
        'login.html': 'navLogin',
        'registrar.html': 'navRegistrar'
    };
    
    if (pageIds[currentPage]) {
        const activeLink = document.getElementById(pageIds[currentPage]);
        if (activeLink) {
            activeLink.classList.add('active');
        }
    }
}

// Función para verificar el estado de autenticación
function checkAuthStatus() {
    const user = JSON.parse(localStorage.getItem('currentUser'));
    
    if (user) {
        showUserMenu(user);
    } else {
        showAuthButtons();
    }
}

// Función para mostrar el menú de usuario
function showUserMenu(userData) {
    const authButtons = document.getElementById('authButtons');
    const userMenu = document.getElementById('userMenu');
    const userName = document.getElementById('userName');
    const userBadge = document.getElementById('userBadge');
    
    if (authButtons) authButtons.style.display = 'none';
    if (userMenu) userMenu.style.display = 'flex';
    if (userName) userName.textContent = userData.nombre || 'Usuario';
    
    if (userBadge) {
        userBadge.textContent = userData.tipo_suscripcion === 'premium' ? 'Premium' : 'Gratuito';
        userBadge.className = `user-badge ${userData.tipo_suscripcion === 'premium' ? 'premium' : 'free'}`;
    }
}

// Función para mostrar botones de autenticación
function showAuthButtons() {
    const authButtons = document.getElementById('authButtons');
    const userMenu = document.getElementById('userMenu');
    
    if (authButtons) authButtons.style.display = 'flex';
    if (userMenu) userMenu.style.display = 'none';
}

// Función para cerrar sesión
function logout() {
    localStorage.removeItem('currentUser');
    localStorage.removeItem('authToken');
    showAuthButtons();
    window.location.href = 'inicio.html';
}

// Hacer funciones globales
window.logout = logout;