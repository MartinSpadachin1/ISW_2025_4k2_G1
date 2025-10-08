import datetime
import pytest

from src.common.utils import validar_fecha


def test_validar_fecha_anterior():
    ayer = datetime.date.today() - datetime.timedelta(days=1)
    assert validar_fecha(ayer) is False


def test_validar_fecha_lunes():
    hoy = datetime.date.today()
    dias_hasta_lunes = (0 - hoy.weekday()) % 7
    if dias_hasta_lunes == 0:
        dias_hasta_lunes = 7
    proximo_lunes = hoy + datetime.timedelta(days=dias_hasta_lunes)
    assert proximo_lunes.weekday() == 0
    assert validar_fecha(proximo_lunes) is False


def test_validar_fecha_navidad():
    year = datetime.date.today().year
    navidad = datetime.date(year, 12, 25)
    if navidad < datetime.date.today():
        navidad = datetime.date(year + 1, 12, 25)
    assert validar_fecha(navidad) is False


def test_validar_fecha_ano_nuevo():
    year = datetime.date.today().year
    primer_enero = datetime.date(year, 1, 1)
    if primer_enero < datetime.date.today():
        primer_enero = datetime.date(year + 1, 1, 1)
    assert validar_fecha(primer_enero) is False


def test_validar_fecha_valida():
    manana = datetime.date.today() + datetime.timedelta(days=1)
    while manana.weekday() == 0 or (manana.month, manana.day) in ((12, 25), (1, 1)):
        manana += datetime.timedelta(days=1)
    assert validar_fecha(manana) is True


def test_validar_fecha_excepciones_raise():
    with pytest.raises(ValueError):
        validar_fecha("2025-13-40")
    with pytest.raises(TypeError):
        validar_fecha(12345)


