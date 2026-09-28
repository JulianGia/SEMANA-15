from typing import List, Optional

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    def __init__(self, archivo_servicio: ArchivoServicio) -> None:
        self.archivo_servicio = archivo_servicio
        self._productos: List[Producto] = archivo_servicio.cargar_productos()
        self._usuarios: List[Usuario] = archivo_servicio.cargar_usuarios()
        self._ventas: List[Venta] = archivo_servicio.cargar_ventas()

    # ---------------- Acceso y usuarios ----------------
    def validar_acceso(self, usuario: str, contrasena: str) -> Optional[Usuario]:
        for u in self._usuarios:
            if u.usuario == usuario and u.contrasena == contrasena:
                return u
        return None

    def listar_usuarios(self) -> List[Usuario]:
        return list(self._usuarios)

    def buscar_usuario(self, id_usuario: int) -> Optional[Usuario]:
        for usuario in self._usuarios:
            if usuario.id_usuario == id_usuario:
                return usuario
        return None

    # ---------------- Productos ----------------
    def listar_productos(self) -> List[Producto]:
        return list(self._productos)

    def buscar_producto(self, id_producto: int) -> Optional[Producto]:
        for producto in self._productos:
            if producto.id_producto == id_producto:
                return producto
        return None

    def registrar_producto(self, id_producto: int, nombre: str, precio: float,
                           categoria: str, stock: int) -> Producto:
        if self.buscar_producto(self._convertir_id(id_producto)) is not None:
            raise ValueError(f"Ya existe un producto con el id {id_producto}.")

        producto = Producto(id_producto, nombre, precio, categoria, stock)
        self._productos.append(producto)
        self.archivo_servicio.guardar_productos(self._productos)
        return producto

    def actualizar_producto(self, id_producto: int, nombre: str, precio: float,
                            categoria: str, stock: int) -> Producto:
        producto = self.buscar_producto(self._convertir_id(id_producto))
        if producto is None:
            raise ValueError(f"No existe un producto con el id {id_producto}.")

        actualizado = Producto(producto.id_producto, nombre, precio, categoria, stock)
        self._productos[self._productos.index(producto)] = actualizado
        self.archivo_servicio.guardar_productos(self._productos)
        return actualizado

    def eliminar_producto(self, id_producto: int) -> bool:
        producto = self.buscar_producto(self._convertir_id(id_producto))
        if producto is None:
            raise ValueError(f"No existe un producto con el id {id_producto}.")

        self._productos.remove(producto)
        self.archivo_servicio.guardar_productos(self._productos)
        return True

    @staticmethod
    def _convertir_id(id_producto: int) -> int:
        try:
            return int(id_producto)
        except (TypeError, ValueError):
            raise ValueError("El id debe ser un número entero.")

    # ---------------- Ventas ----------------
    def listar_ventas(self) -> List[Venta]:
        return list(self._ventas)

    def registrar_venta(self, id_usuario: int, id_producto: int, cantidad: int) -> Venta:
        if self.buscar_usuario(id_usuario) is None:
            raise ValueError("El usuario seleccionado no existe.")

        producto = self.buscar_producto(id_producto)
        if producto is None:
            raise ValueError("El producto seleccionado no existe.")

        venta = Venta(id_usuario, id_producto, cantidad)
        if venta.cantidad > producto.stock:
            raise ValueError(f"Stock insuficiente: solo quedan {producto.stock} de {producto.nombre}.")

        producto.stock -= venta.cantidad
        self._ventas.append(venta)
        self.archivo_servicio.guardar_ventas(self._ventas)
        self.archivo_servicio.guardar_productos(self._productos)
        return venta
