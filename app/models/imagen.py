# models/imagen.py
from app import db

class Imagen(db.Model):
    __tablename__ = 'Imagenes'

    Id = db.Column(db.Integer, primary_key=True)
    CanchaId = db.Column(db.Integer, db.ForeignKey('Canchas.Id'), nullable=False)
    Ruta = db.Column(db.String(255), nullable=False)
    
