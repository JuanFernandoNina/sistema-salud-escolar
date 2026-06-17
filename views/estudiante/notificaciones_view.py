"""Notificaciones de alertas para estudiante."""

from config.settings import COLOR_DANGER
from controllers.control_salud_controller import ControlSaludController
from views.base_view import BaseView
from views.components import header, info_panel


class NotificacionesView(BaseView):
    def __init__(self, parent, estudiante_id: int, controller=None):
        self.estudiante_id = estudiante_id
        super().__init__(parent, controller or ControlSaludController())

    def _build_ui(self):
        header(self._frame, "Notificaciones", "Alertas calculadas desde tu historial de controles.")
        self.content = None
        self.load_data()

    def load_data(self):
        if self.content:
            self.content.destroy()
        response = self.controller.obtener_alertas_estudiante(self.estudiante_id)
        if not response.get("success"):
            lines = [response.get("error") or "No se pudieron cargar las alertas."]
        else:
            lines = [a.get("mensaje", "") for a in response.get("data") or []]
            if not lines:
                lines = ["No tienes alertas activas."]
        self.content = info_panel(self._frame, "Alertas", lines, COLOR_DANGER)
        self.content.pack(fill="x", padx=20, pady=10)
