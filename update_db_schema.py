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
DB_NAME = "recetas_cocina_prueba"

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
            database=DB_NAME,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
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
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

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
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_activo (activo)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        print("Tablas de suscripción y otras funcionalidades creadas exitosamente.")

        # --- Insertar datos de ejemplo ---
        # Insertar categorías de ejemplo
        print("Insertando categorías de ejemplo...")
        categorias_data = [
            ('Desayunos', 'Recetas para comenzar el día', 'fas fa-coffee', 1),
            ('Almuerzos', 'Comidas principales del mediodía', 'fas fa-hamburger', 2),
            ('Cenas', 'Recetas para la noche', 'fas fa-moon', 3),
            ('Postres', 'Dulces y postres deliciosos', 'fas fa-ice-cream', 4),
            ('Bebidas', 'Jugos, batidos y bebidas', 'fas fa-glass-cheers', 5),
            ('Aperitivos', 'Entradas y bocadillos', 'fas fa-cheese', 6),
            ('Vegetarianas', 'Recetas sin carne', 'fas fa-leaf', 7),
            ('Veganas', 'Recetas completamente vegetales', 'fas fa-seedling', 8)
        ]
        cursor.executemany("INSERT INTO categorias (nombre, descripcion, icono, orden) VALUES (%s, %s, %s, %s)", categorias_data)
        conn.commit()
        print(f"{cursor.rowcount} categorías insertadas.")

        # Insertar recetas de ejemplo
        print("Insertando recetas de ejemplo...")
        recetas_data = [
            ('Pancakes Esponjosos', 'Deliciosos pancakes perfectos para el desayuno familiar',
             '2 tazas de harina todo uso\n1 taza de leche entera\n2 huevos grandes\n2 cucharadas de azúcar\n1 cucharadita de polvo de hornear\nPizca de sal\nMantequilla para cocinar\nMiel o jarabe de maple para servir',
             '1. En un bowl grande, mezclar todos los ingredientes secos: harina, azúcar, polvo de hornear y sal\n2. En otro bowl, batir los huevos con la leche hasta integrar completamente\n3. Verter la mezcla líquida sobre los ingredientes secos y mezclar hasta obtener una masa homogénea (no sobre mezclar)\n4. Calentar una sartén antiadherente a fuego medio y agregar un poco de mantequilla\n5. Verter 1/4 taza de masa por cada pancake\n6. Cocinar 2-3 minutos hasta que aparezcan burbujas en la superficie\n7. Voltear cuidadosamente y cocinar 1-2 minutos más hasta dorar\n8. Servir inmediatamente con miel o jarabe de maple caliente',
             20, 4, 'Fácil', 1, 'Chef María González', False),
            ('Ensalada César Gourmet', 'La clásica ensalada César con un toque gourmet y aderezo casero',
             '2 lechugas romanas grandes\n4 rebanadas de pan integral\n100g de queso parmesano\n2 pechugas de pollo\n1/2 taza de aceite de oliva extra virgen\n2 limones\n3 dientes de ajo\n1 cucharada de mostaza Dijon\n4 filetes de anchoas\n1 huevo\nSal y pimienta negra recién molida',
             '1. Lavar y secar completamente las lechugas, cortar en trozos medianos\n2. Para el aderezo: en un bowl pequeño, machacar el ajo con sal hasta formar una pasta\n3. Agregar mostaza Dijon, anchoas picadas y mezclar bien\n4. Incorporar el jugo de limón y batir mientras se agrega el aceite de oliva lentamente\n5. Agregar el huevo y batir hasta obtener una consistencia cremosa\n6. Sazonar con pimienta negra recién molida\n7. Cortar el pan en cubos y tostar en el horno hasta dorar\n8. Cocinar las pechugas de pollo con sal, pimienta y hierbas hasta dorar completamente\n9. Dejar reposar el pollo 5 minutos y cortar en tiras\n10. En un bowl grande, mezclar la lechuga con el aderezo\n11. Agregar el pollo en tiras y los crutones\n12. Espolvorear generosamente con queso parmesano rallado\n13. Servir inmediatamente acompañado de pan tostado',
             35, 2, 'Intermedio', 2, 'Chef Carlos Mendoza', True)
        ]
        cursor.executemany("INSERT INTO recetas (titulo, descripcion, ingredientes, instrucciones, tiempo_preparacion, porciones, dificultad, categoria_id, autor, es_premium) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", recetas_data)
        conn.commit()
        print(f"{cursor.rowcount} recetas insertadas.")

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