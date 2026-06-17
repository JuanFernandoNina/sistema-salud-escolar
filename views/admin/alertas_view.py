"""Vista administrativa de alertas."""

from config.settings import COLOR_DANGER
from controllers.reporte_controller import ReporteController
from views.base_view import BaseView
from views.components import TreeviewWidget, button, header


class AlertasView(BaseView):
    """Listado de alertas calculadas por servicios."""

    columns = (
        ("estudiante_id", "ID estudiante", 100),
        ("estudiante_nombre", "Estudiante", 180),
        ("tipo", "Tipo", 180),
        ("nivel", "Nivel", 100),
        ("mensaje", "Mensaje", 430),
    )

    def __init__(self, parent, controller=None):
        super().__init__(parent, controller or ReporteController())

    def _build_ui(self):
        header(self._frame, "Alertas de salud", "Riesgos detectados automaticamente desde controles de salud.")
        button(self._frame, "Actualizar", self.load_data).pack(anchor="e", padx=20, pady=(0, 10))
        self.table = TreeviewWidget(self._frame, self.columns, height=18)
        self.table.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.load_data()

    def load_data(self):
        response = self.controller.obtener_alertas_todos()
        if response.get("success"):
            self.table.set_data(response.get("data") or [])
        else:
            self.mostrar_error("Error", response.get("error") or "No se pudieron cargar las alertas.")
