from src.project.entities.Visitante import Visitante
from src.common.entradas import VIP, GENERAL, PRECIO_VIP, PRECIO_GENERAL


def test_visitante_bebe_gratis():
    v = Visitante(2, GENERAL)
    assert v.monto == 0, f"Bebé de 2 años debe pagar 0, obtuvo {v.monto}"


def test_visitante_nino_vip_descuento():
    v = Visitante(10, VIP)
    expected = PRECIO_VIP * 0.5
    assert v.monto == expected, f"Niño VIP debe pagar {expected}, obtuvo {v.monto}"


def test_visitante_adulto_general():
    v = Visitante(30, GENERAL)
    expected = PRECIO_GENERAL
    assert v.monto == expected, f"Adulto general debe pagar {expected}, obtuvo {v.monto}"


def test_visitante_adulto_mayor_vip():
    v = Visitante(70, VIP)
    expected = PRECIO_VIP * 0.5
    assert v.monto == expected, f"Adulto mayor VIP debe pagar {expected}, obtuvo {v.monto}"


def test_visitante_atributos():
    v = Visitante(25, GENERAL)
    assert v.edad == 25, f"Edad esperada 25, obtuvo {v.edad}"
    assert v.tipo_entrada == GENERAL, f"Tipo de entrada esperado {GENERAL}, obtuvo {v.tipo_entrada}"

def test_visitante_edad_invalida_negativa():
    try:
        Visitante(-5, VIP)
        assert False, "Se esperaba ValueError para edad negativa"
    except ValueError as e:
        assert str(e) == "La edad debe estar entre 0 y 120 años.", f"Mensaje de error inesperado: {e}"
        
def test_visitante_edad_invalida_alta():
    try:
        Visitante(130, GENERAL)
        assert False, "Se esperaba ValueError para edad mayor a 120"
    except ValueError as e:
        assert str(e) == "La edad debe estar entre 0 y 120 años.", f"Mensaje de error inesperado: {e}"
        
def test_visitante_edad_invalida_none():
    try:
        Visitante(None, VIP)
        assert False, "Se esperaba ValueError para edad None"
    except ValueError as e:
        assert str(e) == "La edad debe estar entre 0 y 120 años.", f"Mensaje de error inesperado: {e}"
        
        