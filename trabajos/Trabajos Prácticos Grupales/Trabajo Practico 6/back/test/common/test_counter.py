from src.common.counter import UniqueCounter


def test_counter_unique_and_singleton():
    # Setup
    c1 = UniqueCounter()
    c2 = UniqueCounter()
    # Assertion: mismo objeto (singleton)
    assert c1 is c2, "UniqueCounter debe ser singleton (misma instancia)"

    # Execution
    a = c1.next()
    b = c2.next()
    c = c1.next()

    # Assertions
    assert a != b != c, "Los valores devueltos por next() deben ser distintos"
    assert a < b < c, "Los valores deben ser crecientes"
