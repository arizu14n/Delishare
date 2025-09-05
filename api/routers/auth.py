# -*- coding: utf-8 -*-
"""
Define las rutas para la autenticación de usuarios (registro y login).

Este archivo contiene:
- Configuración del hasheo de contraseñas.
- Un `UserRepository` para abstraer las operaciones de base de datos para los usuarios.
- La ruta `/register` para crear nuevos usuarios.
- La ruta `/login` para autenticar usuarios existentes.
"""

from flask import Blueprint, request, jsonify, abort
from werkzeug.exceptions import HTTPException
import re
from passlib.context import CryptContext
from datetime import date

from ..database import get_db_session
from ..models.usuario import UsuarioCreate, Usuario, UsuarioInDB, UsuarioDB

# Configurar el contexto de hasheo de contraseñas.
# `passlib` es una biblioteca para manejar el hasheo de contraseñas de forma segura.
# Se definen los esquemas de hasheo a utilizar (bcrypt es el preferido).
pwd_context = CryptContext(schemes=["bcrypt", "sha256_crypt"], deprecated="auto")

# Crear un Blueprint para las rutas de autenticación.
# Los Blueprints permiten organizar las rutas en módulos.
auth_bp = Blueprint('auth', __name__)

# --- Repositorio de Usuarios (Abstracción de la Lógica de Base de Datos) ---
class UserRepository:
    """
    Clase que encapsula el acceso a la base de datos para los usuarios.
    Esto ayuda a mantener el código de las rutas más limpio y centrado en la lógica de la API.
    """
    def __init__(self):
        """
        Inicializa el repositorio obteniendo una sesión de la base de datos.
        """
        self.db_session = get_db_session()

    def get_user_by_email(self, email: str) -> UsuarioInDB | None:
        """
        Busca un usuario por su dirección de correo electrónico.

        Args:
            email: El email del usuario a buscar.

        Returns:
            Un objeto `UsuarioInDB` si se encuentra el usuario, o `None` en caso contrario.
        """
        user_db = self.db_session.query(UsuarioDB).filter(UsuarioDB.email == email).first()
        if user_db:
            # Convierte el objeto SQLAlchemy (UsuarioDB) a un objeto Pydantic (UsuarioInDB).
            return UsuarioInDB.from_orm(user_db)
        return None

    def create_user(self, user: UsuarioCreate, password_hash: str) -> UsuarioInDB:
        """
        Crea un nuevo usuario en la base de datos.

        Args:
            user: El objeto `UsuarioCreate` con los datos del nuevo usuario.
            password_hash: El hash de la contraseña del usuario.

        Returns:
            El objeto `UsuarioInDB` del usuario recién creado.
        """
        # Crea una instancia del modelo SQLAlchemy `UsuarioDB`.
        user_db = UsuarioDB(
            nombre=user.nombre,
            email=user.email,
            password_hash=password_hash
        )
        # Añade el nuevo usuario a la sesión y confirma la transacción.
        self.db_session.add(user_db)
        self.db_session.commit()
        # Refresca el objeto para obtener los datos generados por la base de datos (como el id).
        self.db_session.refresh(user_db)
        return UsuarioInDB.from_orm(user_db)

# Instancia única del repositorio de usuarios.
user_repository = UserRepository()

@auth_bp.route("/register", methods=['POST'])
def register_user():
    """
    Endpoint para registrar un nuevo usuario.

    Valida los datos de entrada, verifica que el email no exista, hashea la contraseña
    y crea el nuevo usuario en la base de datos.
    """
    if not request.is_json:
        abort(400, description="La solicitud debe ser de tipo JSON.")

    try:
        # Valida los datos del request contra el modelo Pydantic `UsuarioCreate`.
        user_data = UsuarioCreate(**request.get_json())
    except Exception as e:
        # Si la validación de Pydantic falla, devuelve un error 400.
        abort(400, description=f"Datos de entrada inválidos: {e}")

    # Doble chequeo de la contraseña (aunque Pydantic ya lo hace).
    # Es una buena práctica de seguridad tener múltiples capas de validación.
    password_regex = r"^[a-zA-Z0-9!@#$%^&*]{8,20}$"
    if not re.match(password_regex, user_data.password):
        abort(400, description="La contraseña no cumple con los requisitos de formato (8-20 caracteres, sin espacios).")

    try:
        # Verificar si el usuario ya existe.
        if user_repository.get_user_by_email(user_data.email):
            abort(409, description="Este correo electrónico ya está registrado.")

        # Hashear la contraseña antes de guardarla.
        password_hash = pwd_context.hash(user_data.password)
        # Crear el usuario en la base de datos.
        new_user_in_db = user_repository.create_user(user_data, password_hash)

        if new_user_in_db:
            # Convertir el usuario de la base de datos al modelo de respuesta `Usuario` (sin contraseña).
            new_user = Usuario.from_orm(new_user_in_db)
            # Devolver una respuesta exitosa con los datos del nuevo usuario.
            return jsonify({"success": True, "user": new_user.dict()}), 201
        else:
            abort(500, description="Error al crear el usuario.")

    except HTTPException as e:
        # Re-lanza las excepciones HTTP (generadas por `abort`) para que Flask las maneje.
        raise e
    except Exception as e:
        # Captura cualquier otro error inesperado y devuelve un error 500.
        abort(500, description=f"Error interno del servidor: {e}")


@auth_bp.route("/login", methods=['POST'])
def login_user():
    """
    Endpoint para autenticar a un usuario.

    Verifica el email y la contraseña. Si son correctos, devuelve los datos del usuario
    y el estado de su suscripción.
    """
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        abort(400, description="Faltan datos: email y password son requeridos.")

    email = data['email']
    password = data['password']

    try:
        # Obtener el usuario de la base de datos.
        user_in_db = user_repository.get_user_by_email(email)

        # Verificar si el usuario existe y si la contraseña es correcta.
        if user_in_db and pwd_context.verify(password, user_in_db.password_hash):
            # Comprobar el estado de la suscripción premium.
            is_active = False
            if user_in_db.tipo_suscripcion == 'premium' and user_in_db.fecha_vencimiento:
                if user_in_db.fecha_vencimiento >= date.today():
                    is_active = True

            # Preparar la respuesta con el modelo `Usuario` (sin contraseña).
            user_response = Usuario.from_orm(user_in_db)
            user_dict = user_response.dict()
            user_dict['suscripcion_activa'] = is_active
            return jsonify({"success": True, "user": user_dict})
        else:
            # Si el email o la contraseña son incorrectos, devolver un error 401.
            abort(401, description="Email o contraseña incorrectos.")

    except Exception as e:
        abort(500, description=f"Error interno del servidor: {e}")