from flask import Blueprint, request, jsonify, abort
from mysql.connector import Error
from passlib.context import CryptContext

from ..database import get_db_connection
from ..models.usuario import UsuarioCreate, Usuario, UsuarioInDB

# Configurar el contexto de hasheo de contraseñas
pwd_context = CryptContext(schemes=["bcrypt", "sha256_crypt"], deprecated="auto")

auth_bp = Blueprint('auth', __name__)

# --- Repositorio de Usuarios (Abstracción de DB) ---
class UserRepository:
    def get_user_by_email(self, email: str):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if conn is None:
                raise ConnectionError("No se pudo conectar a la base de datos.")
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, nombre, email, password_hash, tipo_suscripcion, fecha_suscripcion, fecha_vencimiento, activo, intentos_login, bloqueado_hasta, ultimo_login, created_at, updated_at FROM usuarios WHERE email = %s", (email,))
            user_data = cursor.fetchone()
            if user_data:
                return UsuarioInDB(**user_data)
            return None
        except Error as e:
            raise RuntimeError(f"Error de base de datos al buscar usuario: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def create_user(self, user: UsuarioCreate, password_hash: str):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if conn is None:
                raise ConnectionError("No se pudo conectar a la base de datos.")
            cursor = conn.cursor()
            query = "INSERT INTO usuarios (nombre, email, password_hash) VALUES (%s, %s, %s)"
            cursor.execute(query, (user.nombre, user.email, password_hash))
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            raise RuntimeError(f"Error de base de datos al crear usuario: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

user_repository = UserRepository()

@auth_bp.route("/register", methods=['POST'])
def register_user():
    """
    Registra un nuevo usuario en la base de datos.
    """
    try:
        user_data = UsuarioCreate(**request.get_json())
    except Exception as e:
        abort(400, description=f"Datos de entrada inválidos: {e}")

    try:
        if user_repository.get_user_by_email(user_data.email):
            abort(409, description="Este correo electrónico ya está registrado.")

        password_hash = pwd_context.hash(user_data.password)
        new_user_id = user_repository.create_user(user_data, password_hash)
        
        # Obtener el usuario recién creado para devolverlo
        # Aquí deberíamos obtener el usuario completo de la DB para asegurar que todos los campos estén correctos
        new_user_in_db = user_repository.get_user_by_email(user_data.email)
        if new_user_in_db:
            # Convertir a modelo de respuesta pública
            new_user = Usuario(**new_user_in_db.dict())
            return jsonify({"success": True, "user": new_user.dict()}), 201
        else:
            abort(500, description="Error al recuperar el usuario recién creado.")

    except RuntimeError as e:
        abort(500, description=f"Error interno del servidor: {e}")
    except ConnectionError as e:
        abort(500, description=f"Error de conexión a la base de datos: {e}")
    except Error as e:
        abort(500, description=f"Error de base de datos: {e}")

    finally:
        # Las conexiones se cierran dentro del repositorio
        pass

@auth_bp.route("/login", methods=['POST'])
def login_user():
    """
    Autentica a un usuario y devuelve sus datos si es exitoso.
    """
    data = request.get_json()
    if not data or not 'email' in data or not 'password' in data:
        abort(400, description="Faltan datos: email y password son requeridos.")

    email = data['email']
    password = data['password']

    try:
        user_in_db = user_repository.get_user_by_email(email)

        # Verificar si el usuario existe y la contraseña es correcta
        if user_in_db and pwd_context.verify(password, user_in_db.password_hash):
            # Calcular si la suscripción está activa
            from datetime import date
            is_active = False
            if user_in_db.tipo_suscripcion == 'premium' and user_in_db.fecha_vencimiento:
                if user_in_db.fecha_vencimiento >= date.today():
                    is_active = True
            
            # Convertir a modelo de respuesta pública
            user_response = Usuario(**user_in_db.dict())
            user_dict = user_response.dict()
            user_dict['suscripcion_activa'] = is_active
            return jsonify({"success": True, "user": user_dict})
        else:
            # Error de autenticación genérico para no dar pistas
            abort(401, description="Email o contraseña incorrectos.")

    except RuntimeError as e:
        abort(500, description=f"Error interno del servidor: {e}")
    except ConnectionError as e:
        abort(500, description=f"Error de conexión a la base de datos: {e}")
    except Error as e:
        abort(500, description=f"Error de base de datos: {e}")
