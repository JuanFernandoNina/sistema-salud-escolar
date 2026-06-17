"""
controllers/reporte_controller.py
Controlador para reportes, alertas y dashboard.
"""

from typing import Any, Dict
from controllers.base_controller import BaseController
from services.reporte_service import ReporteService
from services.alerta_service import AlertaService


class ReporteController(BaseController):
    """Expone reportes individuales, por curso y resumen dashboard."""

    def __init__(self) -> None:
        super().__init__()
        self._service = ReporteService()
        self._alerta_service = AlertaService()

    def reporte_individual(self, estudiante_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.reporte_individual(
                self._require_id(estudiante_id, "estudiante_id")
            )
        )

    def reporte_por_curso(self, grado: str) -> Dict[str, Any]:
        return self._handle(lambda: self._service.reporte_por_curso(grado.strip()))

    def resumen_dashboard(self) -> Dict[str, Any]:
        return self._handle(lambda: self._service.resumen_dashboard())

    def obtener_alertas_todos(self) -> Dict[str, Any]:
        return self._handle(lambda: self._alerta_service.obtener_alertas_todos())

    def contar_alertas_activas(self) -> Dict[str, Any]:
        return self._handle(lambda: self._alerta_service.contar_alertas_activas())
