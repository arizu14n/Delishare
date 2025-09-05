# -*- coding: utf-8 -*-
"""
Archivo de configuración para la aplicación.

Este archivo carga las variables de entorno desde un archivo .env y las define como constantes
para ser utilizadas en toda la aplicación. Esto permite una fácil configuración y modificación
de los parámetros de conexión a la base de datos y otras configuraciones sin tener que
modificar el código fuente.
"""

import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env.
# El archivo .env se utiliza para almacenar variables de entorno de forma local
# y no debe ser incluido en el control de versiones.
load_dotenv()

class Settings:
    """
    Clase que contiene las variables de configuración de la aplicación.

    Las variables se cargan desde el entorno y tienen valores por defecto
    en caso de que no se encuentren definidas.
    """
    # Host de la base de datos.
    DB_HOST: str = os.getenv("DB_HOST", "168.197.51.109")
    # Usuario de la base de datos.
    DB_USER: str = os.getenv("DB_USER", "PIN_GRUPO31")
    # Contraseña de la base de datos.
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "PIN_GRUPO31123")
    # Nombre de la base de datos.
    DB_NAME: str = os.getenv("DB_NAME", "PIN_GRUPO31")
    # Driver de la base de datos.
    DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")

# Instancia de la configuración para ser usada en la aplicación.
# Esta instancia se importa en otros módulos para acceder a la configuración.
settings = Settings()