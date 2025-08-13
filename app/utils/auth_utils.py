import secrets
import time
from flask import current_app, url_for, render_template
from flask_mail import Message
from app import mail
from itsdangerous import URLSafeTimedSerializer

def generate_reset_token(email):
    """Genera un token seguro para reset de contraseña"""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

def verify_reset_token(token, expiration=3600):
    """Verifica un token de reset de contraseña"""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt='password-reset-salt',
            max_age=expiration
        )
        return email
    except:
        return None

def send_password_reset_email(user_email, reset_url):
    """Envía email de recuperación de contraseña"""
    try:
        msg = Message('Restablecer Contraseña - Flash Reserver',
                      sender=current_app.config['MAIL_DEFAULT_SENDER'],
                      recipients=[user_email])
        
        # Usar el template HTML
        msg.html = render_template('emails/reset_password_email.html', reset_url=reset_url)
        
        # También incluir versión de texto plano
        msg.body = f"""
        Restablecer Contraseña - Flash Reserver
        
        Has solicitado restablecer tu contraseña.
        
        Para continuar, visita este enlace:
        {reset_url}
        
        Este enlace es válido por 1 hora.
        
        Si no solicitaste este cambio, puedes ignorar este email.
        
        Saludos,
        Equipo de Flash Reserver
        """
        
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Error sending password reset email to {user_email}: {e}")
        return False
