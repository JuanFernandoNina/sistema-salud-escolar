"""
services/alerta_service.py
Detección automática de riesgos de salud (RF05).

Reglas implementadas:
  R1 — Bajo peso en 2+ controles consecutivos.
  R2 — Variación brusca de peso (>5 kg entre controles).
  R3 — Sin crecimiento de talla en 3+ controles consecutivos.
  R4 — Observaciones negativas repetidas (>= 2 con la misma palabra clave).
  R5 — Estado nutricional fuera de normal (sobrepeso / obesidad).
"""

from typing import Any, Dict, List
from database.repositories.control_salud_repository import ControlSaludRepository
from database.repositories.estudiante_repository import EstudianteRepository
from models.control_salud import ControlSalud
import logging

logger = logging.getLogger(__name__)

# Palabras clave que indican observación negativa
PALABRAS_NEGATIVAS = (
    "dolor", "fiebre", "vomito", "vómito", "diarrea",
    "infección", "infeccion", "malestar", "ausente", "débil", "debil",
)


class AlertaService:
    """Evalúa el historial de controles y genera alertas automáticas (RF05)."""

    def __init__(self) -> None:
        self._control_repo   = ControlSaludRepository()
        self._estudiante_repo = EstudianteRepository()

    # ── API pública ───────────────────────────────────────────────────────────

    def obtener_alertas_estudiante(
        self, estudiante_id: int
    ) -> List[Dict[str, Any]]:
        """
        Evalúa el historial de un estudiante y retorna lista de alertas.
        Cada alerta: {"tipo": str, "mensaje": str, "nivel": "warning"|"danger"}
        """
        controles = self._control_repo.obtener_por_estudiante(estudiante_id)
        if not controles:
            return []

        alertas: List[Dict[str, Any]] = []
        alertas += self._regla_bajo_peso_consecutivo(controles)
        alertas += self._regla_variacion_brusca_peso(controles)
        alertas += self._regla_sin_crecimiento(controles)
        alertas += self._regla_observaciones_negativas(controles)
        alertas += self._regla_estado_nutricional(controles[-1])
        return alertas

    def obtener_alertas_todos(self) -> List[Dict[str, Any]]:
        """
        Evalúa TODOS los estudiantes activos y retorna alertas con
        el nombre del estudiante incluido.
        """
        estudiantes = self._estudiante_repo.obtener_todos()
        resultado = []
        for est in estudiantes:
            alertas = self.obtener_alertas_estudiante(est.id)
            for a in alertas:
                a["estudiante_id"]   = est.id
                a["estudiante_nombre"] = est.nombre_completo
                resultado.append(a)
        return resultado

    def contar_alertas_activas(self) -> int:
        return len(self.obtener_alertas_todos())

    # ── Reglas de detección (RF05) ────────────────────────────────────────────

    def _regla_bajo_peso_consecutivo(
        self, controles: List[ControlSalud]
    ) -> List[Dict]:
        """R1 — 2+ controles consecutivos con estado 'Bajo peso'."""
        alertas = []
        consecutivos = 0
        for c in controles:
            if c.estado_nutricional == "Bajo peso":
                consecutivos += 1
                if consecutivos >= 2:
                    alertas.append({
                        "tipo":    "bajo_peso_consecutivo",
                        "mensaje": (
                            f"Bajo peso detectado en {consecutivos} "
                            "controles consecutivos."
                        ),
                        "nivel": "danger",
                    })
                    break
            else:
                consecutivos = 0
        return alertas

    def _regla_variacion_brusca_peso(
        self, controles: List[ControlSalud]
    ) -> List[Dict]:
        """R2 — Variación de peso > 5 kg entre dos controles consecutivos."""
        alertas = []
        for i in range(1, len(controles)):
            delta = abs(controles[i].peso_kg - controles[i - 1].peso_kg)
            if delta > 5:
                alertas.append({
                    "tipo":    "variacion_brusca_peso",
                    "mensaje": (
                        f"Variación brusca de peso: {delta:.1f} kg entre "
                        f"{controles[i-1].fecha_control} y "
                        f"{controles[i].fecha_control}."
                    ),
                    "nivel": "warning",
                })
        return alertas

    def _regla_sin_crecimiento(
        self, controles: List[ControlSalud]
    ) -> List[Dict]:
        """R3 — Talla sin cambio en 3+ controles consecutivos."""
        alertas = []
        if len(controles) < 3:
            return alertas
        sin_cambio = 1
        for i in range(1, len(controles)):
            if abs(controles[i].talla_m - controles[i - 1].talla_m) < 0.001:
                sin_cambio += 1
                if sin_cambio >= 3:
                    alertas.append({
                        "tipo":    "sin_crecimiento_talla",
                        "mensaje": (
                            f"Sin crecimiento de talla en {sin_cambio} "
                            "controles consecutivos."
                        ),
                        "nivel": "warning",
                    })
                    break
            else:
                sin_cambio = 1
        return alertas

    def _regla_observaciones_negativas(
        self, controles: List[ControlSalud]
    ) -> List[Dict]:
        """R4 — 2+ controles con observaciones negativas (palabras clave)."""
        alertas = []
        conteo = sum(
            1 for c in controles
            if c.observaciones and any(
                p in c.observaciones.lower() for p in PALABRAS_NEGATIVAS
            )
        )
        if conteo >= 2:
            alertas.append({
                "tipo":    "observaciones_negativas",
                "mensaje": (
                    f"Se registraron {conteo} controles con "
                    "observaciones negativas repetidas."
                ),
                "nivel": "warning",
            })
        return alertas

    def _regla_estado_nutricional(
        self, ultimo: ControlSalud
    ) -> List[Dict]:
        """R5 — Último control con sobrepeso u obesidad."""
        alertas = []
        if ultimo.estado_nutricional in ("Sobrepeso", "Obesidad"):
            alertas.append({
                "tipo":    "estado_nutricional",
                "mensaje": (
                    f"Estado nutricional actual: {ultimo.estado_nutricional} "
                    f"(IMC={ultimo.imc})."
                ),
                "nivel": "warning" if ultimo.estado_nutricional == "Sobrepeso"
                          else "danger",
            })
        return alertas
