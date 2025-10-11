from aiohttp_retry import List
from src.project.entities.Visitante import Visitante

def calcular_monto(visitantes : List[Visitante]) -> float:
    
    
    if not visitantes:
        raise ValueError("La lista de visitantes no puede estar vacía.")
    
    if len(visitantes) > 10:
        raise ValueError("No se pueden procesar más de 10 visitantes a la vez.")
    
    total = 0
    for visitante in visitantes:
        total += visitante.monto
    
    return total

   

    