from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def empleado_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if current_user.rol.Nombre not in ['Empleado', 'Administrador']:
            flash('No tienes permisos para acceder a esta página', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if current_user.rol.Nombre != 'Administrador':
            flash('No tienes permisos de administrador para acceder a esta página', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def usuario_activo_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if not current_user.Estado:
            flash('Tu cuenta ha sido desactivada. Por favor, comunícate con el administrador para más información.', 'error')
            return redirect(url_for('auth.logout'))
        return f(*args, **kwargs)
    return decorated_function
