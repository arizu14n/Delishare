# -*- coding: utf-8 -*-
"""
Archivo principal de la aplicación Flask.

Este archivo se encarga de:
- Crear y configurar la instancia de la aplicación Flask.
- Configurar CORS para permitir peticiones desde otros dominios.
- Registrar los Blueprints que contienen las rutas de la API.
- Definir un endpoint de bienvenida.
- Manejar errores de forma centralizada.
- Gestionar el cierre de la sesión de la base de datos.
- Iniciar el servidor de desarrollo de Flask.
"""

from flask import Flask, jsonify
from flask_cors import CORS

# Importar los Blueprints desde los archivos de rutas.
# Un Blueprint es un conjunto de rutas que pueden ser registradas en una aplicación.
from .routers.recetas import recetas_bp
from .routers.auth import auth_bp
from .routers.suscripcion import suscripcion_bp
# Importar la función para cerrar la sesión de la base de datos.
from .database import close_db_session

# Crear la instancia de la aplicación Flask.
# `__name__` es el nombre del módulo actual, Flask lo utiliza para localizar recursos.
app = Flask(__name__)

# Configurar CORS (Cross-Origin Resource Sharing) para permitir peticiones
# desde cualquier origen. Esto es necesario para que el frontend pueda
# comunicarse con la API.
CORS(app, resources={r"/*": {"origins": "*"}})

# Registrar los Blueprints en la aplicación.
# Cada Blueprint se asocia con un prefijo de URL.
app.register_blueprint(recetas_bp, url_prefix='/recetas')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(suscripcion_bp, url_prefix='/suscripcion')

# Endpoint de bienvenida para verificar que la API está funcionando correctamente.
# Este endpoint responde a peticiones GET en la raíz de la API ("/").
@app.route("/", methods=['GET'])
def read_root():
    """
    Endpoint de bienvenida.
    """
    return jsonify({"message": "Bienvenido a la API de Delishare con Flask"})

# Manejadores de errores globales.
# Estos decoradores registran funciones para manejar errores HTTP específicos.
# Esto permite devolver respuestas JSON consistentes y amigables para los errores.
@app.errorhandler(400)  # Bad Request
@app.errorhandler(401)  # Unauthorized
@app.errorhandler(404)  # Not Found
@app.errorhandler(409)  # Conflict
@app.errorhandler(500)  # Internal Server Error
def handle_errors(e):
    """
    Manejador de errores centralizado.
    Captura excepciones HTTP y devuelve una respuesta JSON formateada.
    """
    # Obtener el código de estado y la descripción del error.
    code = e.code if hasattr(e, "code") else 500
    description = e.description if hasattr(e, "description") else str(e)
    # Devolver una respuesta JSON con el error.
    return jsonify({
        "success": False,
        "error": description
    }), code

# Registrar una función para que se ejecute al final de cada request.
# `teardown_appcontext` se asegura de que esta función se llame siempre,
# incluso si ocurre una excepción.
@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    Cierra la sesión de la base de datos al final de cada request.
    """
    close_db_session(exception)

# Punto de entrada para ejecutar la aplicación.
# El bloque `if __name__ == '__main__':` se ejecuta solo cuando el archivo
# es ejecutado directamente (no cuando es importado).
if __name__ == '__main__':
    # Iniciar el servidor de desarrollo de Flask.
    # `host='0.0.0.0'` hace que el servidor sea accesible desde cualquier IP.
    # `port=5000` es el puerto en el que se ejecutará el servidor.
    # `debug=True` activa el modo de depuración, que reinicia el servidor
    # automáticamente al detectar cambios en el código y proporciona
    # información de depuración detallada en caso de errores.
    app.run(host='0.0.0.0', port=5000, debug=True)
