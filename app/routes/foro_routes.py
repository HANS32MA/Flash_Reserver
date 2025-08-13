from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, send_from_directory
from flask_login import login_required, current_user
from app.models import Post, Like, ComentarioForo, Usuario
from app import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app.auth.decorators import usuario_activo_required

foro_bp = Blueprint('foro', __name__, url_prefix='/foro')

# Ruta para servir archivos multimedia del foro
@foro_bp.route('/media/<path:filename>')
@login_required
@usuario_activo_required
def servir_multimedia(filename):
    """Sirve archivos multimedia del foro (imágenes y videos)"""
    try:
        # Verificar que el archivo esté en la ruta correcta del foro
        if not filename.startswith('uploads/foro/'):
            return "Ruta de archivo no válida", 400
        
        # Extraer la ruta relativa y el directorio base
        relative_path = filename.replace('uploads/foro/', '')
        base_directory = os.path.join(current_app.root_path, 'static', 'uploads', 'foro',)

        # Verificar que el archivo existe
        full_path = os.path.join(base_directory, relative_path)
        if not os.path.exists(full_path):
            return "Archivo no encontrado", 404
        
        # Determinar el tipo de archivo para el Content-Type
        file_extension = os.path.splitext(relative_path)[1].lower()
        
        # Mapear extensiones a tipos MIME
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.mp4': 'video/mp4',
            '.avi': 'video/x-msvideo',
            '.mov': 'video/quicktime',
            '.webm': 'video/webm',
            '.ogg': 'video/ogg'
        }
        
        content_type = mime_types.get(file_extension, 'application/octet-stream')
        
        # Servir el archivo con el tipo MIME correcto
        response = send_from_directory(base_directory, relative_path)
        response.headers['Content-Type'] = content_type
        
        # Agregar headers para cache y seguridad
        response.headers['Cache-Control'] = 'public, max-age=3600'  # Cache por 1 hora
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        return response
        
    except Exception as e:
        current_app.logger.error(f"Error sirviendo archivo multimedia '{filename}': {e}")
        return "Error interno del servidor", 500

@foro_bp.route('/')
@login_required
@usuario_activo_required
def index():
    # Obtener parámetros de filtro
    categoria_filter = request.args.get('categoria', '').strip()
    orden = request.args.get('orden', 'reciente')  # reciente, popular, antiguo
    
    # Query base
    query = Post.query.filter(Post.Estado == 'Activo')
    
    # Aplicar filtros
    if categoria_filter and categoria_filter != 'Todas':
        query = query.filter(Post.Categoria == categoria_filter)
    
    # Aplicar ordenamiento
    if orden == 'popular':
        query = query.order_by(db.func.count(Like.Id).desc())
    elif orden == 'antiguo':
        query = query.order_by(Post.FechaCreacion.asc())
    else:  # reciente
        query = query.order_by(Post.FechaCreacion.desc())
    
    posts = query.all()
    
    # Obtener categorías únicas para el filtro
    categorias = db.session.query(Post.Categoria).distinct().all()
    categorias = [cat[0] for cat in categorias if cat[0]]
    
    return render_template('foro/index.html', 
                         posts=posts,
                         categorias=categorias,
                         categoria_filter=categoria_filter,
                         orden=orden)

