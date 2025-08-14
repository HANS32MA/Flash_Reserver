from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, make_response, current_app
from flask_login import login_required, current_user
from app.models import Cancha, Reserva, Categoria, TipoCancha, Comentario
from app import db
from datetime import datetime
from app.auth.decorators import usuario_activo_required
from werkzeug.utils import secure_filename
import os
from flask import jsonify, request, send_file
from datetime import datetime
from app.models.mensaje import Mensaje
from app.utils.filters import format_currency
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash

client_bp = Blueprint('client', __name__)
@client_bp.after_request
def agregar_cabeceras_no_cache(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


def liberar_canchas_sin_reservas():
    """Función obsoleta - las canchas permanecen siempre disponibles"""
    # Esta función ya no es necesaria ya que las canchas permanecen siempre disponibles
    # y solo se controlan los horarios para evitar conflictos
    pass

@client_bp.route('/canchas')
@login_required
@usuario_activo_required
def ver_canchas():
    """Ver todas las canchas disponibles para clientes con filtros funcionales"""
    # Obtener parámetros de filtro
    nombre_filter = request.args.get('nombre', '')
    tipo_filter = request.args.get('tipo', '')
    categoria_filter = request.args.get('categoria', '')
    
    # Query base - todas las canchas excepto mantenimiento
    query = Cancha.query.filter(Cancha.Estado != 'Mantenimiento')
    
    # Aplicar filtros
    if nombre_filter:
        query = query.filter(Cancha.Nombre.ilike(f'%{nombre_filter}%'))
    
    if tipo_filter:
        query = query.filter(Cancha.TipoCanchaId == tipo_filter)
    
    if categoria_filter:
        query = query.filter(Cancha.CategoriaId == categoria_filter)
    
    # Obtener canchas con filtros aplicados
    canchas = query.all()
    
    # Calcular disponibilidad real para cada cancha (OPTIMIZADO)
    from datetime import datetime, timedelta
    fecha_actual = datetime.now().date()
    fecha_fin = fecha_actual + timedelta(days=30)  # Próximo mes
    
    # Obtener todas las reservas confirmadas de una vez
    reservas_confirmadas = Reserva.query.filter(
        Reserva.Estado == 'Confirmada',
        Reserva.Fecha >= fecha_actual,
        Reserva.Fecha <= fecha_fin
    ).all()
    
    # Crear un diccionario para acceso rápido
    reservas_por_cancha = {}
    for reserva in reservas_confirmadas:
        if reserva.CanchaId not in reservas_por_cancha:
            reservas_por_cancha[reserva.CanchaId] = []
        reservas_por_cancha[reserva.CanchaId].append(reserva)
    
    canchas_con_disponibilidad = []
    
    for cancha in canchas:
        # Contar slots disponibles en los próximos 30 días
        slots_totales = 30 * 16  # 30 días × 16 horas por día
        slots_ocupados = 0
        
        # Obtener reservas de esta cancha
        reservas_cancha = reservas_por_cancha.get(cancha.Id, [])
        
        # Contar slots ocupados
        for reserva in reservas_cancha:
            # Calcular duración de la reserva en horas
            inicio = datetime.combine(datetime.min, reserva.HoraInicio)
            fin = datetime.combine(datetime.min, reserva.HoraFin)
            if fin <= inicio:  # Si pasa de medianoche
                fin = datetime.combine(datetime.min, reserva.HoraFin) + timedelta(days=1)
            
            duracion_horas = (fin - inicio).total_seconds() / 3600
            
            # Solo contar si está en horario operativo (6:00-22:00)
            hora_inicio = reserva.HoraInicio.hour
            hora_fin = reserva.HoraFin.hour if reserva.HoraFin.hour > 0 else 24
            
            # Ajustar a horario operativo
            if hora_inicio < 6:
                hora_inicio = 6
            if hora_fin > 22:
                hora_fin = 22
            
            # Contar horas ocupadas
            horas_ocupadas = max(0, hora_fin - hora_inicio)
            slots_ocupados += horas_ocupadas
        
        # Calcular porcentaje de disponibilidad
        porcentaje_disponibilidad = ((slots_totales - slots_ocupados) / slots_totales * 100) if slots_totales > 0 else 100
        
        # Determinar si la cancha está completamente ocupada
        completamente_ocupada = porcentaje_disponibilidad <= 5  # 5% o menos disponible
        
        canchas_con_disponibilidad.append({
            'cancha': cancha,
            'porcentaje_disponibilidad': porcentaje_disponibilidad,
            'completamente_ocupada': completamente_ocupada,
            'slots_disponibles': slots_totales - slots_ocupados,
            'slots_totales': slots_totales
        })
    
    # Ordenar por disponibilidad (más disponibles primero)
    canchas_con_disponibilidad.sort(key=lambda x: x['porcentaje_disponibilidad'], reverse=True)
    
    categorias = Categoria.query.all()
    tipos = TipoCancha.query.all()
    
    return render_template(
        'client/canchas.html', 
        canchas_con_disponibilidad=canchas_con_disponibilidad,
        canchas=canchas,  # Mantener para compatibilidad
        categorias=categorias, 
        tipos=tipos,
        format_currency=format_currency,
        nombre_filter=nombre_filter,
        tipo_filter=tipo_filter,
        categoria_filter=categoria_filter
    )



@client_bp.route('/cancha/<int:cancha_id>')
@login_required
@usuario_activo_required
def ver_cancha(cancha_id):
    """Ver detalles de una cancha específica con información de disponibilidad"""
    cancha = Cancha.query.get_or_404(cancha_id)
    
    # Bloquear acceso solo si está en mantenimiento
    if cancha.Estado == 'Mantenimiento':
        flash('Esta cancha está en mantenimiento actualmente', 'warning')
        return redirect(url_for('client.ver_canchas'))

    # Calcular disponibilidad real de la cancha (OPTIMIZADO)
    from datetime import datetime, timedelta
    fecha_actual = datetime.now().date()
    fecha_fin = fecha_actual + timedelta(days=30)  # Próximo mes
    
    slots_totales = 30 * 16  # 30 días × 16 horas por día
    slots_ocupados = 0
    
    # Obtener todas las reservas confirmadas de esta cancha
    reservas_cancha = Reserva.query.filter(
        Reserva.CanchaId == cancha_id,
        Reserva.Estado == 'Confirmada',
        Reserva.Fecha >= fecha_actual,
        Reserva.Fecha <= fecha_fin
    ).all()
    
    # Contar slots ocupados
    for reserva in reservas_cancha:
        # Solo contar si está en horario operativo (6:00-22:00)
        hora_inicio = reserva.HoraInicio.hour
        hora_fin = reserva.HoraFin.hour if reserva.HoraFin.hour > 0 else 24
        
        # Ajustar a horario operativo
        if hora_inicio < 6:
            hora_inicio = 6
        if hora_fin > 22:
            hora_fin = 22
        
        # Contar horas ocupadas
        horas_ocupadas = max(0, hora_fin - hora_inicio)
        slots_ocupados += horas_ocupadas
    
    # Calcular porcentaje de disponibilidad
    porcentaje_disponibilidad = (slots_totales - slots_ocupados) / slots_totales * 100 if slots_totales > 0 else 100
    completamente_ocupada = porcentaje_disponibilidad <= 5  # 5% o menos disponible

    comentarios = Comentario.query.filter_by(
        CanchaId=cancha_id
    ).order_by(Comentario.FechaCreacion.desc()).limit(5).all()

    # Canchas similares (excluyendo mantenimiento)
    similares = Cancha.query.filter(
        Cancha.CategoriaId == cancha.CategoriaId,
        Cancha.Id != cancha.Id,
        Cancha.Estado != 'Mantenimiento'
    ).limit(12).all()

    # Debug: imprimir información de la cancha
    print(f"DEBUG - Cancha ID: {cancha.Id}")
    print(f"DEBUG - Cancha Nombre: {cancha.Nombre}")
    print(f"DEBUG - Cancha Imagen: {cancha.Imagen}")
    print(f"DEBUG - Cancha imagen (relación): {cancha.imagen}")
    if cancha.imagen:
        for img in cancha.imagen:
            print(f"DEBUG - Imagen Ruta: {img.Ruta}")
    
    # Debug: imprimir información de comentarios y usuarios
    if comentarios:
        print(f"DEBUG - Total comentarios: {len(comentarios)}")
        for i, comentario in enumerate(comentarios):
            print(f"DEBUG - Comentario {i+1}:")
            print(f"  - Usuario ID: {comentario.usuario.Id}")
            print(f"  - Usuario Nombre: {comentario.usuario.Nombre}")
            print(f"  - Usuario FotoPerfil: {comentario.usuario.FotoPerfil}")
            print(f"  - Usuario Email: {comentario.usuario.Email}")
    
    return render_template(
        'client/cancha_detalle.html',
        cancha=cancha,
        comentarios=comentarios,
        similares=similares,
        format_currency=format_currency,
        porcentaje_disponibilidad=porcentaje_disponibilidad,
        completamente_ocupada=completamente_ocupada,
        slots_disponibles=slots_totales - slots_ocupados,
        slots_totales=slots_totales
    )

@client_bp.route('/reservar/<int:cancha_id>', methods=['GET', 'POST'])
@login_required
@usuario_activo_required
def reservar(cancha_id):
    """Crear una nueva reserva con lógica de disponibilidad inteligente"""
    cancha = Cancha.query.get_or_404(cancha_id)

    # Solo permitir reservar canchas que no estén en mantenimiento
    if cancha.Estado == 'Mantenimiento':
        flash('No se puede reservar esta cancha porque está en mantenimiento', 'danger')
        return redirect(url_for('client.ver_canchas'))

    # Verificar disponibilidad real de la cancha (OPTIMIZADO)
    from datetime import datetime, timedelta
    fecha_actual = datetime.now().date()
    fecha_fin = fecha_actual + timedelta(days=30)  # Próximo mes
    
    slots_totales = 30 * 16  # 30 días × 16 horas por día
    slots_ocupados = 0
    
    # Obtener todas las reservas confirmadas de esta cancha
    reservas_cancha = Reserva.query.filter(
        Reserva.CanchaId == cancha_id,
        Reserva.Estado == 'Confirmada',
        Reserva.Fecha >= fecha_actual,
        Reserva.Fecha <= fecha_fin
    ).all()
    
    # Contar slots ocupados
    for reserva in reservas_cancha:
        # Solo contar si está en horario operativo (6:00-22:00)
        hora_inicio = reserva.HoraInicio.hour
        hora_fin = reserva.HoraFin.hour if reserva.HoraFin.hour > 0 else 24
        
        # Ajustar a horario operativo
        if hora_inicio < 6:
            hora_inicio = 6
        if hora_fin > 22:
            hora_fin = 22
        
        # Contar horas ocupadas
        horas_ocupadas = max(0, hora_fin - hora_inicio)
        slots_ocupados += horas_ocupadas
    
    # Calcular porcentaje de disponibilidad
    porcentaje_disponibilidad = ((slots_totales - slots_ocupados) / slots_totales * 100) if slots_totales > 0 else 100
    
    # Si la cancha está completamente ocupada (5% o menos disponible), no permitir reservas
    if porcentaje_disponibilidad <= 5:
        flash(f'Esta cancha está completamente ocupada para los próximos 30 días (solo {porcentaje_disponibilidad:.1f}% disponible). Solo puedes ver los detalles.', 'warning')
        return redirect(url_for('client.ver_cancha', cancha_id=cancha_id))

    if request.method == 'POST':
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
        hora_inicio = datetime.strptime(request.form['hora_inicio'], '%H:%M').time()
        hora_fin = datetime.strptime(request.form['hora_fin'], '%H:%M').time()
        observaciones = request.form.get('observaciones', '')

        # Verificar si hay un cruce de horario con una reserva existente
        reserva_existente = Reserva.query.filter_by(
            CanchaId=cancha_id,
            Fecha=fecha,
            Estado='Confirmada'
        ).filter(
            ((Reserva.HoraInicio < hora_fin) & (Reserva.HoraFin > hora_inicio))
        ).first()

        if reserva_existente:
            # Solo mostrar alerta, NO crear la reserva
            flash('¡Atención! Ya existe una reserva en ese horario. Por favor elige otro horario.', 'warning')
            return redirect(url_for('client.reservar', cancha_id=cancha_id))

        # Crear la reserva solo si no hay cruce
        nueva_reserva = Reserva(
            UsuarioId=current_user.Id,
            CanchaId=cancha_id,
            Fecha=fecha,
            HoraInicio=hora_inicio,
            HoraFin=hora_fin,
            Observaciones=observaciones,
            Estado='Confirmada'
        )

        db.session.add(nueva_reserva)
        db.session.commit()

        # Enviar notificación de confirmación por email
        try:
            from app.services.notificacion_service import notificacion_service
            notificacion_service.notificar_reserva_confirmada(nueva_reserva.Id)
            
            # Programar recordatorios automáticos
            from app.services.recordatorio_service import recordatorio_service
            recordatorio_service.programar_recordatorios_reserva(nueva_reserva.Id)
        except Exception as e:
            # Si falla la notificación, no fallar la creación de la reserva
            pass

        flash('Reserva creada exitosamente.', 'success')
        return redirect(url_for('client.mis_reservas'))

    today = datetime.now().date()
    
    # Obtener todas las canchas para el modal de disponibilidad
    canchas = Cancha.query.filter(Cancha.Estado != 'Mantenimiento').all()
    
    return render_template('client/reservar.html', cancha=cancha, canchas=canchas, today=today, format_currency=format_currency)

@client_bp.route('/api/reservar', methods=['POST'])
@login_required
@usuario_activo_required
def api_reservar():
    """Crear reserva vía AJAX"""
    from datetime import datetime

    data = request.get_json()
    cancha_id = data.get('cancha_id')
    fecha = datetime.strptime(data.get('fecha'), '%Y-%m-%d').date()
    hora_inicio = datetime.strptime(data.get('hora_inicio'), '%H:%M').time()
    hora_fin = datetime.strptime(data.get('hora_fin'), '%H:%M').time()
    observaciones = data.get('observaciones', '')

    cancha = Cancha.query.get_or_404(cancha_id)

    # Validar estado
    if cancha.Estado == 'Mantenimiento':
        return jsonify({'success': False, 'message': 'La cancha está en mantenimiento'}), 400

    # Validar horas
    if hora_fin <= hora_inicio:
        return jsonify({'success': False, 'message': 'La hora final debe ser mayor que la inicial'}), 400

    # Verificar conflicto con reservas existentes
    conflicto = Reserva.query.filter_by(
        CanchaId=cancha_id,
        Fecha=fecha,
        Estado='Confirmada'
    ).filter(
        (Reserva.HoraInicio < hora_fin) & (Reserva.HoraFin > hora_inicio)
    ).first()

    if conflicto:
        return jsonify({'success': False, 'message': 'La cancha ya tiene una reserva en ese horario'}), 400

    # Crear la reserva
    nueva_reserva = Reserva(
        UsuarioId=current_user.Id,
        CanchaId=cancha_id,
        Fecha=fecha,
        HoraInicio=hora_inicio,
        HoraFin=hora_fin,
        Observaciones=observaciones,
        Estado='Confirmada'
    )

    db.session.add(nueva_reserva)
    db.session.commit()

    # Enviar notificación de confirmación por email
    try:
        from app.services.notificacion_service import notificacion_service
        notificacion_service.notificar_reserva_confirmada(nueva_reserva.Id)
        
        # Programar recordatorios automáticos
        from app.services.recordatorio_service import recordatorio_service
        recordatorio_service.programar_recordatorios_reserva(nueva_reserva.Id)
    except Exception as e:
        # Si falla la notificación, no fallar la creación de la reserva
        pass

    return jsonify({'success': True, 'message': 'Reserva creada exitosamente'})


@client_bp.route('/mis-reservas')
@login_required
@usuario_activo_required
def mis_reservas():
    """Ver las reservas del usuario actual con filtros"""
    # Obtener parámetros de filtro
    nombre_filter = request.args.get('nombre', '')
    tipo_filter = request.args.get('tipo', '')
    categoria_filter = request.args.get('categoria', '')
    
    # Query base - reservas del usuario actual
    query = db.session.query(Reserva).filter_by(
        UsuarioId=current_user.Id
    ).join(Cancha).join(Categoria).join(TipoCancha)
    
    # Aplicar filtros
    if nombre_filter:
        query = query.filter(Cancha.Nombre.ilike(f'%{nombre_filter}%'))
    
    if tipo_filter:
        query = query.filter(TipoCancha.Id == tipo_filter)
    
    if categoria_filter:
        query = query.filter(Categoria.Id == categoria_filter)
    
    # Obtener reservas con filtros aplicados
    reservas = query.order_by(Reserva.Fecha.desc()).all()
    
    # Cargar las imágenes de las canchas
    for reserva in reservas:
        # Cargar la relación de imágenes si existe
        if hasattr(reserva.cancha, 'imagen'):
            db.session.refresh(reserva.cancha)
            # Forzar la carga de la relación imagen
            _ = reserva.cancha.imagen
    
    # Obtener tipos de cancha y categorías para los filtros
    tipos_cancha = TipoCancha.query.all()
    categorias = Categoria.query.all()
    
    today = datetime.now().date()
    return render_template('client/mis_reservas.html', 
                         reservas=reservas, 
                         today=today,
                         tipos_cancha=tipos_cancha,
                         categorias=categorias,
                         nombre_filter=nombre_filter,
                         tipo_filter=tipo_filter,
                         categoria_filter=categoria_filter)

@client_bp.route('/cancelar-reserva/<int:reserva_id>', methods=['POST'])
@login_required
@usuario_activo_required
def cancelar_reserva(reserva_id):
    """Cancelar una reserva"""
    reserva = Reserva.query.get_or_404(reserva_id)
    
    # Verificar que la reserva pertenece al usuario actual
    if reserva.UsuarioId != current_user.Id:
        flash('No tienes permisos para cancelar esta reserva', 'danger')
        return redirect(url_for('client.mis_reservas'))
    
    # Verificar que la reserva no esté muy cerca
    if reserva.Fecha <= datetime.now().date():
        flash('No se puede cancelar una reserva del día actual o pasada', 'danger')
        return redirect(url_for('client.mis_reservas'))
    
    reserva.Estado = 'Cancelada'
    db.session.commit()

    # Enviar notificación de cancelación por email
    try:
        from app.services.notificacion_service import notificacion_service
        notificacion_service.notificar_cancelacion_reserva(reserva.Id)
        
        # Cancelar recordatorios automáticos
        from app.services.recordatorio_service import recordatorio_service
        recordatorio_service.cancelar_recordatorios_reserva(reserva.Id)
    except Exception as e:
        # Si falla la notificación, no fallar la cancelación
        pass

    # Actualizar estado de canchas
    liberar_canchas_sin_reservas()
    
    flash('Reserva cancelada exitosamente', 'success')
    return redirect(url_for('client.mis_reservas'))

@client_bp.route('/comentar/<int:cancha_id>', methods=['POST'])
@login_required
@usuario_activo_required
def comentar_cancha(cancha_id):
    """Agregar comentario a una cancha"""
    cancha = Cancha.query.get_or_404(cancha_id)
    
    if cancha.Estado == 'Mantenimiento':
        flash('No se pueden agregar comentarios a canchas en mantenimiento', 'warning')
        return redirect(url_for('client.ver_canchas'))
    
    comentario_texto = request.form.get('comentario')
    calificacion = int(request.form.get('calificacion', 5))
    
    if not comentario_texto:
        flash('El comentario no puede estar vacío', 'danger')
        return redirect(url_for('client.ver_cancha', cancha_id=cancha_id))
    
    nuevo_comentario = Comentario(
        UsuarioId=current_user.Id,
        CanchaId=cancha_id,
        Comentario=comentario_texto,
        Calificacion=calificacion
    )
    
    db.session.add(nuevo_comentario)
    db.session.commit()
    
    flash('Comentario agregado exitosamente', 'success')
    return redirect(url_for('client.ver_cancha', cancha_id=cancha_id))

@client_bp.route('/api/horarios-disponibles/<int:cancha_id>')
@login_required
@usuario_activo_required
def horarios_disponibles(cancha_id):
    """API para obtener horarios disponibles de una cancha"""
    cancha = Cancha.query.get_or_404(cancha_id)
    if cancha.Estado == 'Mantenimiento':
        return jsonify({'error': 'Esta cancha está en mantenimiento'}), 403

    fecha = request.args.get('fecha')
    if not fecha:
        return jsonify({'error': 'Fecha requerida'}), 400
    
    fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
    
    # Obtener reservas existentes para esa fecha
    reservas = Reserva.query.filter_by(
        CanchaId=cancha_id,
        Fecha=fecha_obj,
        Estado='Confirmada'
    ).all()
    
    # Generar horarios ocupados
    horarios_ocupados = []
    for reserva in reservas:
        horarios_ocupados.append({
            'inicio': reserva.HoraInicio.strftime('%H:%M'),
            'fin': reserva.HoraFin.strftime('%H:%M')
        })

    # Puedes exponer horario operativo si lo necesitas en UI
    horario_operativo = {
        'inicio': '06:00',
        'fin': '22:00'
    }

    return jsonify({
        'fecha': fecha,
        'cancha_id': cancha_id,
        'horario_operativo': horario_operativo,
        'horarios_ocupados': horarios_ocupados
    })

@client_bp.route('/ayuda')
@login_required
@usuario_activo_required
def ayuda():
    """Página de ayuda para clientes"""
    return render_template('client/ayuda.html')

@client_bp.route('/enviar-mensaje', methods=['POST'])
@login_required
@usuario_activo_required
def enviar_mensaje():
    try:
        data = request.get_json()
        asunto = data.get('asunto')
        mensaje = data.get('mensaje')
        
        if not asunto or not mensaje:
            return jsonify({'success': False, 'error': 'Asunto y mensaje son requeridos'})
        
        # Crear nuevo mensaje
        nuevo_mensaje = Mensaje(
            UsuarioId=current_user.Id,
            Asunto=asunto,
            Mensaje=mensaje
        )
        
        db.session.add(nuevo_mensaje)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Mensaje enviado correctamente'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@client_bp.route('/chat/mensaje', methods=['POST'])
@login_required
@usuario_activo_required
def enviar_mensaje_chat():
    try:
        data = request.get_json()
        mensaje = data.get('mensaje')
        
        if not mensaje:
            return jsonify({'success': False, 'error': 'Mensaje es requerido'})
        
        # Crear nuevo mensaje de chat
        nuevo_mensaje = Mensaje(
            UsuarioId=current_user.Id,
            Asunto='Chat en Tiempo Real',
            Mensaje=mensaje
        )
        
        db.session.add(nuevo_mensaje)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Mensaje de chat enviado correctamente'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@client_bp.route('/chat/mensajes', methods=['GET'])
@login_required
@usuario_activo_required
def obtener_mensajes_chat():
    try:
        # Obtener todos los mensajes del usuario actual
        mensajes = Mensaje.query.filter_by(UsuarioId=current_user.Id).order_by(Mensaje.FechaEnvio).all()
        
        mensajes_data = []
        for mensaje in mensajes:
            mensaje_info = {
                'id': mensaje.Id,
                'mensaje': mensaje.Mensaje,
                'fecha': mensaje.fecha_formateada,
                'respuesta': mensaje.Respuesta,
                'fecha_respuesta': mensaje.fecha_respuesta_formateada if mensaje.Respuesta else None
            }
            mensajes_data.append(mensaje_info)
        
        return jsonify({'success': True, 'mensajes': mensajes_data})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@client_bp.route('/api/canchas')
@login_required
@usuario_activo_required
def api_canchas():
    """API para obtener canchas con filtros"""
    categoria_id = request.args.get('categoria', type=int)
    tipo_id = request.args.get('tipo', type=int)
    precio_min = request.args.get('precio_min', type=float)
    precio_max = request.args.get('precio_max', type=float)
    
    query = Cancha.query.filter(Cancha.Estado != 'Mantenimiento')
    
    if categoria_id:
        query = query.filter(Cancha.CategoriaId == categoria_id)
    if tipo_id:
        query = query.filter(Cancha.TipoCanchaId == tipo_id)
    if precio_min is not None:
        query = query.filter(Cancha.PrecioHora >= precio_min)
    if precio_max is not None:
        query = query.filter(Cancha.PrecioHora <= precio_max)
    
    canchas = query.all()
    
    # Si no hay canchas en la base de datos, crear datos de prueba del Cesar
    if not canchas:
        canchas_data = [
            {
                'id': 1,
                'nombre': 'Cancha de Fútbol Valledupar Centro',
                'descripcion': 'Cancha profesional de fútbol 11 con césped sintético',
                'precio': 150000.0,
                'estado': 'Disponible',
                'imagen': 'images/cancha-futbol-1.jpg',
                'categoria': 'Premium',
                'tipo': 'Fútbol',
                'lat': 10.4631,
                'lng': -73.2532,
                'direccion': 'Calle 15 # 23-45',
                'barrio': 'Centro',
                'ciudad': 'Valledupar'
            },
            {
                'id': 2,
                'nombre': 'Cancha de Tenis Club Valledupar',
                'descripcion': 'Cancha de tenis profesional con superficie de arcilla',
                'precio': 80000.0,
                'estado': 'Disponible',
                'imagen': 'images/cancha-tenis-1.jpg',
                'categoria': 'Premium',
                'tipo': 'Tenis',
                'lat': 10.4680,
                'lng': -73.2480,
                'direccion': 'Carrera 7 # 20-30',
                'barrio': 'San Joaquín',
                'ciudad': 'Valledupar'
            },
            {
                'id': 3,
                'nombre': 'Cancha de Baloncesto Barrio La Nevada',
                'descripcion': 'Cancha de baloncesto techada con tableros profesionales',
                'precio': 60000.0,
                'estado': 'Disponible',
                'imagen': 'images/cancha-basquet-1.jpg',
                'categoria': 'Básica',
                'tipo': 'Baloncesto',
                'lat': 10.4580,
                'lng': -73.2580,
                'direccion': 'Calle 20 # 15-25',
                'barrio': 'La Nevada',
                'ciudad': 'Valledupar'
            },
            {
                'id': 4,
                'nombre': 'Cancha de Pádel Aguachica',
                'descripcion': 'Cancha de pádel profesional con superficie sintética',
                'precio': 120000.0,
                'estado': 'Disponible',
                'imagen': 'images/cancha-padel-1.jpg',
                'categoria': 'Premium',
                'tipo': 'Pádel',
                'lat': 8.3083,
                'lng': -73.6167,
                'direccion': 'Carrera 12 # 8-15',
                'barrio': 'Centro',
                'ciudad': 'Aguachica'
            },
            {
                'id': 5,
                'nombre': 'Cancha de Voleibol Codazzi',
                'descripcion': 'Cancha de voleibol de playa con arena especial',
                'precio': 70000.0,
                'estado': 'Disponible',
                'imagen': 'images/cancha-voleibol-1.jpg',
                'categoria': 'Básica',
                'tipo': 'Voleibol',
                'lat': 9.7500,
                'lng': -73.2333,
                'direccion': 'Calle 5 # 12-20',
                'barrio': 'San José',
                'ciudad': 'Codazzi'
            },
            {
                'id': 6,
                'nombre': 'Cancha de Fútbol 5 El Paso',
                'descripcion': 'Cancha de fútbol 5 con césped sintético y iluminación',
                'precio': 100000.0,
                'estado': 'Disponible',
                'imagen': 'images/futbol5-san-martin.jpg',
                'categoria': 'Básica',
                'tipo': 'Fútbol 5',
                'lat': 9.6667,
                'lng': -73.7500,
                'direccion': 'Carrera 3 # 6-10',
                'barrio': 'El Centro',
                'ciudad': 'El Paso'
            },
            {
                'id': 7,
                'nombre': 'Cancha de Badminton La Jagua',
                'descripcion': 'Cancha de badminton profesional con piso de madera',
                'precio': 90000.0,
                'estado': 'Disponible',
                'imagen': 'images/cancha-badminton-1.jpg',
                'categoria': 'Premium',
                'tipo': 'Badminton',
                'lat': 9.5667,
                'lng': -73.3333,
                'direccion': 'Calle 8 # 10-18',
                'barrio': 'San Martín',
                'ciudad': 'La Jagua de Ibirico'
            },
            {
                'id': 8,
                'nombre': 'Cancha de Tenis Chiriguaná',
                'descripcion': 'Cancha de tenis con superficie dura y iluminación nocturna',
                'precio': 85000.0,
                'estado': 'Disponible',
                'imagen': 'images/cancha-tenis-2.jpg',
                'categoria': 'Premium',
                'tipo': 'Tenis',
                'lat': 9.3667,
                'lng': -73.5000,
                'direccion': 'Carrera 15 # 22-30',
                'barrio': 'El Progreso',
                'ciudad': 'Chiriguaná'
            }
        ]
        
        return jsonify({'success': True, 'canchas': canchas_data, 'demo': True})
    
    # Si hay canchas en la base de datos, usar esos datos
    canchas_data = []
    for cancha in canchas:
        canchas_data.append({
            'id': cancha.Id,
            'nombre': cancha.Nombre,
            'descripcion': cancha.Descripcion,
            'precio': float(cancha.PrecioHora),
            'estado': cancha.Estado,
            'imagen': cancha.Imagen,
            'categoria': cancha.categoria.Nombre if cancha.categoria else 'Sin categoría',
            'tipo': cancha.tipo_cancha.Nombre if cancha.tipo_cancha else 'Sin tipo',
            'lat': float(cancha.Latitud) if cancha.Latitud else None,
            'lng': float(cancha.Longitud) if cancha.Longitud else None,
            'direccion': cancha.Direccion or 'Dirección no disponible',
            'barrio': cancha.Barrio or 'Barrio no disponible',
            'ciudad': cancha.Ciudad or 'Valledupar'
        })
    
    return jsonify({'success': True, 'canchas': canchas_data, 'demo': False})



@client_bp.route('/api/disponibilidad-mensual')
@login_required
@usuario_activo_required
def api_disponibilidad_mensual():
    """API para obtener la disponibilidad mensual de todas las canchas"""
    try:
        from datetime import datetime, timedelta
        from sqlalchemy import extract, func
        
        # Obtener fechas del mes actual y los próximos 2 meses
        fecha_actual = datetime.now().date()
        fecha_fin = fecha_actual + timedelta(days=90)  # 3 meses
        
        # Obtener todas las canchas
        canchas = Cancha.query.filter(Cancha.Estado != 'Mantenimiento').all()
        
        disponibilidad = []
        
        for cancha in canchas:
            # Generar slots de tiempo para cada día
            fecha_actual_iter = fecha_actual
            while fecha_actual_iter <= fecha_fin:
                # Generar slots de 1 hora desde 6:00 AM hasta 10:00 PM
                for hora in range(6, 22):
                    hora_inicio = f"{hora:02d}:00"
                    hora_fin = f"{hora+1:02d}:00"
                    
                    # Verificar si hay reserva en este slot
                    reserva = Reserva.query.filter_by(
                        CanchaId=cancha.Id,
                        Fecha=fecha_actual_iter,
                        Estado='Confirmada'
                    ).filter(
                        ((Reserva.HoraInicio < hora_fin) & (Reserva.HoraFin > hora_inicio))
                    ).first()
                    
                    # Determinar estado
                    if reserva:
                        estado = 'ocupado'
                        cliente = reserva.usuario.Nombre
                    else:
                        estado = 'disponible'
                        cliente = None
                    
                    # Formatear fecha
                    fecha_formateada = fecha_actual_iter.strftime('%d/%m/%Y')
                    
                    disponibilidad.append({
                        'cancha_id': cancha.Id,
                        'cancha_nombre': cancha.Nombre,
                        'fecha': fecha_actual_iter.strftime('%Y-%m-%d'),
                        'fecha_formateada': fecha_formateada,
                        'hora_inicio': hora_inicio,
                        'hora_fin': hora_fin,
                        'estado': estado,
                        'cliente': cliente
                    })
                
                fecha_actual_iter += timedelta(days=1)
        
        return jsonify({
            'success': True,
            'disponibilidad': disponibilidad
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@client_bp.route('/api/filtros')
@login_required
@usuario_activo_required
def api_filtros():
    """API para obtener filtros disponibles (categorías y tipos)"""
    try:
        # Obtener categorías
        categorias = Categoria.query.all()
        categorias_data = [{'id': cat.Id, 'nombre': cat.Nombre} for cat in categorias]
        
        # Obtener tipos de cancha
        tipos = TipoCancha.query.all()
        tipos_data = [{'id': tip.Id, 'nombre': tip.Nombre} for tip in tipos]
        
        return jsonify({
            'success': True,
            'categorias': categorias_data,
            'tipos': tipos_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@client_bp.route('/manual-usuario-pdf')
@login_required
@usuario_activo_required
def manual_usuario_pdf():
    """Descargar manual de usuario en PDF"""
    try:
        # Ruta al archivo PDF del manual
        pdf_path = os.path.join(current_app.root_path, 'static', 'docs', 'manual_usuario_cliente.pdf')
        
        if os.path.exists(pdf_path):
            return send_file(
                pdf_path,
                as_attachment=True,
                download_name='Manual_Usuario_Flash_Reserver.pdf',
                mimetype='application/pdf'
            )
        else:
            flash('El manual de usuario no está disponible actualmente', 'warning')
            return redirect(url_for('client.ver_canchas'))
            
    except Exception as e:
        flash('Error al descargar el manual', 'error')
        return redirect(url_for('client.ver_canchas'))

@client_bp.route('/configuracion')
@login_required
@usuario_activo_required
def configuracion():
    """Página de configuración para clientes"""
    response = make_response(render_template('client/configuracion.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@client_bp.route('/actualizar_perfil', methods=['POST'])
@login_required
@usuario_activo_required
def actualizar_perfil():
    """Actualizar perfil del cliente"""
    try:
        # Obtener datos del formulario
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        direccion = request.form.get('direccion')
        
        # Validar datos requeridos
        if not nombre or not email:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'Nombre y email son campos obligatorios'})
            flash('Nombre y email son campos obligatorios', 'error')
            return redirect(url_for('client.configuracion'))
        
        # Verificar si el email ya existe (excepto para el usuario actual)
        usuario_existente = Usuario.query.filter(
            Usuario.Email == email,
            Usuario.Id != current_user.Id
        ).first()
        
        if usuario_existente:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'El email ya está registrado por otro usuario'})
            flash('El email ya está registrado por otro usuario', 'error')
            return redirect(url_for('client.configuracion'))
        
        # Actualizar datos del usuario
        current_user.Nombre = nombre
        current_user.Email = email
        current_user.Telefono = telefono or None
        current_user.Direccion = direccion or None
        
        if fecha_nacimiento:
            try:
                current_user.FechaNacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            except ValueError:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'success': False, 'message': 'Formato de fecha inválido'})
                flash('Formato de fecha inválido', 'error')
                return redirect(url_for('client.configuracion'))
        
        # Manejar imagen de perfil
        image_url = None
        if 'foto_perfil' in request.files:
            imagen = request.files['foto_perfil']
            if imagen and imagen.filename != '':
                filename = secure_filename(imagen.filename)
                ruta_directorio = os.path.join(current_app.root_path, 'static', 'uploads', 'usuarios')
                os.makedirs(ruta_directorio, exist_ok=True)
                ruta_guardado = os.path.join(ruta_directorio, filename)
                imagen.save(ruta_guardado)
                current_user.FotoPerfil = f'uploads/usuarios/{filename}'
                image_url = url_for('static', filename=current_user.FotoPerfil)
        
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True, 
                'message': 'Perfil actualizado exitosamente',
                'image_url': image_url
            })
        
        flash('Perfil actualizado exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': f'Error al actualizar perfil: {str(e)}'})
        flash(f'Error al actualizar perfil: {str(e)}', 'error')
    
    return redirect(url_for('client.configuracion'))

