# ======================================
# gestor_clientes.py
# ======================================
import json
import csv
from cliente import Cliente
from tipos_clientes import ClienteRegular, ClientePremium, ClienteCorporativo


# --- Excepciones personalizadas ---
class ClienteDuplicadoError(Exception):
    pass

class ClienteNoEncontradoError(Exception):
    pass

class PersistenciaError(Exception):
    pass


class GestorClientes:
    def __init__(self):
        self.__clientes = []

    def agregar(self, cliente):
        if any(c.get_id() == cliente.get_id() for c in self.__clientes):
            raise ClienteDuplicadoError(f"Ya existe un cliente con ID {cliente.get_id()}")
        self.__clientes.append(cliente)

    def listar(self):
        return self.__clientes

    def buscar(self, id_cliente):
        for c in self.__clientes:
            if c.get_id() == id_cliente:
                return c
        raise ClienteNoEncontradoError(f"No se encontró cliente con ID {id_cliente}")

    def eliminar(self, id_cliente):
        cliente = self.buscar(id_cliente)
        self.__clientes.remove(cliente)

    def actualizar(self, id_cliente, **kwargs):
        cliente = self.buscar(id_cliente)
        if "nombre" in kwargs:
            cliente.set_nombre(kwargs["nombre"])
        if "email" in kwargs:
            cliente.set_email(kwargs["email"])
        if "telefono" in kwargs:
            cliente.set_telefono(kwargs["telefono"])
        if "direccion" in kwargs:
            cliente.set_direccion(kwargs["direccion"])

    def guardar_json(self, ruta):
        try:
            datos = [c.to_dict() for c in self.__clientes]
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
        except OSError as e:
            raise PersistenciaError(f"Error al guardar JSON: {e}")

    def cargar_json(self, ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            raise PersistenciaError(f"Error al cargar JSON: {e}")

        self.__clientes = []
        for d in datos:
            tipo = d.get("tipo", "Base")
            if tipo == "Regular":
                c = ClienteRegular(d["id"], d["nombre"], d["email"],
                                   d["telefono"], d["direccion"], d.get("puntos", 0))
            elif tipo == "Premium":
                c = ClientePremium(d["id"], d["nombre"], d["email"],
                                   d["telefono"], d["direccion"])
            elif tipo == "Corporativo":
                c = ClienteCorporativo(d["id"], d["nombre"], d["email"],
                                       d["telefono"], d["direccion"], d.get("empresa", ""))
            else:
                c = Cliente(d["id"], d["nombre"], d["email"],
                            d["telefono"], d["direccion"])
            self.__clientes.append(c)

    def exportar_csv(self, ruta):
        if not self.__clientes:
            raise PersistenciaError("No hay clientes para exportar")
        try:
            with open(ruta, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Nombre", "Email", "Teléfono", "Dirección", "Tipo", "Descuento"])
                for c in self.__clientes:
                    writer.writerow([
                        c.get_id(), c.get_nombre(), c.get_email(),
                        c.get_telefono(), c.get_direccion(),
                        c.get_tipo(), c.calcular_descuento()
                    ])
        except OSError as e:
            raise PersistenciaError(f"Error al exportar CSV: {e}")