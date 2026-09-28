import tkinter as tk
from tkinter import ttk

from servicios.restaurante_servicio import RestauranteServicio
from ui import cargar_imagen


class LoginView(ttk.Frame):
    def __init__(self, contenedor: tk.Widget, restaurante_servicio: RestauranteServicio, al_ingresar) -> None:
        super().__init__(contenedor, padding=20)
        self.restaurante_servicio = restaurante_servicio
        self.al_ingresar = al_ingresar

        self.logo = cargar_imagen("logo.png", 2)
        ttk.Label(self, image=self.logo).grid(row=0, column=0, columnspan=2)
        ttk.Label(self, text="Restaurante App", font=("Segoe UI", 16, "bold")).grid(
            row=1, column=0, columnspan=2, pady=(5, 15)
        )

        ttk.Label(self, text="Usuario:").grid(row=2, column=0, sticky="e", pady=5)
        self.entrada_usuario = ttk.Entry(self)
        self.entrada_usuario.grid(row=2, column=1, pady=5)

        ttk.Label(self, text="Contraseña:").grid(row=3, column=0, sticky="e", pady=5)
        self.entrada_contrasena = ttk.Entry(self, show="*")
        self.entrada_contrasena.grid(row=3, column=1, pady=5)

        ttk.Button(self, text="Ingresar", command=self._intentar_ingresar).grid(
            row=4, column=0, columnspan=2, pady=15
        )

        self.mensaje = ttk.Label(self, text="", foreground="red")
        self.mensaje.grid(row=5, column=0, columnspan=2)

    def _intentar_ingresar(self) -> None:
        usuario = self.entrada_usuario.get().strip()
        contrasena = self.entrada_contrasena.get().strip()

        if not usuario or not contrasena:
            self.mensaje.config(text="Debe ingresar usuario y contraseña.")
            return

        usuario_valido = self.restaurante_servicio.validar_acceso(usuario, contrasena)
        if usuario_valido is None:
            self.mensaje.config(text="Usuario o contraseña incorrectos.")
            return

        self.mensaje.config(text="")
        self.entrada_contrasena.delete(0, tk.END)
        self.al_ingresar(usuario_valido)
