#!/usr/bin/env python3
"""
Script para ejecutar la aplicación ReservaCancha
"""

import os
import sys
from app import create_app

def main():
    """Función principal para ejecutar la aplicación"""
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('app.py'):
        print("❌ Error: No se encontró app.py. Asegúrate de estar en el directorio correcto.")
        sys.exit(1)
    
    # Crear la aplicación
    app = create_app()
    
    print("🚀 Iniciando Flash Reserver...")
    print("📱 La aplicación estará disponible en: http://localhost:5000")
    print("🛑 Presiona Ctrl+C para detener el servidor")
    print("-" * 50)
    
    # Ejecutar la aplicación
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )

if __name__ == '__main__':
    main() 