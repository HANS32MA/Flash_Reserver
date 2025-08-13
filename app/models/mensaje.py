from app import db
from datetime import datetime

class Mensaje(db.Model):
    __tablename__ = 'mensajes'
    
    Id = db.Column(db.Integer, primary_key=True)
    UsuarioId = db.Column(db.Integer, db.ForeignKey('Usuarios.Id'), nullable=False)
    Asunto = db.Column(db.String(200), nullable=False)
    Mensaje = db.Column(db.Text, nullable=False)
    FechaEnvio = db.Column(db.DateTime, default=datetime.utcnow)
    Leido = db.Column(db.Boolean, default=False)
    Respuesta = db.Column(db.Text)
    FechaRespuesta = db.Column(db.DateTime)
    
    # Relación con el usuario que envió el mensaje
    usuario = db.relationship('Usuario', backref='mensajes_enviados')
    
    def __repr__(self):
        return f'<Mensaje {self.Id}: {self.Asunto}>'
    
    @property
    def fecha_formateada(self):
        return self.FechaEnvio.strftime('%d/%m/%Y %H:%M')
    
    @property
    def fecha_respuesta_formateada(self):
        if self.FechaRespuesta:
            return self.FechaRespuesta.strftime('%d/%m/%Y %H:%M')
        return None
