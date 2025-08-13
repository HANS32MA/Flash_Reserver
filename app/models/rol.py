from app import db

class Rol(db.Model):
    __tablename__ = 'Roles'
    
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), unique=True, nullable=False)
    usuarios = db.relationship('Usuario', back_populates='rol', lazy=True)
