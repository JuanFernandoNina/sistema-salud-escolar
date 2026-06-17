"""Historial de controles del estudiante."""

from controllers.control_salud_controller import ControlSaludController
from views.base_view import BaseView
from views.components import TreeviewWidget, button, header


class HistorialView(BaseView):
    columns = (
        ("fecha_control", "Fecha", 120),
        ("peso_kg", "Peso kg", 100),
        ("talla_m", "Talla m", 100),
        ("imc", "IMC", 90),
        ("estado_nutricional", "Estado", 150),
        ("observaciones", "Observaciones", 330),
    )

    def __init__(self, parent, estudiante_id: int, controller=None):
        self.estudiante_id = estudiante_id
        super().__init__(parent, controller or ControlSaludController())

    def _build_ui(self):
        header(self._frame, "Historial de salud", "Controles registrados por fecha.")
        button(self._frame, "Actualizar", self.load_data).pack(anchor="e", padx=20, pady=(0, 10))
        self.table = TreeviewWidget(self._frame, self.columns, height=18)
        self.table.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.load_data()

    def load_data(self):
        response = self.controller.obtener_historial_estudiante(self.estudiante_id)
        if response.get("success"):
            self.table.set_data(response.get("data") or [])
        else:
            self.mostrar_error("Error", response.get("error") or "No se pudo cargar el historial.")
