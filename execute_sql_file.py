import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
import re

# Configurar el contexto de hasheo de contraseñas
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# --- Configuración de la Base de Datos ---
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = "delishare_db" # Aseguramos que siempre sea delishare_db

def execute_sql_from_file(sql_file_path):
    conn = None
    cursor = None
    try:
        # Conexión inicial al servidor MySQL (sin especificar BD)
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Leer el contenido del archivo SQL
        with open(sql_file_path, 'r', encoding='utf8') as f:
            sql_content = f.read()

        # --- Modificaciones al SQL en memoria ---
        # 1. Cambiar el nombre de la base de datos
        sql_content = sql_content.replace('recetas_cocina_prueba', DB_NAME)

        # 2. Cambiar 'password' a 'password_hash' en la tabla usuarios
        sql_content = sql_content.replace('password VARCHAR(255) NOT NULL,', 'password_hash VARCHAR(255) NOT NULL,')

        # 3. Generar hash para admin123 y reemplazar en el SQL
        admin_password_hash = pwd_context.hash("admin123")
        # La contraseña original en el SQL es '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi'
        sql_content = sql_content.replace("'$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi'", f"'{admin_password_hash}'")

        # 4. Eliminar DELIMITER y manejar procedimientos almacenados
        # Extraer el procedimiento almacenado
        procedure_match = re.search(r'CREATE PROCEDURE.*?END //', sql_content, re.DOTALL)
        procedure_sql = ""
        if procedure_match:
            procedure_sql = procedure_match.group(0).replace('END //', 'END').replace('DELIMITER //', '').replace('DELIMITER ;', '')
            sql_content = sql_content.replace(procedure_match.group(0), '') # Eliminarlo del contenido principal

        # Eliminar cualquier otro DELIMITER que pueda quedar
        sql_content = sql_content.replace('DELIMITER //', '').replace('DELIMITER ;', '')

        # Dividir comandos por ;
        sql_commands = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip() and not cmd.strip().startswith('--')]

        # Ejecutar comandos uno por uno
        print(f"Ejecutando SQL en la base de datos '{DB_NAME}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        cursor.execute(f"USE {DB_NAME};")
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        for command in sql_commands:
            try:
                # Evitar ejecutar CREATE DATABASE y USE de nuevo si ya lo hicimos
                if not command.upper().startswith(('CREATE DATABASE', 'USE ')): 
                    cursor.execute(command)
            except Error as e:
                print(f"Error al ejecutar comando SQL: {command[:50]}... Error: {e}")
                # Continuar con el siguiente comando o abortar, según la necesidad

        # Ejecutar el procedimiento almacenado si se encontró
        if procedure_sql:
            print("Ejecutando procedimiento almacenado...")
            try:
                cursor.execute(procedure_sql)
            except Error as e:
                print(f"Error al ejecutar procedimiento almacenado: {e}")

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        conn.commit()
        print("SQL ejecutado exitosamente y base de datos actualizada.")

    except Error as e:
        print(f"Error de base de datos: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            print("Conexión a MySQL cerrada.")

if __name__ == '__main__':
    sql_file = "C:\\xampp\\htdocs\\Delishare\\RECETAS-API\\database\\recetas_db.sql"
    execute_sql_from_file(sql_file)