import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# --- Configuración de la Base de Datos ---
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "delishare_db")

def drop_database():
    """
    Se conecta a MySQL y borra la base de datos del proyecto.
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
    # Una pequeña confirmación para evitar ejecuciones accidentales
    confirm = input(f"¿Estás seguro de que quieres borrar TODA la base de datos '{DB_NAME}'? Esto no se puede deshacer. (escribe 'si' para confirmar): ")
    if confirm.lower() == 'si':
        drop_database()
    else:
        print("Operación cancelada.")
