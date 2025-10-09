from src.common.counter import UniqueCounter


def test_counter_unique_and_singleton():
    c1 = UniqueCounter()
    c2 = UniqueCounter()
    assert c1 is c2, "UniqueCounter debe ser singleton (misma instancia)"

    a = c1.next()
    b = c2.next()
    c = c1.next()

    assert a != b != c, "Los valores devueltos por next() deben ser distintos"
    assert a < b < c, "Los valores deben ser crecientes"
