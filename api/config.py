import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Settings:
    DB_HOST: str = os.getenv("DB_HOST", "168.197.51.109")
    DB_USER: str = os.getenv("DB_USER", "PIN_GRUPO31")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "PIN_GRUPO31123")
    DB_NAME: str = os.getenv("DB_NAME", "PIN_GRUPO31")
    DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")

# Instancia de la configuración para ser usada en la app
settings = Settings()
