from app import db
from datetime import datetime


class Categoria(db.Model):
    __tablename__ = 'Categorias'
    
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False, unique=True)
    Descripcion = db.Column(db.Text)
    FechaCreacion = db.Column(db.DateTime, default=datetime.utcnow)

    
    # Relación sin backref para evitar conflictos
    canchas = db.relationship('Cancha', backref='categoria_rel', overlaps="categoria")

def __str__(self):
    return self.Nombre

def __repr__(self):
    return f"<Categoria {self.Nombre}>"
