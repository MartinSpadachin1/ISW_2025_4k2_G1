

class Entrada():
    def __init__(self, edad, vip):
        if edad >= 0:
            self.edad = edad
        else:
            raise ValueError('La edad es invalida debe ser un numero entre 1-99')
        self.vip = vip
        self.precio = self._calcular_precio(edad, vip)

    def get_edad(self):
        return self.edad

    def set_edad(self, value):
        self.edad = value

    def get_vip(self):
        return self.vip

    def set_vip(self, value):
        self.vip = value

    def get_precio(self):
        return self.precio

    def set_precio(self, value):
        self.precio = value


    def _calcular_precio(self, edad, vip):
        if edad < 4:
            return 0
        elif  15 < edad <= 60:
            if vip:
                return 10000
            else:
                return 5000
        else:
            if vip:
                return 5000
            else:
                return 2500
            