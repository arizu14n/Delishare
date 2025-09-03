from flask import Flask, jsonify
from flask_cors import CORS

from .routers.recetas import recetas_bp
from .routers.auth import auth_bp
from .routers.suscripcion import suscripcion_bp
from .database import close_db_session

# Crear la instancia de la aplicación Flask
app = Flask(__name__)

# Configurar CORS para permitir todas las fuentes
CORS(app, resources={r"/*": {"origins": "*"}})

# Registrar los Blueprints
app.register_blueprint(recetas_bp, url_prefix='/recetas')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(suscripcion_bp, url_prefix='/suscripcion')

# Endpoint de bienvenida para verificar que la API está funcionando
@app.route("/", methods=['GET'])
def read_root():
    return jsonify({"message": "Bienvenido a la API de Delishare con Flask"})

# Manejadores de errores globales para devolver respuestas JSON consistentes
@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(409)
@app.errorhandler(500)
def handle_errors(e):
    # Asegurarse de que el código de estado y la descripción sean correctos
    code = e.code if hasattr(e, "code") else 500
    description = e.description if hasattr(e, "description") else str(e)
    return jsonify({
        "success": False,
        "error": description
    }), code

@app.teardown_appcontext
def shutdown_session(exception=None):
    close_db_session(exception)

# Punto de entrada para ejecutar la aplicación
if __name__ == '__main__':
    # Escucha en todas las interfaces de red en el puerto 5000
    app.run(host='0.0.0.0', port=5000, debug=True)