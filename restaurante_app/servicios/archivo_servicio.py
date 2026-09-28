import json
import os
from typing import List

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class ArchivoServicio:
    def __init__(self, carpeta_datos: str = "datos") -> None:
        self.carpeta_datos = carpeta_datos
        self.ruta_productos = os.path.join(self.carpeta_datos, "productos.json")
        self.ruta_usuarios = os.path.join(self.carpeta_datos, "usuarios.json")
        self.ruta_ventas = os.path.join(self.carpeta_datos, "ventas.json")

    def _leer_json(self, ruta: str) -> list:
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                contenido = json.load(archivo)
        except FileNotFoundError:
            print(f"No se encontró {ruta}, se inicia con la lista vacía.")
            return []
        except json.JSONDecodeError:
            print(f"El archivo {ruta} no tiene un formato válido, se ignora su contenido.")
            return []
        except PermissionError:
            print(f"No hay permisos para leer {ruta}.")
            return []

        if not isinstance(contenido, list):
            print(f"El contenido de {ruta} no es una lista válida.")
            return []
        return contenido

    def _escribir_json(self, ruta: str, datos: list) -> bool:
        try:
            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"No hay permisos para escribir {ruta}.")
            return False

    def cargar_productos(self) -> List[Producto]:
        productos: List[Producto] = []
        for registro in self._leer_json(self.ruta_productos):
            try:
                productos.append(Producto.desde_diccionario(registro))
            except KeyError as error:
                print(f"Se omitió un producto por faltar la clave {error}.")
            except ValueError as error:
                print(f"Se omitió un producto inválido: {error}")
        return productos

    def guardar_productos(self, productos: List[Producto]) -> bool:
        datos = [producto.a_diccionario() for producto in productos]
        return self._escribir_json(self.ruta_productos, datos)

    def cargar_usuarios(self) -> List[Usuario]:
        usuarios: List[Usuario] = []
        for registro in self._leer_json(self.ruta_usuarios):
            try:
                usuarios.append(Usuario.desde_diccionario(registro))
            except KeyError as error:
                print(f"Se omitió un usuario por faltar la clave {error}.")
            except ValueError as error:
                print(f"Se omitió un usuario inválido: {error}")
        return usuarios

    def cargar_ventas(self) -> List[Venta]:
        ventas: List[Venta] = []
        for registro in self._leer_json(self.ruta_ventas):
            try:
                ventas.append(Venta.desde_diccionario(registro))
            except KeyError as error:
                print(f"Se omitió una venta por faltar la clave {error}.")
            except ValueError as error:
                print(f"Se omitió una venta inválida: {error}")
        return ventas

    def guardar_ventas(self, ventas: List[Venta]) -> bool:
        datos = [venta.a_diccionario() for venta in ventas]
        return self._escribir_json(self.ruta_ventas, datos)
