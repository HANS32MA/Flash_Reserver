from app import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'
    
    Id = db.Column(db.Integer, primary_key=True)
    Titulo = db.Column(db.String(200), nullable=False)
    Contenido = db.Column(db.Text, nullable=False)
    Imagen = db.Column(db.String(500), nullable=True)
    Video = db.Column(db.String(500), nullable=True)  # Campo para videos
    FechaCreacion = db.Column(db.DateTime, default=datetime.utcnow)
    FechaActualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    UsuarioId = db.Column(db.Integer, db.ForeignKey('Usuarios.Id'), nullable=False)
    Categoria = db.Column(db.String(50), default='General')  # General, Deportes, Eventos, etc.
    Estado = db.Column(db.String(20), default='Activo')  # Activo, Eliminado
    
    # Relaciones
    usuario = db.relationship('Usuario', backref='posts')
    likes = db.relationship('Like', backref='post', cascade='all, delete-orphan')
    comentarios = db.relationship('ComentarioForo', backref='post', cascade='all, delete-orphan')
    
    @property
    def total_likes(self):
        return len(self.likes)
    
    @property
    def total_comentarios(self):
        return len(self.comentarios)
    
    def is_liked_by(self, usuario_id):
        return any(like.UsuarioId == usuario_id for like in self.likes)
    
    @property
    def tiene_multimedia(self):
        """Verifica si el post tiene imagen o video"""
        return bool(self.Imagen or self.Video)
    
    @property
    def tipo_multimedia(self):
        """Retorna el tipo de multimedia del post"""
        if self.Video:
            return 'video'
        elif self.Imagen:
            return 'imagen'
        return None

class Like(db.Model):
    __tablename__ = 'likes'
    
    Id = db.Column(db.Integer, primary_key=True)
    UsuarioId = db.Column(db.Integer, db.ForeignKey('Usuarios.Id'), nullable=False)
    PostId = db.Column(db.Integer, db.ForeignKey('posts.Id'), nullable=False)
    FechaCreacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación
    usuario = db.relationship('Usuario', backref='likes')
    
    # Índice único para evitar likes duplicados
    __table_args__ = (db.UniqueConstraint('UsuarioId', 'PostId', name='unique_user_post_like'),)

class ComentarioForo(db.Model):
    __tablename__ = 'comentarios_foro'
    
    Id = db.Column(db.Integer, primary_key=True)
    Contenido = db.Column(db.Text, nullable=False)
    FechaCreacion = db.Column(db.DateTime, default=datetime.utcnow)
    FechaActualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    UsuarioId = db.Column(db.Integer, db.ForeignKey('Usuarios.Id'), nullable=False)
    PostId = db.Column(db.Integer, db.ForeignKey('posts.Id'), nullable=False)
    Estado = db.Column(db.String(20), default='Activo')
    
    # Relación
    usuario = db.relationship('Usuario', backref='comentarios_foro') 