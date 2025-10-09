import threading


class UniqueCounter:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(UniqueCounter, cls).__new__(cls)
                    cls._instance._value = 10000
                    cls._instance._value_lock = threading.Lock()
        return cls._instance

    def next(self) -> int:
        with self._value_lock:
            self._value += 1
            return self._value
