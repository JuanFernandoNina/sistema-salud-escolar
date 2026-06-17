"""
controllers/medicamento_controller.py
Controlador para inventario de medicamentos.
"""

from typing import Any, Dict
from controllers.base_controller import BaseController
from services.medicamento_service import MedicamentoService


class MedicamentoController(BaseController):
    """Operaciones de inventario consumidas por las vistas."""

    def __init__(self) -> None:
        super().__init__()
        self._service = MedicamentoService()

    def crear_medicamento(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.crear(datos),
            message="Medicamento registrado correctamente.",
        )

    def actualizar_medicamento(
        self, medicamento_id: int, datos: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.actualizar(
                self._require_id(medicamento_id, "medicamento_id"), datos
            ),
            message="Medicamento actualizado correctamente.",
        )

    def eliminar_medicamento(self, medicamento_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.eliminar(
                self._require_id(medicamento_id, "medicamento_id")
            ),
            message="Medicamento eliminado correctamente.",
        )

    def obtener_medicamento(self, medicamento_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.obtener_por_id(
                self._require_id(medicamento_id, "medicamento_id")
            ),
            not_found_message="Medicamento no encontrado.",
        )

    def listar_medicamentos(self) -> Dict[str, Any]:
        return self._handle(lambda: self._service.obtener_todos())

    def buscar_medicamentos(self, termino: str) -> Dict[str, Any]:
        return self._handle(lambda: self._service.buscar(termino.strip()))

    def obtener_stock_bajo(self) -> Dict[str, Any]:
        return self._handle(lambda: self._service.obtener_con_stock_bajo())

    def ajustar_stock(self, medicamento_id: int, cantidad: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.ajustar_stock(
                self._require_id(medicamento_id, "medicamento_id"), int(cantidad)
            ),
            message="Stock actualizado correctamente.",
        )
