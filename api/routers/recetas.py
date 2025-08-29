from flask import Blueprint, jsonify, abort, request
from mysql.connector import Error
from typing import Optional

from ..database import get_db_connection
from ..models.receta import Receta, RecetaCreate
from ..models.categoria import Categoria

recetas_bp = Blueprint('recetas', __name__)

# --- Repositorio de Categorías ---
class CategoriaRepository:
    def get_all_categorias(self):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if conn is None:
                raise ConnectionError("No se pudo conectar a la base de datos.")
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, nombre, descripcion, icono, activo, orden, created_at FROM categorias ORDER BY nombre ASC")
            categorias_data = cursor.fetchall()
            return [Categoria(**data) for data in categorias_data]
        except Error as e:
            raise RuntimeError(f"Error de base de datos al obtener categorías: {e}")
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    def get_categoria_by_id(self, categoria_id: int):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if conn is None:
                raise ConnectionError("No se pudo conectar a la base de datos.")
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, nombre, descripcion, icono, activo, orden, created_at FROM categorias WHERE id = %s", (categoria_id,))
            categoria_data = cursor.fetchone()
            if categoria_data:
                return Categoria(**categoria_data)
            return None
        except Error as e:
            raise RuntimeError(f"Error de base de datos al obtener categoría por ID: {e}")
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

categoria_repository = CategoriaRepository()

# --- Repositorio de Recetas ---
class RecetaRepository:
    def get_all_recetas(self, search_term: Optional[str] = None):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if conn is None:
                raise ConnectionError("No se pudo conectar a la base de datos.")
            cursor = conn.cursor(dictionary=True)
            
            base_query = ("SELECT r.*, c.nombre as categoria_nombre "
                          "FROM recetas r LEFT JOIN categorias c ON r.categoria_id = c.id "
                          "WHERE r.activo = TRUE")
            
            if search_term:
                query = f"{base_query} AND (r.titulo LIKE %s OR r.ingredientes LIKE %s)"
                params = (f"%{search_term}%", f"%{search_term}%")
            else:
                query = f"{base_query} ORDER BY r.created_at DESC"
                params = ()
                
            cursor.execute(query, params)
            recetas_data = cursor.fetchall()
            return [Receta(**data) for data in recetas_data]

        except Error as e:
            raise RuntimeError(f"Error de base de datos al obtener recetas: {e}")
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    def get_receta_by_id(self, recipe_id: int):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if conn is None:
                raise ConnectionError("No se pudo conectar a la base de datos.")
            cursor = conn.cursor(dictionary=True)
            
            query = ("SELECT r.*, c.nombre as categoria_nombre "
                     "FROM recetas r LEFT JOIN categorias c ON r.categoria_id = c.id "
                     "WHERE r.id = %s AND r.activo = TRUE")
            
            cursor.execute(query, (recipe_id,))
            receta_data = cursor.fetchone()
            
            if receta_data:
                return Receta(**receta_data)
            return None

        except Error as e:
            raise RuntimeError(f"Error de base de datos al obtener receta por ID: {e}")
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    def create_receta(self, receta: RecetaCreate):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if conn is None:
                raise ConnectionError("No se pudo conectar a la base de datos.")
            cursor = conn.cursor()
            
            query = ("INSERT INTO recetas (titulo, descripcion, ingredientes, instrucciones, tiempo_preparacion, "
                     "porciones, dificultad, categoria_id, imagen_url, autor, es_premium) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            
            params = (
                receta.titulo,
                receta.descripcion,
                receta.ingredientes,
                receta.instrucciones,
                receta.tiempo_preparacion,
                receta.porciones,
                receta.dificultad,
                receta.categoria_id,
                receta.imagen_url,
                receta.autor,
                receta.es_premium
            )
            
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid

        except Error as e:
            raise RuntimeError(f"Error de base de datos al crear la receta: {e}")
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

receta_repository = RecetaRepository()

# --- Rutas para Categorías ---
@recetas_bp.route("/categorias", methods=['GET'])
def obtener_categorias():
    """Obtiene una lista de todas las categorías."""
    try:
        categorias = categoria_repository.get_all_categorias()
        return jsonify([cat.dict() for cat in categorias])
    except RuntimeError as e:
        abort(500, description=f"Error interno del servidor: {e}")
    except ConnectionError as e:
        abort(500, description=f"Error de conexión a la base de datos: {e}")

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
    except RuntimeError as e:
        abort(500, description=f"Error interno del servidor: {e}")
    except ConnectionError as e:
        abort(500, description=f"Error de conexión a la base de datos: {e}")

@recetas_bp.route("/<int:recipe_id>", methods=['GET'])
def obtener_receta_por_id(recipe_id):
    """Obtiene los detalles de una receta específica por su ID."""
    try:
        receta = receta_repository.get_receta_by_id(recipe_id)
        if receta is None:
            abort(404, description="Receta no encontrada.")
        return jsonify(receta.dict())
    except RuntimeError as e:
        abort(500, description=f"Error interno del servidor: {e}")
    except ConnectionError as e:
        abort(500, description=f"Error de conexión a la base de datos: {e}")

@recetas_bp.route("/", methods=['POST'])
def crear_receta():
    """Crea una nueva receta."""
    try:
        receta_data = RecetaCreate(**request.get_json())
    except Exception as e:
        abort(400, description=f"Datos de entrada inválidos: {e}")

    try:
        new_recipe_id = receta_repository.create_receta(receta_data)
        return jsonify({"success": True, "message": "Receta creada exitosamente", "id": new_recipe_id}), 201
    except RuntimeError as e:
        abort(500, description=f"Error de base de datos al crear la receta: {e}")
    except ConnectionError as e:
        abort(500, description=f"Error de conexión a la base de datos: {e}")
