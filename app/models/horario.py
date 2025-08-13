from app import db

class Horario(db.Model):
    __tablename__ = 'Horarios'
    
    Id = db.Column(db.Integer, primary_key=True)
    CanchaId = db.Column(db.Integer, db.ForeignKey('Canchas.Id'), nullable=False)
    DiaSemana = db.Column(db.Integer, nullable=False)  # 0=Lunes, 1=Martes, etc.
    HoraInicio = db.Column(db.Time, nullable=False)
    HoraFin = db.Column(db.Time, nullable=False)
    Estado = db.Column(db.Boolean, default=True)  # True=Activo, False=Inactivo
