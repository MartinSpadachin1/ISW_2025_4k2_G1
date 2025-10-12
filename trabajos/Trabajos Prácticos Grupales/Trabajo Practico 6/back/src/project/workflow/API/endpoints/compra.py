# src/project/workflow/API/endpoints/compra.py
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from src.project.entities.Visitante import Visitante
from src.common.utils import validar_fecha
from src.common.counter import UniqueCounter
from src.common.pago import EFECTIVO, TARJETA
from src.project.workflow.API.login.security import verify_token

#Imports del ORM
from src.common.persistance.models import Reserva as ReservaModel, Visitante as VisitanteModel
from src.common.persistance.database import get_session
from datetime import datetime

from src.common.email_utils import send_ticket_email


router_compra = APIRouter()


"""
CREDENTIALS #TODO COMO HACERLO EN EL FRONT??
Requisitos del request

Método: POST
URL: http://127.0.0.1:8000/validar_compra/ (o con prefijo /api/validar_compra/ si aplicaste prefix)
Headers:
Authorization: Bearer <TOKEN> (el token que recibiste en /login)
Content-Type: application/json
Body JSON: { fecha, visitantes, forma_pago } — NO enviar token ni mail si el backend usa el token para obtener el mail.


{
    "fecha": "2023-10-10",
    "visitantes": [
        { "edad": 20, "tipo_entrada": "vip" },
        { "edad": 25, "tipo_entrada": "general" },
    ],
    "forma_pago": "efectivo"
}



"""
@router_compra.post("/validar_compra/")
def validar_compra(
    data: dict,
    user: str = Depends(verify_token),
    session: Session = Depends(get_session)
) -> dict:
    print("Datos recibidos en /validar_compra/:", data)

    # === VALIDACIÓN TOKEN ===
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Token inválido: usuario no presente en token"
        )
    email = user  # email extraído del token

    # === VALIDACIÓN FECHA ===
    fecha = data.get("fecha")
    if not fecha:
        raise HTTPException(
            status_code=400,
            detail="Campo 'fecha' es obligatorio"
        )

    if not validar_fecha(fecha):
        raise HTTPException(
            status_code=400,
            detail="La fecha no es válida según las reglas definidas"
        )

    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Formato de fecha inválido. Use YYYY-MM-DD."
        )

    # === VALIDACIÓN VISITANTES ===
    visitantes_data = data.get("visitantes", [])
    if not isinstance(visitantes_data, list) or len(visitantes_data) == 0:
        raise HTTPException(
            status_code=400,
            detail="Debe incluir al menos un visitante"
        )
    if len(visitantes_data) > 10:
        raise HTTPException(
            status_code=400,
            detail="No se pueden incluir más de 10 visitantes por compra"
        )

    try:
        visitantes = [Visitante(**item) for item in visitantes_data]
    except TypeError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al parsear visitantes: {str(e)}"
        )
    except ValueError as e:
        # Validaciones internas (edad, tipo_entrada) fallaron
        raise HTTPException(
            status_code=400,
            detail=f"Error en datos de visitantes: {str(e)}"
        )

    # === VALIDACIÓN FORMA DE PAGO ===
    forma_pago = data.get("forma_pago")
    if forma_pago not in [EFECTIVO, TARJETA]:
        raise HTTPException(
            status_code=400,
            detail=f"Forma de pago inválida: {forma_pago}. Debe ser '{EFECTIVO}' o '{TARJETA}'"
        )

    # === PERSISTENCIA ===
    db_reserva = ReservaModel(mail=email, fecha=fecha_obj, tipo_pago=forma_pago, pago_realizado=False)
    db_visitantes = []

    for visitante in visitantes:
        db_visitante = VisitanteModel(
            edad=visitante.edad,
            tipo_entrada=visitante.tipo_entrada,
            monto_final=visitante.monto
        )
        db_visitantes.append(db_visitante)

    db_reserva.visitantes = db_visitantes

    session.add(db_reserva)
    session.commit()
    session.refresh(db_reserva)

    ### TODA ESTA PARTE ES PARA PROBAR EL ENVIO DE EMAILS
    statement = select(ReservaModel).where(ReservaModel.id == db_reserva.id)

    reserva = session.exec(statement).first()

    # Enviar email con tickets adjuntos sólo si la forma de pago es EFECTIVO
    if forma_pago == EFECTIVO:
        send_ticket_email(recipient_email=email, reserva=reserva)

    return {
        "valido": True,
        "id_compra": db_reserva.id
    }

