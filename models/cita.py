"""
models/cita.py
Modelo de dominio para la tabla `citas`.

Principios aplicados:
  - Encapsulamiento : estado controlado con validación de transiciones.
  - SRP             : representa únicamente una cita médica.
  - Herencia        : extiende BaseModel.
"""

from typing import Any, Dict, Optional
from models.base_model import BaseModel


class Cita(BaseModel):
    """Representa una cita médica agendada para un estudiante."""

    ESTADOS = ("pendiente", "confirmada", "realizada", "cancelada")

    def __init__(
        self,
        estudiante_id:  int,
        motivo:         str,
        fecha_cita:     str,
        hora_cita:      str  = "08:00",
        personal_id:    Optional[int] = None,
        estado:         str  = "pendiente",
        observaciones:  Optional[str] = None,
        id:             Optional[int] = None,
        creado_en:      Optional[str] = None,
    ) -> None:
        super().__init__(id, creado_en)
        self._estudiante_id = estudiante_id
        self._personal_id   = personal_id
        self._fecha_cita    = fecha_cita
        self._hora_cita     = hora_cita
        self._motivo        = motivo
        self._estado        = estado
        self._observaciones = observaciones

    # ── Propiedades ───────────────────────────────────────────────────────────

    @property
    def estudiante_id(self) -> int:
        return self._estudiante_id

    @property
    def personal_id(self) -> Optional[int]:
        return self._personal_id

    @property
    def fecha_cita(self) -> str:
        return self._fecha_cita

    @property
    def hora_cita(self) -> str:
        return self._hora_cita

    @property
    def motivo(self) -> str:
        return self._motivo

    @motivo.setter
    def motivo(self, v: str) -> None:
        if not v or not v.strip():
            raise ValueError("El motivo no puede estar vacío.")
        self._motivo = v.strip()

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, v: str) -> None:
        if v not in self.ESTADOS:
            raise ValueError(f"Estado inválido. Opciones: {self.ESTADOS}")
        self._estado = v

    @property
    def observaciones(self) -> Optional[str]:
        return self._observaciones

    # ── Contrato BaseModel ────────────────────────────────────────────────────

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":            self._id,
            "estudiante_id": self._estudiante_id,
            "personal_id":   self._personal_id,
            "fecha_cita":    self._fecha_cita,
            "hora_cita":     self._hora_cita,
            "motivo":        self._motivo,
            "estado":        self._estado,
            "observaciones": self._observaciones,
            "creado_en":     self._creado_en,
        }

    def validate(self) -> bool:
        if not self._estudiante_id:
            raise ValueError("El ID del estudiante es obligatorio.")
        if not self._motivo or not self._motivo.strip():
            raise ValueError("El motivo de la cita es obligatorio.")
        if not self._fecha_cita:
            raise ValueError("La fecha de la cita es obligatoria.")
        if self._estado not in self.ESTADOS:
            raise ValueError(f"Estado inválido: {self._estado}")
        return True

    # ── Helpers ───────────────────────────────────────────────────────────────

    def esta_pendiente(self) -> bool:
        return self._estado == "pendiente"

    def esta_cancelada(self) -> bool:
        return self._estado == "cancelada"

    def __repr__(self) -> str:
        return (f"<Cita id={self._id} "
                f"estudiante={self._estudiante_id} "
                f"fecha='{self._fecha_cita}' estado='{self._estado}'>")
