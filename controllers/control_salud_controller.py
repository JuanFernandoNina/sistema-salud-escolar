"""
controllers/control_salud_controller.py
Controlador para controles de salud, historial e IMC.
"""

from typing import Any, Dict
from controllers.base_controller import BaseController
from services.control_salud_service import ControlSaludService
from services.alerta_service import AlertaService


class ControlSaludController(BaseController):
    """Expone operaciones de controles de salud para las vistas."""

    def __init__(self) -> None:
        super().__init__()
        self._service = ControlSaludService()
        self._alerta_service = AlertaService()

    def crear_control(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.crear(datos),
            message="Control de salud registrado correctamente.",
        )

    def actualizar_control(self, control_id: int, datos: Dict[str, Any]) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.actualizar(
                self._require_id(control_id, "control_id"), datos
            ),
            message="Control de salud actualizado correctamente.",
        )

    def eliminar_control(self, control_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.eliminar(self._require_id(control_id, "control_id")),
            message="Control de salud eliminado correctamente.",
        )

    def obtener_control(self, control_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.obtener_por_id(self._require_id(control_id, "control_id")),
            not_found_message="Control de salud no encontrado.",
        )

    def listar_controles(self) -> Dict[str, Any]:
        return self._handle(lambda: self._service.obtener_todos())

    def obtener_historial_estudiante(self, estudiante_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.obtener_historial_estudiante(
                self._require_id(estudiante_id, "estudiante_id")
            )
        )

    def obtener_ultimo_control(self, estudiante_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.obtener_ultimo_control(
                self._require_id(estudiante_id, "estudiante_id")
            ),
            not_found_message="El estudiante no tiene controles registrados.",
        )

    def obtener_evolucion_nutricional(self, estudiante_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.obtener_evolucion_nutricional(
                self._require_id(estudiante_id, "estudiante_id")
            )
        )

    def obtener_por_rango_fecha(self, fecha_inicio: str, fecha_fin: str) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.obtener_por_rango_fecha(fecha_inicio, fecha_fin)
        )

    def obtener_alertas_estudiante(self, estudiante_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._alerta_service.obtener_alertas_estudiante(
                self._require_id(estudiante_id, "estudiante_id")
            )
        )
