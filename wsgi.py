#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar entorno de producción
os.environ['FLASK_ENV'] = 'production'

from app import create_app
from config import ProductionConfig

# Crear aplicación con configuración de producción
application = create_app(ProductionConfig)

if __name__ == "__main__":
    application.run()
