# ======================================
# test_gic.py
# ======================================
import unittest
import os
from gestor_clientes import (
    GestorClientes, ClienteDuplicadoError,
    ClienteNoEncontradoError, PersistenciaError
)
from tipos_clientes import ClienteRegular, ClientePremium, ClienteCorporativo


class TestGestorClientes(unittest.TestCase):

    def setUp(self):
        self.gestor = GestorClientes()

    # --- Agregar ---
    def test_agregar_cliente(self):
        c = ClientePremium(1, "Ana", "ana@mail.com", "123", "Calle 1")
        self.gestor.agregar(c)
        self.assertEqual(len(self.gestor.listar()), 1)

    def test_agregar_duplicado(self):
        c = ClientePremium(1, "Ana", "", "", "")
        self.gestor.agregar(c)
        with self.assertRaises(ClienteDuplicadoError):
            self.gestor.agregar(ClientePremium(1, "Otro", "", "", ""))

    # --- Buscar ---
    def test_buscar_existente(self):
        c = ClienteRegular(2, "Luis", "", "", "", 100)
        self.gestor.agregar(c)
        encontrado = self.gestor.buscar(2)
        self.assertEqual(encontrado.get_nombre(), "Luis")

    def test_buscar_inexistente(self):
        with self.assertRaises(ClienteNoEncontradoError):
            self.gestor.buscar(999)

    # --- Eliminar ---
    def test_eliminar_cliente(self):
        c = ClientePremium(3, "María", "", "", "")
        self.gestor.agregar(c)
        self.gestor.eliminar(3)
        self.assertEqual(len(self.gestor.listar()), 0)

    def test_eliminar_inexistente(self):
        with self.assertRaises(ClienteNoEncontradoError):
            self.gestor.eliminar(999)

    # --- Actualizar ---
    def test_actualizar_nombre(self):
        c = ClientePremium(4, "Pedro", "pedro@email.com", "", "")
        self.gestor.agregar(c)
        self.gestor.actualizar(4, nombre="Pedro Actualizado")
        self.assertEqual(self.gestor.buscar(4).get_nombre(), "Pedro Actualizado")

    # --- Polimorfismo ---
    def test_descuento_regular(self):
        c = ClienteRegular(5, "R", "", "", "", 500)
        self.assertEqual(c.calcular_descuento(), 5.0)

    def test_descuento_premium(self):
        c = ClientePremium(6, "P", "", "", "")
        self.assertEqual(c.calcular_descuento(), 20.0)

    def test_descuento_corporativo(self):
        c = ClienteCorporativo(7, "C", "", "", "", "EmpresaX")
        self.assertEqual(c.calcular_descuento(), 30.0)

    # --- Persistencia JSON ---
    def test_guardar_y_cargar_json(self):
        ruta = "_test_datos.json"
        self.gestor.agregar(ClienteRegular(10, "J", "j@m.com", "1", "D", 50))
        self.gestor.agregar(ClienteCorporativo(11, "K", "", "", "", "Corp"))
        self.gestor.guardar_json(ruta)

        gestor2 = GestorClientes()
        gestor2.cargar_json(ruta)
        self.assertEqual(len(gestor2.listar()), 2)
        os.remove(ruta)

    def test_cargar_json_inexistente(self):
        with self.assertRaises(PersistenciaError):
            self.gestor.cargar_json("archivo_que_no_existe.json")

    # --- Exportar CSV ---
    def test_exportar_csv(self):
        ruta = "_test_datos.csv"
        self.gestor.agregar(ClientePremium(20, "CSV", "", "", ""))
        self.gestor.exportar_csv(ruta)
        self.assertTrue(os.path.exists(ruta))
        os.remove(ruta)

    def test_exportar_csv_vacio(self):
        with self.assertRaises(PersistenciaError):
            self.gestor.exportar_csv("_vacio.csv")


def test():
    """Función simple para ejecutar desde main.py."""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGestorClientes)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print("✔ Todos los tests pasaron")
    else:
        print("⚠ Algunos tests fallaron")


if __name__ == "__main__":
    unittest.main()