@client_bp.route('/cambiar_password', methods=['POST'])
@login_required
@usuario_activo_required
def cambiar_password():
    """Cambiar contraseña del cliente"""
    try:
        password_actual = request.form.get('password_actual')
        password_nuevo = request.form.get('password_nuevo')
        password_confirmar = request.form.get('password_confirmar')
        
        # Validar datos
        if not all([password_actual, password_nuevo, password_confirmar]):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'Todos los campos son obligatorios'})
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('client.configuracion'))
        
        # Verificar contraseña actual
        if not current_user.check_password(password_actual):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'La contraseña actual es incorrecta'})
            flash('La contraseña actual es incorrecta', 'error')
            return redirect(url_for('client.configuracion'))
        
        # Verificar que las nuevas contraseñas coincidan
        if password_nuevo != password_confirmar:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'Las nuevas contraseñas no coinciden'})
            flash('Las nuevas contraseñas no coinciden', 'error')
            return redirect(url_for('client.configuracion'))
        
        # Verificar longitud mínima
        if len(password_nuevo) < 6:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'La nueva contraseña debe tener al menos 6 caracteres'})
            flash('La nueva contraseña debe tener al menos 6 caracteres', 'error')
            return redirect(url_for('client.configuracion'))
        
        # Actualizar contraseña
        current_user.Password = generate_password_hash(password_nuevo)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': 'Contraseña actualizada exitosamente'})
        
        flash('Contraseña cambiada exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': f'Error al cambiar contraseña: {str(e)}'})
        flash(f'Error al cambiar contraseña: {str(e)}', 'error')
    
    return redirect(url_for('client.configuracion'))

