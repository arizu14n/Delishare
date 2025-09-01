<h1>Delishare: Tu Cocina, Nuestros Secretos 👨‍🍳👩‍🍳</h1>

<h2>Descripción del Proyecto</h2>
<p>Delishare es una <strong>aplicación web de recetas</strong> que permite a los usuarios explorar, buscar y compartir una amplia variedad de recetas. La plataforma ofrece autenticación de usuarios, gestión de recetas, visualización por categorías y un sistema de suscripción premium para contenido exclusivo.</p>
<p>El proyecto cuenta con un <strong>frontend interactivo</strong> desarrollado con HTML, CSS y JavaScript puro, y un <strong>backend API RESTful</strong> en PHP conectado a MySQL.</p>

<h2>Características Principales</h2>

<h3>Usuarios No Registrados</h3>
<ul>
  <li>Explorar todas las recetas gratuitas.</li>
  <li>Buscar recetas por título, descripción o ingredientes.</li>
  <li>Filtrar recetas por categoría y dificultad.</li>
  <li>Ver listados de categorías.</li>
  <li>Acceder a páginas de inicio de sesión y registro.</li>
  <li>Conocer planes de suscripción premium.</li>
</ul>

<h3>Usuarios Registrados (Gratuitos)</h3>
<ul>
  <li>Todas las características de usuarios no registrados.</li>
  <li>Añadir nuevas recetas (no premium por defecto).</li>
</ul>

<h3>Usuarios Premium</h3>
<ul>
  <li>Acceso a todas las recetas, incluyendo las marcadas como premium.</li>
  <li>Posibilidad de marcar sus propias recetas como premium al crearlas.</li>
</ul>

<h2>Funcionalidades Técnicas</h2>
<ul>
  <li>API RESTful para gestión de datos.</li>
  <li>Autenticación de usuarios segura (hashing de contraseñas).</li>
  <li>Manejo de CORS para comunicación entre frontend y backend.</li>
  <li>Simulación de activación de suscripciones premium.</li>
  <li>Interfaz interactiva y responsiva.</li>
</ul>

<h2>Tecnologías Utilizadas</h2>

<h3>Backend</h3>
<ul>
  <li><strong>PHP</strong>: Lenguaje principal.</li>
  <li><strong>PDO</strong>: Interacción segura y orientada a objetos con la base de datos.</li>
  <li><strong>MySQL</strong>: Base de datos relacional.</li>
</ul>

<h3>Frontend</h3>
<ul>
  <li><strong>HTML5</strong>: Estructura de las páginas web.</li>
  <li><strong>CSS3</strong>: Estilos y diseño visual.</li>
  <li><strong>JavaScript (Vanilla JS)</strong>: Lógica interactiva, manejo de API y DOM.</li>
  <li><strong>Font Awesome</strong>: Iconos y elementos visuales.</li>
</ul>

<h2>Requisitos</h2>

<h3>Backend</h3>
<ul>
  <li>Servidor Web: Apache, Nginx o similar con soporte PHP.</li>
  <li>PHP 7.4+ (recomendado PHP 8.x).</li>
  <li>Extensión <strong>PDO_MySQL</strong> habilitada.</li>
  <li>MySQL: Base de datos relacional.</li>
</ul>

<h3>Frontend</h3>
<ul>
  <li>Navegador moderno (Chrome, Firefox, Edge, Safari).</li>
</ul>

<h2>Instalación y Configuración</h2>
<ol>
  <li><strong>Clonar el repositorio</strong>
    <pre><code>git clone https://github.com/arizu14n/Delishare.git
cd Delishare</code></pre>
  </li>
  <li><strong>Configurar Backend</strong>
    <p>Crear base de datos MySQL (<code>recetas_cocina_prueba</code>) y tablas según <code>models/</code>. Editar <code>recetas-api/config/config.php</code> con tus credenciales.</p>
  </li>
  <li><strong>Servir Backend</strong>
    <p>Colocar la carpeta <code>recetas-api/</code> en tu servidor web. Ajustar <code>API_BASE_URL</code> en <code>recetas-frontend/js/shared.js</code>.</p>
  </li>
  <li><strong>Servir Frontend</strong>
    <p>Colocar la carpeta <code>recetas-frontend/</code> en tu servidor web o abrir <code>inicio.html</code> en el navegador.</p>
  </li>
</ol>

<h2>Uso de la Aplicación</h2>
<ul>
  <li>Abrir <code>inicio.html</code> en un navegador.</li>
  <li>Explorar recetas, registrarse o iniciar sesión.</li>
  <li>Añadir recetas si estás registrado.</li>
  <li>Simular suscripción premium desde la sección de suscripción.</li>
</ul>

<h2>Endpoints Principales del API</h2>
<ul>
  <li><code>POST /auth.php</code>: Registro e inicio de sesión de usuarios.</li>
  <li><code>GET /recetas.php</code>: Listado de recetas o detalles por ID.</li>
  <li><code>POST /recetas.php</code>: Crear nueva receta.</li>
  <li><code>GET /categorias.php</code>: Listado de categorías.</li>
  <li><code>POST /suscripcion.php</code>: Simular activación/actualización de suscripción.</li>
</ul>

<h2>Posibles Mejoras Futuras</h2>
<ul>
  <li>Autenticación JWT para mayor seguridad y escalabilidad.</li>
  <li>CRUD completo para recetas y categorías desde frontend.</li>
  <li>Integración con pasarelas de pago reales (Stripe, PayPal).</li>
  <li>Perfiles de usuario editables.</li>
  <li>Sistema de favoritos y valoraciones.</li>
  <li>Dashboard de administración.</li>
  <li>Manejo de imágenes directamente en el servidor.</li>
  <li>Manejo de errores consistente con JSON y bloques try-catch.</li>
</ul>

</body>
</html>
