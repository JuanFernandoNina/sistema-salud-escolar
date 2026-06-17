"""
models/reclamo.py
Modelo de dominio para la tabla `reclamos`.

Principios aplicados:
  - Encapsulamiento : estado y respuesta protegidos con lógica de transición.
  - SRP             : representa únicamente un reclamo de estudiante.
  - Herencia        : extiende BaseModel.
"""

from typing import Any, Dict, Optional
from models.base_model import BaseModel


class Reclamo(BaseModel):
    """Representa un reclamo enviado por un estudiante."""

    ESTADOS = ("pendiente", "en_revision", "resuelto", "rechazado")

    def __init__(
        self,
        estudiante_id: int,
        asunto:        str,
        descripcion:   str,
        estado:        str  = "pendiente",
        respuesta:     Optional[str] = None,
        resuelto_en:   Optional[str] = None,
        id:            Optional[int] = None,
        creado_en:     Optional[str] = None,
    ) -> None:
        super().__init__(id, creado_en)
        self._estudiante_id = estudiante_id
        self._asunto        = asunto
        self._descripcion   = descripcion
        self._estado        = estado
        self._respuesta     = respuesta
        self._resuelto_en   = resuelto_en

    # ── Propiedades ───────────────────────────────────────────────────────────

    @property
    def estudiante_id(self) -> int:
        return self._estudiante_id

    @property
    def asunto(self) -> str:
        return self._asunto

    @asunto.setter
    def asunto(self, v: str) -> None:
        if not v or not v.strip():
            raise ValueError("El asunto no puede estar vacío.")
        self._asunto = v.strip()

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, v: str) -> None:
        if not v or not v.strip():
            raise ValueError("La descripción no puede estar vacía.")
        self._descripcion = v.strip()

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, v: str) -> None:
        if v not in self.ESTADOS:
            raise ValueError(f"Estado inválido. Opciones: {self.ESTADOS}")
        self._estado = v

    @property
    def respuesta(self) -> Optional[str]:
        return self._respuesta

    @respuesta.setter
    def respuesta(self, v: str) -> None:
        self._respuesta = v

    @property
    def resuelto_en(self) -> Optional[str]:
        return self._resuelto_en

    # ── Contrato BaseModel ────────────────────────────────────────────────────

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":            self._id,
            "estudiante_id": self._estudiante_id,
            "asunto":        self._asunto,
            "descripcion":   self._descripcion,
            "estado":        self._estado,
            "respuesta":     self._respuesta,
            "resuelto_en":   self._resuelto_en,
            "creado_en":     self._creado_en,
        }

    def validate(self) -> bool:
        if not self._estudiante_id:
            raise ValueError("El ID del estudiante es obligatorio.")
        if not self._asunto or not self._asunto.strip():
            raise ValueError("El asunto del reclamo es obligatorio.")
        if not self._descripcion or not self._descripcion.strip():
            raise ValueError("La descripción del reclamo es obligatoria.")
        if self._estado not in self.ESTADOS:
            raise ValueError(f"Estado inválido: {self._estado}")
        return True

    # ── Helpers ───────────────────────────────────────────────────────────────

    def esta_pendiente(self) -> bool:
        return self._estado == "pendiente"

    def esta_resuelto(self) -> bool:
        return self._estado == "resuelto"

    def __repr__(self) -> str:
        return (f"<Reclamo id={self._id} "
                f"estudiante={self._estudiante_id} "
                f"estado='{self._estado}'>")
