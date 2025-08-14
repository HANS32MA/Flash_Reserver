import logging
from datetime import datetime, timedelta
from flask import current_app
from app import db
from app.models import Reserva, Usuario
from app.services.notificacion_service import notificacion_service
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

logger = logging.getLogger(__name__)

class RecordatorioService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        logger.info("Servicio de recordatorios iniciado")
    
    def programar_recordatorios_reserva(self, reserva_id):
        """Programa recordatorios automáticos para una reserva"""
        try:
            reserva = Reserva.query.get(reserva_id)
            if not reserva:
                logger.error(f"Reserva {reserva_id} no encontrada para programar recordatorios")
                return False
            
            # Calcular fechas para recordatorios
            fecha_reserva = reserva.Fecha
            hora_reserva = reserva.HoraInicio
            
            # Recordatorio 24 horas antes
            recordatorio_24h = datetime.combine(fecha_reserva, hora_reserva) - timedelta(hours=24)
            
            # Recordatorio 2 horas antes
            recordatorio_2h = datetime.combine(fecha_reserva, hora_reserva) - timedelta(hours=2)
            
            # Solo programar si la fecha de recordatorio es futura
            ahora = datetime.now()
            
            if recordatorio_24h > ahora:
                self.scheduler.add_job(
                    func=self._enviar_recordatorio_24h,
                    trigger=DateTrigger(run_date=recordatorio_24h),
                    args=[reserva_id],
                    id=f"recordatorio_24h_{reserva_id}",
                    replace_existing=True
                )
                logger.info(f"Recordatorio 24h programado para reserva {reserva_id} en {recordatorio_24h}")
            
            if recordatorio_2h > ahora:
                self.scheduler.add_job(
                    func=self._enviar_recordatorio_2h,
                    trigger=DateTrigger(run_date=recordatorio_2h),
                    args=[reserva_id],
                    id=f"recordatorio_2h_{reserva_id}",
                    replace_existing=True
                )
                logger.info(f"Recordatorio 2h programado para reserva {reserva_id} en {recordatorio_2h}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error programando recordatorios para reserva {reserva_id}: {e}")
            return False
    
    def cancelar_recordatorios_reserva(self, reserva_id):
        """Cancela los recordatorios programados para una reserva"""
        try:
            # Cancelar recordatorio 24h
            job_id_24h = f"recordatorio_24h_{reserva_id}"
            if self.scheduler.get_job(job_id_24h):
                self.scheduler.remove_job(job_id_24h)
                logger.info(f"Recordatorio 24h cancelado para reserva {reserva_id}")
            
            # Cancelar recordatorio 2h
            job_id_2h = f"recordatorio_2h_{reserva_id}"
            if self.scheduler.get_job(job_id_2h):
                self.scheduler.remove_job(job_id_2h)
                logger.info(f"Recordatorio 2h cancelado para reserva {reserva_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error cancelando recordatorios para reserva {reserva_id}: {e}")
            return False
    
    def _enviar_recordatorio_24h(self, reserva_id):
        """Envía recordatorio 24 horas antes de la reserva"""
        try:
            reserva = Reserva.query.get(reserva_id)
            if not reserva or reserva.Estado != 'Confirmada':
                logger.info(f"Reserva {reserva_id} no encontrada o no confirmada para recordatorio 24h")
                return
            
            # Verificar que la reserva aún es válida
            ahora = datetime.now()
            fecha_hora_reserva = datetime.combine(reserva.Fecha, reserva.HoraInicio)
            
            if fecha_hora_reserva <= ahora:
                logger.info(f"Reserva {reserva_id} ya pasó, no enviar recordatorio 24h")
                return
            
            # Enviar notificación por email
            notificacion_service.crear_notificacion(
                usuario_id=reserva.UsuarioId,
                tipo='email',
                titulo='⏰ Recordatorio de Reserva - Mañana - Flash Reserver',
                mensaje=f'Recordatorio: Tienes una reserva mañana {reserva.Fecha.strftime("%d/%m/%Y")} a las {reserva.HoraInicio.strftime("%H:%M")}.',
                datos_adicionales={
                    'reserva_id': reserva.Id,
                    'fecha': reserva.Fecha.strftime('%d/%m/%Y'),
                    'hora': reserva.HoraInicio.strftime('%H:%M'),
                    'cancha_nombre': reserva.cancha.Nombre if reserva.cancha else 'Cancha Deportiva',
                    'tipo_recordatorio': '24h',
                    'tiempo_restante': '24 horas'
                }
            )
            
            # También enviar notificación in-app
            notificacion_service.crear_notificacion(
                usuario_id=reserva.UsuarioId,
                tipo='in_app',
                titulo='⏰ Recordatorio de Reserva - Mañana',
                mensaje=f'Recordatorio: Tienes una reserva mañana {reserva.Fecha.strftime("%d/%m/%Y")} a las {reserva.HoraInicio.strftime("%H:%M")}.',
                datos_adicionales={
                    'reserva_id': reserva.Id,
                    'fecha': reserva.Fecha.strftime('%d/%m/%Y'),
                    'hora': reserva.HoraInicio.strftime('%H:%M'),
                    'cancha_nombre': reserva.cancha.Nombre if reserva.cancha else 'Cancha Deportiva',
                    'tipo_recordatorio': '24h'
                }
            )
            
            logger.info(f"Recordatorio 24h enviado para reserva {reserva_id}")
            
        except Exception as e:
            logger.error(f"Error enviando recordatorio 24h para reserva {reserva_id}: {e}")
    
    def _enviar_recordatorio_2h(self, reserva_id):
        """Envía recordatorio 2 horas antes de la reserva"""
        try:
            reserva = Reserva.query.get(reserva_id)
            if not reserva or reserva.Estado != 'Confirmada':
                logger.info(f"Reserva {reserva_id} no encontrada o no confirmada para recordatorio 2h")
                return
            
            # Verificar que la reserva aún es válida
            ahora = datetime.now()
            fecha_hora_reserva = datetime.combine(reserva.Fecha, reserva.HoraInicio)
            
            if fecha_hora_reserva <= ahora:
                logger.info(f"Reserva {reserva_id} ya pasó, no enviar recordatorio 2h")
                return
            
            # Enviar notificación por email
            notificacion_service.crear_notificacion(
                usuario_id=reserva.UsuarioId,
                tipo='email',
                titulo='🚨 Recordatorio de Reserva - En 2 Horas - Flash Reserver',
                mensaje=f'Recordatorio URGENTE: Tienes una reserva en 2 horas ({reserva.Fecha.strftime("%d/%m/%Y")} a las {reserva.HoraInicio.strftime("%H:%M")}).',
                datos_adicionales={
                    'reserva_id': reserva.Id,
                    'fecha': reserva.Fecha.strftime('%d/%m/%Y'),
                    'hora': reserva.HoraInicio.strftime('%H:%M'),
                    'cancha_nombre': reserva.cancha.Nombre if reserva.cancha else 'Cancha Deportiva',
                    'tipo_recordatorio': '2h',
                    'tiempo_restante': '2 horas',
                    'es_urgente': True
                }
            )
            
            # También enviar notificación in-app
            notificacion_service.crear_notificacion(
                usuario_id=reserva.UsuarioId,
                tipo='in_app',
                titulo='🚨 Recordatorio URGENTE - En 2 Horas',
                mensaje=f'Recordatorio URGENTE: Tienes una reserva en 2 horas ({reserva.Fecha.strftime("%d/%m/%Y")} a las {reserva.HoraInicio.strftime("%H:%M")}).',
                datos_adicionales={
                    'reserva_id': reserva.Id,
                    'fecha': reserva.Fecha.strftime('%d/%m/%Y'),
                    'hora': reserva.HoraInicio.strftime('%H:%M'),
                    'cancha_nombre': reserva.cancha.Nombre if reserva.cancha else 'Cancha Deportiva',
                    'tipo_recordatorio': '2h',
                    'es_urgente': True
                }
            )
            
            logger.info(f"Recordatorio 2h enviado para reserva {reserva_id}")
            
        except Exception as e:
            logger.error(f"Error enviando recordatorio 2h para reserva {reserva_id}: {e}")
    
    def programar_recordatorios_existentes(self):
        """Programa recordatorios para todas las reservas confirmadas existentes"""
        try:
            # Obtener reservas confirmadas futuras
            ahora = datetime.now()
            reservas_futuras = Reserva.query.filter(
                Reserva.Estado == 'Confirmada',
                Reserva.Fecha > ahora.date()
            ).all()
            
            logger.info(f"Programando recordatorios para {len(reservas_futuras)} reservas existentes")
            
            for reserva in reservas_futuras:
                self.programar_recordatorios_reserva(reserva.Id)
            
            return True
            
        except Exception as e:
            logger.error(f"Error programando recordatorios existentes: {e}")
            return False
    
    def limpiar_recordatorios_antiguos(self):
        """Limpia recordatorios programados para reservas pasadas"""
        try:
            # Obtener todos los jobs del scheduler
            jobs = self.scheduler.get_jobs()
            
            for job in jobs:
                if job.id.startswith('recordatorio_'):
                    # Extraer ID de reserva del job_id
                    reserva_id = job.id.split('_')[-1]
                    
                    try:
                        reserva = Reserva.query.get(int(reserva_id))
                        if not reserva or reserva.Estado != 'Confirmada':
                            # Cancelar job si la reserva no existe o no está confirmada
                            self.scheduler.remove_job(job.id)
                            logger.info(f"Job de recordatorio {job.id} cancelado (reserva inválida)")
                        elif datetime.combine(reserva.Fecha, reserva.HoraInicio) <= datetime.now():
                            # Cancelar job si la reserva ya pasó
                            self.scheduler.remove_job(job.id)
                            logger.info(f"Job de recordatorio {job.id} cancelado (reserva pasada)")
                    except:
                        # Si hay error, cancelar el job
                        self.scheduler.remove_job(job.id)
                        logger.info(f"Job de recordatorio {job.id} cancelado (error)")
            
            return True
            
        except Exception as e:
            logger.error(f"Error limpiando recordatorios antiguos: {e}")
            return False
    
    def obtener_estado_scheduler(self):
        """Retorna el estado del scheduler de recordatorios"""
        try:
            jobs = self.scheduler.get_jobs()
            return {
                'scheduler_activo': self.scheduler.running,
                'total_jobs': len(jobs),
                'jobs_recordatorios': [job.id for job in jobs if job.id.startswith('recordatorio_')]
            }
        except Exception as e:
            logger.error(f"Error obteniendo estado del scheduler: {e}")
            return {'error': str(e)}

# Instancia global del servicio
recordatorio_service = RecordatorioService()
