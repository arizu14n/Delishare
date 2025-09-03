from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# -------------------------
# Configuración de SQLAlchemy
# -------------------------

# URL de conexión a SQL Server usando pyodbc
DATABASE_URL = (
    f"mssql+pyodbc://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}/{settings.DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"
)

# Crear el engine (maneja el pool de conexiones automáticamente)
engine = create_engine(DATABASE_URL, echo=True, future=True)

# SessionLocal nos da sesiones para interactuar con la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

def get_db():
    """Genera una sesión de base de datos (para usar en FastAPI o manual)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
