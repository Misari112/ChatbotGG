# main.py
import secrets
from flask import Flask
from routes.routes import routes
import os
from dotenv import load_dotenv

def create_app():
    # Cargar variables de entorno desde .env
    load_dotenv()

    
    app = Flask(__name__)
    secret_key = os.getenv('SECRET_KEY')
    if not secret_key:
        # Generar una clave secreta si no está definida en el entorno
        secret_key = secrets.token_hex(16)
        app.logger.warning("SECRET_KEY no está definida en las variables de entorno. "
                           "Se generó una clave secreta temporal.")
    app.secret_key = secret_key

    # Registrar el blueprint de las rutas
    app.register_blueprint(routes)

    # Configurar la carpeta de carga de archivos
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    # Configurar carpeta estática y de plantillas
    app.static_folder = 'app/static'
    app.template_folder = 'app/templates'

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
