"""Vista administrativa de medicamentos."""

import tkinter as tk
from tkinter import simpledialog

from controllers.medicamento_controller import MedicamentoController
from views.components import button
from views.crud_view import CrudView


class MedicamentosView(CrudView):
    title = "Medicamentos"
    subtitle = "Inventario del botiquin escolar y control de stock."
    columns = (
        ("id", "ID", 50),
        ("nombre", "Nombre", 170),
        ("descripcion", "Descripcion", 220),
        ("stock", "Stock", 90),
        ("unidad", "Unidad", 100),
        ("stock_minimo", "Minimo", 90),
    )
    fields = (
        ("nombre", "Nombre", "entry", None),
        ("descripcion", "Descripcion", "text", None),
        ("stock", "Stock", "entry", None),
        ("unidad", "Unidad", "entry", None),
        ("stock_minimo", "Stock minimo", "entry", None),
    )

    def __init__(self, parent, controller=None):
        super().__init__(parent, controller or MedicamentoController())

    def _build_ui(self):
        super()._build_ui()
        button(self._frame, "Ajustar stock", self._adjust_stock).pack(anchor="e", padx=20, pady=(0, 16))

    def list_action(self):
        return self.controller.listar_medicamentos()

    def create_action(self, data):
        return self.controller.crear_medicamento(data)

    def update_action(self, item_id, data):
        return self.controller.actualizar_medicamento(item_id, data)

    def delete_action(self, item_id):
        return self.controller.eliminar_medicamento(item_id)

    def _adjust_stock(self):
        row = self._selected_row()
        if not row:
            self.mostrar_advertencia("Seleccion requerida", "Seleccione un medicamento.")
            return
        cantidad = simpledialog.askinteger("Ajustar stock", "Cantidad a sumar o restar:", parent=self._frame)
        if cantidad is None:
            return
        response = self.controller.ajustar_stock(row["id"], cantidad)
        self._after_write(response)
