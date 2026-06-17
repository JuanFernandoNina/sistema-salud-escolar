"""
controllers/personal_salud_controller.py
Controlador para personal de salud.
"""

from typing import Any, Dict
from controllers.base_controller import BaseController
from services.personal_salud_service import PersonalSaludService


class PersonalSaludController(BaseController):
    """API de personal medico para las vistas administrativas."""

    def __init__(self) -> None:
        super().__init__()
        self._service = PersonalSaludService()

    def crear_personal(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.crear(datos),
            message="Personal de salud registrado correctamente.",
        )

    def actualizar_personal(self, personal_id: int, datos: Dict[str, Any]) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.actualizar(
                self._require_id(personal_id, "personal_id"), datos
            ),
            message="Personal de salud actualizado correctamente.",
        )

    def eliminar_personal(self, personal_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.eliminar(self._require_id(personal_id, "personal_id")),
            message="Personal de salud eliminado correctamente.",
        )

    def obtener_personal(self, personal_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.obtener_por_id(
                self._require_id(personal_id, "personal_id")
            ),
            not_found_message="Personal de salud no encontrado.",
        )

    def listar_personal(self) -> Dict[str, Any]:
        return self._handle(lambda: self._service.obtener_todos())

    def buscar_personal(self, termino: str) -> Dict[str, Any]:
        return self._handle(lambda: self._service.buscar(termino.strip()))

    def obtener_por_especialidad(self, especialidad: str) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.obtener_por_especialidad(especialidad.strip())
        )
