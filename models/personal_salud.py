"""
models/personal_salud.py
Modelo de dominio para la tabla `personal_salud`.

Principios aplicados:
  - Encapsulamiento : datos de contacto protegidos.
  - SRP             : representa únicamente un miembro del personal médico.
  - Herencia        : extiende BaseModel.
"""

from typing import Any, Dict, Optional
from models.base_model import BaseModel


class PersonalSalud(BaseModel):
    """Representa un miembro del personal de salud escolar."""

    def __init__(
        self,
        nombre:       str,
        apellido:     str,
        especialidad: str,
        matricula:    Optional[str] = None,
        telefono:     Optional[str] = None,
        email:        Optional[str] = None,
        id:           Optional[int] = None,
        activo:       int = 1,
        creado_en:    Optional[str] = None,
    ) -> None:
        super().__init__(id, creado_en)
        self._nombre       = nombre
        self._apellido     = apellido
        self._especialidad = especialidad
        self._matricula    = matricula
        self._telefono     = telefono
        self._email        = email
        self._activo       = bool(activo)

    # ── Propiedades ───────────────────────────────────────────────────────────

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def apellido(self) -> str:
        return self._apellido

    @property
    def nombre_completo(self) -> str:
        return f"{self._nombre} {self._apellido}"

    @property
    def especialidad(self) -> str:
        return self._especialidad

    @especialidad.setter
    def especialidad(self, v: str) -> None:
        if not v or not v.strip():
            raise ValueError("La especialidad no puede estar vacía.")
        self._especialidad = v.strip()

    @property
    def matricula(self) -> Optional[str]:
        return self._matricula

    @property
    def telefono(self) -> Optional[str]:
        return self._telefono

    @property
    def email(self) -> Optional[str]:
        return self._email

    @property
    def activo(self) -> bool:
        return self._activo

    # ── Contrato BaseModel ────────────────────────────────────────────────────

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":           self._id,
            "nombre":       self._nombre,
            "apellido":     self._apellido,
            "especialidad": self._especialidad,
            "matricula":    self._matricula,
            "telefono":     self._telefono,
            "email":        self._email,
            "activo":       int(self._activo),
            "creado_en":    self._creado_en,
        }

    def validate(self) -> bool:
        if not self._nombre or not self._nombre.strip():
            raise ValueError("El nombre del personal es obligatorio.")
        if not self._apellido or not self._apellido.strip():
            raise ValueError("El apellido del personal es obligatorio.")
        if not self._especialidad or not self._especialidad.strip():
            raise ValueError("La especialidad es obligatoria.")
        if self._email and "@" not in self._email:
            raise ValueError("El email no tiene un formato válido.")
        return True

    def __repr__(self) -> str:
        return (f"<PersonalSalud id={self._id} "
                f"nombre='{self.nombre_completo}' "
                f"especialidad='{self._especialidad}'>")
