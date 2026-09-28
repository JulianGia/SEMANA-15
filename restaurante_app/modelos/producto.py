from typing import Dict, Any


class Producto:
    def __init__(self, id_producto: int, nombre: str, precio: float, categoria: str, stock: int = 0) -> None:
        self.id_producto = self._validar_id(id_producto)
        self.nombre = self._validar_nombre(nombre)
        self.precio = self._validar_precio(precio)
        self.categoria = self._validar_categoria(categoria)
        self.stock = self._validar_stock(stock)

    @staticmethod
    def _validar_id(id_producto: int) -> int:
        try:
            valor = int(id_producto)
        except (TypeError, ValueError):
            raise ValueError("El id debe ser un número entero.")
        if valor <= 0:
            raise ValueError("El id debe ser mayor a cero.")
        return valor

    @staticmethod
    def _validar_nombre(nombre: str) -> str:
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        return nombre.strip()

    @staticmethod
    def _validar_precio(precio: float) -> float:
        try:
            valor = float(precio)
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser numérico.")
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        return valor

    @staticmethod
    def _validar_categoria(categoria: str) -> str:
        if not isinstance(categoria, str) or not categoria.strip():
            raise ValueError("La categoría no puede estar vacía.")
        return categoria.strip()

    @staticmethod
    def _validar_stock(stock: int) -> int:
        try:
            valor = int(stock)
        except (TypeError, ValueError):
            raise ValueError("El stock debe ser un número entero.")
        if valor < 0:
            raise ValueError("El stock no puede ser negativo.")
        return valor

    def a_diccionario(self) -> Dict[str, Any]:
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria,
            "stock": self.stock,
        }

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> "Producto":
        return cls(
            id_producto=datos["id_producto"],
            nombre=datos["nombre"],
            precio=datos["precio"],
            categoria=datos["categoria"],
            stock=datos.get("stock", 0),
        )

    def __str__(self) -> str:
        return f"[{self.id_producto}] {self.nombre} - {self.categoria} - ${self.precio:.2f} - Stock: {self.stock}"
