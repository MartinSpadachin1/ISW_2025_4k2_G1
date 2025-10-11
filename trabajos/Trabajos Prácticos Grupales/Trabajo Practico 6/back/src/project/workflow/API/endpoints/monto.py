from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from src.common.entradas import PRECIO_GENERAL, PRECIO_VIP
from src.project.entities.Visitante import Visitante
from src.project.workflow.compra_calculo import calcular_monto

router_monto = APIRouter()


@router_monto.post("/monto_total/")
def obtener_monto_total(data: dict) -> float:
    visitantes = [Visitante(**item) for item in data.get("visitantes", [])]
    return calcular_monto(visitantes)

@router_monto.post("/monto_unico/")
def obtener_monto_unico(data: dict) -> float:
    visitante = Visitante(**data)
    return visitante.monto

@router_monto.get("/edades/", response_model=dict)
def obtener_edades() -> Dict[str, Any]:
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