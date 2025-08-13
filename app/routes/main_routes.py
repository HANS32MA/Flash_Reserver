from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.auth.decorators import usuario_activo_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    try:
        return render_template('index.html', show_footer=True)
    except Exception as e:
        return f"Error: {str(e)}", 500

@main_bp.route('/test')
def test():
    return "¡El servidor está funcionando correctamente!"

@main_bp.route('/dashboard')
@login_required
@usuario_activo_required
def dashboard():
    """Dashboard principal que redirige según el rol"""
    if current_user.rol.Nombre == 'Cliente':
        return redirect(url_for('client.ver_canchas'))
    elif current_user.rol.Nombre in ['Empleado', 'Administrador']:
        return redirect(url_for('admin.dashboard'))
    else:
        return render_template('dashboard.html', 
                              user=current_user,
                              rol=current_user.rol.Nombre)


