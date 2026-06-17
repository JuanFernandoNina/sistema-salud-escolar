"""Vista de reportes y estadisticas."""

import tkinter as tk
from tkinter import ttk

from controllers.reporte_controller import ReporteController
from views.base_view import BaseView
from views.components import TreeviewWidget, button, header, info_panel


class EstadisticasView(BaseView):
    """Reportes por curso con distribucion nutricional."""

    columns = (
        ("id", "ID", 50),
        ("nombre_completo", "Estudiante", 180),
        ("codigo_ruat", "RUAT", 120),
        ("edad", "Edad", 80),
        ("sexo", "Sexo", 70),
        ("ultimo_control", "Ultimo control", 130),
        ("imc", "IMC", 80),
        ("estado_nutricional", "Estado", 130),
        ("total_alertas", "Alertas", 80),
    )

    def __init__(self, parent, controller=None):
        super().__init__(parent, controller or ReporteController())

    def _build_ui(self):
        header(self._frame, "Estadisticas por curso", "Reporte nutricional agrupado por grado.")
        top = tk.Frame(self._frame, bg=self._frame["bg"])
        top.pack(fill=tk.X, padx=20, pady=(0, 10))
        tk.Label(top, text="Grado:", bg=self._frame["bg"]).pack(side=tk.LEFT)
        self.grade = ttk.Combobox(top, values=("1ro", "2do", "3ro", "4to", "5to", "6to"), state="readonly", width=8)
        self.grade.set("4to")
        self.grade.pack(side=tk.LEFT, padx=8)
        button(top, "Generar", self.load_data).pack(side=tk.LEFT)
        self.summary = tk.Frame(self._frame, bg=self._frame["bg"])
        self.summary.pack(fill=tk.X, padx=20, pady=(0, 10))
        self.table = TreeviewWidget(self._frame, self.columns, height=14)
        self.table.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.load_data()

    def load_data(self):
        for child in self.summary.winfo_children():
            child.destroy()
        response = self.controller.reporte_por_curso(self.grade.get())
        if not response.get("success"):
            self.mostrar_error("Error", response.get("error") or "No se pudo generar el reporte.")
            return
        data = response["data"]
        dist = data.get("distribucion_nutricional", {})
        lines = [
            f"Total estudiantes: {data.get('total_estudiantes', 0)}",
            f"IMC promedio: {data.get('imc_promedio') or 'Sin datos'}",
            "Distribucion: " + ", ".join(f"{k}: {v}" for k, v in dist.items()),
        ]
        info_panel(self.summary, f"Resumen {data.get('grado')}", lines).pack(fill=tk.X)
        self.table.set_data(data.get("estudiantes") or [])
