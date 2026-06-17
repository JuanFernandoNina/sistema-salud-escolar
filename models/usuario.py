"""
models/usuario.py
Modelo de dominio para la tabla `usuarios`.

Principios aplicados:
  - Encapsulamiento : atributos privados con propiedades.
  - SRP             : solo representa un usuario del sistema.
  - Herencia        : extiende BaseModel e implementa su contrato.
"""

from typing import Any, Dict, Optional
from models.base_model import BaseModel


class Usuario(BaseModel):
    """Representa un usuario del sistema (admin o estudiante)."""

    ROLES = ("admin", "estudiante")

    def __init__(
        self,
        username: str,
        password_hash: str,
        rol: str,
        id: Optional[int] = None,
        activo: int = 1,
        creado_en: Optional[str] = None,
        ultimo_acceso: Optional[str] = None,
    ) -> None:
        super().__init__(id, creado_en)
        self._username      = username
        self._password_hash = password_hash
        self._rol           = rol
        self._activo        = bool(activo)
        self._ultimo_acceso = ultimo_acceso

    # ── Propiedades ───────────────────────────────────────────────────────────

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("El username no puede estar vacío.")
        self._username = value.strip()

    @property
    def password_hash(self) -> str:
        return self._password_hash

    @password_hash.setter
    def password_hash(self, value: str) -> None:
        self._password_hash = value

    @property
    def rol(self) -> str:
        return self._rol

    @rol.setter
    def rol(self, value: str) -> None:
        if value not in self.ROLES:
            raise ValueError(f"Rol inválido. Debe ser: {self.ROLES}")
        self._rol = value

    @property
    def activo(self) -> bool:
        return self._activo

    @activo.setter
    def activo(self, value: bool) -> None:
        self._activo = bool(value)

    @property
    def ultimo_acceso(self) -> Optional[str]:
        return self._ultimo_acceso

    @ultimo_acceso.setter
    def ultimo_acceso(self, value: str) -> None:
        self._ultimo_acceso = value

    # ── Contrato BaseModel ────────────────────────────────────────────────────

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":            self._id,
            "username":      self._username,
            "password_hash": self._password_hash,
            "rol":           self._rol,
            "activo":        int(self._activo),
            "creado_en":     self._creado_en,
            "ultimo_acceso": self._ultimo_acceso,
        }

    def validate(self) -> bool:
        if not self._username or not self._username.strip():
            raise ValueError("El username es obligatorio.")
        if not self._password_hash:
            raise ValueError("El hash de contraseña es obligatorio.")
        if self._rol not in self.ROLES:
            raise ValueError(f"Rol inválido: {self._rol}")
        return True

    # ── Helpers ───────────────────────────────────────────────────────────────

    def es_admin(self) -> bool:
        return self._rol == "admin"

    def es_estudiante(self) -> bool:
        return self._rol == "estudiante"

    def __repr__(self) -> str:
        return f"<Usuario id={self._id} username='{self._username}' rol='{self._rol}'>"
