# src/project/workflow/API/endpoints/pago.py
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from src.project.workflow.API.login.security import verify_token
from src.common.persistance.database import get_session
from src.common.utils import validar_pago
from src.project.entities.Reserva import Reserva  # DTO/entidad de dominio (no-ORM)
from sqlmodel import select
from src.common.persistance.models import Reserva as ReservaModel
from src.common.email_utils import send_ticket_email
from src.common.persistance.models import Reserva as ReservaModel

router_pago = APIRouter()


"""
json:
{
    "id_reserva": 1,
    "numero_tarjeta": "1234567812345678",
    "cvv": "123",
    "fecha_expiracion": "2025-12-31"
}"""

@router_pago.post("/procesar_pago/")
def procesar_pago(
    data: dict,
    user: str = Depends(verify_token),
    session: Session = Depends(get_session)
) -> dict:
    print("Datos recibidos en /procesar_pago/:", data)

    # === VALIDACIÓN TOKEN ===
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Token inválido: usuario no presente en token"
        )
    email = user  # email extraído del token

    if not validar_pago(data.get("numero_tarjeta"), cvv=data.get("cvv"), fecha_expiracion=data.get("fecha_expiracion")):
        raise HTTPException(
            status_code=400,
            detail="Datos de pago inválidos"
        )
    
    #TODO: Poner en la reserva que el pago fue realizado (persistencia)
    statement = select(ReservaModel).where(ReservaModel.id == data.get("id_reserva"), ReservaModel.mail == email)
    reserva = session.exec(statement).first()

    if not reserva:
        raise HTTPException(
            status_code=404,
            detail="Reserva no encontrada"
        )

    reserva.pago_realizado = True
    session.add(reserva)
    session.commit()
    session.refresh(reserva)

    # Enviar email con tickets adjuntos
    send_ticket_email(recipient_email=email, reserva=reserva)

    return {
        "message": "Pago procesado exitosamente",
        "email": email,
        "data": data,
        "reserva_id": reserva.id
    }