@foro_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@usuario_activo_required
def nuevo_post():
    if request.method == 'POST':
        try:
            post = Post(
                Titulo=request.form['titulo'],
                Contenido=request.form['contenido'],
                Categoria=request.form.get('categoria', 'General'),
                UsuarioId=current_user.Id
            )
            
            # Manejo de imagen
            imagen = request.files.get('imagen')
            if imagen and imagen.filename != '':
                filename = secure_filename(imagen.filename)
                ruta_directorio = os.path.join(current_app.root_path, 'static', 'uploads', 'foro', 'imagenes')
                os.makedirs(ruta_directorio, exist_ok=True)
                ruta_guardado = os.path.join(ruta_directorio, filename)
                imagen.save(ruta_guardado)
                post.Imagen = f'uploads/foro/imagenes/{filename}'
            
            # Manejo de video
            video = request.files.get('video')
            if video and video.filename != '':
                filename = secure_filename(video.filename)
                ruta_directorio = os.path.join(current_app.root_path, 'static', 'uploads', 'foro', 'videos')
                os.makedirs(ruta_directorio, exist_ok=True)
                ruta_guardado = os.path.join(ruta_directorio, filename)
                video.save(ruta_guardado)
                post.Video = f'uploads/foro/videos/{filename}'
            
            db.session.add(post)
            db.session.commit()
            flash('¡Post creado exitosamente! Tu publicación ya está disponible en el foro.', 'success')
            return redirect(url_for('foro.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el post. Por favor, intenta de nuevo.', 'error')
    
    categorias = ['General', 'Deportes', 'Eventos', 'Consejos', 'Noticias', 'Otros']
    return render_template('foro/nuevo_post.html', categorias=categorias)

@foro_bp.route('/post/<int:post_id>')
@login_required
@usuario_activo_required
def ver_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('foro/ver_post.html', post=post)

@foro_bp.route('/post/<int:post_id>/like', methods=['POST'])
@login_required
@usuario_activo_required
def toggle_like(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Verificar si ya existe el like
    like_existente = Like.query.filter_by(
        UsuarioId=current_user.Id,
        PostId=post_id
    ).first()
    
    if like_existente:
        # Quitar like
        db.session.delete(like_existente)
        mensaje = 'Like removido'
    else:
        # Agregar like
        nuevo_like = Like(UsuarioId=current_user.Id, PostId=post_id)
        db.session.add(nuevo_like)
        mensaje = 'Like agregado'
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'total_likes': post.total_likes,
        'is_liked': post.is_liked_by(current_user.Id),
        'mensaje': mensaje
    })

@foro_bp.route('/post/<int:post_id>/comentar', methods=['POST'])
@login_required
@usuario_activo_required
def comentar(post_id):
    post = Post.query.get_or_404(post_id)
    contenido = request.form.get('contenido', '').strip()
    
    if not contenido:
        flash('El comentario no puede estar vacío. Por favor, escribe algo antes de comentar.', 'warning')
        return redirect(url_for('foro.ver_post', post_id=post_id))
    
    try:
        comentario = ComentarioForo(
            Contenido=contenido,
            UsuarioId=current_user.Id,
            PostId=post_id
        )
        
        db.session.add(comentario)
        db.session.commit()
        flash('¡Comentario agregado exitosamente! Tu opinión ha sido publicada.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al agregar comentario. Por favor, intenta de nuevo.', 'error')
    
    return redirect(url_for('foro.ver_post', post_id=post_id))

