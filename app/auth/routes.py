from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from app.forms.auth_forms import LoginForm, RegistroForm, RecuperarPasswordForm, CambiarPasswordForm, ResetPasswordForm
from app.models import Usuario, Rol
from app import db
from app.utils.auth_utils import generate_reset_token, verify_reset_token, send_password_reset_email
from werkzeug.security import generate_password_hash, check_password_hash

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

