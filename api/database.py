# -*- coding: utf-8 -*-
"""
Archivo de configuración de la base de datos.

Este archivo se encarga de establecer la conexión con la base de datos,
crear el motor de SQLAlchemy, y gestionar las sesiones de la base de datos.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from .config import settings
import urllib

# URL de conexión a SQL Server usando pyodbc.
# La contraseña se codifica para manejar caracteres especiales de forma segura.
quoted_password = urllib.parse.quote_plus(settings.DB_PASSWORD)
DATABASE_URL = (
    f"mssql+pyodbc://{settings.DB_USER}:{quoted_password}"
    f"@{settings.DB_HOST}/{settings.DB_NAME}?driver={settings.DB_DRIVER.replace(' ', '+')}"
)

# Crear el motor (engine) de SQLAlchemy.
# `echo=True` hace que SQLAlchemy muestre las consultas SQL que genera.
# `future=True` habilita el uso de la API 2.0 de SQLAlchemy.
engine = create_engine(DATABASE_URL, echo=True, future=True)

# Se utiliza `scoped_session` para asegurar que cada solicitud web (request)
# tenga su propia sesión de base de datos. Esto es crucial para evitar problemas
# de concurrencia en aplicaciones web.
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# `declarative_base()` crea una clase base para los modelos de SQLAlchemy.
# Todos los modelos de la aplicación heredarán de esta clase.
Base = declarative_base()
# `query_property` proporciona una propiedad `query` a los modelos para
# facilitar la construcción de consultas.
Base.query = db_session.query_property()

def init_db():
    """
    Inicializa la base de datos.

    Importa todos los modelos de la aplicación y utiliza `Base.metadata.create_all()`
    para crear las tablas correspondientes en la base de datos si no existen.
    """
    # Es necesario importar los modelos aquí para que SQLAlchemy los reconozca
    # y pueda crear las tablas.
    import api.models.categoria
    import api.models.receta
    Base.metadata.create_all(bind=engine)

def get_db_session():
    """
    Obtiene una sesión de la base de datos.

    Retorna la sesión de base de datos actual gestionada por `scoped_session`.
    FastAPI utiliza esta función como una dependencia para inyectar la sesión
    en las rutas.
    """
    return db_session

def close_db_session(exception=None):
    """
    Cierra la sesión de la base de datos.

    Se llama después de cada solicitud para devolver la sesión al pool
    y limpiar los recursos.
    """
    db_session.remove()
