import os
from config import config


# Determinar el entorno
def get_config():
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])

if __name__ == '__main__':
    # Configuración fija para entorno local solicitada por el usuario
    host = '127.0.0.1'
    port = 5000
    debug = True
    try:
        # Importación diferida para poder capturar errores de dependencias
        from app import create_app

        app = create_app(get_config())

        # Configurar carpeta de uploads
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Mostrar un solo mensaje personalizado y evitar duplicarlo con el reloader
        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or not debug:
            print(f"Conexion exitosa | Debug activo: {debug} | Servidor: http://{host}:{port}")

        app.run(host=host, port=port, debug=debug)
    except Exception as exc:
        print("Error de conexion")
        print(f"Detalles: {exc}")
        raise SystemExit(1)