@foro_bp.route('/post/<int:post_id>/editar', methods=['GET', 'POST'])
@login_required
@usuario_activo_required
def editar_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Solo el autor o admin puede editar
    es_admin = current_user.rol and current_user.rol.Nombre.lower() in ['admin', 'administrador']
    if post.UsuarioId != current_user.Id and not es_admin:
        flash('No tienes permisos para editar este post. Solo el autor o administradores pueden editarlo.', 'error')
        return redirect(url_for('foro.ver_post', post_id=post_id))
    
    if request.method == 'POST':
        try:
            post.Titulo = request.form['titulo']
            post.Contenido = request.form['contenido']
            post.Categoria = request.form.get('categoria', 'General')
            
            # Manejo de imagen
            imagen = request.files.get('imagen')
            if imagen and imagen.filename != '':
                filename = secure_filename(imagen.filename)
                ruta_directorio = os.path.join(current_app.root_path, 'static', 'uploads', 'foro', 'imagenes')
                os.makedirs(ruta_directorio, exist_ok=True)
                ruta_guardado = os.path.join(ruta_directorio, filename)
                imagen.save(ruta_guardado)
                post.Imagen = f'uploads/foro/imagenes/{filename}'
            
            # Manejo de video
            video = request.files.get('video')
            if video and video.filename != '':
                filename = secure_filename(video.filename)
                ruta_directorio = os.path.join(current_app.root_path, 'static', 'uploads', 'foro', 'videos')
                os.makedirs(ruta_directorio, exist_ok=True)
                ruta_guardado = os.path.join(ruta_directorio, filename)
                video.save(ruta_guardado)
                post.Video = f'uploads/foro/videos/{filename}'
            
            db.session.commit()
            flash('¡Post actualizado exitosamente! Los cambios han sido guardados.', 'success')
            return redirect(url_for('foro.ver_post', post_id=post_id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el post. Por favor, intenta de nuevo.', 'error')
    
    categorias = ['General', 'Deportes', 'Eventos', 'Consejos', 'Noticias', 'Otros']
    return render_template('foro/editar_post.html', post=post, categorias=categorias)

@foro_bp.route('/post/<int:post_id>/eliminar', methods=['POST'])
@login_required
@usuario_activo_required
def eliminar_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Solo el autor o admin puede eliminar
    es_admin = current_user.rol and current_user.rol.Nombre.lower() in ['admin', 'administrador']
    if post.UsuarioId != current_user.Id and not es_admin:
        flash('No tienes permisos para eliminar este post. Solo el autor o administradores pueden eliminarlo.', 'error')
        return redirect(url_for('foro.ver_post', post_id=post_id))
    
    try:
        post.Estado = 'Eliminado'
        db.session.commit()
        flash('¡Post eliminado exitosamente! La publicación ha sido removida del foro.', 'success')
        return redirect(url_for('foro.index'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el post. Por favor, intenta de nuevo.', 'error')
        return redirect(url_for('foro.ver_post', post_id=post_id))

@foro_bp.route('/comentarios-recientes')
@login_required
@usuario_activo_required
def comentarios_recientes():
    # Obtener los 10 comentarios más recientes
    comentarios = ComentarioForo.query.filter(
        ComentarioForo.Estado == 'Activo'
    ).order_by(ComentarioForo.FechaCreacion.desc()).limit(10).all()
    
    comentarios_data = []
    for comentario in comentarios:
        comentarios_data.append({
            'id': comentario.Id,
            'contenido': comentario.Contenido[:100] + '...' if len(comentario.Contenido) > 100 else comentario.Contenido,
            'fecha': comentario.FechaCreacion.strftime('%d/%m/%Y %H:%M'),
            'usuario': {
                'nombre': comentario.usuario.Nombre,
                'foto': comentario.usuario.FotoPerfil or 'images/default-user.png'
            },
            'post_id': comentario.PostId,
            'post_titulo': comentario.post.Titulo[:30] + '...' if len(comentario.post.Titulo) > 30 else comentario.post.Titulo
        })
    
    return jsonify({'comentarios': comentarios_data})

@foro_bp.route('/post/<int:post_id>/comentar-ajax', methods=['POST'])
@login_required
@usuario_activo_required
def comentar_ajax(post_id):
    post = Post.query.get_or_404(post_id)
    contenido = request.json.get('contenido', '').strip()
    
    if not contenido:
        return jsonify({'success': False, 'error': 'El comentario no puede estar vacío'})
    
    try:
        comentario = ComentarioForo(
            Contenido=contenido,
            UsuarioId=current_user.Id,
            PostId=post_id
        )
        
        db.session.add(comentario)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'comentario': {
                'id': comentario.Id,
                'contenido': comentario.Contenido,
                'fecha': comentario.FechaCreacion.strftime('%d/%m/%Y %H:%M'),
                'usuario': {
                    'nombre': comentario.usuario.Nombre,
                    'foto': comentario.usuario.FotoPerfil or 'images/default-user.png'
                }
            },
            'total_comentarios': post.total_comentarios
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Error al agregar comentario'})

@foro_bp.route('/comentario/<int:comentario_id>/eliminar', methods=['POST'])
@login_required
@usuario_activo_required
def eliminar_comentario(comentario_id):
    comentario = ComentarioForo.query.get_or_404(comentario_id)
    
    # Solo el autor o admin puede eliminar
    es_admin = current_user.rol and current_user.rol.Nombre.lower() in ['admin', 'administrador']
    if comentario.UsuarioId != current_user.Id and not es_admin:
        flash('No tienes permisos para eliminar este comentario. Solo el autor o administradores pueden eliminarlo.', 'error')
        return redirect(url_for('foro.ver_post', post_id=comentario.PostId))
    
    try:
        comentario.Estado = 'Eliminado'
        db.session.commit()
        flash('¡Comentario eliminado exitosamente! El comentario ha sido removido.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el comentario. Por favor, intenta de nuevo.', 'error')
    
    return redirect(url_for('foro.ver_post', post_id=comentario.PostId))

# ===== RUTAS ESPECIALES PARA ADMINISTRADORES =====





@foro_bp.route('/admin/post/<int:post_id>/toggle-estado', methods=['POST'])
@login_required
@usuario_activo_required
def admin_toggle_post_estado(post_id):
    """Permite al administrador cambiar el estado de cualquier post"""
    # Verificar si es administrador (aceptar tanto 'admin' como 'Administrador')
    es_admin = current_user.rol and current_user.rol.Nombre.lower() in ['admin', 'administrador']
    
    if not es_admin:
        return jsonify({'success': False, 'error': 'Acceso denegado'})
    
    post = Post.query.get_or_404(post_id)
    nuevo_estado = 'Activo' if post.Estado != 'Activo' else 'Oculto'
    
    try:
        post.Estado = nuevo_estado
        db.session.commit()
        
        return jsonify({
            'success': True,
            'nuevo_estado': nuevo_estado,
            'mensaje': f'Post marcado como {nuevo_estado}'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Error al cambiar estado'})

@foro_bp.route('/admin/post/<int:post_id>/eliminar-permanentemente', methods=['POST'])
@login_required
@usuario_activo_required
def admin_eliminar_post_permanentemente(post_id):
    """Permite al administrador eliminar permanentemente cualquier post"""
    # Verificar si es administrador (aceptar tanto 'admin' como 'Administrador')
    es_admin = current_user.rol and current_user.rol.Nombre.lower() in ['admin', 'administrador']
    
    if not es_admin:
        flash('Acceso denegado. Solo los administradores pueden eliminar posts permanentemente.', 'error')
        return redirect(url_for('foro.index'))
    
    post = Post.query.get_or_404(post_id)
    
    try:
        # Eliminar likes asociados
        Like.query.filter_by(PostId=post_id).delete()
        
        # Eliminar comentarios asociados
        ComentarioForo.query.filter_by(PostId=post_id).delete()
        
        # Eliminar el post
        db.session.delete(post)
        db.session.commit()
        
        flash('¡Post eliminado permanentemente! Todos los datos asociados han sido removidos.', 'success')
        return redirect(url_for('admin.admin_gestionar_posts'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el post permanentemente. Por favor, intenta de nuevo.', 'error')
        return redirect(url_for('admin.admin_gestionar_posts'))

@foro_bp.route('/admin/comentario/<int:comentario_id>/toggle-estado', methods=['POST'])
@login_required
@usuario_activo_required
def admin_toggle_comentario_estado(comentario_id):
    """Permite al administrador cambiar el estado de cualquier comentario"""
    # Verificar si es administrador (aceptar tanto 'admin' como 'Administrador')
    es_admin = current_user.rol and current_user.rol.Nombre.lower() in ['admin', 'administrador']
    
    if not es_admin:
        return jsonify({'success': False, 'error': 'Acceso denegado'})
    
    comentario = ComentarioForo.query.get_or_404(comentario_id)
    nuevo_estado = 'Activo' if comentario.Estado != 'Activo' else 'Oculto'
    
    try:
        comentario.Estado = nuevo_estado
        db.session.commit()
        
        return jsonify({
            'success': True,
            'nuevo_estado': nuevo_estado,
            'mensaje': f'Comentario marcado como {nuevo_estado}'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Error al cambiar estado'})

@foro_bp.route('/admin/comentario/<int:comentario_id>/eliminar-permanentemente', methods=['POST'])
@login_required
@usuario_activo_required
def admin_eliminar_comentario_permanentemente(comentario_id):
    """Permite al administrador eliminar permanentemente cualquier comentario"""
    # Verificar si es administrador (aceptar tanto 'admin' como 'Administrador')
    es_admin = current_user.rol and current_user.rol.Nombre.lower() in ['admin', 'administrador']
    
    if not es_admin:
        flash('Acceso denegado. Solo los administradores pueden eliminar comentarios permanentemente.', 'error')
        return redirect(url_for('foro.index'))
    
    comentario = ComentarioForo.query.get_or_404(comentario_id)
    post_id = comentario.PostId
    
    try:
        db.session.delete(comentario)
        db.session.commit()
        
        flash('¡Comentario eliminado permanentemente!', 'success')
        return redirect(url_for('foro.ver_post', post_id=post_id))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el comentario permanentemente. Por favor, intenta de nuevo.', 'error')
        return redirect(url_for('foro.ver_post', post_id=post_id))

 