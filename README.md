# Delishare - Backend Python (Flask) y Frontend (HTML/CSS/JS)

Este proyecto contiene el backend de Delishare, migrado de PHP a Python (Flask), y su frontend basado en HTML, CSS y JavaScript.

## Requisitos

Asegúrate de tener instalado lo siguiente:

*   **Python 3.8+**
*   **MySQL Server** (o MariaDB)
*   **Cliente de línea de comandos de MySQL** (asegúrate de que `mysql` esté en tu PATH o conoce su ruta completa)

## Configuración del Proyecto

1.  **Clonar el Repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd Delishare
    ```

2.  **Configurar Variables de Entorno:**
    Crea un archivo `.env` en la raíz del proyecto (`Delishare/`) con el siguiente contenido. Asegúrate de reemplazar los valores con tus credenciales de MySQL.

    ```
    DB_HOST="localhost"
    DB_USER="root"
    DB_PASSWORD=""
    ```
    *(Nota: `DB_NAME` se gestiona internamente por el script de configuración de la base de datos.)*

3.  **Instalar Dependencias de Python:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar la Base de Datos:**
    Este paso creará la base de datos `recetas_cocina_prueba` y poblará las tablas con los datos iniciales.

    ```bash
    python setup_db.py
    ```
    *   Si el comando `mysql` no se encuentra, el script te dará instrucciones sobre cómo añadirlo a tu PATH o usar la ruta completa.
    *   Te pedirá la contraseña de tu usuario de MySQL (si tienes una).

5.  **Ejecutar el Servidor Flask:**
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

El frontend se encuentra en la carpeta `RECETAS-FRONTEND/`. Puedes abrir `RECETAS-FRONTEND/inicio.html` (o `recetas.html`, `login.html`, etc.) directamente en tu navegador para interactuar con la aplicación. Asegúrate de que el servidor Flask esté corriendo para que el frontend pueda comunicarse con el backend.

---

**Desarrollado por:** [Cuarteto de Códigos]
