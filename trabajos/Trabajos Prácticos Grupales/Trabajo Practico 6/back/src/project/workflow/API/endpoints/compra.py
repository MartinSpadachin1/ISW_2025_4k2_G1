# src/project/workflow/API/endpoints/compra.py
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from src.project.entities.Visitante import Visitante
from src.common.utils import validar_fecha
from src.common.counter import UniqueCounter
from src.common.pago import EFECTIVO, TARJETA
from src.project.workflow.API.login.security import verify_token

#Imports del ORM
from src.common.persistance.models import Reserva as ReservaModel, Visitante as VisitanteModel
from src.common.persistance.database import get_session
from datetime import datetime


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
def validar_compra(data: dict, 
                   user: str = Depends(verify_token),
                   session: Session = Depends(get_session)) -> dict: 
    print("Datos recibidos en /validar_compra/:", data)
    visitantes = [Visitante(**item) for item in data.get("visitantes", [])]
    fecha = data.get("fecha", "")
    unique = UniqueCounter()
    id = unique.next()
    email = user  # email extraído del token

    
    if not user:
        raise HTTPException(status_code=401, detail="Token inválido: usuario no presente en token")
    
    if validar_fecha(fecha) and 1 <= len(visitantes) <= 10 and data.get("forma_pago", "") in [EFECTIVO, TARJETA]:
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD.")

        #Creacion entidad Reserva
        db_reserva = ReservaModel(mail=email, fecha=fecha_obj)

        db_visitantes = []

        for visitante in visitantes:
            db_visitante = VisitanteModel(
                edad=visitante.edad,
                tipo_entrada=visitante.tipo_entrada,
                monto_final=visitante.monto
            )
            db_visitantes.append(db_visitante)

        # Asignar la lista de visitantes a la reserva
        db_reserva.visitantes = db_visitantes

        #Persistir en la base de datos
        session.add(db_reserva)
        session.commit()
        session.refresh(db_reserva)

         # El ID de la reserva recién creada
        id = db_reserva.id

        return {"valido": True,
                "id_compra": id}
    else:
        return {"valido": False,
                "razon": "Fecha inválida o más de 10 visitantes."}
