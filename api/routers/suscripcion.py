from flask import Blueprint, jsonify, abort, request
from mysql.connector import Error
from datetime import date, timedelta

from ..database import get_db_connection
from ..models.suscripcion import PlanSuscripcion, SuscripcionUpdate

suscripcion_bp = Blueprint('suscripcion', __name__)

# --- Repositorio de Suscripciones ---
class SuscripcionRepository:
    def get_all_subscription_plans(self):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if conn is None:
                raise ConnectionError("No se pudo conectar a la base de datos.")
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, nombre, precio, duracion_dias, descripcion, activo, created_at FROM planes_suscripcion WHERE activo = TRUE ORDER BY precio ASC")
            plans_data = cursor.fetchall()
            return [PlanSuscripcion(**data) for data in plans_data]
        except Error as e:
            raise RuntimeError(f"Error de base de datos al obtener planes de suscripción: {e}")
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    def update_user_subscription(self, usuario_id: int, plan_name: str):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            if conn is None:
                raise ConnectionError("No se pudo conectar a la base de datos.")
            cursor = conn.cursor()

            # Calcular fecha de vencimiento
            today = date.today()
            if plan_name == 'anual':
                fecha_vencimiento = today + timedelta(days=365)
            elif plan_name == 'mensual':
                fecha_vencimiento = today + timedelta(days=30)
            elif plan_name == 'trimestral':
                fecha_vencimiento = today + timedelta(days=90)
            else:
                raise ValueError("Plan no válido. Debe ser 'mensual', 'trimestral' o 'anual'.")

            # Actualizar la tabla de usuarios
            query = "UPDATE usuarios SET tipo_suscripcion = %s, fecha_suscripcion = %s, fecha_vencimiento = %s WHERE id = %s"
            cursor.execute(query, ('premium', today, fecha_vencimiento, usuario_id))
            conn.commit()

            if cursor.rowcount == 0:
                return False # Usuario no encontrado o no se pudo actualizar
            return fecha_vencimiento

        except Error as e:
            raise RuntimeError(f"Error de base de datos al actualizar suscripción del usuario: {e}")
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

suscripcion_repository = SuscripcionRepository()

@suscripcion_bp.route("/planes", methods=['GET'])
def get_subscription_plans():
    """
    Obtiene todos los planes de suscripción disponibles.
    """
    try:
        plans = suscripcion_repository.get_all_subscription_plans()
        return jsonify([plan.dict() for plan in plans])
    except RuntimeError as e:
        abort(500, description=f"Error interno del servidor: {e}")
    except ConnectionError as e:
        abort(500, description=f"Error de conexión a la base de datos: {e}")

@suscripcion_bp.route("/subscribe", methods=['POST'])
def subscribe_user():
    """
    Activa o actualiza la suscripción de un usuario.
    """
    try:
        data = SuscripcionUpdate(**request.get_json())
    except Exception as e:
        abort(400, description=f"Datos de entrada inválidos: {e}")

    try:
        fecha_vencimiento = suscripcion_repository.update_user_subscription(data.usuario_id, data.plan)
        if fecha_vencimiento is False:
            abort(404, description="Usuario no encontrado o no se pudo actualizar.")

        return jsonify({"success": True, "message": "Suscripción activada exitosamente", "plan": data.plan, "fecha_vencimiento": fecha_vencimiento.strftime('%Y-%m-%d')})

    except ValueError as e:
        abort(400, description=f"Error de validación: {e}")
    except RuntimeError as e:
        abort(500, description=f"Error interno del servidor: {e}")
    except ConnectionError as e:
        abort(500, description=f"Error de conexión a la base de datos: {e}")
