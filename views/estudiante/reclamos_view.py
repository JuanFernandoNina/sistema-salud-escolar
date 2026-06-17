"""Reclamos del estudiante."""

import tkinter as tk

from controllers.reclamo_controller import ReclamoController
from views.base_view import BaseView
from views.components import FormDialog, TreeviewWidget, button, header, success_button


class ReclamosView(BaseView):
    columns = (
        ("id", "ID", 50),
        ("asunto", "Asunto", 180),
        ("descripcion", "Descripcion", 260),
        ("estado", "Estado", 120),
        ("respuesta", "Respuesta", 260),
    )
    fields = (
        ("asunto", "Asunto", "entry", None),
        ("descripcion", "Descripcion", "text", None),
    )

    def __init__(self, parent, estudiante_id: int, controller=None):
        self.estudiante_id = estudiante_id
        super().__init__(parent, controller or ReclamoController())

    def _build_ui(self):
        header(self._frame, "Mis reclamos", "Seguimiento de solicitudes y respuestas.")
        actions = tk.Frame(self._frame, bg=self._frame["bg"])
        actions.pack(fill=tk.X, padx=20, pady=(0, 10))
        success_button(actions, "Nuevo reclamo", self._create).pack(side=tk.LEFT)
        button(actions, "Actualizar", self.load_data).pack(side=tk.LEFT, padx=8)
        self.table = TreeviewWidget(self._frame, self.columns, height=17)
        self.table.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.load_data()

    def load_data(self):
        response = self.controller.obtener_por_estudiante(self.estudiante_id)
        if response.get("success"):
            self.table.set_data(response.get("data") or [])
        else:
            self.mostrar_error("Error", response.get("error") or "No se pudieron cargar los reclamos.")

    def _create(self):
        dialog = FormDialog(self._frame, "Nuevo reclamo", self.fields)
        self._frame.wait_window(dialog)
        if not dialog.result:
            return
        data = dict(dialog.result)
        data["estudiante_id"] = self.estudiante_id
        response = self.controller.crear_reclamo(data)
        if response.get("success"):
            self.mostrar_exito("Reclamo enviado", response.get("message") or "Reclamo enviado.")
            self.load_data()
        else:
            self.mostrar_error("Error", response.get("error") or "No se pudo enviar el reclamo.")
