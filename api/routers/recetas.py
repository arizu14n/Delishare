# -*- coding: utf-8 -*-
"""
Define las rutas para la gestión de recetas y categorías.

Este archivo contiene:
- Un `CategoriaRepository` para obtener datos de las categorías.
- Un `RecetaRepository` para realizar operaciones CRUD (Crear, Leer) en las recetas.
- Rutas para obtener todas las categorías.
- Rutas para obtener, buscar y crear recetas.
"""

from flask import Blueprint, jsonify, abort, request
from sqlalchemy.orm import joinedload
from typing import Optional

from ..database import get_db_session
from ..models.receta import Receta, RecetaCreate, RecetaDB
from ..models.categoria import Categoria, CategoriaDB

# Crear un Blueprint para las rutas relacionadas con las recetas.
recetas_bp = Blueprint('recetas', __name__)

# --- Repositorio de Categorías ---
class CategoriaRepository:
    """
    Clase que encapsula el acceso a la base de datos para las categorías.
    """
    def __init__(self):
        self.db_session = get_db_session()

    def get_all_categorias(self) -> list[Categoria]:
        """
        Obtiene todas las categorías de la base de datos, ordenadas por nombre.

        Returns:
            Una lista de objetos `Categoria` de Pydantic.
        """
        categorias_db = self.db_session.query(CategoriaDB).order_by(CategoriaDB.nombre.asc()).all()
        # Convierte los objetos SQLAlchemy (CategoriaDB) a objetos Pydantic (Categoria).
        return [Categoria.from_orm(cat) for cat in categorias_db]

    def get_categoria_by_id(self, categoria_id: int) -> Optional[Categoria]:
        """
        Obtiene una categoría por su ID.

        Args:
            categoria_id: El ID de la categoría a buscar.

        Returns:
            Un objeto `Categoria` si se encuentra, o `None`.
        """
        categoria_db = self.db_session.query(CategoriaDB).filter(CategoriaDB.id == categoria_id).first()
        if categoria_db:
            return Categoria.from_orm(categoria_db)
        return None

# Instancia única del repositorio de categorías.
categoria_repository = CategoriaRepository()

# --- Repositorio de Recetas ---
class RecetaRepository:
    """
    Clase que encapsula el acceso a la base de datos para las recetas.
    """
    def __init__(self):
        self.db_session = get_db_session()

    def get_all_recetas(self, search_term: Optional[str] = None) -> list[Receta]:
        """
        Obtiene todas las recetas activas, con opción de búsqueda.

        Args:
            search_term: Un término de búsqueda opcional para filtrar por título o ingredientes.

        Returns:
            Una lista de objetos `Receta` de Pydantic.
        """
        # `joinedload(RecetaDB.categoria)` optimiza la consulta cargando la categoría
        # relacionada en la misma consulta (evita el problema N+1).
        query = self.db_session.query(RecetaDB).options(joinedload(RecetaDB.categoria)).filter(RecetaDB.activo == True)

        if search_term:
            # `ilike` realiza una búsqueda insensible a mayúsculas y minúsculas.
            query = query.filter(RecetaDB.titulo.ilike(f"%{search_term}%") | RecetaDB.ingredientes.ilike(f"%{search_term}%"))

        recetas_db = query.order_by(RecetaDB.created_at.desc()).all()

        # Mapear los resultados de la base de datos a los modelos Pydantic.
        recetas = []
        for rec in recetas_db:
            receta_pydantic = Receta.from_orm(rec)
            # Asignar el nombre de la categoría al modelo Pydantic.
            if rec.categoria:
                receta_pydantic.categoria_nombre = rec.categoria.nombre
            recetas.append(receta_pydantic)
        return recetas

    def get_receta_by_id(self, recipe_id: int) -> Optional[Receta]:
        """
        Obtiene una receta específica por su ID.

        Args:
            recipe_id: El ID de la receta a buscar.

        Returns:
            Un objeto `Receta` si se encuentra, o `None`.
        """
        receta_db = self.db_session.query(RecetaDB).options(joinedload(RecetaDB.categoria)).filter(RecetaDB.id == recipe_id, RecetaDB.activo == True).first()

        if receta_db:
            receta_pydantic = Receta.from_orm(receta_db)
            if receta_db.categoria:
                receta_pydantic.categoria_nombre = receta_db.categoria.nombre
            return receta_pydantic
        return None

    def create_receta(self, receta: RecetaCreate) -> int:
        """
        Crea una nueva receta en la base de datos.

        Args:
            receta: Un objeto `RecetaCreate` con los datos de la nueva receta.

        Returns:
            El ID de la receta recién creada.
        """
        # `**receta.dict()` desempaqueta el diccionario del modelo Pydantic
        # para crear una nueva instancia del modelo SQLAlchemy `RecetaDB`.
        receta_db = RecetaDB(**receta.dict())
        self.db_session.add(receta_db)
        self.db_session.commit()
        self.db_session.refresh(receta_db)
        return receta_db.id

# Instancia única del repositorio de recetas.
receta_repository = RecetaRepository()

# --- Rutas para Categorías ---
@recetas_bp.route("/categorias", methods=['GET'])
def obtener_categorias():
    """Endpoint para obtener una lista de todas las categorías."""
    try:
        categorias = categoria_repository.get_all_categorias()
        return jsonify([cat.dict() for cat in categorias])
    except Exception as e:
        abort(500, description=f"Error interno del servidor: {e}")

# --- Rutas para Recetas ---
@recetas_bp.route("/", methods=['GET'])
def obtener_recetas():
    """
    Endpoint para obtener una lista de todas las recetas o buscar por un término.
    Acepta un parámetro de query `search` (ej: /recetas/?search=pollo).
    """
    search_term = request.args.get('search', None)

    try:
        recetas = receta_repository.get_all_recetas(search_term)
        return jsonify([rec.dict() for rec in recetas])
    except Exception as e:
        abort(500, description=f"Error interno del servidor: {e}")

@recetas_bp.route("/<int:recipe_id>", methods=['GET'])
def obtener_receta_por_id(recipe_id):
    """Endpoint para obtener los detalles de una receta específica por su ID."""
    try:
        receta = receta_repository.get_receta_by_id(recipe_id)
        if receta is None:
            abort(404, description="Receta no encontrada.")
        return jsonify(receta.dict())
    except Exception as e:
        abort(500, description=f"Error interno del servidor: {e}")

@recetas_bp.route("/", methods=['POST'])
def crear_receta():
    """Endpoint para crear una nueva receta."""
    if not request.is_json:
        abort(400, description="La solicitud debe ser de tipo JSON.")

    try:
        # Validar los datos de entrada con el modelo Pydantic.
        receta_data = RecetaCreate(**request.get_json())
    except Exception as e:
        abort(400, description=f"Datos de entrada inválidos: {e}")

    try:
        new_recipe_id = receta_repository.create_receta(receta_data)
        return jsonify({"success": True, "message": "Receta creada exitosamente", "id": new_recipe_id}), 201
    except Exception as e:
        abort(500, description=f"Error de base de datos al crear la receta: {e}")
