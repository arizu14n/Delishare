from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from .config import settings
import urllib

# URL de conexión a SQL Server usando pyodbc
# Es importante codificar la contraseña para manejar caracteres especiales
quoted_password = urllib.parse.quote_plus(settings.DB_PASSWORD)
DATABASE_URL = (
    f"mssql+pyodbc://{settings.DB_USER}:{quoted_password}"
    f"@{settings.DB_HOST}/{settings.DB_NAME}?driver={settings.DB_DRIVER.replace(' ', '+')}"
)

# Crear el engine
engine = create_engine(DATABASE_URL, echo=True, future=True)

# Usamos scoped_session para asegurar que cada request tenga su propia sesión
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Base para los modelos SQLAlchemy
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    """
    Importa todos los modelos y crea las tablas en la base de datos.
    """
    # Importa aquí todos los módulos que contienen modelos de SQLAlchemy
    import api.models.categoria 
    import api.models.receta
    Base.metadata.create_all(bind=engine)

def get_db_session():
    """
    Retorna una sesión de base de datos del registro de scoped_session.
    """
    return db_session

def close_db_session(exception=None):
    """
    Cierra la sesión de la base de datos al final del request.
    """
    db_session.remove()