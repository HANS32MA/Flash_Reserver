from app import db
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

class Reserva(db.Model):
    __tablename__ = 'Reservas'
    
    Id = db.Column(db.Integer, primary_key=True)
    UsuarioId = db.Column(db.Integer, db.ForeignKey('Usuarios.Id'), nullable=False)
    CanchaId = db.Column(db.Integer, db.ForeignKey('Canchas.Id'), nullable=False)
    Fecha = db.Column(db.Date, nullable=False)
    HoraInicio = db.Column(db.Time, nullable=False)
    HoraFin = db.Column(db.Time, nullable=False)
    Estado = db.Column(db.String(20), default='Confirmada')  # Confirmada, Cancelada, Completada
    FechaCreacion = db.Column(db.DateTime, default=datetime.utcnow)
    Observaciones = db.Column(db.Text)

    # Relaciones correctas
    usuario = db.relationship('Usuario', backref='reservas')
    cancha = db.relationship('Cancha', foreign_keys=[CanchaId], back_populates='reservas')

    @property
    def duracion_horas(self):
        inicio = datetime.combine(datetime.min, self.HoraInicio)
        fin = datetime.combine(datetime.min, self.HoraFin)
        duracion = fin - inicio
        return duracion.total_seconds() / 3600

    @property
    def precio_total(self):
        total = self.cancha.PrecioHora * Decimal(str(self.duracion_horas))
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
