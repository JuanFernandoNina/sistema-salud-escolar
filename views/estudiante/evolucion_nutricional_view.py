"""Evolucion nutricional del estudiante."""

import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from controllers.control_salud_controller import ControlSaludController
from views.base_view import BaseView
from views.components import TreeviewWidget, button, header, info_panel


class EvolucionNutricionalView(BaseView):
    columns = (
        ("fecha", "Fecha", 120),
        ("peso_kg", "Peso kg", 100),
        ("talla_m", "Talla m", 100),
        ("imc", "IMC", 90),
        ("estado_nutricional", "Estado", 150),
    )

    def __init__(self, parent, estudiante_id: int, controller=None):
        self.estudiante_id = estudiante_id
        self._canvas = None
        super().__init__(parent, controller or ControlSaludController())

    def _build_ui(self):
        header(self._frame, "Evolucion nutricional", "Grafico de peso, talla e IMC por fecha.")
        button(self._frame, "Actualizar", self.load_data).pack(anchor="e", padx=20, pady=(0, 8))
        self.chart_frame = tk.Frame(self._frame, bg=self._frame["bg"])
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        self.table = TreeviewWidget(self._frame, self.columns, height=7)
        self.table.pack(fill=tk.X, padx=20, pady=(0, 20))
        self.load_data()

    def load_data(self):
        response = self.controller.obtener_evolucion_nutricional(self.estudiante_id)
        if not response.get("success"):
            self.mostrar_error("Error", response.get("error") or "No se pudo cargar la evolucion.")
            return
        rows = response.get("data") or []
        self.table.set_data(rows)
        self._draw_chart(rows)

    def _draw_chart(self, rows):
        for child in self.chart_frame.winfo_children():
            child.destroy()
        if not rows:
            info_panel(self.chart_frame, "Sin datos", ["Aun no hay controles para graficar."]).pack(fill=tk.X)
            return
        dates = [row["fecha"] for row in rows]
        weights = [row["peso_kg"] for row in rows]
        heights = [row["talla_m"] for row in rows]
        imcs = [row["imc"] for row in rows]

        figure = Figure(figsize=(7.5, 3.8), dpi=100)
        ax = figure.add_subplot(111)
        ax.plot(dates, weights, marker="o", label="Peso kg")
        ax.plot(dates, imcs, marker="o", label="IMC")
        ax.plot(dates, heights, marker="o", label="Talla m")
        ax.set_title("Evolucion nutricional")
        ax.grid(True, alpha=0.3)
        ax.legend()
        figure.autofmt_xdate(rotation=25)

        self._canvas = FigureCanvasTkAgg(figure, master=self.chart_frame)
        self._canvas.draw()
        self._canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
