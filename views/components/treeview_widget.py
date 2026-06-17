"""
views/components/treeview_widget.py
Tabla reutilizable basada en ttk.Treeview.
"""

import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


class TreeviewWidget(ttk.Frame):
    """Treeview con scrollbar, carga de diccionarios y seleccion simple."""

    def __init__(
        self,
        parent: tk.Widget,
        columns: Sequence[Tuple[str, str, int]],
        height: int = 12,
    ) -> None:
        super().__init__(parent)
        self._columns = list(columns)
        keys = [col[0] for col in self._columns]

        self.tree = ttk.Treeview(
            self,
            columns=keys,
            show="headings",
            height=height,
            selectmode="browse",
        )
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        for key, title, width in self._columns:
            self.tree.heading(key, text=title)
            self.tree.column(key, width=width, anchor=tk.W, stretch=True)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def set_data(self, rows: Iterable[Dict[str, Any]]) -> None:
        self.clear()
        for row in rows:
            row_id = row.get("id", "")
            values = [self._format(row.get(key, "")) for key, _, _ in self._columns]
            self.tree.insert("", tk.END, iid=str(row_id) if row_id != "" else None, values=values)

    def clear(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

    def selected_id(self) -> Optional[int]:
        selected = self.tree.selection()
        if not selected:
            return None
        try:
            return int(selected[0])
        except ValueError:
            return None

    def bind_double_click(self, callback) -> None:
        self.tree.bind("<Double-1>", lambda _event: callback())

    @staticmethod
    def _format(value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, float):
            return f"{value:.2f}"
        return str(value)
