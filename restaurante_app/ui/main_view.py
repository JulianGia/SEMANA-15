import tkinter as tk
from tkinter import ttk, messagebox

from modelos.usuario import Usuario
from ui import cargar_imagen
from servicios.restaurante_servicio import RestauranteServicio


class MainView(ttk.Frame):
    def __init__(self, contenedor: tk.Widget, restaurante_servicio: RestauranteServicio,
                 usuario_activo: Usuario, al_cerrar_sesion) -> None:
        super().__init__(contenedor, padding=10)
        self.restaurante_servicio = restaurante_servicio
        self.usuario_activo = usuario_activo
        self.al_cerrar_sesion = al_cerrar_sesion

        # se guardan como atributos para que Tkinter no las elimine
        self.logo = cargar_imagen("logo.png", 4)
        self.icono_productos = cargar_imagen("productos.png")
        self.icono_usuarios = cargar_imagen("usuarios.png")
        self.icono_ventas = cargar_imagen("ventas.png")
        self.icono_salir = cargar_imagen("salir.png")
        self.icono_registrar = cargar_imagen("registrar.png")

        self._construir_encabezado()
        self._construir_secciones()
        self._cargar_tabla_productos()
        self._cargar_tabla_usuarios()
        self._cargar_combos_venta()
        self._cargar_tabla_ventas()

    # ---------------- Encabezado ----------------
    def _construir_encabezado(self) -> None:
        encabezado = ttk.Frame(self)
        encabezado.pack(fill="x", pady=(0, 10))

        ttk.Label(encabezado, image=self.logo).pack(side="left", padx=(0, 8))
        ttk.Label(
            encabezado,
            text=f"Restaurante App — {self.usuario_activo.nombre} ({self.usuario_activo.rol})",
            font=("Segoe UI", 13, "bold"),
        ).pack(side="left")

        ttk.Button(encabezado, text=" Cerrar sesión", image=self.icono_salir, compound="left",
                   command=self.al_cerrar_sesion).pack(side="right")

    # ---------------- Secciones (pestañas) ----------------
    def _construir_secciones(self) -> None:
        self.secciones = ttk.Notebook(self)
        self.secciones.pack(fill="both", expand=True)

        self.pestana_productos = ttk.Frame(self.secciones, padding=10)
        self.pestana_usuarios = ttk.Frame(self.secciones, padding=10)

        self.pestana_ventas = ttk.Frame(self.secciones, padding=10)

        self.secciones.add(self.pestana_productos, text=" Productos", image=self.icono_productos, compound="left")
        self.secciones.add(self.pestana_usuarios, text=" Usuarios", image=self.icono_usuarios, compound="left")
        self.secciones.add(self.pestana_ventas, text=" Ventas", image=self.icono_ventas, compound="left")

        self._construir_seccion_productos()
        self._construir_seccion_usuarios()
        self._construir_seccion_ventas()

    # ---------------- Productos ----------------
    def _construir_seccion_productos(self) -> None:
        formulario = ttk.LabelFrame(self.pestana_productos, text="Datos del producto", padding=10)
        formulario.pack(fill="x")

        self.entrada_id = self._agregar_campo(formulario, "Código:", 0, 0)
        self.entrada_nombre = self._agregar_campo(formulario, "Nombre:", 0, 2)
        self.entrada_precio = self._agregar_campo(formulario, "Precio:", 1, 0)
        self.entrada_stock = self._agregar_campo(formulario, "Stock:", 1, 2)

        ttk.Label(formulario, text="Categoría:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.combo_categoria = ttk.Combobox(
            formulario,
            values=["Platos fuertes", "Bebidas", "Entradas", "Postres"],
            state="readonly",
            width=18,
        )
        self.combo_categoria.grid(row=2, column=1, padx=5, pady=5)
        self.combo_categoria.set("Platos fuertes")

        acciones = ttk.Frame(self.pestana_productos)
        acciones.pack(fill="x", pady=10)

        ttk.Button(acciones, text="Registrar", command=self._registrar_producto).pack(side="left", padx=4)
        ttk.Button(acciones, text="Cargar", command=self._cargar_producto).pack(side="left", padx=4)
        ttk.Button(acciones, text="Actualizar", command=self._actualizar_producto).pack(side="left", padx=4)
        ttk.Button(acciones, text="Eliminar", command=self._eliminar_producto).pack(side="left", padx=4)
        ttk.Button(acciones, text="Limpiar", command=self._limpiar_formulario).pack(side="left", padx=4)

        listado = ttk.LabelFrame(self.pestana_productos, text="Productos registrados", padding=10)
        listado.pack(fill="both", expand=True)

        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tabla_productos = ttk.Treeview(listado, columns=columnas, show="headings", height=8)
        for columna, titulo, ancho in [
            ("codigo", "Código", 70),
            ("nombre", "Nombre", 170),
            ("categoria", "Categoría", 130),
            ("precio", "Precio", 90),
            ("stock", "Stock", 70),
        ]:
            self.tabla_productos.heading(columna, text=titulo)
            self.tabla_productos.column(columna, width=ancho, anchor="center")

        barra = ttk.Scrollbar(listado, orient="vertical", command=self.tabla_productos.yview)
        self.tabla_productos.configure(yscrollcommand=barra.set)
        self.tabla_productos.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        self.mensaje = ttk.Label(self.pestana_productos, text="", foreground="green")
        self.mensaje.pack(anchor="w", pady=(8, 0))

    def _agregar_campo(self, contenedor: ttk.Widget, etiqueta: str, fila: int, columna: int) -> ttk.Entry:
        ttk.Label(contenedor, text=etiqueta).grid(row=fila, column=columna, sticky="e", padx=5, pady=5)
        entrada = ttk.Entry(contenedor, width=20)
        entrada.grid(row=fila, column=columna + 1, padx=5, pady=5)
        return entrada

    def _leer_formulario(self) -> tuple:
        return (
            self.entrada_id.get().strip(),
            self.entrada_nombre.get().strip(),
            self.entrada_precio.get().strip(),
            self.combo_categoria.get(),
            self.entrada_stock.get().strip(),
        )

    def _limpiar_formulario(self) -> None:
        for entrada in (self.entrada_id, self.entrada_nombre, self.entrada_precio, self.entrada_stock):
            entrada.delete(0, tk.END)
        self.combo_categoria.set("Platos fuertes")
        self.mensaje.config(text="")

    def _cargar_tabla_productos(self) -> None:
        for fila in self.tabla_productos.get_children():
            self.tabla_productos.delete(fila)
        for producto in self.restaurante_servicio.listar_productos():
            self.tabla_productos.insert(
                "",
                tk.END,
                values=(
                    producto.id_producto,
                    producto.nombre,
                    producto.categoria,
                    f"{producto.precio:.2f}",
                    producto.stock,
                ),
            )
        self._cargar_combos_venta()

    def _registrar_producto(self) -> None:
        id_producto, nombre, precio, categoria, stock = self._leer_formulario()
        if not id_producto or not nombre or not precio or not stock:
            messagebox.showwarning("Datos incompletos", "Complete todos los campos del formulario.")
            return
        try:
            self.restaurante_servicio.registrar_producto(id_producto, nombre, precio, categoria, stock)
            self._cargar_tabla_productos()
            self._limpiar_formulario()
            self.mensaje.config(text="Producto registrado correctamente.", foreground="green")
        except ValueError as error:
            messagebox.showerror("No se pudo registrar", str(error))

    def _cargar_producto(self) -> None:
        id_producto = self.entrada_id.get().strip()
        if not id_producto:
            messagebox.showwarning("Falta el código", "Ingrese el código del producto a consultar.")
            return
        try:
            producto = self.restaurante_servicio.buscar_producto(int(id_producto))
        except ValueError:
            messagebox.showerror("Código inválido", "El código debe ser un número entero.")
            return

        if producto is None:
            messagebox.showinfo("Sin resultados", "No existe un producto con ese código.")
            return

        self.entrada_nombre.delete(0, tk.END)
        self.entrada_nombre.insert(0, producto.nombre)
        self.entrada_precio.delete(0, tk.END)
        self.entrada_precio.insert(0, str(producto.precio))
        self.entrada_stock.delete(0, tk.END)
        self.entrada_stock.insert(0, str(producto.stock))
        self.combo_categoria.set(producto.categoria)
        self.mensaje.config(text="Producto cargado en el formulario.", foreground="blue")

    def _actualizar_producto(self) -> None:
        id_producto, nombre, precio, categoria, stock = self._leer_formulario()
        if not id_producto or not nombre or not precio or not stock:
            messagebox.showwarning("Datos incompletos", "Complete todos los campos del formulario.")
            return
        try:
            self.restaurante_servicio.actualizar_producto(id_producto, nombre, precio, categoria, stock)
            self._cargar_tabla_productos()
            self.mensaje.config(text="Producto actualizado correctamente.", foreground="green")
        except ValueError as error:
            messagebox.showerror("No se pudo actualizar", str(error))

    def _eliminar_producto(self) -> None:
        id_producto = self.entrada_id.get().strip()
        if not id_producto:
            messagebox.showwarning("Falta el código", "Ingrese el código del producto a eliminar.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar el producto {id_producto}?"):
            return
        try:
            self.restaurante_servicio.eliminar_producto(id_producto)
            self._cargar_tabla_productos()
            self._limpiar_formulario()
            self.mensaje.config(text="Producto eliminado correctamente.", foreground="green")
        except ValueError as error:
            messagebox.showerror("No se pudo eliminar", str(error))

    # ---------------- Usuarios ----------------
    def _construir_seccion_usuarios(self) -> None:
        listado = ttk.LabelFrame(self.pestana_usuarios, text="Usuarios registrados", padding=10)
        listado.pack(fill="both", expand=True)

        columnas = ("id", "nombre", "usuario", "rol")
        self.tabla_usuarios = ttk.Treeview(listado, columns=columnas, show="headings", height=10)
        for columna, titulo, ancho in [
            ("id", "Id", 60),
            ("nombre", "Nombre", 200),
            ("usuario", "Usuario", 140),
            ("rol", "Rol", 140),
        ]:
            self.tabla_usuarios.heading(columna, text=titulo)
            self.tabla_usuarios.column(columna, width=ancho, anchor="center")
        self.tabla_usuarios.pack(fill="both", expand=True)

        ttk.Button(self.pestana_usuarios, text="Actualizar listado",
                   command=self._cargar_tabla_usuarios).pack(anchor="w", pady=8)

    def _cargar_tabla_usuarios(self) -> None:
        for fila in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(fila)
        for usuario in self.restaurante_servicio.listar_usuarios():
            self.tabla_usuarios.insert(
                "", tk.END,
                values=(usuario.id_usuario, usuario.nombre, usuario.usuario, usuario.rol),
            )

    # ---------------- Ventas ----------------
    def _construir_seccion_ventas(self) -> None:
        formulario = ttk.LabelFrame(self.pestana_ventas, text="Nueva venta", padding=10)
        formulario.pack(fill="x")

        ttk.Label(formulario, text="Usuario:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.combo_usuario_venta = ttk.Combobox(formulario, state="readonly", width=28)
        self.combo_usuario_venta.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Producto:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.combo_producto_venta = ttk.Combobox(formulario, state="readonly", width=28)
        self.combo_producto_venta.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Cantidad:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entrada_cantidad_venta = ttk.Spinbox(formulario, from_=1, to=100, width=8)
        self.entrada_cantidad_venta.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.entrada_cantidad_venta.set(1)

        # command= recibe la función sin paréntesis: se ejecuta cuando se presiona el botón
        ttk.Button(formulario, text=" Registrar venta", image=self.icono_registrar, compound="left",
                   command=self._registrar_venta).grid(row=3, column=1, sticky="w", padx=5, pady=(10, 0))

        listado = ttk.LabelFrame(self.pestana_ventas, text="Ventas registradas", padding=10)
        listado.pack(fill="both", expand=True, pady=(10, 0))

        columnas = ("fecha", "usuario", "producto", "cantidad")
        self.tabla_ventas = ttk.Treeview(listado, columns=columnas, show="headings", height=8)
        for columna, titulo, ancho in [
            ("fecha", "Fecha", 130),
            ("usuario", "Usuario", 170),
            ("producto", "Producto", 170),
            ("cantidad", "Cantidad", 80),
        ]:
            self.tabla_ventas.heading(columna, text=titulo)
            self.tabla_ventas.column(columna, width=ancho, anchor="center")

        barra = ttk.Scrollbar(listado, orient="vertical", command=self.tabla_ventas.yview)
        self.tabla_ventas.configure(yscrollcommand=barra.set)
        self.tabla_ventas.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        self.mensaje_venta = ttk.Label(self.pestana_ventas, text="")
        self.mensaje_venta.pack(anchor="w", pady=(8, 0))

    def _cargar_combos_venta(self) -> None:
        self.combo_usuario_venta["values"] = [
            f"{u.id_usuario} - {u.nombre}" for u in self.restaurante_servicio.listar_usuarios()
        ]
        self.combo_producto_venta["values"] = [
            f"{p.id_producto} - {p.nombre}" for p in self.restaurante_servicio.listar_productos()
        ]

    def _cargar_tabla_ventas(self) -> None:
        for fila in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(fila)
        for venta in self.restaurante_servicio.listar_ventas():
            usuario = self.restaurante_servicio.buscar_usuario(venta.id_usuario)
            producto = self.restaurante_servicio.buscar_producto(venta.id_producto)
            self.tabla_ventas.insert(
                "", tk.END,
                values=(
                    venta.fecha,
                    usuario.nombre if usuario else "(usuario eliminado)",
                    producto.nombre if producto else "(producto eliminado)",
                    venta.cantidad,
                ),
            )

    def _registrar_venta(self) -> None:
        """Callback del botón 'Registrar venta': toma los datos, se los pasa al servicio y actualiza la vista."""
        usuario_elegido = self.combo_usuario_venta.get()
        producto_elegido = self.combo_producto_venta.get()

        if not usuario_elegido or not producto_elegido:
            messagebox.showwarning("Datos incompletos", "Seleccione un usuario y un producto.")
            return

        try:
            id_usuario = int(usuario_elegido.split(" - ")[0])
            id_producto = int(producto_elegido.split(" - ")[0])
            self.restaurante_servicio.registrar_venta(
                id_usuario, id_producto, self.entrada_cantidad_venta.get()
            )
        except ValueError as error:
            messagebox.showerror("No se pudo registrar la venta", str(error))
            return

        self._cargar_tabla_ventas()
        self._cargar_tabla_productos()  # el stock cambió
        self.entrada_cantidad_venta.set(1)
        self.mensaje_venta.config(text="Venta registrada correctamente.", foreground="green")
