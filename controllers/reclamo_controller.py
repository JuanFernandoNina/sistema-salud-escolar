"""
controllers/reclamo_controller.py
Controlador para reclamos de estudiantes.
"""

from typing import Any, Dict
from controllers.base_controller import BaseController
from services.reclamo_service import ReclamoService


class ReclamoController(BaseController):
    """Gestiona reclamos desde vistas estudiante y admin."""

    def __init__(self) -> None:
        super().__init__()
        self._service = ReclamoService()

    def crear_reclamo(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.crear(datos),
            message="Reclamo enviado correctamente.",
        )

    def actualizar_reclamo(self, reclamo_id: int, datos: Dict[str, Any]) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.actualizar(
                self._require_id(reclamo_id, "reclamo_id"), datos
            ),
            message="Reclamo actualizado correctamente.",
        )

    def eliminar_reclamo(self, reclamo_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.eliminar(self._require_id(reclamo_id, "reclamo_id")),
            message="Reclamo eliminado correctamente.",
        )

    def obtener_reclamo(self, reclamo_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.obtener_por_id(self._require_id(reclamo_id, "reclamo_id")),
            not_found_message="Reclamo no encontrado.",
        )

    def listar_reclamos(self) -> Dict[str, Any]:
        return self._handle(lambda: self._service.obtener_todos())

    def obtener_por_estudiante(self, estudiante_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.obtener_por_estudiante(
                self._require_id(estudiante_id, "estudiante_id")
            )
        )

    def obtener_pendientes(self) -> Dict[str, Any]:
        return self._handle(lambda: self._service.obtener_pendientes())

    def resolver_reclamo(self, reclamo_id: int, respuesta: str) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.resolver(
                self._require_id(reclamo_id, "reclamo_id"), respuesta
            ),
            message="Reclamo resuelto correctamente.",
        )

    def rechazar_reclamo(self, reclamo_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.rechazar(self._require_id(reclamo_id, "reclamo_id")),
            message="Reclamo rechazado correctamente.",
        )
