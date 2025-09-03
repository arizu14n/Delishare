from flask import Blueprint, jsonify, abort, request
from datetime import date, timedelta

from ..database import get_db_session
from ..models.suscripcion import PlanSuscripcion, SuscripcionUpdate, PlanSuscripcionDB
from ..models.usuario import UsuarioDB

suscripcion_bp = Blueprint('suscripcion', __name__)

# --- Repositorio de Suscripciones ---
class SuscripcionRepository:
    def __init__(self):
        self.db_session = get_db_session()

    def get_all_subscription_plans(self) -> list[PlanSuscripcion]:
        plans_db = self.db_session.query(PlanSuscripcionDB).filter(PlanSuscripcionDB.activo == True).order_by(PlanSuscripcionDB.precio.asc()).all()
        return [PlanSuscripcion.from_orm(plan) for plan in plans_db]

    def update_user_subscription(self, usuario_id: int, plan_name: str):
        user = self.db_session.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()
        if not user:
            return False

        # Asumo que el nombre del plan en la DB es 'mensual', 'trimestral', 'anual'
        plan = self.db_session.query(PlanSuscripcionDB).filter(PlanSuscripcionDB.nombre == plan_name).first()
        if not plan:
            raise ValueError(f"Plan '{plan_name}' no válido.")

        today = date.today()
        fecha_vencimiento = today + timedelta(days=plan.duracion_dias)

        user.tipo_suscripcion = 'premium'
        user.fecha_suscripcion = today
        user.fecha_vencimiento = fecha_vencimiento
        
        self.db_session.commit()

        return fecha_vencimiento

suscripcion_repository = SuscripcionRepository()

@suscripcion_bp.route("/planes", methods=['GET'])
def get_subscription_plans():
    """
    Obtiene todos los planes de suscripción disponibles.
    """
    try:
        plans = suscripcion_repository.get_all_subscription_plans()
        return jsonify([plan.dict() for plan in plans])
    except Exception as e:
        abort(500, description=f"Error interno del servidor: {e}")

@suscripcion_bp.route("/subscribe", methods=['POST'])
def subscribe_user():
    """
    Activa o actualiza la suscripción de un usuario.
    """
    if not request.is_json:
        abort(400, description="La solicitud debe ser de tipo JSON.")

    try:
        data = SuscripcionUpdate(**request.get_json())
    except Exception as e:
        abort(400, description=f"Datos de entrada inválidos: {e}")

    try:
        fecha_vencimiento = suscripcion_repository.update_user_subscription(data.usuario_id, data.plan)
        if fecha_vencimiento is False:
            abort(404, description="Usuario no encontrado.")

        return jsonify({"success": True, "message": "Suscripción activada exitosamente", "plan": data.plan, "fecha_vencimiento": fecha_vencimiento.strftime('%Y-%m-%d')})

    except ValueError as e:
        abort(400, description=f"Error de validación: {e}")
    except Exception as e:
        abort(500, description=f"Error interno del servidor: {e}")