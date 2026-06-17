"""Vista de inicio de sesion."""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from config.settings import COLOR_ACCENT, COLOR_GRAY, COLOR_PRIMARY, COLOR_WHITE, FONT_BUTTON, FONT_NORMAL, FONT_TITLE
from controllers.auth_controller import AuthController
from views.base_view import BaseView
from views.components import configure_styles


class LoginView(BaseView):
    """Login para administrador/docente y estudiante."""

    def __init__(
        self,
        parent,
        controller=None,
        on_admin_login: Optional[Callable] = None,
        on_student_login: Optional[Callable] = None,
    ):
        self._on_admin_login = on_admin_login
        self._on_student_login = on_student_login
        super().__init__(parent, controller or AuthController())

    def _build_ui(self):
        configure_styles()
        container = tk.Frame(self._frame, bg=COLOR_GRAY)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(container, text="Sistema de Salud Escolar", bg=COLOR_GRAY, fg=COLOR_PRIMARY, font=FONT_TITLE).pack(pady=(0, 18))
        card = tk.Frame(container, bg=COLOR_WHITE, padx=28, pady=24, highlightthickness=1, highlightbackground="#DADDE2")
        card.pack()

        self.mode = tk.StringVar(value="admin")
        modes = tk.Frame(card, bg=COLOR_WHITE)
        modes.pack(fill=tk.X, pady=(0, 12))
        ttk.Radiobutton(modes, text="Administrador", variable=self.mode, value="admin").pack(side=tk.LEFT, padx=(0, 14))
        ttk.Radiobutton(modes, text="Estudiante", variable=self.mode, value="student").pack(side=tk.LEFT)

        tk.Label(card, text="Usuario", bg=COLOR_WHITE, font=FONT_NORMAL).pack(anchor="w")
        self.username = tk.Entry(card, width=34, font=FONT_NORMAL)
        self.username.pack(pady=(4, 10))
        tk.Label(card, text="Password (RUAT)", bg=COLOR_WHITE, font=FONT_NORMAL).pack(anchor="w")
        self.password = tk.Entry(card, width=34, show="*", font=FONT_NORMAL)
        self.password.pack(pady=(4, 16))
        tk.Button(card, text="Ingresar", command=self._login, bg=COLOR_PRIMARY, fg=COLOR_WHITE, activebackground=COLOR_ACCENT, activeforeground=COLOR_WHITE, relief=tk.FLAT, font=FONT_BUTTON, padx=16, pady=8).pack(fill=tk.X)
        self.username.focus_set()

    def _login(self):
        username = self.username.get().strip()
        password = self.password.get()
        if self.mode.get() == "admin":
            response = self.controller.login_admin(username, password)
            if response.get("success"):
                if self._on_admin_login:
                    self._on_admin_login(response["data"])
                return
        else:
            response = self.controller.login_estudiante(username, password)
            if response.get("success"):
                if self._on_student_login:
                    self._on_student_login(response["data"])
                return
        self.mostrar_error("Login invalido", response.get("error") or "Credenciales invalidas.")
