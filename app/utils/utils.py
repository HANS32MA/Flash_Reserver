# app/utils.py
from datetime import datetime
from app.models import Cancha, Reserva
from app import db

def liberar_canchas_sin_reservas():
    """Libera automáticamente canchas que ya no tienen reservas futuras."""
    hoy = datetime.now().date()
    canchas = Cancha.query.all()

    for cancha in canchas:
        # Si la cancha está en mantenimiento, no se toca
        if cancha.Estado == 'Mantenimiento':
            continue

        # Contar reservas confirmadas futuras
        reservas_activas = Reserva.query.filter(
            Reserva.CanchaId == cancha.Id,
            Reserva.Fecha >= hoy,
            Reserva.Estado == 'Confirmada'
        ).count()

        # Si no hay reservas, vuelve a Disponible
        if reservas_activas == 0:
            cancha.Estado = 'Disponible'
        else:
            cancha.Estado = 'Ocupado'

    db.session.commit()
