import tkinter as tk

from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class Aplicacion:
    def __init__(self) -> None:
        self.raiz = tk.Tk()
        self.raiz.title("Restaurante App")
        self.raiz.geometry("780x640")

        archivo_servicio = ArchivoServicio()
        self.restaurante_servicio = RestauranteServicio(archivo_servicio)

        self.vista_actual = None
        self.mostrar_login()

    def mostrar_login(self) -> None:
        if self.vista_actual is not None:
            self.vista_actual.destroy()
        self.vista_actual = LoginView(self.raiz, self.restaurante_servicio, self.mostrar_main)
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_main(self, usuario_activo) -> None:
        if self.vista_actual is not None:
            self.vista_actual.destroy()
        self.vista_actual = MainView(self.raiz, self.restaurante_servicio, usuario_activo, self.mostrar_login)
        self.vista_actual.pack(fill="both", expand=True)

    def ejecutar(self) -> None:
        self.raiz.mainloop()


def main() -> None:
    Aplicacion().ejecutar()


if __name__ == "__main__":
    main()
