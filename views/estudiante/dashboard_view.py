"""Dashboard del estudiante."""

import tkinter as tk

from config.settings import COLOR_ACCENT, COLOR_DANGER, COLOR_PRIMARY, COLOR_SUCCESS
from controllers.estudiante_controller import EstudianteController
from views.base_view import BaseView
from views.components import header, info_panel, stat_card


class DashboardEstudianteView(BaseView):
    def __init__(self, parent, estudiante_id: int, controller=None):
        self.estudiante_id = estudiante_id
        super().__init__(parent, controller or EstudianteController())

    def _build_ui(self):
        header(self._frame, "Mi panel de salud", "Resumen personal de controles, citas y notificaciones.")
        self.cards = tk.Frame(self._frame, bg=self._frame["bg"])
        self.cards.pack(fill=tk.X, padx=20, pady=10)
        self.details = tk.Frame(self._frame, bg=self._frame["bg"])
        self.details.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.load_data()

    def load_data(self):
        response = self.controller.obtener_perfil_estudiante(self.estudiante_id)
        if not response.get("success"):
            info_panel(self.details, "Panel", [response.get("error") or "No disponible"]).pack(fill=tk.X)
            return
        data = response["data"]
        ultimo = data.get("ultimo_control") or {}
        items = [
            ("Edad", data.get("edad", 0), COLOR_PRIMARY),
            ("IMC actual", ultimo.get("imc", "Sin datos"), COLOR_ACCENT),
            ("Estado", ultimo.get("estado_nutricional", "Sin datos"), COLOR_SUCCESS),
            ("Alertas", len(data.get("alertas") or []), COLOR_DANGER),
            ("Citas", len(data.get("citas") or []), COLOR_PRIMARY),
        ]
        for index, item in enumerate(items):
            card = stat_card(self.cards, item[0], item[1], item[2])
            card.grid(row=0, column=index, sticky="nsew", padx=5)
            self.cards.columnconfigure(index, weight=1)

        est = data["estudiante"]
        lines = [
            f"Estudiante: {est.get('nombre')} {est.get('apellido')}",
            f"RUAT: {est.get('codigo_ruat')}",
            f"Ultimo control: {ultimo.get('fecha_control', 'Sin datos')}",
            f"Observaciones: {ultimo.get('observaciones') or 'Sin observaciones'}",
        ]
        info_panel(self.details, "Resumen", lines).pack(fill=tk.X)
