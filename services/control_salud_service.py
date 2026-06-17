"""
services/control_salud_service.py
Lógica de negocio para controles de salud (RF03, RF04, RF06).
"""

from typing import Any, Dict, List, Optional
from datetime import date
from services.base_service import BaseService
from database.repositories.control_salud_repository import ControlSaludRepository
from models.control_salud import ControlSalud
import logging

logger = logging.getLogger(__name__)


class ControlSaludService(BaseService[ControlSalud]):

    def __init__(self) -> None:
        super().__init__()
        self._repo = ControlSaludRepository()

    # ── Contrato BaseService ──────────────────────────────────────────────────

    def crear(self, datos: Dict[str, Any]) -> ControlSalud:
        control = ControlSalud(
            estudiante_id=datos["estudiante_id"],
            peso_kg=float(datos["peso_kg"]),
            talla_m=float(datos["talla_m"]),
            fecha_control=datos.get("fecha_control", date.today().isoformat()),
            personal_id=datos.get("personal_id"),
            observaciones=datos.get("observaciones"),
        )
        return self._repo.guardar(control)

    def actualizar(self, id: int, datos: Dict[str, Any]) -> ControlSalud:
        control = self._repo.obtener_por_id(id)
        if not control:
            raise ValueError(f"Control id={id} no encontrado.")
        for campo in ("peso_kg", "talla_m", "fecha_control",
                      "personal_id", "observaciones"):
            if campo in datos:
                control.__dict__[f"_{campo}"] = datos[campo]
        return self._repo.guardar(control)

    def eliminar(self, id: int) -> bool:
        if not self._repo.existe(id):
            raise ValueError(f"Control id={id} no encontrado.")
        return self._repo.eliminar(id)

    def obtener_por_id(self, id: int) -> Optional[ControlSalud]:
        return self._repo.obtener_por_id(id)

    def obtener_todos(self) -> List[ControlSalud]:
        return self._repo.obtener_todos()

    # ── Historial y evolución (RF06) ──────────────────────────────────────────

    def obtener_historial_estudiante(
        self, estudiante_id: int
    ) -> List[ControlSalud]:
        return self._repo.obtener_por_estudiante(estudiante_id)

    def obtener_ultimo_control(
        self, estudiante_id: int
    ) -> Optional[ControlSalud]:
        return self._repo.obtener_ultimo_por_estudiante(estudiante_id)

    def obtener_evolucion_nutricional(
        self, estudiante_id: int
    ) -> List[Dict[str, Any]]:
        """
        Retorna lista de dicts con fecha, peso, talla, imc y
        estado_nutricional — listos para graficar (RF06 + panel estudiante).
        """
        controles = self._repo.obtener_por_estudiante(estudiante_id)
        return [
            {
                "fecha":              c.fecha_control,
                "peso_kg":            c.peso_kg,
                "talla_m":            c.talla_m,
                "imc":                c.imc,
                "estado_nutricional": c.estado_nutricional,
            }
            for c in controles
        ]

    def obtener_por_rango_fecha(
        self, fecha_inicio: str, fecha_fin: str
    ) -> List[ControlSalud]:
        return self._repo.obtener_por_rango_fecha(fecha_inicio, fecha_fin)
