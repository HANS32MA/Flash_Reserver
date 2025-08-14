from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session
import os
from flask_login import login_user, logout_user, current_user, login_required
from app.forms.auth_forms import LoginForm, RegistroForm, RecuperarPasswordForm, CambiarPasswordForm, ResetPasswordForm
from app.models import Usuario, Rol
from app import db, oauth
from app.utils.auth_utils import generate_reset_token, verify_reset_token, send_password_reset_email
from werkzeug.security import generate_password_hash, check_password_hash
import requests

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(Email=form.email.data).first()
        
        if user and check_password_hash(user.Contrasena, form.password.data):
            # Verificar si el usuario está activo
            if not user.Estado:
                flash('Tu cuenta ha sido desactivada. Por favor, comunícate con el administrador para más información.', 'error')
                return render_template('auth/login.html', form=form)
            
            login_user(user)
            next_page = request.args.get('next')
            flash('¡Bienvenido de vuelta!', 'success')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash('Credenciales inválidas. Por favor, verifica tu email y contraseña.', 'error')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/login/google')
def login_google():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    # Guardar next si viene
    next_page = request.args.get('next')
    if next_page:
        session['next_after_login'] = next_page
    redirect_uri = url_for('auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/google/callback')
def google_callback():
    try:
        token = oauth.google.authorize_access_token()
    except Exception as e:
        current_app.logger.error(f"OAuth error: {e}")
        flash('No se pudo completar el inicio de sesión con Google.', 'error')
        return redirect(url_for('auth.login'))

    # Obtener userinfo endpoint absoluto desde metadata OpenID
    try:
        metadata = oauth.google.load_server_metadata()
        userinfo_endpoint = metadata.get('userinfo_endpoint') or 'https://openidconnect.googleapis.com/v1/userinfo'
    except Exception as e:
        current_app.logger.warning(f"No se pudo cargar metadata OpenID: {e}")
        userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo'

    resp = oauth.google.get(userinfo_endpoint)
    if not resp or resp.status_code != 200:
        current_app.logger.error(f"No se pudo obtener userinfo. resp={getattr(resp, 'status_code', None)} body={getattr(resp, 'text', '')}")
        flash('No se pudo obtener la información de Google.', 'error')
        return redirect(url_for('auth.login'))

    userinfo = resp.json()
    email = userinfo.get('email')
    name = userinfo.get('name') or userinfo.get('given_name') or 'Usuario Google'
    picture_url = userinfo.get('picture')

    if not email:
        flash('Tu cuenta de Google no tiene un email disponible.', 'error')
        return redirect(url_for('auth.login'))

    user = Usuario.query.filter_by(Email=email).first()
    if not user:
        # Crear usuario nuevo con rol Cliente
        cliente_rol = Rol.query.filter_by(Nombre='Cliente').first()
        if not cliente_rol:
            flash('Error en el sistema: Rol Cliente no existe. Contacta al administrador.', 'error')
            return redirect(url_for('auth.login'))

        # Generar una contraseña aleatoria ya que no se usará para login
        random_password = generate_password_hash(os.urandom(16).hex())

        user = Usuario(
            Nombre=name,
            Email=email,
            Telefono='0000000000',
            Contrasena=random_password,
            RolId=cliente_rol.Id,
            Estado=True
        )
        # Intentar guardar foto de perfil si viene
        try:
            if picture_url:
                # Guardar como URL directa dentro de static? Las plantillas esperan ruta relativa a static.
                # Usaremos static/uploads/perfiles/google_<hash>.jpg
                filename = f"uploads/perfiles/google_{os.urandom(8).hex()}.jpg"
                save_path = os.path.join(current_app.root_path, 'static', filename)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                response = requests.get(picture_url, timeout=10)
                if response.status_code == 200:
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    user.FotoPerfil = filename
        except Exception as e:
            current_app.logger.warning(f"No se pudo guardar la foto de Google: {e}")
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creando usuario Google: {e}")
            flash('No se pudo crear tu cuenta con Google. Intenta más tarde.', 'error')
            return redirect(url_for('auth.login'))

    # Si el usuario ya existía y no tenía foto local, intentar setearla una vez
    if user and not user.FotoPerfil and picture_url:
        try:
            filename = f"uploads/perfiles/google_{os.urandom(8).hex()}.jpg"
            save_path = os.path.join(current_app.root_path, 'static', filename)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            response = requests.get(picture_url, timeout=10)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                user.FotoPerfil = filename
                db.session.commit()
        except Exception as e:
            current_app.logger.warning(f"No se pudo actualizar la foto de Google del usuario existente: {e}")

    if not user.Estado:
        flash('Tu cuenta ha sido desactivada. Por favor, comunícate con el administrador para más información.', 'error')
        return redirect(url_for('auth.login'))

    login_user(user)
    next_page = session.pop('next_after_login', None)
    flash('¡Bienvenido!', 'success')
    return redirect(next_page or url_for('main.dashboard'))

