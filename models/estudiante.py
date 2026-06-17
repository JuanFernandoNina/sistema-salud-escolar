"""
models/estudiante.py
Modelo de dominio para la tabla `estudiantes`.

Principios aplicados:
  - Encapsulamiento : atributos privados con propiedades y validaciones.
  - SRP             : representa únicamente un estudiante del sistema.
  - Herencia        : extiende BaseModel.
"""

from typing import Any, Dict, Optional
from models.base_model import BaseModel
from datetime import date


class Estudiante(BaseModel):
    """Representa un estudiante de la escuela primaria."""

    SEXOS  = ("M", "F")
    GRADOS = ("1ro", "2do", "3ro", "4to", "5to", "6to")

    def __init__(
        self,
        codigo_ruat:      str,
        nombre:           str,
        apellido:         str,
        fecha_nacimiento: str,
        sexo:             str,
        grado:            str,
        seccion:          str  = "A",
        direccion:        Optional[str] = None,
        telefono_tutor:   Optional[str] = None,
        nombre_tutor:     Optional[str] = None,
        usuario_id:       Optional[int] = None,
        id:               Optional[int] = None,
        activo:           int = 1,
        creado_en:        Optional[str] = None,
    ) -> None:
        super().__init__(id, creado_en)
        self._codigo_ruat      = codigo_ruat
        self._nombre           = nombre
        self._apellido         = apellido
        self._fecha_nacimiento = fecha_nacimiento
        self._sexo             = sexo
        self._grado            = grado
        self._seccion          = seccion
        self._direccion        = direccion
        self._telefono_tutor   = telefono_tutor
        self._nombre_tutor     = nombre_tutor
        self._usuario_id       = usuario_id
        self._activo           = bool(activo)

    # ── Propiedades ───────────────────────────────────────────────────────────

    @property
    def codigo_ruat(self) -> str:
        return self._codigo_ruat

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, v: str) -> None:
        if not v or not v.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = v.strip()

    @property
    def apellido(self) -> str:
        return self._apellido

    @apellido.setter
    def apellido(self, v: str) -> None:
        if not v or not v.strip():
            raise ValueError("El apellido no puede estar vacío.")
        self._apellido = v.strip()

    @property
    def nombre_completo(self) -> str:
        return f"{self._nombre} {self._apellido}"

    @property
    def fecha_nacimiento(self) -> str:
        return self._fecha_nacimiento

    @property
    def sexo(self) -> str:
        return self._sexo

    @property
    def grado(self) -> str:
        return self._grado

    @grado.setter
    def grado(self, v: str) -> None:
        if v not in self.GRADOS:
            raise ValueError(f"Grado inválido. Opciones: {self.GRADOS}")
        self._grado = v

    @property
    def seccion(self) -> str:
        return self._seccion

    @property
    def direccion(self) -> Optional[str]:
        return self._direccion

    @property
    def telefono_tutor(self) -> Optional[str]:
        return self._telefono_tutor

    @property
    def nombre_tutor(self) -> Optional[str]:
        return self._nombre_tutor

    @property
    def usuario_id(self) -> Optional[int]:
        return self._usuario_id

    @property
    def activo(self) -> bool:
        return self._activo

    # ── Contrato BaseModel ────────────────────────────────────────────────────

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":               self._id,
            "codigo_ruat":      self._codigo_ruat,
            "nombre":           self._nombre,
            "apellido":         self._apellido,
            "fecha_nacimiento": self._fecha_nacimiento,
            "sexo":             self._sexo,
            "grado":            self._grado,
            "seccion":          self._seccion,
            "direccion":        self._direccion,
            "telefono_tutor":   self._telefono_tutor,
            "nombre_tutor":     self._nombre_tutor,
            "usuario_id":       self._usuario_id,
            "activo":           int(self._activo),
            "creado_en":        self._creado_en,
        }

    def validate(self) -> bool:
        if not self._codigo_ruat:
            raise ValueError("El código RUAT es obligatorio.")
        if not self._nombre or not self._apellido:
            raise ValueError("Nombre y apellido son obligatorios.")
        if self._sexo not in self.SEXOS:
            raise ValueError(f"Sexo inválido. Debe ser M o F.")
        if self._grado not in self.GRADOS:
            raise ValueError(f"Grado inválido: {self._grado}")
        return True

    # ── Helpers ───────────────────────────────────────────────────────────────

    def calcular_edad(self) -> int:
        """Calcula la edad actual en años."""
        try:
            nacimiento = date.fromisoformat(self._fecha_nacimiento)
            hoy = date.today()
            return hoy.year - nacimiento.year - (
                (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day)
            )
        except Exception:
            return 0

    def __repr__(self) -> str:
        return (f"<Estudiante id={self._id} "
                f"ruat='{self._codigo_ruat}' "
                f"nombre='{self.nombre_completo}'>")
