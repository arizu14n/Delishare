# -*- coding: utf-8 -*-
"""
Define las rutas para la gestión de suscripciones.

Este archivo contiene:
- Un `SuscripcionRepository` para manejar la lógica de negocio de las suscripciones.
- La ruta `/planes` para obtener los planes de suscripción disponibles.
- La ruta `/subscribe` para activar o actualizar la suscripción de un usuario.
"""

from flask import Blueprint, jsonify, abort, request
from datetime import date, timedelta

from ..database import get_db_session
from ..models.suscripcion import PlanSuscripcion, SuscripcionUpdate, PlanSuscripcionDB
from ..models.usuario import UsuarioDB

# Crear un Blueprint para las rutas de suscripción.
suscripcion_bp = Blueprint('suscripcion', __name__)

# --- Repositorio de Suscripciones ---
class SuscripcionRepository:
    """
    Clase que encapsula la lógica de negocio para las suscripciones.
    """
    def __init__(self):
        self.db_session = get_db_session()

    def get_all_subscription_plans(self) -> list[PlanSuscripcion]:
        """
        Obtiene todos los planes de suscripción activos, ordenados por precio.

        Returns:
            Una lista de objetos `PlanSuscripcion` de Pydantic.
        """
        plans_db = self.db_session.query(PlanSuscripcionDB).filter(PlanSuscripcionDB.activo == True).order_by(PlanSuscripcionDB.precio.asc()).all()
        return [PlanSuscripcion.from_orm(plan) for plan in plans_db]

    def update_user_subscription(self, usuario_id: int, plan_name: str):
        """
        Actualiza la suscripción de un usuario a un plan específico.

        Args:
            usuario_id: El ID del usuario a actualizar.
            plan_name: El nombre del plan al que se va a suscribir (ej: 'mensual').

        Returns:
            La nueva fecha de vencimiento si la actualización es exitosa.
            `False` si el usuario no se encuentra.
        
        Raises:
            ValueError: Si el nombre del plan no es válido.
        """
        user = self.db_session.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()
        if not user:
            return False

        # Buscar el plan de suscripción por su nombre.
        plan = self.db_session.query(PlanSuscripcionDB).filter(PlanSuscripcionDB.nombre == plan_name).first()
        if not plan:
            raise ValueError(f"Plan '{plan_name}' no válido.")

        # Calcular la nueva fecha de vencimiento.
        today = date.today()
        fecha_vencimiento = today + timedelta(days=plan.duracion_dias)

        # Actualizar los datos del usuario.
        user.tipo_suscripcion = 'premium'
        user.fecha_suscripcion = today
        user.fecha_vencimiento = fecha_vencimiento
        
        # Confirmar la transacción en la base de datos.
        self.db_session.commit()

        return fecha_vencimiento

# Instancia única del repositorio de suscripciones.
suscripcion_repository = SuscripcionRepository()

@suscripcion_bp.route("/planes", methods=['GET'])
def get_subscription_plans():
    """
    Endpoint para obtener todos los planes de suscripción disponibles.
    """
    try:
        plans = suscripcion_repository.get_all_subscription_plans()
        return jsonify([plan.dict() for plan in plans])
    except Exception as e:
        abort(500, description=f"Error interno del servidor: {e}")

@suscripcion_bp.route("/subscribe", methods=['POST'])
def subscribe_user():
    """
    Endpoint para activar o actualizar la suscripción de un usuario a un plan.
    """
    if not request.is_json:
        abort(400, description="La solicitud debe ser de tipo JSON.")

    try:
        # Validar los datos de entrada con el modelo Pydantic `SuscripcionUpdate`.
        data = SuscripcionUpdate(**request.get_json())
    except Exception as e:
        abort(400, description=f"Datos de entrada inválidos: {e}")

    try:
        # Llamar al método del repositorio para actualizar la suscripción.
        fecha_vencimiento = suscripcion_repository.update_user_subscription(data.usuario_id, data.plan)
        
        if fecha_vencimiento is False:
            abort(404, description="Usuario no encontrado.")

        # Devolver una respuesta exitosa con la nueva fecha de vencimiento.
        return jsonify({
            "success": True,
            "message": "Suscripción activada exitosamente",
            "plan": data.plan,
            "fecha_vencimiento": fecha_vencimiento.strftime('%Y-%m-%d')
        })

    except ValueError as e:
        # Capturar errores de validación (ej: plan no válido).
        abort(400, description=f"Error de validación: {e}")
    except Exception as e:
        # Capturar cualquier otro error inesperado.
        abort(500, description=f"Error interno del servidor: {e}")
