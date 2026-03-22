# ======================================
# interfaz.py
# ======================================
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    from gestor_clientes import (
        GestorClientes, ClienteDuplicadoError,
        ClienteNoEncontradoError, PersistenciaError
    )
    from tipos_clientes import ClienteRegular, ClientePremium, ClienteCorporativo

    class AplicacionClientes:
        def __init__(self, root):
            self.gestor = GestorClientes()
            self.root = root
            self.root.title("Sistema de Gestión de Clientes")
            self._crear_widgets()

        def _crear_widgets(self):
            # --- Frame de entrada de datos ---
            frame_datos = tk.LabelFrame(self.root, text="Datos del Cliente")
            frame_datos.pack(padx=10, pady=5, fill="x")

            tk.Label(frame_datos, text="ID:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
            self.entry_id = tk.Entry(frame_datos)
            self.entry_id.grid(row=0, column=1, padx=5, pady=2)

            tk.Label(frame_datos, text="Nombre:").grid(row=0, column=2, sticky="e", padx=5, pady=2)
            self.entry_nombre = tk.Entry(frame_datos)
            self.entry_nombre.grid(row=0, column=3, padx=5, pady=2)

            tk.Label(frame_datos, text="Email:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
            self.entry_email = tk.Entry(frame_datos)
            self.entry_email.grid(row=1, column=1, padx=5, pady=2)

            tk.Label(frame_datos, text="Teléfono:").grid(row=1, column=2, sticky="e", padx=5, pady=2)
            self.entry_telefono = tk.Entry(frame_datos)
            self.entry_telefono.grid(row=1, column=3, padx=5, pady=2)

            tk.Label(frame_datos, text="Dirección:").grid(row=2, column=0, sticky="e", padx=5, pady=2)
            self.entry_direccion = tk.Entry(frame_datos)
            self.entry_direccion.grid(row=2, column=1, padx=5, pady=2)

            tk.Label(frame_datos, text="Tipo:").grid(row=2, column=2, sticky="e", padx=5, pady=2)
            self.combo_tipo = ttk.Combobox(
                frame_datos, values=["Regular", "Premium", "Corporativo"], state="readonly"
            )
            self.combo_tipo.grid(row=2, column=3, padx=5, pady=2)
            self.combo_tipo.set("Regular")
            self.combo_tipo.bind("<<ComboboxSelected>>", self._actualizar_campo_extra)

            self.label_extra = tk.Label(frame_datos, text="Puntos:")
            self.label_extra.grid(row=3, column=0, sticky="e", padx=5, pady=2)
            self.entry_extra = tk.Entry(frame_datos)
            self.entry_extra.grid(row=3, column=1, padx=5, pady=2)

            # --- Frame de botones CRUD ---
            frame_botones = tk.Frame(self.root)
            frame_botones.pack(padx=10, pady=5)

            tk.Button(frame_botones, text="Agregar", command=self._agregar).pack(side="left", padx=5)
            tk.Button(frame_botones, text="Buscar", command=self._buscar).pack(side="left", padx=5)
            tk.Button(frame_botones, text="Actualizar", command=self._actualizar).pack(side="left", padx=5)
            tk.Button(frame_botones, text="Eliminar", command=self._eliminar).pack(side="left", padx=5)
            tk.Button(frame_botones, text="Limpiar", command=self._limpiar).pack(side="left", padx=5)

            # --- Tabla de clientes ---
            self.tabla = ttk.Treeview(
                self.root,
                columns=("ID", "Nombre", "Email", "Teléfono", "Dirección", "Tipo", "Descuento"),
                show="headings"
            )
            for col in ("ID", "Nombre", "Email", "Teléfono", "Dirección", "Tipo", "Descuento"):
                self.tabla.heading(col, text=col)
                self.tabla.column(col, width=100)
            self.tabla.pack(padx=10, pady=5, fill="both", expand=True)
            self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila)

            # --- Frame de botones de archivos ---
            frame_archivos = tk.Frame(self.root)
            frame_archivos.pack(padx=10, pady=5)

            tk.Button(frame_archivos, text="Guardar JSON", command=self._guardar_json).pack(side="left", padx=5)
            tk.Button(frame_archivos, text="Cargar JSON", command=self._cargar_json).pack(side="left", padx=5)
            tk.Button(frame_archivos, text="Exportar CSV", command=self._exportar_csv).pack(side="left", padx=5)

        def _actualizar_campo_extra(self, event=None):
            tipo = self.combo_tipo.get()
            if tipo == "Regular":
                self.label_extra.config(text="Puntos:")
                self.entry_extra.config(state="normal")
            elif tipo == "Corporativo":
                self.label_extra.config(text="Empresa:")
                self.entry_extra.config(state="normal")
            else:
                self.label_extra.config(text="(N/A):")
                self.entry_extra.delete(0, tk.END)
                self.entry_extra.config(state="disabled")

        def _validar_campos(self):
            if not self.entry_id.get().strip():
                raise ValueError("El campo ID es obligatorio")
            try:
                int(self.entry_id.get().strip())
            except ValueError:
                raise ValueError("El ID debe ser un número entero")
            if not self.entry_nombre.get().strip():
                raise ValueError("El campo Nombre es obligatorio")

        def _agregar(self):
            try:
                self._validar_campos()
                id_cliente = int(self.entry_id.get().strip())
                nombre = self.entry_nombre.get().strip()
                email = self.entry_email.get().strip()
                telefono = self.entry_telefono.get().strip()
                direccion = self.entry_direccion.get().strip()
                tipo = self.combo_tipo.get()
                extra = self.entry_extra.get().strip()

                if tipo == "Regular":
                    puntos = int(extra) if extra else 0
                    cliente = ClienteRegular(id_cliente, nombre, email, telefono, direccion, puntos)
                elif tipo == "Premium":
                    cliente = ClientePremium(id_cliente, nombre, email, telefono, direccion)
                elif tipo == "Corporativo":
                    cliente = ClienteCorporativo(id_cliente, nombre, email, telefono, direccion, extra)
                else:
                    raise ValueError("Seleccione un tipo de cliente")

                self.gestor.agregar(cliente)
                self._actualizar_tabla()
                self._limpiar()
                messagebox.showinfo("Éxito", "Cliente agregado correctamente")
            except (ValueError, ClienteDuplicadoError) as e:
                messagebox.showerror("Error", str(e))

        def _buscar(self):
            try:
                if not self.entry_id.get().strip():
                    raise ValueError("Ingrese un ID para buscar")
                id_cliente = int(self.entry_id.get().strip())
                cliente = self.gestor.buscar(id_cliente)
                self._mostrar_cliente(cliente)
            except (ValueError, ClienteNoEncontradoError) as e:
                messagebox.showerror("Error", str(e))

        def _actualizar(self):
            try:
                self._validar_campos()
                id_cliente = int(self.entry_id.get().strip())
                campos = {}
                nombre = self.entry_nombre.get().strip()
                if nombre:
                    campos["nombre"] = nombre
                email = self.entry_email.get().strip()
                if email:
                    campos["email"] = email
                telefono = self.entry_telefono.get().strip()
                if telefono:
                    campos["telefono"] = telefono
                direccion = self.entry_direccion.get().strip()
                if direccion:
                    campos["direccion"] = direccion

                self.gestor.actualizar(id_cliente, **campos)
                self._actualizar_tabla()
                self._limpiar()
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
            except (ValueError, ClienteNoEncontradoError) as e:
                messagebox.showerror("Error", str(e))

        def _eliminar(self):
            try:
                if not self.entry_id.get().strip():
                    raise ValueError("Ingrese un ID para eliminar")
                id_cliente = int(self.entry_id.get().strip())
                self.gestor.eliminar(id_cliente)
                self._actualizar_tabla()
                self._limpiar()
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
            except (ValueError, ClienteNoEncontradoError) as e:
                messagebox.showerror("Error", str(e))

        def _limpiar(self):
            self.entry_id.delete(0, tk.END)
            self.entry_nombre.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            self.entry_telefono.delete(0, tk.END)
            self.entry_direccion.delete(0, tk.END)
            self.combo_tipo.set("Regular")
            self.entry_extra.config(state="normal")
            self.entry_extra.delete(0, tk.END)
            self._actualizar_campo_extra()

        def _mostrar_cliente(self, cliente):
            self._limpiar()
            self.entry_id.insert(0, str(cliente.get_id()))
            self.entry_nombre.insert(0, cliente.get_nombre())
            self.entry_email.insert(0, cliente.get_email())
            self.entry_telefono.insert(0, cliente.get_telefono())
            self.entry_direccion.insert(0, cliente.get_direccion())
            self.combo_tipo.set(cliente.get_tipo())
            self._actualizar_campo_extra()
            if cliente.get_tipo() == "Regular":
                self.entry_extra.insert(0, str(cliente.get_puntos()))
            elif cliente.get_tipo() == "Corporativo":
                self.entry_extra.insert(0, cliente.get_empresa())

        def _seleccionar_fila(self, event=None):
            seleccion = self.tabla.selection()
            if seleccion:
                valores = self.tabla.item(seleccion[0], "values")
                id_cliente = int(valores[0])
                try:
                    cliente = self.gestor.buscar(id_cliente)
                    self._mostrar_cliente(cliente)
                except ClienteNoEncontradoError:
                    pass

        def _actualizar_tabla(self):
            for row in self.tabla.get_children():
                self.tabla.delete(row)
            for c in self.gestor.listar():
                self.tabla.insert("", "end", values=(
                    c.get_id(), c.get_nombre(), c.get_email(),
                    c.get_telefono(), c.get_direccion(),
                    c.get_tipo(), f"{c.calcular_descuento()}%"
                ))

        def _guardar_json(self):
            try:
                ruta = filedialog.asksaveasfilename(
                    defaultextension=".json",
                    filetypes=[("JSON", "*.json")]
                )
                if ruta:
                    self.gestor.guardar_json(ruta)
                    messagebox.showinfo("Éxito", "Datos guardados en JSON")
            except PersistenciaError as e:
                messagebox.showerror("Error", str(e))

        def _cargar_json(self):
            try:
                ruta = filedialog.askopenfilename(
                    filetypes=[("JSON", "*.json")]
                )
                if ruta:
                    self.gestor.cargar_json(ruta)
                    self._actualizar_tabla()
                    messagebox.showinfo("Éxito", "Datos cargados desde JSON")
            except PersistenciaError as e:
                messagebox.showerror("Error", str(e))

        def _exportar_csv(self):
            try:
                ruta = filedialog.asksaveasfilename(
                    defaultextension=".csv",
                    filetypes=[("CSV", "*.csv")]
                )
                if ruta:
                    self.gestor.exportar_csv(ruta)
                    messagebox.showinfo("Éxito", "Datos exportados a CSV")
            except PersistenciaError as e:
                messagebox.showerror("Error", str(e))

except ImportError:
    AplicacionClientes = None