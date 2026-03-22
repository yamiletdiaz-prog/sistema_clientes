# ======================================
# cliente.py
# ======================================
class Cliente:
    def __init__(self, id, nombre, email, telefono, direccion):
        self.__id = id
        self.__nombre = nombre
        self.__email = email
        self.__telefono = telefono
        self.__direccion = direccion

    # Getters
    def get_id(self): return self.__id
    def get_nombre(self): return self.__nombre
    def get_email(self): return self.__email
    def get_telefono(self): return self.__telefono
    def get_direccion(self): return self.__direccion

    # Setters
    def set_id(self, cliente_id): self.__id = cliente_id
    def set_nombre(self, nombre): self.__nombre = nombre
    def set_email(self, email): self.__email = email
    def set_telefono(self, telefono): self.__telefono = telefono
    def set_direccion(self, direccion): self.__direccion = direccion

    def get_tipo(self): return "Base"
    def calcular_descuento(self): return 0.0

    def to_dict(self):
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "email": self.__email,
            "telefono": self.__telefono,
            "direccion": self.__direccion,
            "tipo": self.get_tipo()
        }

    def __str__(self):
        return f"{self.__id} - {self.__nombre} ({self.get_tipo()})"