from fastapi import APIRouter, HTTPException, Depends
from src.project.entities.Visitante import Visitante
from src.common.utils import validar_fecha
from src.common.counter import UniqueCounter
from fastapi.middleware.cors import CORSMiddleware
from src.common.pago import EFECTIVO, TARJETA
from src.common.utils import validar_token
from src.project.entities.Reserva import Reserva
from src.project.workflow.API.login.security import verify_token
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
def validar_compra(data: dict, user: str = Depends(verify_token)) -> dict:
    visitantes = [Visitante(**item) for item in data.get("visitantes", [])]
    fecha = data.get("fecha", "")
    unique = UniqueCounter()
    id = unique.next()
    email = user  # email extraído del token
    if not user:
        raise HTTPException(status_code=401, detail="Token inválido: usuario no presente en token")
    if validar_fecha(fecha) and 1 <= len(visitantes) <= 10 and data.get("forma_pago", "") in [EFECTIVO, TARJETA]:
        reserva = Reserva(id, email, visitantes, fecha)
        # TODO: Persistir la reserva en la base de datos
        return {"valido": True,
                "id_compra": id}
    else:
        return {"valido": False,
                "razon": "Fecha inválida o más de 10 visitantes."}
