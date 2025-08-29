import mysql.connector
from mysql.connector import Error
import os

# --- Configuración de la Base de Datos (HARDCODED) ---
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = "delishare_db" # Nombre hardcodeado para asegurar que sea el correcto

def drop_database_noninteractive():
    """
    Se conecta a MySQL y borra la base de datos del proyecto sin pedir confirmación.
    """
    try:
        print(f"Conectando al servidor MySQL en '{DB_HOST}'...")
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        print(f"Borrando la base de datos '{DB_NAME}' si existe...")
        cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
        
        print(f"Base de datos '{DB_NAME}' borrada exitosamente.")
        cursor.close()
        conn.close()

    except Error as e:
        print(f"Error al borrar la base de datos: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn and conn.is_connected():
            conn.close()
            print("Conexión a MySQL cerrada.")

if __name__ == '__main__':
    print("Ejecutando borrado no interactivo de la base de datos...")
    drop_database_noninteractive()