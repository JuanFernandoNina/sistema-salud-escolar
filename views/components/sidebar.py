"""
views/components/sidebar.py
Barra lateral para navegacion de paneles.
"""

import tkinter as tk
from typing import Callable, Iterable, Tuple

from config.settings import COLOR_ACCENT, COLOR_PRIMARY, COLOR_TEXT_LIGHT, FONT_BUTTON, FONT_SMALL, FONT_SUBTITLE


class Sidebar(tk.Frame):
    """Menu vertical reutilizable."""

    def __init__(
        self,
        parent: tk.Widget,
        title: str,
        items: Iterable[Tuple[str, Callable]],
        logout_command: Callable = None,
    ) -> None:
        super().__init__(parent, bg=COLOR_PRIMARY, width=220)
        self.pack_propagate(False)
        tk.Label(self, text=title, bg=COLOR_PRIMARY, fg=COLOR_TEXT_LIGHT, font=FONT_SUBTITLE, wraplength=180, justify=tk.LEFT).pack(anchor="w", padx=16, pady=(18, 10))
        for text, command in items:
            tk.Button(
                self,
                text=text,
                command=command,
                bg=COLOR_PRIMARY,
                fg=COLOR_TEXT_LIGHT,
                activebackground=COLOR_ACCENT,
                activeforeground=COLOR_TEXT_LIGHT,
                relief=tk.FLAT,
                anchor="w",
                font=FONT_BUTTON,
                padx=14,
                pady=8,
                cursor="hand2",
            ).pack(fill=tk.X, padx=8, pady=2)
        tk.Frame(self, bg=COLOR_PRIMARY).pack(fill=tk.BOTH, expand=True)
        if logout_command:
            tk.Button(
                self,
                text="Cerrar sesion",
                command=logout_command,
                bg=COLOR_ACCENT,
                fg=COLOR_TEXT_LIGHT,
                relief=tk.FLAT,
                font=FONT_SMALL,
                padx=10,
                pady=7,
            ).pack(fill=tk.X, padx=12, pady=14)
