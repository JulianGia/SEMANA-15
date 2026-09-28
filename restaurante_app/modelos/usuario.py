from typing import Dict, Any


class Usuario:
    def __init__(self, id_usuario: int, nombre: str, usuario: str, contrasena: str, rol: str) -> None:
        self.id_usuario = self._validar_id(id_usuario)
        self.nombre = self._validar_texto(nombre, "nombre")
        self.usuario = self._validar_texto(usuario, "usuario")
        self.contrasena = self._validar_texto(contrasena, "contraseña")
        self.rol = self._validar_texto(rol, "rol")

    @staticmethod
    def _validar_id(id_usuario: int) -> int:
        try:
            valor = int(id_usuario)
        except (TypeError, ValueError):
            raise ValueError("El id del usuario debe ser un número entero.")
        if valor <= 0:
            raise ValueError("El id del usuario debe ser mayor a cero.")
        return valor

    @staticmethod
    def _validar_texto(texto: str, campo: str) -> str:
        if not isinstance(texto, str) or not texto.strip():
            raise ValueError(f"El {campo} no puede estar vacío.")
        return texto.strip()

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> "Usuario":
        return cls(
            id_usuario=datos["id_usuario"],
            nombre=datos["nombre"],
            usuario=datos["usuario"],
            contrasena=datos["contrasena"],
            rol=datos["rol"],
        )

    def __str__(self) -> str:
        return f"[{self.id_usuario}] {self.nombre} - {self.rol}"
