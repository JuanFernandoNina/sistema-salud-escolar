"""
views/crud_view.py
Base reutilizable para vistas CRUD de administracion.
"""

import tkinter as tk
from typing import Any, Callable, Dict, List, Sequence, Tuple

from views.base_view import BaseView
from views.components import FormDialog, TreeviewWidget, button, danger_button, header, success_button, toolbar


class CrudView(BaseView):
    """Pantalla CRUD generica con tabla y formulario modal."""

    title = "Gestion"
    subtitle = ""
    columns: Sequence[Tuple[str, str, int]] = ()
    fields: Sequence[Tuple[str, str, str, Any]] = ()

    def _build_ui(self) -> None:
        header(self._frame, self.title, self.subtitle)
        actions = toolbar(self._frame)
        success_button(actions, "Nuevo", self._create).pack(side=tk.LEFT, padx=(0, 8))
        button(actions, "Editar", self._edit).pack(side=tk.LEFT, padx=(0, 8))
        danger_button(actions, "Eliminar", self._delete).pack(side=tk.LEFT, padx=(0, 8))
        button(actions, "Actualizar", self.load_data).pack(side=tk.LEFT)
        self.table = TreeviewWidget(self._frame, self.columns, height=16)
        self.table.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.table.bind_double_click(self._edit)
        self.load_data()

    def list_action(self) -> Dict[str, Any]:
        raise NotImplementedError

    def create_action(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    def update_action(self, item_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    def delete_action(self, item_id: int) -> Dict[str, Any]:
        raise NotImplementedError

    def load_data(self) -> None:
        response = self.list_action()
        if response.get("success"):
            self._rows = response.get("data") or []
            self.table.set_data(self._rows)
        else:
            self.mostrar_error("Error", response.get("error") or "No se pudieron cargar los datos.")

    def _selected_row(self) -> Dict[str, Any]:
        selected_id = self.table.selected_id()
        if selected_id is None:
            return {}
        for row in getattr(self, "_rows", []):
            if row.get("id") == selected_id:
                return row
        return {}

    def _create(self) -> None:
        dialog = FormDialog(self._frame, f"Nuevo - {self.title}", self.fields)
        self._frame.wait_window(dialog)
        if dialog.result:
            response = self.create_action(dialog.result)
            self._after_write(response)

    def _edit(self) -> None:
        row = self._selected_row()
        if not row:
            self.mostrar_advertencia("Seleccion requerida", "Seleccione un registro para editar.")
            return
        dialog = FormDialog(self._frame, f"Editar - {self.title}", self.fields, row)
        self._frame.wait_window(dialog)
        if dialog.result:
            response = self.update_action(row["id"], dialog.result)
            self._after_write(response)

    def _delete(self) -> None:
        row = self._selected_row()
        if not row:
            self.mostrar_advertencia("Seleccion requerida", "Seleccione un registro para eliminar.")
            return
        if not self.confirmar("Confirmar", "Desea eliminar el registro seleccionado?"):
            return
        self._after_write(self.delete_action(row["id"]))

    def _after_write(self, response: Dict[str, Any]) -> None:
        if response.get("success"):
            self.mostrar_exito("Operacion completada", response.get("message") or "Operacion realizada.")
            self.load_data()
        else:
            self.mostrar_error("Error", response.get("error") or "No se pudo completar la operacion.")
