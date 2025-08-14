import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.template.loader import render_to_string

def render_template(template_name, output_file, context=None):
    """
    Renderiza una plantilla HTML de Django y la guarda en un archivo
    
    Args:
        template_name: Nombre de la plantilla (ej: 'admin/dashboard.html')
        output_file: Archivo de salida (ej: 'output.html')
        context: Diccionario con variables para la plantilla
    """
    if context is None:
        context = {}
    
    try:
        html = render_to_string(template_name, context)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Plantilla '{template_name}' renderizada exitosamente en '{output_file}'")
        return True
        
    except Exception as e:
        print(f"❌ Error al renderizar la plantilla: {e}")
        return False

# Ejemplos de uso
if __name__ == '__main__':
    print("🚀 Renderizador de Plantillas Django")
    print("=" * 40)
    
    # Ejemplo 1: Dashboard admin
    print("\n1. Renderizando dashboard admin...")
    render_template(
        'admin/dashboard.html',
        'dashboard_output.html',
        {
            'usuario': {'nombre': 'Administrador', 'rol': 'admin'},
            'estadisticas': {'total_usuarios': 150, 'total_reservas': 300}
        }
    )
    
    # Ejemplo 2: Lista de canchas
    print("\n2. Renderizando lista de canchas...")
    render_template(
        'client/canchas.html',
        'canchas_output.html',
        {
            'canchas': [
                {'nombre': 'Cancha 1', 'precio': 50},
                {'nombre': 'Cancha 2', 'precio': 60}
            ]
        }
    )
    
    # Ejemplo 3: Plantilla simple sin contexto
    print("\n3. Renderizando plantilla base...")
    render_template('base.html', 'base_output.html')
    
    print("\n✨ ¡Listo! Revisa los archivos generados.")
    print("\nPara renderizar otras plantillas, usa:")
    print("render_template('nombre_plantilla.html', 'archivo_salida.html', contexto)")
