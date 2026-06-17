"""
views/base_view.py
Clase abstracta base para todas las vistas Tkinter del sistema.

Patrones y principios aplicados:
  - Template Method : define el ciclo de vida de una vista (setup → build → show).
  - SRP             : solo gestiona la estructura visual base.
  - OCP             : las subclases extienden sin modificar esta clase.
  - Encapsulamiento : el frame raíz y la ventana están protegidos.
"""

from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from config.settings import (
    COLOR_PRIMARY, COLOR_WHITE, COLOR_GRAY,
    COLOR_DANGER, COLOR_SUCCESS, COLOR_WARNING,
    FONT_TITLE, FONT_NORMAL, FONT_BUTTON,
    APP_WIDTH, APP_HEIGHT
)


class BaseView(ABC):
    """
    Clase abstracta base para todas las vistas del sistema.
    Define el ciclo de vida: __init__ → _setup_ui() → _build_ui() → show().

    Subclases deben implementar:
        _build_ui() : construye los widgets específicos de la vista.
    """

    def __init__(self, parent: tk.Widget, controller=None) -> None:
        self._parent = parent
        self._controller = controller
        self._frame = tk.Frame(parent, bg=COLOR_WHITE)
        self._setup_ui()

    # ── Ciclo de vida ─────────────────────────────────────────────────────────

    def _setup_ui(self) -> None:
        """
        Inicialización base: configura el frame raíz y llama a _build_ui().
        No sobreescribir salvo necesidad justificada.
        """
        self._frame.configure(bg=COLOR_GRAY)
        self._build_ui()

    @abstractmethod
    def _build_ui(self) -> None:
        """
        Construye todos los widgets de la vista.
        Obligatorio en cada subclase.
        """
        ...

    def show(self) -> None:
        """Hace visible el frame principal de la vista."""
        self._frame.pack(fill=tk.BOTH, expand=True)

    def hide(self) -> None:
        """Oculta el frame principal sin destruirlo."""
        self._frame.pack_forget()

    def destroy(self) -> None:
        """Destruye el frame y libera recursos."""
        self._frame.destroy()

    # ── Propiedades ───────────────────────────────────────────────────────────

    @property
    def frame(self) -> tk.Frame:
        return self._frame

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, value) -> None:
        self._controller = value

    # ── Helpers de UI reutilizables ───────────────────────────────────────────

    def _crear_titulo(self, parent: tk.Widget,
                      texto: str) -> tk.Label:
        """Crea una etiqueta de título estándar."""
        lbl = tk.Label(
            parent, text=texto,
            font=FONT_TITLE,
            bg=COLOR_GRAY,
            fg=COLOR_PRIMARY
        )
        lbl.pack(anchor="w", padx=20, pady=(20, 5))
        return lbl

    def _crear_separador(self, parent: tk.Widget) -> ttk.Separator:
        """Crea una línea separadora horizontal."""
        sep = ttk.Separator(parent, orient="horizontal")
        sep.pack(fill=tk.X, padx=20, pady=5)
        return sep

    def _crear_boton(self, parent: tk.Widget, texto: str,
                     comando, color: str = COLOR_PRIMARY,
                     ancho: int = 15) -> tk.Button:
        """Crea un botón estilizado estándar."""
        return tk.Button(
            parent,
            text=texto,
            command=comando,
            font=FONT_BUTTON,
            bg=color,
            fg=COLOR_WHITE,
            relief=tk.FLAT,
            cursor="hand2",
            width=ancho,
            padx=10, pady=6,
            activebackground=COLOR_GRAY,
            activeforeground=COLOR_PRIMARY
        )

    # ── Diálogos estándar ─────────────────────────────────────────────────────

    def mostrar_error(self, titulo: str, mensaje: str) -> None:
        messagebox.showerror(titulo, mensaje)

    def mostrar_exito(self, titulo: str, mensaje: str) -> None:
        messagebox.showinfo(titulo, mensaje)

    def mostrar_advertencia(self, titulo: str, mensaje: str) -> None:
        messagebox.showwarning(titulo, mensaje)

    def confirmar(self, titulo: str, mensaje: str) -> bool:
        return messagebox.askyesno(titulo, mensaje)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
