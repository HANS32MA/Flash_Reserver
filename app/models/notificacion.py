from datetime import datetime
from app import db

class Notificacion(db.Model):
    __tablename__ = 'notificaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.Id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'email', 'push', 'sms', 'in_app'
    titulo = db.Column(db.String(200), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    estado = db.Column(db.String(20), default='pendiente')  # 'pendiente', 'enviado', 'fallido'
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_envio = db.Column(db.DateTime, nullable=True)
    intentos = db.Column(db.Integer, default=0)
    max_intentos = db.Column(db.Integer, default=3)
    datos_adicionales = db.Column(db.JSON, nullable=True)
    
    # Relaciones
    usuario = db.relationship('Usuario', backref='notificaciones')
    
    def __repr__(self):
        return f'<Notificacion {self.tipo} para {self.usuario_id}>'
    
    def marcar_enviado(self):
        self.estado = 'enviado'
        self.fecha_envio = datetime.utcnow()
        db.session.commit()
    
    def marcar_fallido(self):
        self.intentos += 1
        if self.intentos >= self.max_intentos:
            self.estado = 'fallido'
        db.session.commit()
    
    def puede_reintentar(self):
        return self.intentos < self.max_intentos and self.estado != 'enviado'
