from app import create_app, db
from app.models import Rol, Usuario, TipoCancha, Categoria, Cancha
from datetime import datetime

app = create_app()

with app.app_context():
    # Forzar la creación de tablas
    db.drop_all()
    db.create_all()
    
    # Verificar si hay roles (en lugar de crear duplicados)
    if not Rol.query.first():
        print("Creando datos iniciales...")
        
        # Crear roles
        roles_data = [
            Rol(Nombre='Cliente'),
            Rol(Nombre='Empleado'),
            Rol(Nombre='Administrador')
        ]
        db.session.bulk_save_objects(roles_data)
        db.session.commit()
        
        # Crear tipos de cancha
        tipos_data = [
            TipoCancha(Nombre='Césped Natural', Descripcion='Cancha con césped natural de alta calidad'),
            TipoCancha(Nombre='Césped Sintético', Descripcion='Cancha con césped sintético profesional'),
            TipoCancha(Nombre='Concreto', Descripcion='Cancha de concreto pulido'),
            TipoCancha(Nombre='Parquet', Descripcion='Cancha con piso de parquet deportivo'),
            TipoCancha(Nombre='Arcilla', Descripcion='Cancha de arcilla para tenis')
        ]
        db.session.bulk_save_objects(tipos_data)
        
        # Crear categorías
        categorias_data = [
            Categoria(Nombre='Fútbol', Descripcion='Canchas para fútbol 11, 7 y 5'),
            Categoria(Nombre='Tenis', Descripcion='Canchas de tenis individual y dobles'),
            Categoria(Nombre='Pádel', Descripcion='Canchas de pádel profesionales'),
            Categoria(Nombre='Básquetbol', Descripcion='Canchas de básquetbol'),
            Categoria(Nombre='Vóleibol', Descripcion='Canchas de vóleibol'),
            Categoria(Nombre='Fútbol Sala', Descripcion='Canchas de fútbol sala')
        ]
        db.session.bulk_save_objects(categorias_data)
        db.session.commit()
        
        # Obtener referencias
        cliente_rol = Rol.query.filter_by(Nombre='Cliente').first()
        empleado_rol = Rol.query.filter_by(Nombre='Empleado').first()
        admin_rol = Rol.query.filter_by(Nombre='Administrador').first()
        
        futbol_cat = Categoria.query.filter_by(Nombre='Fútbol').first()
        tenis_cat = Categoria.query.filter_by(Nombre='Tenis').first()
        padel_cat = Categoria.query.filter_by(Nombre='Pádel').first()
        basquet_cat = Categoria.query.filter_by(Nombre='Básquetbol').first()
        
        cesped_nat = TipoCancha.query.filter_by(Nombre='Césped Natural').first()
        cesped_sint = TipoCancha.query.filter_by(Nombre='Césped Sintético').first()
        concreto = TipoCancha.query.filter_by(Nombre='Concreto').first()
        parquet = TipoCancha.query.filter_by(Nombre='Parquet').first()
        arcilla = TipoCancha.query.filter_by(Nombre='Arcilla').first()
        
        # Crear usuarios de ejemplo
        usuarios_data = [
            Usuario(
                Nombre='Admin Root',
                Email='admin@reserva.com',
                Telefono='0000000000',
                Contrasena='admin123',
                RolId=admin_rol.Id
            ),
            Usuario(
                Nombre='Juan Pérez',
                Email='juan@example.com',
                Telefono='1234567890',
                Contrasena='cliente123',
                RolId=cliente_rol.Id
            ),
            Usuario(
                Nombre='María García',
                Email='maria@example.com',
                Telefono='0987654321',
                Contrasena='cliente123',
                RolId=cliente_rol.Id
            ),
            Usuario(
                Nombre='Carlos López',
                Email='carlos@reserva.com',
                Telefono='5555555555',
                Contrasena='empleado123',
                RolId=empleado_rol.Id
            )
        ]
        db.session.bulk_save_objects(usuarios_data)
        
        # Crear canchas de ejemplo
        canchas_data = [
            Cancha(
                Nombre='Cancha 1 - Fútbol 11',
                TipoCanchaId=cesped_nat.Id,
                CategoriaId=futbol_cat.Id,
                PrecioHora=50.00
            ),
            Cancha(
                Nombre='Cancha 2 - Fútbol 7',
                TipoCanchaId=cesped_sint.Id,
                CategoriaId=futbol_cat.Id,
                PrecioHora=40.00
            ),
            Cancha(
                Nombre='Cancha 3 - Fútbol 5',
                TipoCanchaId=cesped_sint.Id,
                CategoriaId=futbol_cat.Id,
                PrecioHora=30.00
            ),
            Cancha(
                Nombre='Cancha 4 - Tenis Arcilla',
                TipoCanchaId=arcilla.Id,
                CategoriaId=tenis_cat.Id,
                PrecioHora=35.00
            ),
            Cancha(
                Nombre='Cancha 5 - Tenis Concreto',
                TipoCanchaId=concreto.Id,
                CategoriaId=tenis_cat.Id,
                PrecioHora=30.00
            ),
            Cancha(
                Nombre='Cancha 6 - Pádel',
                TipoCanchaId=concreto.Id,
                CategoriaId=padel_cat.Id,
                PrecioHora=25.00
            ),
            Cancha(
                Nombre='Cancha 7 - Básquetbol',
                TipoCanchaId=concreto.Id,
                CategoriaId=basquet_cat.Id,
                PrecioHora=20.00
            )
        ]
        db.session.bulk_save_objects(canchas_data)
        db.session.commit()
            
        print("✅ Datos iniciales creados correctamente")
        print("\n📋 Usuarios de prueba:")
        print("👤 Admin: admin@reserva.com / admin123")
        print("👤 Cliente 1: juan@example.com / cliente123")
        print("👤 Cliente 2: maria@example.com / cliente123")
        print("👤 Empleado: carlos@reserva.com / empleado123")
        print("\n⚽ Canchas creadas: 7 canchas de diferentes deportes")
        print("\n🎯 El sistema está listo para usar!")
    else:
        print("ℹ️ Los datos iniciales ya existen en la base de datos")
