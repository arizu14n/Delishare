
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# --- Configuración de la Base de Datos ---
# Obtiene los datos de conexión desde las variables de entorno
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "delishare_db")

def create_database_and_tables():
    """
    Se conecta a MySQL, crea la base de datos si no existe,
    y luego crea las tablas del proyecto.
    """
    try:
        # 1. Conexión inicial al servidor MySQL para crear la base de datos
        print(f"Conectando al servidor MySQL en '{DB_HOST}'...")
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        # 2. Crear la base de datos si no existe
        print(f"Creando la base de datos '{DB_NAME}' si no existe...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        print(f"Base de datos '{DB_NAME}' lista.")
        cursor.close()
        conn.close()

        # 3. Conexión a la base de datos específica para crear las tablas
        print(f"Conectando a la base de datos '{DB_NAME}'...")
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # 4. Definición y creación de las tablas
        
        # --- Tabla de Categorías ---
        print("Creando tabla 'categorias'...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL UNIQUE,
            descripcion TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB;
        """)

        # --- Tabla de Usuarios ---
        print("Creando tabla 'usuarios'...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB;
        """)

        # --- Tabla de Recetas ---
        print("Creando tabla 'recetas'...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS recetas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            descripcion TEXT,
            ingredientes TEXT NOT NULL,
            instrucciones TEXT NOT NULL,
            tiempo_preparacion INT DEFAULT 0,
            porciones INT DEFAULT 1,
            dificultad VARCHAR(50) DEFAULT 'Fácil',
            imagen_url VARCHAR(255),
            es_premium BOOLEAN DEFAULT FALSE,
            activo BOOLEAN DEFAULT TRUE,
            vistas INT DEFAULT 0,
            likes INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            categoria_id INT,
            usuario_id INT,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """)

        print("\nTablas creadas exitosamente en la base de datos.")
        
        # Insertar categorías de ejemplo si la tabla está vacía
        cursor.execute("SELECT COUNT(*) FROM categorias")
        if cursor.fetchone()[0] == 0:
            print("Insertando categorías de ejemplo...")
            default_categories = [
                ('Postres', 'Recetas dulces y postres.'),
                ('Ensaladas', 'Ensaladas frescas y saludables.'),
                ('Platos Fuertes', 'Platos principales para almuerzo o cena.'),
                ('Sopas', 'Sopas y cremas calientes o frías.'),
                ('Bebidas', 'Bebidas, batidos y cócteles.')
            ]
            cursor.executemany("INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s)", default_categories)
            conn.commit()
            print(f"{cursor.rowcount} categorías insertadas.")

    except Error as e:
        print(f"Error al configurar la base de datos: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn and conn.is_connected():
            conn.close()
            print("Conexión a MySQL cerrada.")

if __name__ == '__main__':
    create_database_and_tables()
