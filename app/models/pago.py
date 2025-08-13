from app import db
from datetime import datetime

class Pago(db.Model):
    __tablename__ = 'Pagos'
    
    Id = db.Column(db.Integer, primary_key=True)
    ReservaId = db.Column(db.Integer, db.ForeignKey('Reservas.Id'), nullable=False)
    Monto = db.Column(db.Numeric(10,2), nullable=False)
    MetodoPago = db.Column(db.String(50), nullable=False)  # Efectivo, Tarjeta, Transferencia
    Estado = db.Column(db.String(20), default='Pendiente')  # Pendiente, Pagado, Cancelado
    FechaPago = db.Column(db.DateTime, default=datetime.utcnow)
    
    reserva = db.relationship('Reserva', backref='pago', uselist=False)
