from fastapi import FastAPI
from typing import Dict, Any
from src.common.entradas import PRECIO_GENERAL, PRECIO_VIP
from src.project.entities.Visitante import Visitante
from src.project.workflow.compra import calcular_monto
from src.common.utils import validar_fecha
from src.common.counter import UniqueCounter
from fastapi.middleware.cors import CORSMiddleware
from src.common.pago import EFECTIVO, TARJETA
from src.common.utils import validar_token

app = FastAPI() # LA API SE LEVANTA CON ESTE COMANDO: uvicorn src.project.workflow.API.main:app --reload

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o ["http://localhost:3000"] si usás React local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

@app.post("/monto/")
def realizar_compra(data: dict) -> float:
    visitantes = [Visitante(**item) for item in data.get("visitantes", [])]
    return calcular_monto(visitantes)

@app.post("/monto_unico/")
def obtener_monto_unico(data: dict) -> float:
    visitante = Visitante(**data)
    return visitante.monto

@app.get("/menor_edad/", response_model=dict)
def obtener_menor_edad() -> Dict[str, Any]:
    dic = {
        "bebes": {
            "rango": {
                "desde": 0,
                "hasta": 3,
            },
            "vip": 0,
            "general": 0,
        },
        "niños": {
            "rango": {
                "desde": 4,
                "hasta": 15,
            },
            "vip": PRECIO_VIP * 0.5,
            "general": PRECIO_GENERAL * 0.5,
        },
        "adultos": {
            "rango": {
                "desde": 16,
                "hasta": 65,
            },
            "vip": PRECIO_VIP,
            "general": PRECIO_GENERAL,
        },
        "adulto_mayor": {
            "rango": {
                "desde": 66,
                "hasta": 120,
            },
            "vip": PRECIO_VIP * 0.5,
            "general": PRECIO_GENERAL * 0.5,
        },
    }
    return dic

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
@app.post("/validar_compra/")
def validar_compra(data: dict) -> dict:
    visitantes = [Visitante(**item) for item in data.get("visitantes", [])]
    fecha = data.get("fecha", "")
    unique = UniqueCounter()
    id = unique.next()
    if validar_fecha(fecha) and len(visitantes) < 10  and validar_token(data.get("token", "")) and data.get("forma_pago", "") in [EFECTIVO, TARJETA]:
        return {"valido": True,
                "id_compra": id}
    else:
        return {"valido": False,
                "razon": "Fecha inválida o más de 10 visitantes."}
