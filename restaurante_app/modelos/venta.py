from datetime import datetime
from typing import Dict, Any, Optional


class Venta:
    def __init__(self, id_usuario: int, id_producto: int, cantidad: int, fecha: Optional[str] = None) -> None:
        self.id_usuario = id_usuario
        self.id_producto = id_producto
        self.cantidad = self._validar_cantidad(cantidad)
        self.fecha = fecha if fecha else datetime.now().strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def _validar_cantidad(cantidad: int) -> int:
        try:
            valor = int(cantidad)
        except (TypeError, ValueError):
            raise ValueError("La cantidad debe ser un número entero.")
        if valor <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        return valor

    def a_diccionario(self) -> Dict[str, Any]:
        return {
            "id_usuario": self.id_usuario,
            "id_producto": self.id_producto,
            "cantidad": self.cantidad,
            "fecha": self.fecha,
        }

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> "Venta":
        return cls(
            id_usuario=datos["id_usuario"],
            id_producto=datos["id_producto"],
            cantidad=datos["cantidad"],
            fecha=datos["fecha"],
        )
