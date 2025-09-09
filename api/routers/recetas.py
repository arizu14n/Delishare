from flask import Blueprint, jsonify, abort, request
from sqlalchemy.orm import joinedload
from typing import Optional
import bleach
from ..utils import sanitize_input
from ..database import get_db_session
from ..models.receta import Receta, RecetaCreate, RecetaDB
from ..models.categoria import Categoria, CategoriaDB

recetas_bp = Blueprint('recetas', __name__)

# --- Repositorio de Categorías ---
class CategoriaRepository:
    def __init__(self):
        self.db_session = get_db_session()

    def get_all_categorias(self) -> list[Categoria]:
        categorias_db = self.db_session.query(CategoriaDB).order_by(CategoriaDB.nombre.asc()).all()
        return [Categoria.from_orm(cat) for cat in categorias_db]

    def get_categoria_by_id(self, categoria_id: int) -> Optional[Categoria]:
        categoria_db = self.db_session.query(CategoriaDB).filter(CategoriaDB.id == categoria_id).first()
        if categoria_db:
            return Categoria.from_orm(categoria_db)
        return None

categoria_repository = CategoriaRepository()

# --- Repositorio de Recetas ---
class RecetaRepository:
    def __init__(self):
        self.db_session = get_db_session()

    def get_all_recetas(self, search_term: Optional[str] = None) -> list[Receta]:
        query = self.db_session.query(RecetaDB).options(joinedload(RecetaDB.categoria)).filter(RecetaDB.activo == True)

        if search_term:
            search_pattern = f"%{search_term}%"
            query = query.filter(RecetaDB.titulo.ilike(search_pattern) | RecetaDB.ingredientes.ilike(search_pattern))

        recetas_db = query.order_by(RecetaDB.created_at.desc()).all()
        
        recetas = []
        for rec in recetas_db:
            receta_pydantic = Receta.from_orm(rec)
            if rec.categoria:
                receta_pydantic.categoria_nombre = rec.categoria.nombre
            recetas.append(receta_pydantic)
        return recetas

    def get_receta_by_id(self, recipe_id: int) -> Optional[Receta]:
        receta_db = self.db_session.query(RecetaDB).options(joinedload(RecetaDB.categoria)).filter(RecetaDB.id == recipe_id, RecetaDB.activo == True).first()
        
        if receta_db:
            receta_pydantic = Receta.from_orm(receta_db)
            if receta_db.categoria:
                receta_pydantic.categoria_nombre = receta_db.categoria.nombre
            return receta_pydantic
        return None

    def create_receta(self, receta: RecetaCreate) -> int:
        receta_db = RecetaDB(**receta.dict())
        self.db_session.add(receta_db)
        self.db_session.commit()
        self.db_session.refresh(receta_db)
        return receta_db.id

receta_repository = RecetaRepository()

# --- Rutas para Categorías ---
@recetas_bp.route("/categorias", methods=['GET'])
def obtener_categorias():
    """Obtiene una lista de todas las categorías.""" 
    try:
        categorias = categoria_repository.get_all_categorias()
        return jsonify([cat.dict() for cat in categorias])
    except Exception as e:
        abort(500, description=f"Error interno del servidor: {e}")

# --- Rutas para Recetas ---
@recetas_bp.route("/", methods=['GET'])
def obtener_recetas():
    """
    Obtiene una lista de todas las recetas o busca recetas por un término.
    Acepta un parámetro de búsqueda 'search'.
    """
    search_term = request.args.get('search', None)
    
    try:
        recetas = receta_repository.get_all_recetas(search_term)
        return jsonify([rec.dict() for rec in recetas])
    except Exception as e:
        abort(500, description=f"Error interno del servidor: {e}")

@recetas_bp.route("/<int:recipe_id>", methods=['GET'])
def obtener_receta_por_id(recipe_id):
    """Obtiene los detalles de una receta específica por su ID."""
    try:
        receta = receta_repository.get_receta_by_id(recipe_id)
        if receta is None:
            abort(404, description="Receta no encontrada.")
        return jsonify(receta.dict())
    except Exception as e:
        abort(500, description=f"Error interno del servidor: {e}")

@recetas_bp.route("/", methods=['POST'])
def crear_receta():
    """Crea una nueva receta."""
    if not request.is_json:
        abort(400, description="La solicitud debe ser de tipo JSON.")
        
    try:
        raw_data = request.get_json()
        sanitized_data = sanitize_input(raw_data)
        receta_data = RecetaCreate(**sanitized_data)
    except Exception as e:
        abort(400, description=f"Datos de entrada inválidos: {e}")

    try:
        new_recipe_id = receta_repository.create_receta(receta_data)
        return jsonify({"success": True, "message": "Receta creada exitosamente", "id": new_recipe_id}), 201
    except Exception as e:
        abort(500, description=f"Error de base de datos al crear la receta: {e}")