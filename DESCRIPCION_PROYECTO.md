
# Descripción del Proyecto: Delishare

## 1. Resumen General

Delishare es una aplicación web diseñada para que los amantes de la cocina puedan compartir, descubrir y explorar una amplia variedad de recetas. La plataforma permite a los usuarios registrarse, gestionar su perfil, y acceder a un catálogo de recetas clasificadas por categorías. Además, ofrece un sistema de suscripción "premium" que podría dar acceso a contenido exclusivo.

El proyecto está construido con una arquitectura desacoplada, con un **backend (API)** desarrollado en Python y un **frontend** (interfaz de usuario) que consume los servicios de esta API.

## 2. Stack Tecnológico

- **Backend:**
  - **Lenguaje:** Python 3
  - **Framework:** Flask
  - **ORM:** SQLAlchemy (para la interacción con la base de datos)
  - **Validación de Datos:** Pydantic (para definir modelos de datos y validar la información de entrada/salida de la API)
  - **Servidor de Base de Datos:** Microsoft SQL Server
  - **Manejo de Contraseñas:** Passlib (para hasheo seguro de contraseñas)

- **Frontend:**
  - **Lenguajes:** HTML, CSS, JavaScript
  - **Librerías:** (No se especifican, pero se asume el uso de librerías estándar para peticiones AJAX, como `fetch`).

## 3. Estructura del Proyecto

El proyecto se divide principalmente en dos grandes componentes: el backend (`api`) y el frontend (`RECETAS-FRONTEND`).

### Backend (`api/`)

Es el cerebro de la aplicación. Gestiona la lógica de negocio, la autenticación de usuarios y la comunicación con la base de datos.

- `main.py`: Es el punto de entrada de la API. Crea la aplicación Flask, registra las rutas (Blueprints), configura CORS y define el manejo de errores.
- `database.py`: Configura la conexión a la base de datos SQL Server utilizando SQLAlchemy. Gestiona la creación del "engine" y las sesiones de base de datos.
- `config.py`: Centraliza las variables de configuración, como las credenciales de la base de datos, cargándolas desde un archivo `.env`.
- **`models/`**: Define la estructura de los datos.
    - Contiene los **modelos de SQLAlchemy** (`...DB`), que mapean las clases de Python a las tablas de la base de datos (ej: `RecetaDB`, `UsuarioDB`).
    - Contiene los **modelos de Pydantic** (ej: `Receta`, `UsuarioCreate`), que se usan para validar los datos que entran y salen de la API, asegurando que la información sea correcta y completa.
- **`routers/`**: Define los endpoints o rutas de la API.
    - `auth.py`: Gestiona el registro (`/register`) y el inicio de sesión (`/login`) de los usuarios.
    - `recetas.py`: Proporciona los endpoints para interactuar con las recetas y categorías (crear, leer, buscar).
    - `suscripcion.py`: Maneja la lógica de los planes de suscripción y la actualización del estado de un usuario a "premium".

### Frontend (`RECETAS-FRONTEND/`)

Es la parte visible de la aplicación con la que interactúa el usuario.

- `.html`: Archivos que estructuran las diferentes páginas (inicio, login, recetas, etc.).
- `css/`: Contiene los archivos de estilo para dar un diseño visual a la aplicación.
- `js/`: Contiene la lógica del lado del cliente.
    - `auth.js`: Maneja las peticiones de registro y login a la API.
    - `recetas.js`: Se encarga de obtener las recetas de la API y mostrarlas en la página.
    - `suscripcion.js`: Gestiona la interacción con los planes de suscripción.

## 4. Funcionamiento General y Flujo de Datos

1.  **Inicio y Carga de Datos**:
    - Cuando un usuario abre la página de `recetas.html`, el archivo `recetas.js` realiza una petición `GET` al endpoint `/recetas/` de la API.
    - La API (en `routers/recetas.py`) recibe la petición, consulta la base de datos a través de SQLAlchemy para obtener la lista de recetas, y la devuelve en formato JSON.
    - El frontend recibe este JSON y lo utiliza para renderizar dinámicamente la lista de recetas en la página.

2.  **Registro de Usuario**:
    - El usuario rellena el formulario en `registrar.html`.
    - Al enviar, `auth.js` captura los datos y realiza una petición `POST` al endpoint `/auth/register` de la API con el nombre, email y contraseña.
    - La API (en `routers/auth.py`) valida los datos. Si son correctos, hashea la contraseña (nunca la guarda en texto plano) y crea un nuevo registro en la tabla `usuario` de la base de datos.

3.  **Login de Usuario**:
    - El usuario introduce su email y contraseña en `login.html`.
    - `auth.js` envía estos datos en una petición `POST` al endpoint `/auth/login`.
    - La API busca al usuario por su email, y si lo encuentra, compara el hash de la contraseña guardada con el hash de la contraseña introducida.
    - Si coinciden, devuelve los datos del usuario (sin la contraseña) y el estado de su suscripción.

4.  **Suscripción Premium**:
    - El usuario, desde `suscripcion.html`, elige un plan.
    - `suscripcion.js` envía una petición `POST` al endpoint `/suscripcion/subscribe` con el ID del usuario y el plan seleccionado.
    - La API (en `routers/suscripcion.py`) actualiza el registro del usuario en la base de datos, cambiando su `tipo_suscripcion` a "premium" y estableciendo una fecha de vencimiento.

## 5. Endpoints Principales de la API

- `GET /`: Mensaje de bienvenida de la API.
- **Autenticación (`/auth`)**:
    - `POST /register`: Registra un nuevo usuario.
    - `POST /login`: Inicia sesión.
- **Recetas (`/recetas`)**:
    - `GET /`: Obtiene todas las recetas (permite búsqueda con `?search=termino`).
    - `POST /`: Crea una nueva receta.
    - `GET /<id>`: Obtiene una receta por su ID.
    - `GET /categorias`: Obtiene todas las categorías de recetas.
- **Suscripción (`/suscripcion`)**:
    - `GET /planes`: Obtiene los planes de suscripción disponibles.
    - `POST /subscribe`: Actualiza la suscripción de un usuario a un plan.

