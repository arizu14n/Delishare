import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from passlib.context import CryptContext

# Configurar el contexto de hasheo de contraseñas
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# --- Configuración de la Base de Datos ---
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = "delishare_db"

def update_database_schema():
    print(f"DEBUG: Intentando conectar a la base de datos: {DB_NAME}")
    """
    Actualiza el esquema de la base de datos para incluir las tablas y columnas necesarias
    para las suscripciones y otras funcionalidades del proyecto original.
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        print("Actualizando esquema de la base de datos...")

        # Deshabilitar comprobación de claves foráneas temporalmente
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        # --- Borrar y recrear tablas para asegurar la estructura correcta ---
        # Borrar todas las tablas en un orden seguro
        cursor.execute("DROP TABLE IF EXISTS favoritos;")
        cursor.execute("DROP TABLE IF EXISTS valoraciones;")
        cursor.execute("DROP TABLE IF EXISTS logs_actividad;")
        cursor.execute("DROP TABLE IF EXISTS planes_suscripcion;")
        cursor.execute("DROP TABLE IF EXISTS recetas;") 
        cursor.execute("DROP TABLE IF EXISTS categorias;") 
        cursor.execute("DROP TABLE IF EXISTS usuarios;") 

        print("Tablas existentes borradas (si existían).")

        # --- Tabla de usuarios con mejoras (password_hash y suscripciones) ---
        print("Creando tabla 'usuarios'...")
        cursor.execute("""
        CREATE TABLE usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            email VARCHAR(150) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL, -- Cambiado de 'password' a 'password_hash'
            tipo_suscripcion ENUM('gratuito', 'premium') DEFAULT 'gratuito',
            fecha_suscripcion DATE NULL,
            fecha_vencimiento DATE NULL,
            activo BOOLEAN DEFAULT TRUE,
            intentos_login INT DEFAULT 0,
            bloqueado_hasta TIMESTAMP NULL,
            ultimo_login TIMESTAMP NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            
            INDEX idx_email (email),
            INDEX idx_tipo_suscripcion (tipo_suscripcion),
            INDEX idx_activo (activo)
        ) ENGINE=InnoDB;
        """)

        # --- Tabla de categorías ---
        print("Creando tabla 'categorias'...")
        cursor.execute("""
        CREATE TABLE categorias (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL UNIQUE,
            descripcion TEXT,
            icono VARCHAR(50) DEFAULT 'fas fa-utensils',
            activo BOOLEAN DEFAULT TRUE,
            orden INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            INDEX idx_activo (activo),
            INDEX idx_orden (orden)
        ) ENGINE=InnoDB;
        """

        # --- Tabla de recetas mejorada ---
        print("Creando tabla 'recetas'...")
        cursor.execute("""
        CREATE TABLE recetas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(200) NOT NULL,
            descripcion TEXT,
            ingredientes TEXT NOT NULL,
            instrucciones TEXT NOT NULL,
            tiempo_preparacion INT DEFAULT 0, -- en minutos
            porciones INT DEFAULT 1,
            dificultad ENUM('Fácil', 'Intermedio', 'Difícil') DEFAULT 'Fácil',
            categoria_id INT,
            imagen_url VARCHAR(500),
            autor VARCHAR(100) DEFAULT 'Anónimo',
            es_premium BOOLEAN DEFAULT FALSE,
            vistas INT DEFAULT 0,
            likes INT DEFAULT 0,
            activo BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            
            FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL,
            
            INDEX idx_categoria (categoria_id),
            INDEX idx_es_premium (es_premium),
            INDEX idx_dificultad (dificultad),
            INDEX idx_activo (activo),
            INDEX idx_created_at (created_at),
            FULLTEXT idx_busqueda (titulo, descripcion, ingredientes)
        ) ENGINE=InnoDB;
        """)

        # --- Tabla de planes de suscripción ---
        print("Creando tabla 'planes_suscripcion'...")
        cursor.execute("""
        CREATE TABLE planes_suscripcion (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            precio DECIMAL(10,2) NOT NULL,
            duracion_dias INT NOT NULL,
            descripcion TEXT,
            activo BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            
            INDEX idx_activo (activo)
        ) ENGINE=InnoDB;
        """)

        # --- Tabla de valoraciones ---
        print("Creando tabla 'valoraciones'...")
        cursor.execute("""
        CREATE TABLE valoraciones (
            id INT AUTO_INCREMENT PRIMARY KEY,
            receta_id INT NOT NULL,
            usuario_id INT NULL,
            puntuacion INT CHECK (puntuacion >= 1 AND puntuacion <= 5),
            comentario TEXT,
            nombre_usuario VARCHAR(100),
            activo BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (receta_id) REFERENCES recetas(id) ON DELETE CASCADE,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
            
            INDEX idx_receta (receta_id),
            INDEX idx_usuario (usuario_id),
            INDEX idx_puntuacion (puntuacion)
        ) ENGINE=InnoDB;
        """)

        # --- Tabla de favoritos ---
        print("Creando tabla 'favoritos'...")
        cursor.execute("""
        CREATE TABLE favoritos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario_id INT NOT NULL,
            receta_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (receta_id) REFERENCES recetas(id) ON DELETE CASCADE,
            
            UNIQUE KEY unique_favorito (usuario_id, receta_id),
            INDEX idx_usuario (usuario_id),
            INDEX idx_receta (receta_id)
        ) ENGINE=InnoDB;
        """)

        # --- Tabla de logs de actividad ---
        print("Creando tabla 'logs_actividad'...")
        cursor.execute("""
        CREATE TABLE logs_actividad (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario_id INT NULL,
            accion VARCHAR(100) NOT NULL,
            tabla_afectada VARCHAR(50),
            registro_id INT,
            ip_address VARCHAR(45),
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
            
            INDEX idx_usuario (usuario_id),
            INDEX idx_accion (accion),
            INDEX idx_created_at (created_at)
        ) ENGINE=InnoDB;
        """)

        print("Tablas de suscripción y otras funcionalidades creadas exitosamente.")

        # --- Insertar datos de ejemplo ---
        # Insertar planes de suscripción
        print("Insertando planes de suscripción de ejemplo...")
        planes_data = [
            ('Mensual', 9.99, 30, 'Acceso completo por 1 mes'),
            ('Trimestral', 24.99, 90, 'Acceso completo por 3 meses (17% descuento)'),
            ('Anual', 79.99, 365, 'Acceso completo por 1 año (33% descuento)')
        ]
        cursor.executemany("INSERT INTO planes_suscripcion (nombre, precio, duracion_dias, descripcion) VALUES (%s, %s, %s, %s)", planes_data)
        conn.commit()
        print(f"{cursor.rowcount} planes de suscripción insertados.")

        # Insertar usuario administrador (contraseña: admin123)
        print("Insertando usuario administrador (admin@recetas.com, admin123)...")
        admin_password_hash = pwd_context.hash("admin123")
        cursor.execute("INSERT INTO usuarios (nombre, email, password_hash, tipo_suscripcion) VALUES (%s, %s, %s, %s)",
                       ('Administrador', 'admin@recetas.com', admin_password_hash, 'premium'))
        conn.commit()
        print("Usuario administrador insertado.")

        print("Esquema de base de datos actualizado y datos iniciales insertados.")

        # Habilitar comprobación de claves foráneas de nuevo
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    except Error as e:
        print(f"Error al actualizar el esquema de la base de datos: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            print("Conexión a MySQL cerrada.")

if __name__ == '__main__':
    update_database_schema()