from fastapi import APIRouter, HTTPException
from src.project.entities.Visitante import Visitante
from src.common.utils import validar_fecha
from src.common.counter import UniqueCounter
from fastapi.middleware.cors import CORSMiddleware
from src.common.pago import EFECTIVO, TARJETA
from src.common.utils import validar_token


router_compra = APIRouter()


"""
{
    "token": "string",
    "fecha": "2023-10-10",
    "visitantes": [
        { "edad": 20, "tipo_entrada": "vip" },
        { "edad": 25, "tipo_entrada": "general" },
    ],
    "forma_pago": "efectivo"
}



"""
@router_compra.post("/validar_compra/")
def validar_compra(data: dict) -> dict:
    visitantes = [Visitante(**item) for item in data.get("visitantes", [])]
    fecha = data.get("fecha", "")
    unique = UniqueCounter()
    id = unique.next()
    if validar_fecha(fecha) and 1 <= len(visitantes) <= 10 and validar_token(data.get("token", "")) and data.get("forma_pago", "") in [EFECTIVO, TARJETA]:
        return {"valido": True,
                "id_compra": id}
    else:
        return {"valido": False,
                "razon": "Fecha inválida o más de 10 visitantes."}
