"""
controllers/cita_controller.py
Controlador para gestion de citas medicas.
"""

from typing import Any, Dict
from controllers.base_controller import BaseController
from services.cita_service import CitaService


class CitaController(BaseController):
    """API de citas para vistas administrativas y de estudiante."""

    def __init__(self) -> None:
        super().__init__()
        self._service = CitaService()

    def crear_cita(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.crear(datos),
            message="Cita registrada correctamente.",
        )

    def actualizar_cita(self, cita_id: int, datos: Dict[str, Any]) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.actualizar(self._require_id(cita_id, "cita_id"), datos),
            message="Cita actualizada correctamente.",
        )

    def eliminar_cita(self, cita_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.eliminar(self._require_id(cita_id, "cita_id")),
            message="Cita eliminada correctamente.",
        )

    def obtener_cita(self, cita_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.obtener_por_id(self._require_id(cita_id, "cita_id")),
            not_found_message="Cita no encontrada.",
        )

    def listar_citas(self) -> Dict[str, Any]:
        return self._handle(lambda: self._service.obtener_todos())

    def obtener_por_estudiante(self, estudiante_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.obtener_por_estudiante(
                self._require_id(estudiante_id, "estudiante_id")
            )
        )

    def obtener_pendientes(self) -> Dict[str, Any]:
        return self._handle(lambda: self._service.obtener_pendientes())

    def obtener_por_fecha(self, fecha: str) -> Dict[str, Any]:
        return self._handle(lambda: self._service.obtener_por_fecha(fecha))

    def confirmar_cita(self, cita_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.confirmar(self._require_id(cita_id, "cita_id")),
            message="Cita confirmada correctamente.",
        )

    def realizar_cita(self, cita_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.realizar(self._require_id(cita_id, "cita_id")),
            message="Cita marcada como realizada.",
        )

    def cancelar_cita(self, cita_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.cancelar(self._require_id(cita_id, "cita_id")),
            message="Cita cancelada correctamente.",
        )
