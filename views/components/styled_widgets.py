"""
views/components/styled_widgets.py
Controles visuales reutilizables para Tkinter.
"""

import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple

from config.settings import (
    COLOR_ACCENT,
    COLOR_DANGER,
    COLOR_GRAY,
    COLOR_PRIMARY,
    COLOR_SUCCESS,
    COLOR_TEXT_DARK,
    COLOR_TEXT_LIGHT,
    COLOR_WARNING,
    COLOR_WHITE,
    FONT_BUTTON,
    FONT_NORMAL,
    FONT_SMALL,
    FONT_SUBTITLE,
)


def configure_styles() -> None:
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure("Treeview", rowheight=28, font=FONT_NORMAL)
    style.configure("Treeview.Heading", font=FONT_SUBTITLE, background=COLOR_PRIMARY, foreground=COLOR_TEXT_LIGHT)
    style.configure("TCombobox", padding=4)


def page(parent: tk.Widget) -> tk.Frame:
    frame = tk.Frame(parent, bg=COLOR_GRAY)
    frame.pack(fill=tk.BOTH, expand=True)
    return frame


def header(parent: tk.Widget, title: str, subtitle: str = "") -> tk.Frame:
    box = tk.Frame(parent, bg=COLOR_GRAY)
    box.pack(fill=tk.X, padx=20, pady=(18, 8))
    tk.Label(box, text=title, bg=COLOR_GRAY, fg=COLOR_PRIMARY, font=("Segoe UI", 18, "bold")).pack(anchor="w")
    if subtitle:
        tk.Label(box, text=subtitle, bg=COLOR_GRAY, fg=COLOR_TEXT_DARK, font=FONT_SMALL).pack(anchor="w", pady=(2, 0))
    return box


def toolbar(parent: tk.Widget) -> tk.Frame:
    frame = tk.Frame(parent, bg=COLOR_GRAY)
    frame.pack(fill=tk.X, padx=20, pady=(0, 10))
    return frame


def button(parent: tk.Widget, text: str, command: Callable, color: str = COLOR_PRIMARY) -> tk.Button:
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=COLOR_WHITE,
        activebackground=COLOR_ACCENT,
        activeforeground=COLOR_WHITE,
        relief=tk.FLAT,
        padx=12,
        pady=6,
        font=FONT_BUTTON,
        cursor="hand2",
    )


def danger_button(parent: tk.Widget, text: str, command: Callable) -> tk.Button:
    return button(parent, text, command, COLOR_DANGER)


def success_button(parent: tk.Widget, text: str, command: Callable) -> tk.Button:
    return button(parent, text, command, COLOR_SUCCESS)


def stat_card(parent: tk.Widget, title: str, value: Any, color: str = COLOR_PRIMARY) -> tk.Frame:
    frame = tk.Frame(parent, bg=COLOR_WHITE, bd=0, highlightthickness=1, highlightbackground="#DADDE2")
    tk.Label(frame, text=str(value), bg=COLOR_WHITE, fg=color, font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=14, pady=(12, 0))
    tk.Label(frame, text=title, bg=COLOR_WHITE, fg=COLOR_TEXT_DARK, font=FONT_NORMAL).pack(anchor="w", padx=14, pady=(0, 12))
    return frame


def info_panel(parent: tk.Widget, title: str, lines: Iterable[str], color: str = COLOR_PRIMARY) -> tk.Frame:
    frame = tk.Frame(parent, bg=COLOR_WHITE, highlightthickness=1, highlightbackground="#DADDE2")
    tk.Label(frame, text=title, bg=COLOR_WHITE, fg=color, font=FONT_SUBTITLE).pack(anchor="w", padx=14, pady=(12, 6))
    for line in lines:
        tk.Label(frame, text=line, bg=COLOR_WHITE, fg=COLOR_TEXT_DARK, font=FONT_NORMAL, wraplength=720, justify=tk.LEFT).pack(anchor="w", padx=14, pady=2)
    return frame


class FormDialog(tk.Toplevel):
    """Dialogo modal simple para crear o editar registros."""

    def __init__(
        self,
        parent: tk.Widget,
        title: str,
        fields: Sequence[Tuple[str, str, str, Any]],
        initial: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.configure(bg=COLOR_GRAY)
        self.result: Optional[Dict[str, Any]] = None
        self._entries: Dict[str, Any] = {}
        self._field_types: Dict[str, str] = {}
        initial = initial or {}

        body = tk.Frame(self, bg=COLOR_GRAY)
        body.pack(fill=tk.BOTH, expand=True, padx=18, pady=18)

        for row, (key, label, kind, options) in enumerate(fields):
            self._field_types[key] = kind
            tk.Label(body, text=label, bg=COLOR_GRAY, fg=COLOR_TEXT_DARK, font=FONT_NORMAL).grid(row=row, column=0, sticky="w", pady=5)
            value = initial.get(key, "")
            if kind == "combo":
                widget = ttk.Combobox(body, values=list(options), state="readonly", width=30)
                widget.set(value or (options[0] if options else ""))
            elif kind == "text":
                widget = tk.Text(body, width=32, height=4, font=FONT_NORMAL)
                widget.insert("1.0", "" if value is None else str(value))
            elif kind == "password":
                widget = tk.Entry(body, width=34, show="*", font=FONT_NORMAL)
                widget.insert(0, "" if value is None else str(value))
            else:
                widget = tk.Entry(body, width=34, font=FONT_NORMAL)
                widget.insert(0, "" if value is None else str(value))
            widget.grid(row=row, column=1, sticky="ew", padx=(12, 0), pady=5)
            self._entries[key] = widget

        actions = tk.Frame(body, bg=COLOR_GRAY)
        actions.grid(row=len(fields), column=0, columnspan=2, sticky="e", pady=(14, 0))
        button(actions, "Cancelar", self.destroy, COLOR_WARNING).pack(side=tk.RIGHT, padx=(8, 0))
        success_button(actions, "Guardar", self._save).pack(side=tk.RIGHT)

        self.transient(parent.winfo_toplevel())
        self.grab_set()
        self.wait_visibility()
        self.focus()

    def _save(self) -> None:
        data: Dict[str, Any] = {}
        for key, widget in self._entries.items():
            if self._field_types[key] == "text":
                value = widget.get("1.0", tk.END).strip()
            else:
                value = widget.get().strip()
            data[key] = value if value != "" else None
        self.result = data
        self.destroy()
