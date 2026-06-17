"""
controllers/estudiante_controller.py
Controlador de gestion de estudiantes.
"""

from typing import Any, Dict
from controllers.base_controller import BaseController
from services.estudiante_service import EstudianteService
from services.control_salud_service import ControlSaludService
from services.alerta_service import AlertaService
from services.cita_service import CitaService
from services.reclamo_service import ReclamoService


class EstudianteController(BaseController):
    """Operaciones usadas por vistas admin y panel del estudiante."""

    def __init__(self) -> None:
        super().__init__()
        self._service = EstudianteService()
        self._control_service = ControlSaludService()
        self._alerta_service = AlertaService()
        self._cita_service = CitaService()
        self._reclamo_service = ReclamoService()

    def crear_estudiante(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.crear(datos),
            message="Estudiante registrado correctamente.",
        )

    def actualizar_estudiante(self, estudiante_id: int, datos: Dict[str, Any]) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.actualizar(
                self._require_id(estudiante_id, "estudiante_id"), datos
            ),
            message="Estudiante actualizado correctamente.",
        )

    def eliminar_estudiante(self, estudiante_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.eliminar(self._require_id(estudiante_id, "estudiante_id")),
            message="Estudiante eliminado correctamente.",
        )

    def obtener_estudiante(self, estudiante_id: int) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.obtener_por_id(
                self._require_id(estudiante_id, "estudiante_id")
            ),
            not_found_message="Estudiante no encontrado.",
        )

    def listar_estudiantes(self) -> Dict[str, Any]:
        return self._handle(lambda: self._service.obtener_todos())

    def buscar_estudiantes(self, termino: str) -> Dict[str, Any]:
        return self._handle(lambda: self._service.buscar(termino.strip()))

    def listar_por_grado(self, grado: str) -> Dict[str, Any]:
        return self._handle(lambda: self._service.obtener_por_grado(grado.strip()))

    def obtener_por_ruat(self, codigo_ruat: str) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.obtener_por_ruat(codigo_ruat.strip()),
            not_found_message="Estudiante no encontrado.",
        )

    def obtener_perfil_estudiante(self, estudiante_id: int) -> Dict[str, Any]:
        def action():
            estudiante_id_validado = self._require_id(estudiante_id, "estudiante_id")
            estudiante = self._service.obtener_por_id(estudiante_id_validado)
            if not estudiante:
                return None
            ultimo_control = self._control_service.obtener_ultimo_control(estudiante_id_validado)
            return {
                "estudiante": estudiante,
                "edad": estudiante.calcular_edad(),
                "ultimo_control": ultimo_control,
                "alertas": self._alerta_service.obtener_alertas_estudiante(estudiante_id_validado),
                "citas": self._cita_service.obtener_por_estudiante(estudiante_id_validado),
                "reclamos": self._reclamo_service.obtener_por_estudiante(estudiante_id_validado),
            }

        return self._handle(action, not_found_message="Estudiante no encontrado.")
