"""
models/control_salud.py
Modelo de dominio para la tabla `controles_salud`.
Incluye cálculo de IMC y clasificación nutricional (RF04).

Principios aplicados:
  - Encapsulamiento : IMC calculado internamente como propiedad.
  - SRP             : representa un control de salud y su lógica nutricional.
  - Herencia        : extiende BaseModel.
"""

from typing import Any, Dict, Optional
from models.base_model import BaseModel
from config.settings import (
    IMC_BAJO_PESO, IMC_NORMAL_MAX, IMC_SOBREPESO
)


class ControlSalud(BaseModel):
    """
    Representa un control periódico de salud de un estudiante.
    Calcula IMC y estado nutricional automáticamente.
    """

    def __init__(
        self,
        estudiante_id:     int,
        peso_kg:           float,
        talla_m:           float,
        fecha_control:     Optional[str] = None,
        personal_id:       Optional[int] = None,
        observaciones:     Optional[str] = None,
        id:                Optional[int] = None,
        creado_en:         Optional[str] = None,
        # Columnas calculadas de SQLite (se ignoran al crear, se usan al leer)
        imc:               Optional[float] = None,
        estado_nutricional: Optional[str]  = None,
    ) -> None:
        super().__init__(id, creado_en)
        self._estudiante_id  = estudiante_id
        self._personal_id    = personal_id
        self._fecha_control  = fecha_control
        self._peso_kg        = peso_kg
        self._talla_m        = talla_m
        self._observaciones  = observaciones

    # ── Propiedades ───────────────────────────────────────────────────────────

    @property
    def estudiante_id(self) -> int:
        return self._estudiante_id

    @property
    def personal_id(self) -> Optional[int]:
        return self._personal_id

    @property
    def fecha_control(self) -> Optional[str]:
        return self._fecha_control

    @property
    def peso_kg(self) -> float:
        return self._peso_kg

    @peso_kg.setter
    def peso_kg(self, v: float) -> None:
        if v <= 0:
            raise ValueError("El peso debe ser mayor a 0.")
        self._peso_kg = v

    @property
    def talla_m(self) -> float:
        return self._talla_m

    @talla_m.setter
    def talla_m(self, v: float) -> None:
        if v <= 0:
            raise ValueError("La talla debe ser mayor a 0.")
        self._talla_m = v

    @property
    def observaciones(self) -> Optional[str]:
        return self._observaciones

    # ── IMC y clasificación (RF04) ────────────────────────────────────────────

    @property
    def imc(self) -> float:
        """Calcula el IMC: peso / talla²"""
        return round(self._peso_kg / (self._talla_m ** 2), 2)

    @property
    def estado_nutricional(self) -> str:
        """Clasifica el estado nutricional según rangos del sistema."""
        imc = self.imc
        if imc < IMC_BAJO_PESO:
            return "Bajo peso"
        elif imc <= IMC_NORMAL_MAX:
            return "Normal"
        elif imc <= IMC_SOBREPESO:
            return "Sobrepeso"
        else:
            return "Obesidad"

    @property
    def tiene_riesgo(self) -> bool:
        """Retorna True si el estado nutricional no es Normal."""
        return self.estado_nutricional != "Normal"

    # ── Contrato BaseModel ────────────────────────────────────────────────────

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":                self._id,
            "estudiante_id":     self._estudiante_id,
            "personal_id":       self._personal_id,
            "fecha_control":     self._fecha_control,
            "peso_kg":           self._peso_kg,
            "talla_m":           self._talla_m,
            "imc":               self.imc,
            "estado_nutricional":self.estado_nutricional,
            "observaciones":     self._observaciones,
            "creado_en":         self._creado_en,
        }

    def validate(self) -> bool:
        if not self._estudiante_id:
            raise ValueError("El ID del estudiante es obligatorio.")
        if self._peso_kg <= 0:
            raise ValueError("El peso debe ser mayor a 0 kg.")
        if self._talla_m <= 0:
            raise ValueError("La talla debe ser mayor a 0 m.")
        if self._talla_m > 3.0:
            raise ValueError("La talla parece incorrecta (> 3m).")
        if self._peso_kg > 300:
            raise ValueError("El peso parece incorrecto (> 300kg).")
        return True

    def __repr__(self) -> str:
        return (f"<ControlSalud id={self._id} "
                f"estudiante={self._estudiante_id} "
                f"imc={self.imc} [{self.estado_nutricional}]>")
