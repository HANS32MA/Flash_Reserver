import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from app import db
from app.models.reserva import Reserva
from app.services.notificacion_service import notificacion_service
from app.services.websocket_service import websocket_service

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        logger.info("Servicio de programación iniciado")
    
    def schedule_reservation_reminders(self):
        """Programa recordatorios para todas las reservas futuras"""
        try:
            # Obtener reservas para mañana
            tomorrow = datetime.now().date() + timedelta(days=1)
            reservas_tomorrow = Reserva.query.filter(
                Reserva.fecha == tomorrow,
                Reserva.estado == 'confirmada'
            ).all()
            
            for reserva in reservas_tomorrow:
                # Programar recordatorio para 24 horas antes
                reminder_time = datetime.combine(reserva.fecha, reserva.horario.hora_inicio) - timedelta(hours=24)
                
                if reminder_time > datetime.now():
                    self.scheduler.add_job(
                        func=self.send_reminder,
                        trigger=DateTrigger(run_date=reminder_time),
                        args=[reserva.id],
                        id=f"reminder_{reserva.id}",
                        replace_existing=True
                    )
                    logger.info(f"Recordatorio programado para reserva {reserva.id} a las {reminder_time}")
            
            logger.info(f"Se programaron {len(reservas_tomorrow)} recordatorios")
            
        except Exception as e:
            logger.error(f"Error programando recordatorios: {e}")
    
    def send_reminder(self, reserva_id):
        """Envía recordatorio para una reserva específica"""
        try:
            reserva = Reserva.query.get(reserva_id)
            if not reserva or reserva.estado != 'confirmada':
                return
            
            # Enviar notificación por email
            notificacion_service.notificar_recordatorio_reserva(reserva_id)
            
            # Enviar notificación en tiempo real
            datos = {
                'reserva_id': reserva.id,
                'fecha': reserva.fecha.strftime('%d/%m/%Y'),
                'hora': reserva.horario.hora_inicio.strftime('%H:%M'),
                'timestamp': datetime.now().isoformat()
            }
            
            websocket_service.send_reminder_notification(reserva.usuario_id, datos)
            
            logger.info(f"Recordatorio enviado para reserva {reserva_id}")
            
        except Exception as e:
            logger.error(f"Error enviando recordatorio para reserva {reserva_id}: {e}")
    
    def schedule_daily_cleanup(self):
        """Programa limpieza diaria de notificaciones antiguas"""
        try:
            # Ejecutar todos los días a las 2:00 AM
            self.scheduler.add_job(
                func=self.cleanup_old_notifications,
                trigger='cron',
                hour=2,
                minute=0,
                id="daily_cleanup",
                replace_existing=True
            )
            logger.info("Limpieza diaria programada para las 2:00 AM")
            
        except Exception as e:
            logger.error(f"Error programando limpieza diaria: {e}")
    
    def cleanup_old_notifications(self):
        """Limpia notificaciones antiguas de la base de datos"""
        try:
            from app.models.notificacion import Notificacion
            
            # Eliminar notificaciones más antiguas de 30 días
            cutoff_date = datetime.now() - timedelta(days=30)
            
            old_notifications = Notificacion.query.filter(
                Notificacion.fecha_creacion < cutoff_date,
                Notificacion.estado.in_(['enviado', 'fallido'])
            ).all()
            
            count = len(old_notifications)
            for notif in old_notifications:
                db.session.delete(notif)
            
            db.session.commit()
            logger.info(f"Se eliminaron {count} notificaciones antiguas")
            
        except Exception as e:
            logger.error(f"Error en limpieza de notificaciones: {e}")
            db.session.rollback()
    
    def schedule_weekly_reports(self):
        """Programa reportes semanales para administradores"""
        try:
            # Ejecutar todos los lunes a las 9:00 AM
            self.scheduler.add_job(
                func=self.send_weekly_report,
                trigger='cron',
                day_of_week='mon',
                hour=9,
                minute=0,
                id="weekly_report",
                replace_existing=True
            )
            logger.info("Reporte semanal programado para los lunes a las 9:00 AM")
            
        except Exception as e:
            logger.error(f"Error programando reporte semanal: {e}")
    
    def send_weekly_report(self):
        """Envía reporte semanal a administradores"""
        try:
            from app.models.usuario import Usuario
            from app.models.reserva import Reserva
            
            # Obtener estadísticas de la semana
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=7)
            
            total_reservas = Reserva.query.filter(
                Reserva.fecha.between(start_date, end_date)
            ).count()
            
            reservas_confirmadas = Reserva.query.filter(
                Reserva.fecha.between(start_date, end_date),
                Reserva.estado == 'confirmada'
            ).count()
            
            reservas_canceladas = Reserva.query.filter(
                Reserva.fecha.between(start_date, end_date),
                Reserva.estado == 'cancelada'
            ).count()
            
            # Obtener administradores
            admins = Usuario.query.filter_by(rol_id=1).all()  # Asumiendo que rol_id=1 es admin
            
            # Enviar notificación a administradores
            for admin in admins:
                notification_data = {
                    'type': 'weekly_report',
                    'title': 'Reporte Semanal - Flash Reserver',
                    'message': f'Resumen de la semana: {total_reservas} reservas totales, {reservas_confirmadas} confirmadas, {reservas_canceladas} canceladas',
                    'data': {
                        'total_reservas': total_reservas,
                        'reservas_confirmadas': reservas_confirmadas,
                        'reservas_canceladas': reservas_canceladas,
                        'periodo': f"{start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}"
                    },
                    'timestamp': datetime.now().isoformat()
                }
                
                websocket_service.send_notification_to_user(admin.id, notification_data)
                
                # También enviar por email
                notificacion_service.crear_notificacion(
                    usuario_id=admin.id,
                    tipo='email',
                    titulo='Reporte Semanal - Flash Reserver',
                    mensaje=f'Resumen de la semana: {total_reservas} reservas totales, {reservas_confirmadas} confirmadas, {reservas_canceladas} canceladas',
                    datos_adicionales=notification_data['data']
                )
            
            logger.info(f"Reporte semanal enviado a {len(admins)} administradores")
            
        except Exception as e:
            logger.error(f"Error enviando reporte semanal: {e}")
    
    def schedule_reservation_confirmations(self):
        """Programa confirmaciones automáticas de reservas"""
        try:
            # Ejecutar cada 5 minutos
            self.scheduler.add_job(
                func=self.process_pending_reservations,
                trigger='interval',
                minutes=5,
                id="reservation_confirmations",
                replace_existing=True
            )
            logger.info("Procesamiento de reservas pendientes programado cada 5 minutos")
            
        except Exception as e:
            logger.error(f"Error programando confirmaciones de reservas: {e}")
    
    def process_pending_reservations(self):
        """Procesa reservas pendientes y envía confirmaciones"""
        try:
            from app.models.reserva import Reserva
            
            # Obtener reservas pendientes
            pending_reservations = Reserva.query.filter_by(estado='pendiente').all()
            
            for reserva in pending_reservations:
                # Aquí podrías implementar lógica de confirmación automática
                # Por ejemplo, verificar disponibilidad, etc.
                
                # Por ahora, solo enviar notificación de confirmación
                notificacion_service.notificar_reserva_confirmada(reserva.id)
                
                # Marcar como confirmada
                reserva.estado = 'confirmada'
                db.session.commit()
                
                logger.info(f"Reserva {reserva.id} confirmada automáticamente")
            
            if pending_reservations:
                logger.info(f"Se procesaron {len(pending_reservations)} reservas pendientes")
                
        except Exception as e:
            logger.error(f"Error procesando reservas pendientes: {e}")
            db.session.rollback()
    
    def start_all_schedules(self):
        """Inicia todos los trabajos programados"""
        try:
            self.schedule_reservation_reminders()
            self.schedule_daily_cleanup()
            self.schedule_weekly_reports()
            self.schedule_reservation_confirmations()
            
            logger.info("Todos los trabajos programados han sido iniciados")
            
        except Exception as e:
            logger.error(f"Error iniciando trabajos programados: {e}")
    
    def stop_scheduler(self):
        """Detiene el scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler detenido")
    
    def get_scheduler_status(self):
        """Retorna el estado del scheduler"""
        return {
            'running': self.scheduler.running,
            'jobs': len(self.scheduler.get_jobs()),
            'next_run': self.scheduler.get_jobs()[0].next_run_time if self.scheduler.get_jobs() else None
        }

# Instancia global del servicio
scheduler_service = SchedulerService()
