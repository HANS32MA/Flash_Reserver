from app import db

class TipoCancha(db.Model):
    __tablename__ = 'TiposCancha'
    
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False, unique=True)
    Descripcion = db.Column(db.Text)
    
    # Relación sin backref para evitar conflictos
    canchas = db.relationship('Cancha', backref='tipo_cancha_rel', overlaps="tipo_cancha")
    
def __str__(self):
    return self.Nombre

def __repr__(self):
    return f"<TipoCancha {self.Nombre}>"