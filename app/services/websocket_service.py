import json
import logging
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import request, session
from app.models.notificacion import Notificacion
from app.models.usuario import Usuario

logger = logging.getLogger(__name__)

class WebSocketService:
    def __init__(self, app=None):
        self.socketio = None
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Inicializa el servicio de WebSockets con la aplicación Flask"""
        self.socketio = SocketIO(app, cors_allowed_origins="*")
        self._register_handlers()
    
    def _register_handlers(self):
        """Registra los manejadores de eventos de WebSocket"""
        
        @self.socketio.on('connect')
        def handle_connect():
            """Maneja la conexión de un cliente"""
            logger.info(f"Cliente conectado: {request.sid}")
            emit('connected', {'message': 'Conectado exitosamente'})
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Maneja la desconexión de un cliente"""
            logger.info(f"Cliente desconectado: {request.sid}")
        
        @self.socketio.on('join_user_room')
        def handle_join_user_room(data):
            """Permite a un usuario unirse a su sala personal para notificaciones"""
            try:
                user_id = data.get('user_id')
                if user_id:
                    room_name = f"user_{user_id}"
                    join_room(room_name)
                    logger.info(f"Usuario {user_id} se unió a la sala {room_name}")
                    emit('joined_room', {'room': room_name, 'message': 'Sala unida exitosamente'})
                else:
                    emit('error', {'message': 'ID de usuario requerido'})
            except Exception as e:
                logger.error(f"Error uniendo usuario a sala: {e}")
                emit('error', {'message': 'Error interno del servidor'})
        
        @self.socketio.on('leave_user_room')
        def handle_leave_user_room(data):
            """Permite a un usuario salir de su sala personal"""
            try:
                user_id = data.get('user_id')
                if user_id:
                    room_name = f"user_{user_id}"
                    leave_room(room_name)
                    logger.info(f"Usuario {user_id} salió de la sala {room_name}")
                    emit('left_room', {'room': room_name, 'message': 'Sala abandonada exitosamente'})
                else:
                    emit('error', {'message': 'ID de usuario requerido'})
            except Exception as e:
                logger.error(f"Error sacando usuario de sala: {e}")
                emit('error', {'message': 'Error interno del servidor'})
        
        @self.socketio.on('join_admin_room')
        def handle_join_admin_room(data):
            """Permite a un administrador unirse a la sala de administradores"""
            try:
                user_id = data.get('user_id')
                is_admin = data.get('is_admin', False)
                
                if user_id and is_admin:
                    room_name = "admin_room"
                    join_room(room_name)
                    logger.info(f"Administrador {user_id} se unió a la sala de administradores")
                    emit('joined_admin_room', {'message': 'Sala de administradores unida'})
                else:
                    emit('error', {'message': 'Acceso denegado'})
            except Exception as e:
                logger.error(f"Error uniendo administrador a sala: {e}")
                emit('error', {'message': 'Error interno del servidor'})
        
        @self.socketio.on('send_notification')
        def handle_send_notification(data):
            """Maneja el envío de notificaciones entre usuarios"""
            try:
                target_user_id = data.get('target_user_id')
                message = data.get('message')
                notification_type = data.get('type', 'message')
                
                if target_user_id and message:
                    # Enviar notificación al usuario específico
                    self.send_notification_to_user(target_user_id, {
                        'type': notification_type,
                        'message': message,
                        'from_user': data.get('from_user'),
                        'timestamp': data.get('timestamp')
                    })
                    emit('notification_sent', {'message': 'Notificación enviada exitosamente'})
                else:
                    emit('error', {'message': 'Datos incompletos para enviar notificación'})
            except Exception as e:
                logger.error(f"Error enviando notificación: {e}")
                emit('error', {'message': 'Error interno del servidor'})
    
    def send_notification_to_user(self, user_id, notification_data):
        """Envía una notificación en tiempo real a un usuario específico"""
        try:
            room_name = f"user_{user_id}"
            emit('new_notification', notification_data, room=room_name)
            logger.info(f"Notificación enviada a usuario {user_id}: {notification_data}")
            return True
        except Exception as e:
            logger.error(f"Error enviando notificación en tiempo real: {e}")
            return False
    
    def send_notification_to_admins(self, notification_data):
        """Envía una notificación a todos los administradores"""
        try:
            emit('admin_notification', notification_data, room="admin_room")
            logger.info(f"Notificación enviada a administradores: {notification_data}")
            return True
        except Exception as e:
            logger.error(f"Error enviando notificación a administradores: {e}")
            return False
    
    def broadcast_notification(self, notification_data):
        """Envía una notificación a todos los usuarios conectados"""
        try:
            emit('broadcast_notification', notification_data, broadcast=True)
            logger.info(f"Notificación broadcast enviada: {notification_data}")
            return True
        except Exception as e:
            logger.error(f"Error enviando notificación broadcast: {e}")
            return False
    
    def send_reservation_notification(self, user_id, reservation_data):
        """Envía una notificación específica de reserva"""
        notification = {
            'type': 'reservation',
            'title': 'Nueva Reserva',
            'message': f'Reserva confirmada para {reservation_data.get("fecha")} a las {reservation_data.get("hora")}',
            'data': reservation_data,
            'timestamp': reservation_data.get('timestamp')
        }
        return self.send_notification_to_user(user_id, notification)
    
    def send_reminder_notification(self, user_id, reminder_data):
        """Envía una notificación de recordatorio"""
        notification = {
            'type': 'reminder',
            'title': 'Recordatorio de Reserva',
            'message': f'Recordatorio: Tienes una reserva mañana {reminder_data.get("fecha")} a las {reminder_data.get("hora")}',
            'data': reminder_data,
            'timestamp': reminder_data.get('timestamp')
        }
        return self.send_notification_to_user(user_id, notification)
    
    def send_cancellation_notification(self, user_id, cancellation_data):
        """Envía una notificación de cancelación"""
        notification = {
            'type': 'cancellation',
            'title': 'Reserva Cancelada',
            'message': f'Tu reserva para {cancellation_data.get("fecha")} a las {cancellation_data.get("hora")} ha sido cancelada',
            'data': cancellation_data,
            'timestamp': cancellation_data.get('timestamp')
        }
        return self.send_notification_to_user(user_id, notification)
    
    def get_socketio(self):
        """Retorna la instancia de SocketIO"""
        return self.socketio

# Instancia global del servicio
websocket_service = WebSocketService()
