from app import db

class Cancha(db.Model):
    __tablename__ = 'Canchas'
    
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Descripcion = db.Column(db.String(255), nullable=True)
    TipoCanchaId = db.Column(db.Integer, db.ForeignKey('TiposCancha.Id'), nullable=False)
    CategoriaId = db.Column(db.Integer, db.ForeignKey('Categorias.Id'), nullable=False)
    PrecioHora = db.Column(db.Numeric(10,2), nullable=False)
    Imagen = db.Column(db.String(255), nullable=True)
    Estado = db.Column(db.String(20), nullable=False, default='Disponible')
    
    # Campos de ubicación
    Latitud = db.Column(db.Float, nullable=True)
    Longitud = db.Column(db.Float, nullable=True)
    Direccion = db.Column(db.String(255), nullable=True)
    Barrio = db.Column(db.String(100), nullable=True)
    Ciudad = db.Column(db.String(100), nullable=True, default='Valledupar')

    # Relaciones
    tipo_cancha = db.relationship('TipoCancha', foreign_keys=[TipoCanchaId], overlaps="tipo_cancha_rel")
    categoria = db.relationship('Categoria', foreign_keys=[CategoriaId], overlaps="categoria_rel")
    horarios = db.relationship('Horario', backref='cancha', lazy=True)
    comentarios = db.relationship('Comentario', backref='cancha', lazy=True)
    imagen = db.relationship('Imagen', backref='cancha', lazy=True)

    # RELACIÓN CORREGIDA CON RESERVAS
    reservas = db.relationship("Reserva", back_populates="cancha", lazy=True)
