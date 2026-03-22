# ======================================
# main.py
# ======================================
from test_sistemas import test

try:
    import tkinter as tk
    from interfaz import AplicacionClientes
    TK_AVAILABLE = True
except ImportError:
    TK_AVAILABLE = False

if __name__ == "__main__":
    test()

    if TK_AVAILABLE and AplicacionClientes:
        root = tk.Tk()
        app = AplicacionClientes(root)
        root.mainloop()
    else:
        print("⚠ tkinter no disponible. Ejecutando en consola")
        from gestor_clientes import GestorClientes
        from tipos_clientes import ClientePremium

        g = GestorClientes()
        g.agregar(ClientePremium(1, "Demo", "", "", ""))
        for c in g.listar():
            print(c)