@client_bp.route('/eliminar_cuenta', methods=['POST'])
@login_required
@usuario_activo_required
def eliminar_cuenta():
    """Eliminar cuenta del cliente"""
    try:
        # Verificar que no tenga reservas activas
        reservas_activas = Reserva.query.filter(
            Reserva.UsuarioId == current_user.Id,
            Reserva.Fecha >= datetime.now().date(),
            Reserva.Estado.in_(['Confirmada', 'Pendiente'])
        ).count()
        
        if reservas_activas > 0:
            flash('No puedes eliminar tu cuenta mientras tengas reservas activas', 'error')
            return redirect(url_for('client.configuracion'))
        
        # Eliminar usuario (esto también eliminará las reservas pasadas por CASCADE)
        db.session.delete(current_user)
        db.session.commit()
        
        flash('Tu cuenta ha sido eliminada exitosamente', 'success')
        return redirect(url_for('auth.logout'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar cuenta: {str(e)}', 'error')
        return redirect(url_for('client.configuracion'))

@client_bp.route('/configuracion/actualizar_campo', methods=['POST'])
@login_required
@usuario_activo_required
def actualizar_campo_configuracion():
    """Actualizar un campo específico de configuración del cliente"""
    try:
        # Obtener el nombre y valor del campo
        field_name = None
        field_value = None
        
        for key, value in request.form.items():
            field_name = key
            field_value = value
            break
        
        if not field_name:
            return jsonify({'success': False, 'message': 'No se especificó ningún campo'})
        
        # Aquí se guardaría el campo específico en la base de datos o archivo de configuración
        # Por ahora solo mostramos un mensaje de éxito
        
        return jsonify({'success': True, 'message': f'Campo {field_name} actualizado correctamente'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error al actualizar campo: {str(e)}'})

@client_bp.route('/perfil/obtener_info', methods=['GET'])
@login_required
@usuario_activo_required
def obtener_info_perfil():
    """Obtener información del perfil del usuario actual"""
    try:
        user_info = {
            'id': current_user.Id,
            'nombre': current_user.Nombre,
            'email': current_user.Email,
            'telefono': current_user.Telefono,
            'direccion': current_user.Direccion,
            'fecha_nacimiento': current_user.FechaNacimiento.isoformat() if current_user.FechaNacimiento else None,
            'imagen': current_user.FotoPerfil,
            'imagen_url': url_for('static', filename=current_user.FotoPerfil) if current_user.FotoPerfil else url_for('static', filename='images/default-user.png')
        }
        
        return jsonify({'success': True, 'data': user_info})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error al obtener información: {str(e)}'})