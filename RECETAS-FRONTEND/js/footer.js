// footer.js - Script para inyectar el footer global
document.addEventListener('DOMContentLoaded', function() {
    // Crear el elemento footer
    const footer = document.createElement('footer');
    footer.className = 'footer';
    footer.innerHTML = `
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h4>Delishare</h4>
                    <p>Tu cocina, nuestros secretos. Descubrí el mundo de la gastronomía profesional.</p>
                </div>
                <div class="footer-section">
                    <h4>Enlaces</h4>
                    <a href="inicio.html">Inicio</a>
                    <a href="recetas.html">Recetas</a>
                    <a href="suscripcion.html">Suscripción</a>
                </div>
                <div class="footer-section">
                    <h4>Soporte</h4>
                    <a href="#">Ayuda</a>
                    <a href="#">Contacto</a>
                    <a href="#">Términos</a>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 Delishare. Todos los derechos reservados.</p>
            </div>
        </div>
    `;
    
    // Insertar el footer al final del body
    document.body.appendChild(footer);
});