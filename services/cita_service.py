"""
services/cita_service.py
Lógica de negocio para gestión de citas médicas.
"""

from typing import Any, Dict, List, Optional
from datetime import date
from services.base_service import BaseService
from database.repositories.cita_repository import CitaRepository
from models.cita import Cita
import logging

logger = logging.getLogger(__name__)


class CitaService(BaseService[Cita]):

    def __init__(self) -> None:
        super().__init__()
        self._repo = CitaRepository()

    def crear(self, datos: Dict[str, Any]) -> Cita:
        cita = Cita(
            estudiante_id=datos["estudiante_id"],
            motivo=datos["motivo"],
            fecha_cita=datos["fecha_cita"],
            hora_cita=datos.get("hora_cita", "08:00"),
            personal_id=datos.get("personal_id"),
            estado=datos.get("estado", "pendiente"),
            observaciones=datos.get("observaciones"),
        )
        return self._repo.guardar(cita)

    def actualizar(self, id: int, datos: Dict[str, Any]) -> Cita:
        cita = self._repo.obtener_por_id(id)
        if not cita:
            raise ValueError(f"Cita id={id} no encontrada.")
        for campo in ("motivo", "fecha_cita", "hora_cita",
                      "personal_id", "estado", "observaciones"):
            if campo in datos:
                cita.__dict__[f"_{campo}"] = datos[campo]
        return self._repo.guardar(cita)

    def eliminar(self, id: int) -> bool:
        if not self._repo.existe(id):
            raise ValueError(f"Cita id={id} no encontrada.")
        return self._repo.eliminar(id)

    def obtener_por_id(self, id: int) -> Optional[Cita]:
        return self._repo.obtener_por_id(id)

    def obtener_todos(self) -> List[Cita]:
        return self._repo.obtener_todos()

    # ── Métodos específicos ───────────────────────────────────────────────────

    def obtener_por_estudiante(self, estudiante_id: int) -> List[Cita]:
        return self._repo.obtener_por_estudiante(estudiante_id)

    def obtener_pendientes(self) -> List[Cita]:
        return self._repo.obtener_pendientes()

    def confirmar(self, id: int) -> bool:
        return self._repo.cambiar_estado(id, "confirmada")

    def realizar(self, id: int) -> bool:
        return self._repo.cambiar_estado(id, "realizada")

    def cancelar(self, id: int) -> bool:
        return self._repo.cambiar_estado(id, "cancelada")

    def obtener_por_fecha(self, fecha: str) -> List[Cita]:
        return self._repo.obtener_por_fecha(fecha)
