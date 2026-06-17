"""
services/reclamo_service.py
Lógica de negocio para reclamos de estudiantes.
"""

from typing import Any, Dict, List, Optional
from services.base_service import BaseService
from database.repositories.reclamo_repository import ReclamoRepository
from models.reclamo import Reclamo
import logging

logger = logging.getLogger(__name__)


class ReclamoService(BaseService[Reclamo]):

    def __init__(self) -> None:
        super().__init__()
        self._repo = ReclamoRepository()

    def crear(self, datos: Dict[str, Any]) -> Reclamo:
        reclamo = Reclamo(
            estudiante_id=datos["estudiante_id"],
            asunto=datos["asunto"],
            descripcion=datos["descripcion"],
            estado="pendiente",
        )
        return self._repo.guardar(reclamo)

    def actualizar(self, id: int, datos: Dict[str, Any]) -> Reclamo:
        reclamo = self._repo.obtener_por_id(id)
        if not reclamo:
            raise ValueError(f"Reclamo id={id} no encontrado.")
        for campo in ("asunto", "descripcion", "estado", "respuesta"):
            if campo in datos:
                reclamo.__dict__[f"_{campo}"] = datos[campo]
        return self._repo.guardar(reclamo)

    def eliminar(self, id: int) -> bool:
        if not self._repo.existe(id):
            raise ValueError(f"Reclamo id={id} no encontrado.")
        return self._repo.eliminar(id)

    def obtener_por_id(self, id: int) -> Optional[Reclamo]:
        return self._repo.obtener_por_id(id)

    def obtener_todos(self) -> List[Reclamo]:
        return self._repo.obtener_todos()

    # ── Métodos específicos ───────────────────────────────────────────────────

    def obtener_por_estudiante(self, estudiante_id: int) -> List[Reclamo]:
        return self._repo.obtener_por_estudiante(estudiante_id)

    def obtener_pendientes(self) -> List[Reclamo]:
        return self._repo.obtener_pendientes()

    def resolver(self, id: int, respuesta: str) -> bool:
        if not respuesta or not respuesta.strip():
            raise ValueError("La respuesta no puede estar vacía.")
        return self._repo.resolver(id, respuesta)

    def rechazar(self, id: int) -> bool:
        reclamo = self._repo.obtener_por_id(id)
        if not reclamo:
            raise ValueError(f"Reclamo id={id} no encontrado.")
        reclamo._estado = "rechazado"
        self._repo.guardar(reclamo)
        return True
