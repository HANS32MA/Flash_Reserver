import logging
from datetime import datetime, timedelta
from flask import current_app, render_template_string
from flask_mail import Message
from app import db, mail
from app.models.notificacion import Notificacion
from app.models.usuario import Usuario
from app.models.reserva import Reserva
import threading
import queue
import time

logger = logging.getLogger(__name__)

class NotificacionService:
    def __init__(self):
        self.cola_notificaciones = queue.Queue()
        self.worker_activo = False
    
    def iniciar_worker(self):
        """Inicia el worker en background para procesar notificaciones"""
        if not self.worker_activo:
            self.worker_activo = True
            thread = threading.Thread(target=self._procesar_cola, daemon=True)
            thread.start()
            logger.info("Worker de notificaciones iniciado")
    
    def _procesar_cola(self):
        """Procesa la cola de notificaciones en background"""
        while self.worker_activo:
            try:
                # Procesar notificaciones pendientes
                notificaciones_pendientes = Notificacion.query.filter_by(
                    estado='pendiente'
                ).filter(
                    Notificacion.intentos < Notificacion.max_intentos
                ).all()
                
                for notif in notificaciones_pendientes:
                    try:
                        if notif.tipo == 'email':
                            self._enviar_email(notif)
                        elif notif.tipo == 'sms':
                            self._enviar_sms(notif)
                        elif notif.tipo == 'push':
                            self._enviar_push(notif)
                        elif notif.tipo == 'in_app':
                            self._enviar_in_app(notif)
                    except Exception as e:
                        logger.error(f"Error enviando notificación {notif.id}: {e}")
                        notif.marcar_fallido()
                
                time.sleep(30)  # Esperar 30 segundos antes de la siguiente verificación
                
            except Exception as e:
                logger.error(f"Error en worker de notificaciones: {e}")
                time.sleep(60)  # Esperar 1 minuto en caso de error
    
    def crear_notificacion(self, usuario_id, tipo, titulo, mensaje, datos_adicionales=None):
        """Crea una nueva notificación en la base de datos"""
        try:
            notif = Notificacion(
                usuario_id=usuario_id,
                tipo=tipo,
                titulo=titulo,
                mensaje=mensaje,
                datos_adicionales=datos_adicionales
            )
            db.session.add(notif)
            db.session.commit()
            
            # Procesar inmediatamente las notificaciones de email
            if tipo == 'email':
                try:
                    self._enviar_email(notif)
                except Exception as e:
                    logger.error(f"Error enviando email inmediatamente: {e}")
                    # Si falla el envío inmediato, se procesará por el worker
                    pass
            
            # Agregar a la cola para procesamiento por el worker (para otros tipos)
            self.cola_notificaciones.put(notif)
            
            logger.info(f"Notificación creada: {tipo} para usuario {usuario_id}")
            return notif
            
        except Exception as e:
            logger.error(f"Error creando notificación: {e}")
            db.session.rollback()
            return None
    
    def _enviar_email(self, notificacion):
        """Envía una notificación por email"""
        try:
            usuario = Usuario.query.get(notificacion.usuario_id)
            if not usuario or not usuario.Email:
                notificacion.marcar_fallido()
                return False
            
            # Renderizar plantilla de email
            html_content = self._renderizar_plantilla_email(
                notificacion.titulo,
                notificacion.mensaje,
                usuario,
                notificacion.datos_adicionales
            )
            
            msg = Message(
                subject=notificacion.titulo,
                recipients=[usuario.Email],
                html=html_content
            )
            
            mail.send(msg)
            notificacion.marcar_enviado()
            logger.info(f"Email enviado exitosamente a {usuario.Email}")
            return True
            
        except Exception as e:
            logger.error(f"Error enviando email: {e}")
            notificacion.marcar_fallido()
            return False
    
    def _enviar_sms(self, notificacion):
        """Envía una notificación por SMS (placeholder para implementación futura)"""
        try:
            # Aquí implementarías la lógica para enviar SMS
            # Por ahora solo marcamos como enviado
            logger.info(f"SMS enviado (placeholder) para usuario {notificacion.usuario_id}")
            notificacion.marcar_enviado()
            return True
        except Exception as e:
            logger.error(f"Error enviando SMS: {e}")
            notificacion.marcar_fallido()
            return False
    
    def _enviar_push(self, notificacion):
        """Envía una notificación push (placeholder para implementación futura)"""
        try:
            # Aquí implementarías la lógica para notificaciones push
            # Por ahora solo marcamos como enviado
            logger.info(f"Push enviado (placeholder) para usuario {notificacion.usuario_id}")
            notificacion.marcar_enviado()
            return True
        except Exception as e:
            logger.error(f"Error enviando push: {e}")
            notificacion.marcar_fallido()
            return False
    
    def _enviar_in_app(self, notificacion):
        """Envía una notificación in-app (se almacena para mostrar en la interfaz)"""
        try:
            # Las notificaciones in-app se almacenan y se muestran en la interfaz
            notificacion.marcar_enviado()
            logger.info(f"Notificación in-app creada para usuario {notificacion.usuario_id}")
            return True
        except Exception as e:
            logger.error(f"Error creando notificación in-app: {e}")
            notificacion.marcar_fallido()
            return False
    
    def _renderizar_plantilla_email(self, titulo, mensaje, usuario, datos_adicionales=None):
        """Renderiza la plantilla de email con los datos del usuario"""
        
        # Determinar si es una cancelación basándose en el título
        es_cancelacion = 'cancelada' in titulo.lower()
        
        if es_cancelacion:
            # Plantilla específica para cancelaciones con diseño moderno
            template = """
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{{ titulo }}</title>
                <style>
                    * { margin: 0; padding: 0; box-sizing: border-box; }
                    body { 
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                        line-height: 1.6; 
                        color: #333; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                        padding: 20px 0;
                    }
                    .email-container { 
                        max-width: 600px; 
                        margin: 0 auto; 
                        background: #ffffff; 
                        border-radius: 20px; 
                        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                        overflow: hidden;
                    }
                    .header { 
                        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
                        color: white; 
                        padding: 40px 30px; 
                        text-align: center; 
                        position: relative;
                    }
                    .header::before {
                        content: '';
                        position: absolute;
                        top: 0;
                        left: 0;
                        right: 0;
                        bottom: 0;
                        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="80" cy="40" r="1.5" fill="rgba(255,255,255,0.1)"/><circle cx="40" cy="80" r="1" fill="rgba(255,255,255,0.1)"/></svg>');
                        opacity: 0.3;
                    }
                    .header h1 { 
                        margin: 0; 
                        font-size: 32px; 
                        font-weight: 700;
                        position: relative;
                        z-index: 1;
                    }
                    .header .subtitle { 
                        margin-top: 10px; 
                        font-size: 18px;
                        opacity: 0.9;
                        position: relative;
                        z-index: 1;
                    }
                    .header .icon { 
                        font-size: 48px; 
                        margin-bottom: 20px;
                        position: relative;
                        z-index: 1;
                    }
                    .content { 
                        padding: 40px 30px; 
                        background: #ffffff; 
                    }
                    .greeting {
                        text-align: center;
                        margin-bottom: 30px;
                        padding: 20px;
                        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                        border-radius: 15px;
                        border-left: 5px solid #dc3545;
                    }
                    .greeting h2 { 
                        color: #dc3545; 
                        margin-bottom: 10px;
                        font-size: 24px;
                    }
                    .greeting p {
                        font-size: 16px;
                        color: #666;
                        margin: 0;
                    }
                    .reserva-details { 
                        background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
                        border: 2px solid #feb2b2;
                        border-radius: 20px; 
                        padding: 30px; 
                        margin: 30px 0;
                        box-shadow: 0 10px 30px rgba(220, 53, 69, 0.1);
                    }
                    .reserva-details h3 { 
                        color: #dc3545; 
                        margin-bottom: 25px;
                        font-size: 20px;
                        text-align: center;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        gap: 10px;
                    }
                    .detail-row { 
                        display: flex; 
                        justify-content: space-between; 
                        align-items: center;
                        margin: 15px 0; 
                        padding: 15px; 
                        background: white;
                        border-radius: 12px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                        transition: transform 0.2s ease;
                    }
                    .detail-row:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                    }
                    .detail-label { 
                        font-weight: 600; 
                        color: #555;
                        display: flex;
                        align-items: center;
                        gap: 8px;
                    }
                    .detail-value { 
                        color: #dc3545; 
                        font-weight: 600;
                        font-size: 16px;
                    }
                    .cancel-info { 
                        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
                        border: 2px solid #ffd43b;
                        border-radius: 20px; 
                        padding: 25px; 
                        margin: 25px 0;
                        box-shadow: 0 10px 30px rgba(255, 193, 7, 0.1);
                    }
                    .cancel-info h4 { 
                        color: #856404; 
                        margin-bottom: 20px;
                        font-size: 18px;
                        display: flex;
                        align-items: center;
                        gap: 10px;
                    }
                    .cancel-info ul {
                        list-style: none;
                        padding: 0;
                    }
                    .cancel-info li {
                        padding: 8px 0;
                        border-bottom: 1px solid rgba(133, 100, 4, 0.1);
                        display: flex;
                        align-items: center;
                        gap: 10px;
                    }
                    .cancel-info li:last-child {
                        border-bottom: none;
                    }
                    .btn-container {
                        text-align: center;
                        margin: 40px 0;
                    }
                    .btn { 
                        display: inline-block; 
                        padding: 16px 32px; 
                        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
                        color: white; 
                        text-decoration: none; 
                        border-radius: 50px; 
                        font-weight: 600;
                        font-size: 16px;
                        transition: all 0.3s ease;
                        box-shadow: 0 8px 25px rgba(0, 123, 255, 0.3);
                        border: none;
                        cursor: pointer;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                    }
                    .btn:hover {
                        transform: translateY(-3px);
                        box-shadow: 0 12px 35px rgba(0, 123, 255, 0.4);
                        background: linear-gradient(135deg, #0056b3 0%, #004085 100%);
                    }
                    .btn-secondary {
                        background: linear-gradient(135deg, #6c757d 0%, #545b62 100%);
                        box-shadow: 0 8px 25px rgba(108, 117, 125, 0.3);
                        margin-left: 15px;
                    }
                    .btn-secondary:hover {
                        box-shadow: 0 12px 35px rgba(108, 117, 125, 0.4);
                        background: linear-gradient(135deg, #545b62 0%, #3d4449 100%);
                    }
                    .footer { 
                        text-align: center; 
                        padding: 30px; 
                        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                        color: #666; 
                        font-size: 14px;
                        border-top: 1px solid #dee2e6;
                    }
                    .footer h5 {
                        color: #495057;
                        margin-bottom: 15px;
                        font-size: 16px;
                    }
                    .contact-info {
                        display: flex;
                        justify-content: center;
                        gap: 20px;
                        margin: 20px 0;
                        flex-wrap: wrap;
                    }
                    .contact-item {
                        display: flex;
                        align-items: center;
                        gap: 8px;
                        color: #007bff;
                        text-decoration: none;
                        transition: color 0.2s ease;
                    }
                    .contact-item:hover {
                        color: #0056b3;
                    }
                    .social-links {
                        margin-top: 20px;
                    }
                    .social-links a {
                        display: inline-block;
                        margin: 0 10px;
                        color: #6c757d;
                        font-size: 20px;
                        transition: color 0.2s ease;
                    }
                    .social-links a:hover {
                        color: #007bff;
                    }
                    @media (max-width: 600px) {
                        .email-container { margin: 10px; border-radius: 15px; }
                        .header { padding: 30px 20px; }
                        .content { padding: 30px 20px; }
                        .detail-row { flex-direction: column; text-align: center; gap: 10px; }
                        .btn { display: block; margin: 10px 0; }
                        .contact-info { flex-direction: column; gap: 15px; }
                    }
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="header">
                        <div class="icon">❌</div>
                        <h1>Flash Reserver</h1>
                        <div class="subtitle">Reserva Cancelada</div>
                    </div>
                    
                    <div class="content">
                        <div class="greeting">
                            <h2>¡Hola {{ usuario.Nombre }}!</h2>
                            <p>{{ mensaje }}</p>
                        </div>
                        
                        {% if datos_adicionales %}
                        <div class="reserva-details">
                            <h3>📋 Detalles de la Reserva Cancelada</h3>
                            {% if datos_adicionales.reserva_id %}
                            <div class="detail-row">
                                <span class="detail-label">🆔 ID de Reserva</span>
                                <span class="detail-value">#{{ datos_adicionales.reserva_id }}</span>
                            </div>
                            {% endif %}
                            {% if datos_adicionales.fecha %}
                            <div class="detail-row">
                                <span class="detail-label">📅 Fecha Programada</span>
                                <span class="detail-value">{{ datos_adicionales.fecha }}</span>
                            </div>
                            {% endif %}
                            {% if datos_adicionales.hora %}
                            <div class="detail-row">
                                <span class="detail-label">🕐 Hora Programada</span>
                                <span class="detail-value">{{ datos_adicionales.hora }}</span>
                            </div>
                            {% endif %}
                            {% if datos_adicionales.cancha_nombre %}
                            <div class="detail-row">
                                <span class="detail-label">⚽ Cancha Reservada</span>
                                <span class="detail-value">{{ datos_adicionales.cancha_nombre }}</span>
                            </div>
                            {% endif %}
                            <div class="detail-row">
                                <span class="detail-label">❌ Estado Actual</span>
                                <span class="detail-value">Cancelada</span>
                            </div>
                        </div>
                        
                        <div class="cancel-info">
                            <h4>📅 Información de la Cancelación</h4>
                            <ul>
                                {% if datos_adicionales.fecha_cancelacion %}
                                <li>🕐 <strong>Fecha de cancelación:</strong> {{ datos_adicionales.fecha_cancelacion }}</li>
                                {% endif %}
                                {% if datos_adicionales.motivo_cancelacion %}
                                <li>📝 <strong>Motivo:</strong> {{ datos_adicionales.motivo_cancelacion }}</li>
                                {% endif %}
                                <li>💰 <strong>Política:</strong> Sin cargos por cancelación con más de 2 horas de anticipación</li>
                                <li>🔄 <strong>Reembolso:</strong> Procesamiento automático en 3-5 días hábiles</li>
                            </ul>
                        </div>
                        {% endif %}
                        
                        <div class="btn-container">
                            <a href="http://127.0.0.1:5000/client/canchas" class="btn">
                                🏟️ Hacer Nueva Reserva
                            </a>
                            <a href="http://127.0.0.1:5000/client/mis-reservas" class="btn btn-secondary">
                                📋 Ver Mis Reservas
                            </a>
                        </div>
                        
                        <div style="text-align: center; margin: 30px 0; padding: 20px; background: #f8f9fa; border-radius: 15px;">
                            <h4 style="color: #495057; margin-bottom: 15px;">💡 ¿Necesitas ayuda?</h4>
                            <p style="color: #666; margin-bottom: 20px;">
                                Nuestro equipo de soporte está disponible para ayudarte con cualquier consulta sobre tu reserva o para hacer una nueva reserva.
                            </p>
                        </div>
                    </div>
                    
                    <div class="footer">
                        <h5>📞 Contacto y Soporte</h5>
                        <div class="contact-info">
                            <a href="mailto:soporte@flashreserver.com" class="contact-item">
                                📧 soporte@flashreserver.com
                            </a>
                            <a href="tel:+15551234567" class="contact-item">
                                📱 +1 (555) 123-4567
                            </a>
                            <a href="http://127.0.0.1:5000/client/ayuda" class="contact-item">
                                ❓ Centro de Ayuda
                            </a>
                        </div>
                        
                        <div class="social-links">
                            <a href="#" title="Facebook">📘</a>
                            <a href="#" title="Instagram">📷</a>
                            <a href="#" title="Twitter">🐦</a>
                            <a href="#" title="WhatsApp">📱</a>
                        </div>
                        
                        <p style="margin-top: 20px; font-size: 12px; color: #adb5bd;">
                            Este es un email automático generado por Flash Reserver.<br>
                            Por favor no respondas a este mensaje.
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
        else:
            # Plantilla estándar para confirmaciones con diseño moderno
            template = """
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{{ titulo }}</title>
                <style>
                    * { margin: 0; padding: 0; box-sizing: border-box; }
                    body { 
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                        line-height: 1.6; 
                        color: #333; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                        padding: 20px 0;
                    }
                    .email-container { 
                        max-width: 600px; 
                        margin: 0 auto; 
                        background: #ffffff; 
                        border-radius: 20px; 
                        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                        overflow: hidden;
                    }
                    .header { 
                        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                        color: white; 
                        padding: 40px 30px; 
                        text-align: center; 
                        position: relative;
                    }
                    .header::before {
                        content: '';
                        position: absolute;
                        top: 0;
                        left: 0;
                        right: 0;
                        bottom: 0;
                        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="80" cy="40" r="1.5" fill="rgba(255,255,255,0.1)"/><circle cx="40" cy="80" r="1" fill="rgba(255,255,255,0.1)"/></svg>');
                        opacity: 0.3;
                    }
                    .header h1 { 
                        margin: 0; 
                        font-size: 32px; 
                        font-weight: 700;
                        position: relative;
                        z-index: 1;
                    }
                    .header .subtitle { 
                        margin-top: 10px; 
                        font-size: 18px;
                        opacity: 0.9;
                        position: relative;
                        z-index: 1;
                    }
                    .header .icon { 
                        font-size: 48px; 
                        margin-bottom: 20px;
                        position: relative;
                        z-index: 1;
                    }
                    .content { 
                        padding: 40px 30px; 
                        background: #ffffff; 
                    }
                    .greeting {
                        text-align: center;
                        margin-bottom: 30px;
                        padding: 20px;
                        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                        border-radius: 15px;
                        border-left: 5px solid #28a745;
                    }
                    .greeting h2 { 
                        color: #28a745; 
                        margin-bottom: 10px;
                        font-size: 24px;
                    }
                    .greeting p {
                        font-size: 16px;
                        color: #666;
                        margin: 0;
                    }
                    .reserva-details { 
                        background: linear-gradient(135deg, #f0fff4 0%, #dcffe4 100%);
                        border: 2px solid #9ae6b4;
                        border-radius: 20px; 
                        padding: 30px; 
                        margin: 30px 0;
                        box-shadow: 0 10px 30px rgba(40, 167, 69, 0.1);
                    }
                    .reserva-details h3 { 
                        color: #28a745; 
                        margin-bottom: 25px;
                        font-size: 20px;
                        text-align: center;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        gap: 10px;
                    }
                    .detail-row { 
                        display: flex; 
                        justify-content: space-between; 
                        align-items: center;
                        margin: 15px 0; 
                        padding: 15px; 
                        background: white;
                        border-radius: 12px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                        transition: transform 0.2s ease;
                    }
                    .detail-row:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                    }
                    .detail-label { 
                        font-weight: 600; 
                        color: #555;
                        display: flex;
                        align-items: center;
                        gap: 8px;
                    }
                    .detail-value { 
                        color: #28a745; 
                        font-weight: 600;
                        font-size: 16px;
                    }
                    .tips-section { 
                        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
                        border: 2px solid #ffd43b;
                        border-radius: 20px; 
                        padding: 25px; 
                        margin: 25px 0;
                        box-shadow: 0 10px 30px rgba(255, 193, 7, 0.1);
                    }
                    .tips-section h4 { 
                        color: #856404; 
                        margin-bottom: 20px;
                        font-size: 18px;
                        display: flex;
                        align-items: center;
                        gap: 10px;
                    }
                    .tips-section ul {
                        list-style: none;
                        padding: 0;
                    }
                    .tips-section li {
                        padding: 8px 0;
                        border-bottom: 1px solid rgba(133, 100, 4, 0.1);
                        display: flex;
                        align-items: center;
                        gap: 10px;
                    }
                    .tips-section li:last-child {
                        border-bottom: none;
                    }
                    .btn-container {
                        text-align: center;
                        margin: 40px 0;
                    }
                    .btn { 
                        display: inline-block; 
                        padding: 16px 32px; 
                        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
                        color: white; 
                        text-decoration: none; 
                        border-radius: 50px; 
                        font-weight: 600;
                        font-size: 16px;
                        transition: all 0.3s ease;
                        box-shadow: 0 8px 25px rgba(0, 123, 255, 0.3);
                        border: none;
                        cursor: pointer;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                    }
                    .btn:hover {
                        transform: translateY(-3px);
                        box-shadow: 0 12px 35px rgba(0, 123, 255, 0.4);
                        background: linear-gradient(135deg, #0056b3 0%, #004085 100%);
                    }
                    .btn-secondary {
                        background: linear-gradient(135deg, #6c757d 0%, #545b62 100%);
                        box-shadow: 0 8px 25px rgba(108, 117, 125, 0.3);
                        margin-left: 15px;
                    }
                    .btn-secondary:hover {
                        box-shadow: 0 12px 35px rgba(108, 117, 125, 0.4);
                        background: linear-gradient(135deg, #545b62 0%, #3d4449 100%);
                    }
                    .footer { 
                        text-align: center; 
                        padding: 30px; 
                        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                        color: #666; 
                        font-size: 14px;
                        border-top: 1px solid #dee2e6;
                    }
                    .footer h5 {
                        color: #495057;
                        margin-bottom: 15px;
                        font-size: 16px;
                    }
                    .contact-info {
                        display: flex;
                        justify-content: center;
                        gap: 20px;
                        margin: 20px 0;
                        flex-wrap: wrap;
                    }
                    .contact-item {
                        display: flex;
                        align-items: center;
                        gap: 8px;
                        color: #007bff;
                        text-decoration: none;
                        transition: color 0.2s ease;
                    }
                    .contact-item:hover {
                        color: #0056b3;
                    }
                    .social-links {
                        margin-top: 20px;
                    }
                    .social-links a {
                        display: inline-block;
                        margin: 0 10px;
                        color: #6c757d;
                        font-size: 20px;
                        transition: color 0.2s ease;
                    }
                    .social-links a:hover {
                        color: #007bff;
                    }
                    @media (max-width: 600px) {
                        .email-container { margin: 10px; border-radius: 15px; }
                        .header { padding: 30px 20px; }
                        .content { padding: 30px 20px; }
                        .detail-row { flex-direction: column; text-align: center; gap: 10px; }
                        .btn { display: block; margin: 10px 0; }
                        .contact-info { flex-direction: column; gap: 15px; }
                    }
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="header">
                        <div class="icon">⚽</div>
                        <h1>Flash Reserver</h1>
                        <div class="subtitle">Tu plataforma de reservas deportivas</div>
                    </div>
                    
                    <div class="content">
                        <div class="greeting">
                            <h2>¡Hola {{ usuario.Nombre }}!</h2>
                            <p>{{ mensaje }}</p>
                        </div>
                        
                        {% if datos_adicionales %}
                        <div class="reserva-details">
                            <h3>📋 Detalles de tu Reserva</h3>
                            {% if datos_adicionales.reserva_id %}
                            <div class="detail-row">
                                <span class="detail-label">🆔 ID de Reserva</span>
                                <span class="detail-value">#{{ datos_adicionales.reserva_id }}</span>
                            </div>
                            {% endif %}
                            {% if datos_adicionales.fecha %}
                            <div class="detail-row">
                                <span class="detail-label">📅 Fecha de Reserva</span>
                                <span class="detail-value">{{ datos_adicionales.fecha }}</span>
                            </div>
                            {% endif %}
                            {% if datos_adicionales.hora %}
                            <div class="detail-row">
                                <span class="detail-label">🕐 Hora de Reserva</span>
                                <span class="detail-value">{{ datos_adicionales.hora }}</span>
                            </div>
                            {% endif %}
                            {% if datos_adicionales.cancha_nombre %}
                            <div class="detail-row">
                                <span class="detail-label">⚽ Cancha Reservada</span>
                                <span class="detail-value">{{ datos_adicionales.cancha_nombre }}</span>
                            </div>
                            {% endif %}
                            <div class="detail-row">
                                <span class="detail-label">✅ Estado Actual</span>
                                <span class="detail-value">Confirmada</span>
                            </div>
                        </div>
                        
                        <div class="tips-section">
                            <h4>💡 Preparativos para tu Reserva</h4>
                            <ul>
                                <li>⏰ <strong>Llega 10 minutos antes</strong> de tu hora reservada</li>
                                <li>🏃 <strong>Trae tu implemento deportivo</strong> necesario</li>
                                <li>💧 <strong>Lleva agua</strong> y ropa cómoda</li>
                                <li>📱 <strong>Confirma tu asistencia</strong> si es necesario</li>
                                <li>🚗 <strong>Estacionamiento disponible</strong> en el complejo</li>
                            </ul>
                        </div>
                        {% endif %}
                        
                        <div class="btn-container">
                            <a href="http://127.0.0.1:5000/client/mis-reservas" class="btn">
                                📋 Ver Mis Reservas
                            </a>
                            <a href="http://127.0.0.1:5000/client/canchas" class="btn btn-secondary">
                                🏟️ Hacer Otra Reserva
                            </a>
                        </div>
                        
                        <div style="text-align: center; margin: 30px 0; padding: 20px; background: #f8f9fa; border-radius: 15px;">
                            <h4 style="color: #495057; margin-bottom: 15px;">❓ ¿Necesitas cambiar tu reserva?</h4>
                            <p style="color: #666; margin-bottom: 20px;">
                                Si necesitas cancelar o reprogramar tu reserva, hazlo con al menos 2 horas de anticipación para evitar cargos adicionales.
                            </p>
                            <a href="http://127.0.0.1:5000/client/mis-reservas" style="color: #007bff; text-decoration: none; font-weight: 600;">
                                🔄 Gestionar Mi Reserva
                            </a>
                        </div>
                    </div>
                    
                    <div class="footer">
                        <h5>📞 Contacto y Soporte</h5>
                        <div class="contact-info">
                            <a href="mailto:soporte@flashreserver.com" class="contact-item">
                                📧 soporte@flashreserver.com
                            </a>
                            <a href="tel:+15551234567" class="contact-item">
                                📱 +1 (555) 123-4567
                            </a>
                            <a href="http://127.0.0.1:5000/client/ayuda" class="contact-item">
                                ❓ Centro de Ayuda
                            </a>
                        </div>
                        
                        <div class="social-links">
                            <a href="#" title="Facebook">📘</a>
                            <a href="#" title="Instagram">📷</a>
                            <a href="#" title="Twitter">🐦</a>
                            <a href="#" title="WhatsApp">📱</a>
                        </div>
                        
                        <p style="margin-top: 20px; font-size: 12px; color: #adb5bd;">
                            Este es un email automático generado por Flash Reserver.<br>
                            Por favor no respondas a este mensaje.
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
        
        return render_template_string(template, 
                                   titulo=titulo, 
                                   mensaje=mensaje, 
                                   usuario=usuario,
                                   datos_adicionales=datos_adicionales or {})
    
    # Métodos específicos para diferentes tipos de notificaciones
    def notificar_reserva_confirmada(self, reserva_id):
        """Envía notificación de confirmación de reserva"""
        try:
            reserva = Reserva.query.get(reserva_id)
            if not reserva:
                return False
            
            datos = {
                'reserva_id': reserva.Id,
                'fecha': reserva.Fecha.strftime('%d/%m/%Y'),
                'hora': reserva.HoraInicio.strftime('%H:%M'),
                'cancha_nombre': reserva.cancha.Nombre if reserva.cancha else 'Cancha Deportiva'
            }
            
            # Crear notificación por email
            self.crear_notificacion(
                usuario_id=reserva.UsuarioId,
                tipo='email',
                titulo='Reserva Confirmada - Flash Reserver',
                mensaje=f'Tu reserva para el {datos["fecha"]} a las {datos["hora"]} ha sido confirmada exitosamente.',
                datos_adicionales=datos
            )
            
            # También crear notificación in-app
            self.crear_notificacion(
                usuario_id=reserva.UsuarioId,
                tipo='in_app',
                titulo='Reserva Confirmada',
                mensaje=f'Tu reserva para el {datos["fecha"]} a las {datos["hora"]} ha sido confirmada.',
                datos_adicionales=datos
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error notificando reserva confirmada: {e}")
            return False
    
    def notificar_recordatorio_reserva(self, reserva_id):
        """Envía recordatorio de reserva (24 horas antes)"""
        try:
            reserva = Reserva.query.get(reserva_id)
            if not reserva:
                return False
            
            datos = {
                'reserva_id': reserva.id,
                'fecha': reserva.fecha.strftime('%d/%m/%Y'),
                'hora': reserva.horario.hora_inicio.strftime('%H:%M')
            }
            
            self.crear_notificacion(
                usuario_id=reserva.usuario_id,
                tipo='email',
                titulo='Recordatorio de Reserva - Flash Reserver',
                mensaje=f'Recordatorio: Tienes una reserva mañana {datos["fecha"]} a las {datos["hora"]}.',
                datos_adicionales=datos
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error notificando recordatorio: {e}")
            return False
    
    def notificar_cancelacion_reserva(self, reserva_id):
        """Envía notificación de cancelación de reserva"""
        try:
            reserva = Reserva.query.get(reserva_id)
            if not reserva:
                return False
            
            datos = {
                'reserva_id': reserva.Id,
                'fecha': reserva.Fecha.strftime('%d/%m/%Y'),
                'hora': reserva.HoraInicio.strftime('%H:%M'),
                'cancha_nombre': reserva.cancha.Nombre if reserva.cancha else 'Cancha Deportiva',
                'fecha_cancelacion': datetime.utcnow().strftime('%d/%m/%Y %H:%M'),
                'motivo_cancelacion': 'Cancelación solicitada por el usuario',
                'url_nueva_reserva': '/client/ver_canchas'
            }
            
            # Crear notificación por email
            self.crear_notificacion(
                usuario_id=reserva.UsuarioId,
                tipo='email',
                titulo='Reserva Cancelada - Flash Reserver',
                mensaje=f'Tu reserva para el {datos["fecha"]} a las {datos["hora"]} ha sido cancelada exitosamente.',
                datos_adicionales=datos
            )
            
            # También crear notificación in-app
            self.crear_notificacion(
                usuario_id=reserva.UsuarioId,
                tipo='in_app',
                titulo='Reserva Cancelada',
                mensaje=f'Tu reserva para el {datos["fecha"]} a las {datos["hora"]} ha sido cancelada.',
                datos_adicionales=datos
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error notificando cancelación de reserva: {e}")
            return False

# Instancia global del servicio
notificacion_service = NotificacionService()

# Importar servicio de recordatorios
from .recordatorio_service import recordatorio_service
