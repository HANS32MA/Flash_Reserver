from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
# from flask_migrate import Migrate  # 👈 Comentado temporalmente
import os
from flask import send_file

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
# migrate = Migrate()  # 👈 Comentado temporalmente

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # Forzar recarga de plantillas en cambios
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    
    # Inicializar extensiones
    db.init_app(app)
    # migrate.init_app(app, db)  # 👈 Comentado temporalmente
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    mail.init_app(app)
    
    # Configurar user_loader
    from app.models.usuario import Usuario
    from app.models.mensaje import Mensaje
    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    # Ruta para servir imágenes de canchas
    @app.route('/uploads/canchas/<filename>')
    def servir_imagen_cancha(filename):
        """Servir imágenes de canchas desde la carpeta uploads"""
        try:
            # Construir la ruta completa al archivo
            uploads_dir = os.path.join(app.root_path, 'static', 'uploads', 'canchas')
            file_path = os.path.join(uploads_dir, filename)
            
            # Verificar que el archivo existe
            if os.path.exists(file_path):
                return send_file(file_path)
            else:
                # Si no existe, devolver imagen por defecto
                default_image = os.path.join(app.root_path, 'static', 'images', 'default-cancha.jpg')
                if os.path.exists(default_image):
                    return send_file(default_image)
                else:
                    # Si no hay imagen por defecto, devolver 404
                    return 'Imagen no encontrada', 404
                    
        except Exception as e:
            # En caso de error, devolver imagen por defecto
            try:
                default_image = os.path.join(app.root_path, 'static', 'images', 'default-cancha.jpg')
                if os.path.exists(default_image):
                    return send_file(default_image)
            except:
                pass
            return 'Error al cargar imagen', 500
    
    # Ruta para servir imágenes de perfil de usuarios
    @app.route('/uploads/perfiles/<filename>')
    def servir_imagen_perfil(filename):
        """Servir imágenes de perfil de usuarios desde la carpeta uploads"""
        try:
            # Construir la ruta completa al archivo
            uploads_dir = os.path.join(app.root_path, 'static', 'uploads', 'perfiles')
            file_path = os.path.join(uploads_dir, filename)
            
            # Verificar que el archivo existe
            if os.path.exists(file_path):
                return send_file(file_path)
            else:
                # Si no existe, devolver imagen por defecto
                default_image = os.path.join(app.root_path, 'static', 'images', 'default-user.png')
                if os.path.exists(default_image):
                    return send_file(default_image)
                else:
                    # Si no hay imagen por defecto, devolver 404
                    return 'Imagen no encontrada', 404
                    
        except Exception as e:
            # En caso de error, devolver imagen por defecto
            try:
                default_image = os.path.join(app.root_path, 'static', 'images', 'default-user.png')
                if os.path.exists(default_image):
                    return send_file(default_image)
            except:
                pass
            return 'Error al cargar imagen', 500
    
    # Ruta para servir imágenes y videos del foro
    @app.route('/uploads/foro/<path:filename>')
    def servir_multimedia_foro(filename):
        """Servir imágenes y videos del foro desde la carpeta uploads"""
        try:
            # Construir la ruta completa al archivo
            uploads_dir = os.path.join(app.root_path, 'static', 'uploads', 'foro')
            file_path = os.path.join(uploads_dir, filename)
            
            # Verificar que el archivo existe
            if os.path.exists(file_path):
                return send_file(file_path)
            else:
                # Si no existe, devolver 404
                return 'Archivo no encontrado', 404
                    
        except Exception as e:
            app.logger.error(f"Error sirviendo archivo del foro '{filename}': {e}")
            return 'Error al cargar archivo', 500
    
    # Registrar blueprints
    from app.routes.main_routes import main_bp
    from app.auth.routes import auth_bp
    from app.routes.client_routes import client_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.foro_routes import foro_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(client_bp, url_prefix='/client')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(foro_bp, url_prefix='/foro')
    
    # Configuración específica para producción
    if hasattr(config_class, 'init_app'):
        config_class.init_app(app)
    
    return app
    