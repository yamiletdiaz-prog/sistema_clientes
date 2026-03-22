# ======================================
# tipos_clientes.py
# ======================================
from cliente import Cliente

class ClienteRegular(Cliente):
    def __init__(self, id, nombre, email, telefono, direccion, puntos=0):
        super().__init__(id, nombre, email, telefono, direccion)
        self.__puntos = puntos

    def get_puntos(self): return self.__puntos
    def set_puntos(self, puntos): self.__puntos = puntos
    def calcular_descuento(self): return self.__puntos * 0.01
    def get_tipo(self): return "Regular"

    def to_dict(self):
        d = super().to_dict()
        d["puntos"] = self.__puntos
        return d


class ClientePremium(Cliente):
    def calcular_descuento(self): return 20.0
    def get_tipo(self): return "Premium"


class ClienteCorporativo(Cliente):
    def __init__(self, id, nombre, email, telefono, direccion, empresa=""):
        super().__init__(id, nombre, email, telefono, direccion)
        self.__empresa = empresa

    def get_empresa(self): return self.__empresa
    def set_empresa(self, empresa): self.__empresa = empresa
    def calcular_descuento(self): return 30.0
    def get_tipo(self): return "Corporativo"

    def to_dict(self):
        d = super().to_dict()
        d["empresa"] = self.__empresa
        return d
