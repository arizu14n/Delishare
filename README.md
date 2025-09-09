<h1> Delishare: Tu Cocina, Nuestros Secretos 👨‍🍳👩‍🍳</h1>

Este proyecto contiene el backend de Delishare, migrado de PHP a Python (Flask), y su frontend basado en HTML, CSS y JavaScript.

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
