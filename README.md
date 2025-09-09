<h1> Delishare: Tu Cocina, Nuestros Secretos 👨‍🍳👩‍🍳</h1>

<h2>Descripción del Proyecto</h2>

<p>Delishare es una <strong>aplicación web de recetas</strong> que permite a los usuarios explorar, buscar y compartir una amplia variedad de recetas. La plataforma ofrece autenticación de usuarios, gestión de recetas, visualización por categorías y un sistema de suscripción premium para contenido exclusivo.</p>

<p>El proyecto cuenta con un <strong>frontend interactivo</strong> desarrollado con HTML, CSS y JavaScript puro, y un <strong>backend API RESTful</strong> en Python (Flask) conectado a SQLServer.</p>

## Características Principales</h2>

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
  <li>Todas las características de los usuarios registrados gratuitos.</li>
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

<h3>Backend</h3>
<ul>
  <li><strong>Python</strong>: Lenguaje principal.</li>
  <li><strong>SQLServer</strong>: Base de datos relacional.</li>
</ul>

<h3>Frontend</h3>
<ul>
  <li><strong>HTML5</strong>: Estructura de las páginas web.</li>
  <li><strong>CSS3</strong>: Estilos y diseño visual.</li>
  <li><strong>JavaScript (Vanilla JS)</strong>: Lógica interactiva, manejo de API y DOM.</li>
  <li><strong>Font Awesome</strong>: Iconos y elementos visuales.</li>
</ul>

## Requisitos

Asegúrate de tener instalado lo siguiente:

*   **Python 3.8+**
*   **SQL Server** (2016 o superior)
*   **ODBC Driver** (17+ para SQL Server)
*   **Herramientas de SQL Server ** (SSMS opcional para gestión)

## Configuración del Proyecto

1.  **Clonar el Repositorio:**
    ```bash
    git clone <https://github.com/arizu14n/Delishare>
    cd Delishare
    ```

2.  **Configurar Variables de Entorno:**
    Crea un archivo `.env` en la raíz del proyecto (`Delishare/`) con el siguiente contenido. Asegúrate de reemplazar los valores con tus credenciales de SQLServer.

    ```
    DB_HOST="localhost"
    DB_USER="sa"
    DB_PASSWORD="tu_password_sql_server"
    DB_NAME="delishare_db"
    DB_DRIVER="ODBC Driver 17 for SQL Server"
    ```

3.  **Instalar Dependencias de Python:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar el Servidor Flask:**
    Una vez que la base de datos esté configurada, puedes iniciar el servidor Flask.

    ```bash
    python -m api.main
    ```
    El servidor se ejecutará en `http://127.0.0.1:5000` (o `http://0.0.0.0:5000`).

## Uso de la API

El backend de Flask expone los siguientes endpoints principales:

*   **`GET /recetas/categorias`**: Obtiene todas las categorías de recetas.
*   **`GET /recetas/`**: Obtiene todas las recetas. Acepta `?search=<término>` para buscar.
*   **`GET /recetas/<id>`**: Obtiene los detalles de una receta por ID.
*   **`POST /recetas/`**: Crea una nueva receta (requiere autenticación/autorización).
*   **`POST /auth/register`**: Registra un nuevo usuario.
*   **`POST /auth/login`**: Inicia sesión de un usuario.
*   **`GET /suscripcion/planes`**: Obtiene los planes de suscripción disponibles.
*   **`POST /suscripcion/subscribe`**: Suscribe a un usuario a un plan.

## Frontend

El frontend se encuentra en la carpeta `RECETAS-FRONTEND/`. Puedes abrir `RECETAS-FRONTEND/inicio.html` (o `recetas.html`, `login.html`, etc.) directamente en tu navegador para interactuar con la aplicación. 

```bash
    # Navegar al frontend
    cd RECETAS-FRONTEND

    # Abrir en navegador (ejemplo)
    start inicio.html
```
Asegúrate de que el servidor Flask esté corriendo para que el frontend pueda comunicarse con el backend.

---

**Desarrollado por:** [Cuarteto de Códigos]
