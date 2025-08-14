from flask.cli import FlaskGroup
from flask_migrate import Migrate
from app import create_app, db
from app.models import Usuario, Rol, Cancha, Reserva, Categoria, TipoCancha, Comentario, Notificacion  # importa todos tus modelos

# Crear la app desde la app factory
app = create_app()

# Inicializar Flask-Migrate
migrate = Migrate(app, db)

# CLI para Flask
cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()
