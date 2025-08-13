from app import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = 'Usuarios'
    
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Telefono = db.Column(db.String(20), nullable=False)
    Contrasena = db.Column(db.String(255), nullable=False)
    RolId = db.Column(db.Integer, db.ForeignKey('Roles.Id'), nullable=False)
    FotoPerfil = db.Column(db.String(255), nullable=True)
    FechaRegistro = db.Column(db.DateTime, server_default=db.func.now())
    Estado = db.Column(db.Boolean, default=True, nullable=False)
    rol = db.relationship('Rol', back_populates='usuarios')  
    
    def get_id(self):
        return str(self.Id)
    
    @property
    def estado_texto(self):
        """Retorna el texto del estado del usuario"""
        return "Activo" if self.Estado else "Inactivo"
    
    @property
    def estado_badge_class(self):
        """Retorna la clase CSS para el badge del estado"""
        return "success" if self.Estado else "danger"