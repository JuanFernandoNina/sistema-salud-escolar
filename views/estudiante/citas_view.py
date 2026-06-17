"""Citas del estudiante."""

from controllers.cita_controller import CitaController
from views.base_view import BaseView
from views.components import TreeviewWidget, button, header


class CitasEstudianteView(BaseView):
    columns = (
        ("fecha_cita", "Fecha", 120),
        ("hora_cita", "Hora", 80),
        ("motivo", "Motivo", 260),
        ("estado", "Estado", 120),
        ("observaciones", "Observaciones", 300),
    )

    def __init__(self, parent, estudiante_id: int, controller=None):
        self.estudiante_id = estudiante_id
        super().__init__(parent, controller or CitaController())

    def _build_ui(self):
        header(self._frame, "Mis citas", "Agenda medica asociada a tu perfil.")
        button(self._frame, "Actualizar", self.load_data).pack(anchor="e", padx=20, pady=(0, 10))
        self.table = TreeviewWidget(self._frame, self.columns, height=18)
        self.table.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.load_data()

    def load_data(self):
        response = self.controller.obtener_por_estudiante(self.estudiante_id)
        if response.get("success"):
            self.table.set_data(response.get("data") or [])
        else:
            self.mostrar_error("Error", response.get("error") or "No se pudieron cargar las citas.")
