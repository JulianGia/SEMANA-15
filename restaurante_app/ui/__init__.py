import os
import tkinter as tk

CARPETA_ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")


def cargar_imagen(nombre: str, reducir: int = 1) -> tk.PhotoImage:
    imagen = tk.PhotoImage(file=os.path.join(CARPETA_ASSETS, nombre))
    return imagen.subsample(reducir) if reducir > 1 else imagen