@auth_bp.route('/debug/google-config')
def debug_google_config():
    """Muestra configuración relevante de Google OAuth solo en modo debug."""
    if not current_app.debug:
        return "No disponible en producción", 404
    client_id = current_app.config.get('GOOGLE_CLIENT_ID')
    client_secret = current_app.config.get('GOOGLE_CLIENT_SECRET')
    redirect_uri = url_for('auth.google_callback', _external=True)
    raw = request.args.get('raw') == '1'

    def mask(value):
        if not value:
            return 'None'
        if len(value) <= 8:
            return '****'
        return value[:6] + '...' + value[-8:]

    show_id = client_id if raw else mask(client_id)
    show_secret = client_secret if raw else mask(client_secret)

    return (
        f"GOOGLE_CLIENT_ID: {show_id}\n"
        f"GOOGLE_CLIENT_SECRET: {show_secret}\n"
        f"Callback esperado: {redirect_uri}\n"
        f"Debug activo: {current_app.debug}"
    ), 200, {"Content-Type": "text/plain; charset=utf-8"}

@auth_bp.route('/registro', methods=['GET', 'POST'])
def register():
    form = RegistroForm()
    if form.validate_on_submit():
        # Verificar si el email ya existe
        if Usuario.query.filter_by(Email=form.email.data).first():
            flash('Este email ya está registrado en el sistema. Por favor, usa otro email o inicia sesión.', 'error')
            return redirect(url_for('auth.register'))

        # Crear nuevo usuario como Cliente
        cliente_rol = Rol.query.filter_by(Nombre='Cliente').first()
        if not cliente_rol:
            flash('Error en el sistema: Rol Cliente no existe. Contacta al administrador.', 'error')
            return redirect(url_for('auth.register'))

        nuevo_usuario = Usuario(
            Nombre=form.nombre.data,
            Email=form.email.data,
            Telefono=form.telefono.data,
            Contrasena=generate_password_hash(form.password.data),
            RolId=cliente_rol.Id
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('¡Registro exitoso! Tu cuenta ha sido creada correctamente. Por favor inicia sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('main.index'))

@auth_bp.route('/recuperar-password', methods=['GET', 'POST'])
def recuperar_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RecuperarPasswordForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(Email=form.email.data).first()
        if user:
            token = generate_reset_token(user.Email)
            reset_url = url_for('auth.reset_password', token=token, _external=True)

            # Intentar enviar email
            try:
                if send_password_reset_email(user.Email, reset_url):
                    flash('Se ha enviado un enlace de recuperación a tu email.', 'success')
                    return redirect(url_for('auth.login'))
                else:
                    flash('Error al enviar el email. Por favor, contacta al administrador.', 'error')
                    return redirect(url_for('auth.login'))
            except Exception as e:
                current_app.logger.error(f"Error sending email: {e}")
                flash('Error al enviar el email. Por favor, contacta al administrador.', 'error')
                return redirect(url_for('auth.login'))
        else:
            # Por seguridad, mostramos el mismo mensaje aunque el email no exista
            flash('Se ha enviado un enlace de recuperación a tu email.', 'success')

        return redirect(url_for('auth.login'))

    return render_template('auth/recuperar_password.html', form=form)

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    # Verificar token
    email = verify_reset_token(token)
    if not email:
        flash('El enlace de recuperación es inválido o ha expirado.', 'error')
        return redirect(url_for('auth.recuperar_password'))
    
    # Verificar que el usuario exista
    user = Usuario.query.filter_by(Email=email).first()
    if not user:
        flash('La cuenta asociada a este enlace no existe.', 'error')
        return redirect(url_for('auth.recuperar_password'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.Contrasena = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Tu contraseña ha sido restablecida correctamente.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form=form, email=email)



@auth_bp.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    form = CambiarPasswordForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.Contrasena, form.password_actual.data):
            current_user.Contrasena = generate_password_hash(form.password.data)
            db.session.commit()
            flash('Tu contraseña ha sido cambiada correctamente.', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('La contraseña actual es incorrecta.', 'error')
    
    return render_template('auth/cambiar_password.html', form=form)

@auth_bp.route('/test-token/<email>')
def test_token(email):
    """Ruta de prueba para generar tokens (solo en desarrollo)"""
    if not current_app.debug:
        return "No disponible en producción", 404
    
    user = Usuario.query.filter_by(Email=email).first()
    if user:
        token = generate_reset_token(user.Email)
        reset_url = url_for('auth.reset_password', token=token, _external=True)
        return f"""
        <h2>Token de Prueba para {email}</h2>
        <p><strong>Token:</strong> {token}</p>
        <p><strong>URL completa:</strong> <a href="{reset_url}">{reset_url}</a></p>
        <p><a href="{reset_url}">Hacer clic aquí para probar</a></p>
        """
    else:
        return f"Usuario {email} no encontrado", 404

@auth_bp.route('/get-token/<email>')
def get_token(email):
    """Ruta simple para obtener token completo (solo en desarrollo)"""
    if not current_app.debug:
        return "No disponible en producción", 404
    
    user = Usuario.query.filter_by(Email=email).first()
    if user:
        token = generate_reset_token(user.Email)
        reset_url = url_for('auth.reset_password', token=token, _external=True)
        return render_template('auth/token_display.html', 
                             token=token, 
                             reset_url=reset_url,
                             email=user.Email)
    else:
        return f"❌ Usuario {email} no encontrado", 404

