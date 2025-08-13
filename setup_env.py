#!/usr/bin/env python3
"""
Script para crear archivo .env con configuración de Gmail
"""

def create_env_file():
    print("🔧 Configurador de Email para Flash Reserver")
    print("=" * 50)
    
    # Solicitar datos del usuario
    print("\n📧 Configuración de Gmail:")
    email = input("Ingresa tu email de Gmail: ")
    
    print("\n🔑 Necesitas una 'Contraseña de Aplicación' de Google:")
    print("   1. Ve a myaccount.google.com")
    print("   2. Seguridad → Verificación en 2 pasos (debe estar habilitada)")
    print("   3. Contraseñas de aplicaciones → Correo → Windows Computer")
    print("   4. Copia la contraseña de 16 caracteres")
    print()
    
    app_password = input("Pega aquí tu contraseña de aplicación (16 caracteres): ").replace(" ", "")
    
    # Crear contenido del archivo .env
    env_content = f"""# Configuración de Flash Reserver
SECRET_KEY=mi-clave-secreta-super-segura-flash-reserver-2024
DATABASE_URI=sqlite:///reservas.db

# Configuración de Email - Gmail
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME={email}
MAIL_PASSWORD={app_password}
MAIL_DEFAULT_SENDER={email}
"""
    
    # Escribir archivo
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("\n✅ ¡Archivo .env creado exitosamente!")
        print(f"📧 Email configurado: {email}")
        print("🔐 Contraseña de aplicación guardada")
        print()
        print("🚀 Próximos pasos:")
        print("   1. Ejecuta: python test_email.py")
        print("   2. Si funciona, reinicia la aplicación")
        print("   3. ¡Prueba la función de recuperar contraseña!")
        
    except Exception as e:
        print(f"❌ Error creando archivo .env: {e}")

if __name__ == '__main__':
    create_env_file()
