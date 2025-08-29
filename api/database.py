import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector import Error
from .config import settings

# Crear un "pool" de conexiones para reutilizar conexiones y mejorar el rendimiento
try:
    pool = MySQLConnectionPool(
        pool_name="delishare_pool",
        pool_size=5,
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        charset='utf8mb4'
    )
    print("Pool de conexiones a la base de datos creado exitosamente.")

except Error as e:
    print(f"Error al crear el pool de conexiones a la base de datos: {e}")
    pool = None

def get_db_connection():
    """Obtiene una conexión del pool."""
    if pool is None:
        raise ConnectionError("El pool de conexiones no está disponible.")
    
    try:
        # Obtener una conexión del pool
        conn = pool.get_connection()
        if conn.is_connected():
            return conn
        else:
            # Si la conexión no es válida, intentar reconectar (aunque el pool debería manejar esto)
            conn.reconnect()
            return conn
            
    except Error as e:
        print(f"Error al obtener una conexión de la base de datos: {e}")
        return None

# Ejemplo de cómo se usaría (no se ejecuta directamente):
#
# def alguna_funcion_de_api():
#     conn = None
#     cursor = None
#     try:
#         conn = get_db_connection()
#         if conn:
#             cursor = conn.cursor(dictionary=True)
#             cursor.execute("SELECT * FROM recetas")
#             resultados = cursor.fetchall()
#             return resultados
#     except Error as e:
#         print(f"Error en la consulta: {e}")
#         return {"error": "No se pudo realizar la consulta"}
#     finally:
#         if cursor:
#             cursor.close()
#         if conn and conn.is_connected():
#             conn.close() # Devuelve la conexión al pool
