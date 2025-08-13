from app import db
from datetime import datetime

class Comentario(db.Model):
    __tablename__ = 'Comentarios'
    
    Id = db.Column(db.Integer, primary_key=True)
    UsuarioId = db.Column(db.Integer, db.ForeignKey('Usuarios.Id'), nullable=False)
    CanchaId = db.Column(db.Integer, db.ForeignKey('Canchas.Id'), nullable=False)
    Comentario = db.Column(db.Text, nullable=False)
    Calificacion = db.Column(db.Integer, nullable=False)  # 1-5 estrellas
    FechaCreacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones sin backref para evitar conflictos
    usuario = db.relationship('Usuario', backref='comentarios')
