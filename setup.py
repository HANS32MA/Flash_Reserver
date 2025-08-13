#!/usr/bin/env python3
"""
Script de configuración automática para ReservaCancha
"""

import os
import sys
import subprocess
import mysql.connector
from mysql.connector import Error

def check_python_version():
    """Verificar versión de Python"""
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    return True

def install_requirements():
    """Instalar dependencias"""
    print("📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error al instalar dependencias")
        return False

def create_database():
    """Crear base de datos MySQL"""
    print("🗄️ Configurando base de datos...")
    
    # Configuración de la base de datos
    config = {
        'host': 'localhost',
        'user': 'oinodecam',
        'password': '123456789',
        'database': 'ReservaCancha'
    }
    
    try:
        # Conectar sin especificar base de datos
        connection = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password']
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Crear base de datos si no existe
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']}")
            print(f"✅ Base de datos '{config['database']}' creada/verificada")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ Error de conexión a MySQL: {e}")
        print("💡 Asegúrate de que MySQL esté ejecutándose y las credenciales sean correctas")
        return False

def initialize_database():
    """Inicializar la base de datos con datos de ejemplo"""
    print("🔧 Inicializando base de datos...")
    try:
        subprocess.check_call([sys.executable, "init_db.py"])
        print("✅ Base de datos inicializada correctamente")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error al inicializar la base de datos")
        return False

def create_env_file():
    """Crear archivo .env si no existe"""
    env_file = '.env'
    if not os.path.exists(env_file):
        print("📝 Creando archivo .env...")
        env_content = """# Configuración de ReservaCancha
SECRET_KEY=tu_clave_secreta_muy_segura_aqui_cambiala_en_produccion
DATABASE_URI=mysql+pymysql://oinodecam:123456789@localhost/ReservaCancha
FLASK_ENV=development
FLASK_DEBUG=True
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Archivo .env creado")
    else:
        print("ℹ️ Archivo .env ya existe")

def main():
    """Función principal de configuración"""
    print("🏟️ Configurando ReservaCancha...")
    print("=" * 50)
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Instalar dependencias
    if not install_requirements():
        sys.exit(1)
    
    # Crear archivo .env
    create_env_file()
    
    # Configurar base de datos
    if not create_database():
        print("⚠️ No se pudo configurar la base de datos")
        print("💡 Puedes continuar y configurarla manualmente después")
    
    # Inicializar base de datos
    if not initialize_database():
        print("⚠️ No se pudo inicializar la base de datos")
        print("💡 Puedes ejecutar 'python init_db.py' manualmente")
    
    print("=" * 50)
    print("🎉 ¡Configuración completada!")
    print("\n📋 Próximos pasos:")
    print("1. Ejecuta: python run.py")
    print("2. Abre: http://localhost:5000")
    print("3. Usa las credenciales de prueba del README.md")
    print("\n👤 Usuarios de prueba:")
    print("   Admin: admin@reserva.com / admin123")
    print("   Cliente: juan@example.com / cliente123")
    print("   Empleado: carlos@reserva.com / empleado123")

if __name__ == '__main__':
    main() 