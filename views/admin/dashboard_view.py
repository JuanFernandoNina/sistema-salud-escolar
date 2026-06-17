"""Dashboard administrativo."""

import tkinter as tk

from config.settings import COLOR_ACCENT, COLOR_DANGER, COLOR_PRIMARY, COLOR_SUCCESS, COLOR_WARNING
from controllers.reporte_controller import ReporteController
from views.base_view import BaseView
from views.components import button, header, info_panel, stat_card


class DashboardView(BaseView):
    """Resumen rapido para administrador/docente."""

    def __init__(self, parent, controller=None):
        super().__init__(parent, controller or ReporteController())

    def _build_ui(self):
        header(self._frame, "Panel administrativo", "Indicadores principales del sistema de salud escolar.")
        self.cards = tk.Frame(self._frame, bg=self._frame["bg"])
        self.cards.pack(fill=tk.X, padx=20, pady=10)
        button(self._frame, "Actualizar", self.load_data).pack(anchor="e", padx=20, pady=(0, 10))
        self.alert_frame = tk.Frame(self._frame, bg=self._frame["bg"])
        self.alert_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.load_data()

    def load_data(self):
        for child in self.cards.winfo_children():
            child.destroy()
        for child in self.alert_frame.winfo_children():
            child.destroy()

        response = self.controller.resumen_dashboard()
        if not response.get("success"):
            self.mostrar_error("Error", response.get("error") or "No se pudo cargar el dashboard.")
            return
        data = response["data"]
        items = [
            ("Estudiantes", data.get("total_estudiantes", 0), COLOR_PRIMARY),
            ("Alertas activas", data.get("alertas_activas", 0), COLOR_DANGER),
            ("Citas pendientes", data.get("citas_pendientes", 0), COLOR_ACCENT),
            ("Stock bajo", data.get("medicamentos_bajos", 0), COLOR_WARNING),
            ("Reclamos pendientes", data.get("reclamos_pendientes", 0), COLOR_SUCCESS),
        ]
        for index, item in enumerate(items):
            card = stat_card(self.cards, item[0], item[1], item[2])
            card.grid(row=0, column=index, sticky="nsew", padx=5)
            self.cards.columnconfigure(index, weight=1)

        alerts = self.controller.obtener_alertas_todos()
        lines = []
        if alerts.get("success"):
            lines = [
                f"{a.get('estudiante_nombre', 'Estudiante')} - {a.get('mensaje', '')}"
                for a in alerts.get("data", [])[:8]
            ]
        if not lines:
            lines = ["No hay alertas activas registradas."]
        info_panel(self.alert_frame, "Alertas recientes", lines, COLOR_DANGER).pack(fill=tk.X)
