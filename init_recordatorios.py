#!/usr/bin/env python3
"""
Script para inicializar recordatorios automáticos para todas las reservas existentes
"""

from app import create_app
from app.services.recordatorio_service import recordatorio_service

def inicializar_recordatorios():
    """Inicializa recordatorios para todas las reservas confirmadas existentes"""
    print("🚀 INICIALIZANDO SISTEMA DE RECORDATORIOS AUTOMÁTICOS")
    print("=" * 60)
    
    try:
        app = create_app()
        
        with app.app_context():
            print("✅ Aplicación Flask iniciada")
            
            # Programar recordatorios para reservas existentes
            print("\n📅 Programando recordatorios para reservas existentes...")
            resultado = recordatorio_service.programar_recordatorios_existentes()
            
            if resultado:
                print("✅ Recordatorios programados exitosamente")
            else:
                print("❌ Error programando recordatorios")
            
            # Limpiar recordatorios antiguos
            print("\n🧹 Limpiando recordatorios antiguos...")
            resultado_limpieza = recordatorio_service.limpiar_recordatorios_antiguos()
            
            if resultado_limpieza:
                print("✅ Limpieza completada")
            else:
                print("❌ Error en limpieza")
            
            # Obtener estado del scheduler
            print("\n📊 Estado del Scheduler de Recordatorios:")
            estado = recordatorio_service.obtener_estado_scheduler()
            
            if 'error' not in estado:
                print(f"  ✅ Scheduler activo: {estado['scheduler_activo']}")
                print(f"  📋 Total de jobs: {estado['total_jobs']}")
                print(f"  ⏰ Jobs de recordatorios: {len(estado['jobs_recordatorios'])}")
                
                if estado['jobs_recordatorios']:
                    print("  📝 Jobs programados:")
                    for job in estado['jobs_recordatorios'][:5]:  # Mostrar solo los primeros 5
                        print(f"    - {job}")
                    if len(estado['jobs_recordatorios']) > 5:
                        print(f"    ... y {len(estado['jobs_recordatorios']) - 5} más")
            else:
                print(f"  ❌ Error obteniendo estado: {estado['error']}")
            
            print(f"\n🎉 ¡Inicialización completada!")
            print(f"💡 El sistema ahora enviará recordatorios automáticos para todas las reservas")
            print(f"📧 Recordatorios se envían 24h y 2h antes de cada reserva")
            
    except Exception as e:
        print(f"❌ Error durante la inicialización: {e}")

if __name__ == "__main__":
    inicializar_recordatorios()
