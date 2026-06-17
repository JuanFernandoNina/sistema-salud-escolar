"""Vista administrativa de citas medicas."""

import tkinter as tk

from controllers.cita_controller import CitaController
from views.components import button, success_button
from views.crud_view import CrudView


class CitasView(CrudView):
    title = "Citas medicas"
    subtitle = "Agenda, confirmacion y seguimiento de citas."
    columns = (
        ("id", "ID", 50),
        ("estudiante_id", "Estudiante", 90),
        ("fecha_cita", "Fecha", 110),
        ("hora_cita", "Hora", 80),
        ("motivo", "Motivo", 220),
        ("estado", "Estado", 120),
        ("observaciones", "Observaciones", 220),
    )
    fields = (
        ("estudiante_id", "ID estudiante", "entry", None),
        ("motivo", "Motivo", "entry", None),
        ("fecha_cita", "Fecha cita (YYYY-MM-DD)", "entry", None),
        ("hora_cita", "Hora cita (HH:MM)", "entry", None),
        ("personal_id", "ID personal salud", "entry", None),
        ("estado", "Estado", "combo", ("pendiente", "confirmada", "realizada", "cancelada")),
        ("observaciones", "Observaciones", "text", None),
    )

    def __init__(self, parent, controller=None):
        super().__init__(parent, controller or CitaController())

    def _build_ui(self):
        super()._build_ui()
        actions = tk.Frame(self._frame, bg=self._frame["bg"])
        actions.pack(anchor="e", padx=20, pady=(0, 16))
        success_button(actions, "Confirmar", lambda: self._change_status("confirmar")).pack(side=tk.LEFT, padx=4)
        button(actions, "Realizada", lambda: self._change_status("realizar")).pack(side=tk.LEFT, padx=4)
        button(actions, "Cancelar cita", lambda: self._change_status("cancelar")).pack(side=tk.LEFT, padx=4)

    def list_action(self):
        return self.controller.listar_citas()

    def create_action(self, data):
        return self.controller.crear_cita(data)

    def update_action(self, item_id, data):
        data.pop("estudiante_id", None)
        return self.controller.actualizar_cita(item_id, data)

    def delete_action(self, item_id):
        return self.controller.eliminar_cita(item_id)

    def _change_status(self, action):
        row = self._selected_row()
        if not row:
            self.mostrar_advertencia("Seleccion requerida", "Seleccione una cita.")
            return
        actions = {
            "confirmar": self.controller.confirmar_cita,
            "realizar": self.controller.realizar_cita,
            "cancelar": self.controller.cancelar_cita,
        }
        self._after_write(actions[action](row["id"]))
