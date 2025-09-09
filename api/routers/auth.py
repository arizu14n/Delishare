from flask import Blueprint, request, jsonify, abort
from werkzeug.exceptions import HTTPException
import re
from passlib.context import CryptContext
from datetime import date
from ..utils import sanitize_input

from ..database import get_db_session
from ..models.usuario import UsuarioCreate, Usuario, UsuarioInDB, UsuarioDB

# Configurar el contexto de hasheo de contraseñas
pwd_context = CryptContext(schemes=["bcrypt", "sha256_crypt"], deprecated="auto")

auth_bp = Blueprint('auth', __name__)

# --- Repositorio de Usuarios (Abstracción de DB) ---
class UserRepository:
    def __init__(self):
        self.db_session = get_db_session()

    def get_user_by_email(self, email: str) -> UsuarioInDB | None:
        user_db = self.db_session.query(UsuarioDB).filter(UsuarioDB.email == email).first()
        if user_db:
            return UsuarioInDB.from_orm(user_db)
        return None

    def create_user(self, user: UsuarioCreate, password_hash: str) -> UsuarioInDB:
        user_db = UsuarioDB(
            nombre=user.nombre,
            email=user.email,
            password_hash=password_hash
        )
        self.db_session.add(user_db)
        self.db_session.commit()
        self.db_session.refresh(user_db)
        return UsuarioInDB.from_orm(user_db)

user_repository = UserRepository()

@auth_bp.route("/register", methods=['POST'])
def register_user():
    """
    Registra un nuevo usuario en la base de datos.
    """
    if not request.is_json:
        abort(400, description="La solicitud debe ser de tipo JSON.")

    try:
        user_data = UsuarioCreate(**sanitize_input(request.get_json()))
    except Exception as e:
        abort(400, description=f"Datos de entrada inválidos: {e}")

    # La validación de la contraseña con RegEx ya se hace en el modelo de Pydantic (UsuarioCreate)
    # pero la mantenemos aquí como doble chequeo por si el modelo cambia.
    password_regex = r"^[a-zA-Z0-9!@#$%^&*]{8,20}$"
    if not re.match(password_regex, user_data.password):
        abort(400, description="La contraseña no cumple con los requisitos de formato (8-20 caracteres, sin espacios).")

    try:
        if user_repository.get_user_by_email(user_data.email):
            abort(409, description="Este correo electrónico ya está registrado.")

        password_hash = pwd_context.hash(user_data.password)
        new_user_in_db = user_repository.create_user(user_data, password_hash)
        
        if new_user_in_db:
            new_user = Usuario.from_orm(new_user_in_db)
            return jsonify({"success": True, "user": new_user.dict()}), 201
        else:
            abort(500, description="Error al crear el usuario.")

    except HTTPException as e:
        # Re-lanza las excepciones HTTP (como abort) para que Flask las maneje
        raise e
    except Exception as e:
        # Atrapa otros errores inesperados
        abort(500, description=f"Error interno del servidor: {e}")


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

        if user_in_db and pwd_context.verify(password, user_in_db.password_hash):
            is_active = False
            if user_in_db.tipo_suscripcion == 'premium' and user_in_db.fecha_vencimiento:
                if user_in_db.fecha_vencimiento >= date.today():
                    is_active = True
            
            user_response = Usuario.from_orm(user_in_db)
            user_dict = user_response.dict()
            user_dict['suscripcion_activa'] = is_active
            return jsonify({"success": True, "user": user_dict})
        else:
            abort(401, description="Email o contraseña incorrectos.")

    except Exception as e:
        abort(500, description=f"Error interno del servidor: {e}")
