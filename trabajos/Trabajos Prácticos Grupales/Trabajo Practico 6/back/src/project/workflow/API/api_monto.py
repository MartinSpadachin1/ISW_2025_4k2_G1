from fastapi import FastAPI
from src.common.entradas import PRECIO_GENERAL, PRECIO_VIP
from src.project.entities.Visitante import Visitante
from src.project.workflow.compra import calcular_monto
from src.common.utils import validar_fecha
from src.common.counter import UniqueCounter

app = FastAPI()

@app.post("/monto/")
def realizar_compra(data: dict) -> float:
    visitantes = [Visitante(**item) for item in data.get("visitantes", [])]
    return calcular_monto(visitantes)

@app.post("/monto_unico/")
def obtener_monto_unico(data: dict) -> float:
    visitante = Visitante(**data)
    return visitante.monto

@app.get("/menor_edad/")
def obtener_menor_edad() -> float:
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


@app.post("/validar_compra/")
def validar_compra(data: dict) -> dict:
    visitantes = [Visitante(**item) for item in data.get("visitantes", [])]
    fecha = data.get("fecha", "")
    unique = UniqueCounter()
    id = unique.next()
    if validar_fecha(fecha) and len(visitantes) < 10:
        return {"valido": True,
                "id_compra": id}
    else:
        return {"valido": False,
                "razon": "Fecha inválida o más de 10 visitantes."}
