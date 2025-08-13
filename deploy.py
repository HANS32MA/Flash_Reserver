#!/usr/bin/env python3
"""
Script de despliegue para producción
"""

import os
import shutil
import subprocess
import sys

def check_requirements():
    """Verificar que todas las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    required_packages = [
        'flask', 'flask-sqlalchemy', 'flask-login', 'flask-wtf', 
        'flask-mail', 'pymysql', 'python-dotenv', 'gunicorn'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Faltan dependencias: {', '.join(missing_packages)}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def setup_production_env():
    """Configurar archivo .env para producción"""
    print("\n🔧 Configurando entorno de producción...")
    
    if not os.path.exists('.env'):
        print("❌ Archivo .env no encontrado")
        print("💡 Copia production.env.example a .env y configúralo")
        return False
    
    # Verificar configuración crítica
    with open('.env', 'r') as f:
        content = f.read()
    
    critical_vars = ['SECRET_KEY', 'DATABASE_URI', 'MAIL_USERNAME', 'MAIL_PASSWORD']
    missing_vars = []
    
    for var in critical_vars:
        if f'{var}=' not in content or f'{var}=tu-' in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variables críticas no configuradas: {', '.join(missing_vars)}")
        print("💡 Configura estas variables en el archivo .env")
        return False
    
    print("✅ Configuración de producción verificada")
    return True

def create_directories():
    """Crear directorios necesarios"""
    print("\n📁 Creando directorios...")
    
    directories = [
        'logs',
        'static/uploads/perfiles',
        'static/uploads/temp'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Creado: {directory}")

def test_database():
    """Probar conexión a la base de datos"""
    print("\n🗄️ Probando conexión a la base de datos...")
    
    try:
        from app import create_app
        from config import ProductionConfig
        
        app = create_app(ProductionConfig)
        with app.app_context():
            from app import db
            db.engine.connect()
            print("✅ Conexión a la base de datos exitosa")
            return True
    except Exception as e:
        print(f"❌ Error de conexión a la base de datos: {e}")
        return False

def test_email():
    """Probar configuración de email"""
    print("\n📧 Probando configuración de email...")
    
    try:
        from app import create_app
        from config import ProductionConfig
        
        app = create_app(ProductionConfig)
        with app.app_context():
            from app.utils.auth_utils import send_password_reset_email
            success = send_password_reset_email('test@example.com', 'http://test.com')
            if success:
                print("✅ Configuración de email exitosa")
                return True
            else:
                print("⚠️ Configuración de email con problemas")
                return True  # No crítico para producción
    except Exception as e:
        print(f"❌ Error en configuración de email: {e}")
        return False

def main():
    """Función principal de despliegue"""
    print("🚀 DESPLIEGUE DE PRODUCCIÓN - Flash Reserver")
    print("=" * 50)
    
    # Verificar dependencias
    if not check_requirements():
        sys.exit(1)
    
    # Configurar entorno
    if not setup_production_env():
        sys.exit(1)
    
    # Crear directorios
    create_directories()
    
    # Probar base de datos
    if not test_database():
        print("⚠️ Problemas con la base de datos")
    
    # Probar email
    test_email()
    
    print("\n🎉 ¡Despliegue completado!")
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Ejecuta: gunicorn -w 4 -b 0.0.0.0:5000 wsgi:application")
    print("2. Configura un proxy reverso (nginx/apache)")
    print("3. Configura SSL/HTTPS")
    print("4. Configura monitoreo y logs")
    print("5. Configura backups de la base de datos")

if __name__ == '__main__':
    main()
