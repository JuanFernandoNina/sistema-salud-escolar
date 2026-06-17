"""Punto de entrada del Sistema de Salud Escolar."""

import tkinter as tk
from tkinter import messagebox

from config.settings import APP_HEIGHT, APP_NAME, APP_WIDTH, COLOR_GRAY
from database.connection import get_db
from views.admin import (
    AlertasView,
    CitasView,
    ControlesSaludView,
    DashboardView,
    EstadisticasView,
    EstudiantesView,
    MedicamentosView,
    PersonalSaludView,
)
from views.components.sidebar import Sidebar
from views.estudiante import (
    CitasEstudianteView,
    DashboardEstudianteView,
    EvolucionNutricionalView,
    HistorialView,
    NotificacionesView,
    PerfilView,
    ReclamosView,
)
from views.login_view import LoginView


class SaludEscolarApp:
    """Coordina la ventana principal, autenticacion y navegacion."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.minsize(980, 620)
        self.root.configure(bg=COLOR_GRAY)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.current_view = None
        self.shell = None
        self.content = None
        self.show_login()

    def run(self) -> None:
        self.root.mainloop()

    def clear_window(self) -> None:
        for child in self.root.winfo_children():
            child.destroy()
        self.current_view = None
        self.shell = None
        self.content = None

    def show_login(self) -> None:
        self.clear_window()
        self.current_view = LoginView(
            self.root,
            on_admin_login=self.show_admin_panel,
            on_student_login=self.show_student_panel,
        )
        self.current_view.show()

    def build_shell(self, title: str, items) -> None:
        self.clear_window()
        self.shell = tk.Frame(self.root, bg=COLOR_GRAY)
        self.shell.pack(fill=tk.BOTH, expand=True)
        Sidebar(self.shell, title, items, logout_command=self.show_login).pack(
            side=tk.LEFT, fill=tk.Y
        )
        self.content = tk.Frame(self.shell, bg=COLOR_GRAY)
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def show_view(self, view_factory) -> None:
        if self.current_view:
            self.current_view.destroy()
        self.current_view = view_factory(self.content)
        self.current_view.show()

    def show_admin_panel(self, usuario) -> None:
        items = [
            ("Dashboard", lambda: self.show_view(DashboardView)),
            ("Estudiantes", lambda: self.show_view(EstudiantesView)),
            ("Personal salud", lambda: self.show_view(PersonalSaludView)),
            ("Controles", lambda: self.show_view(ControlesSaludView)),
            ("Citas", lambda: self.show_view(CitasView)),
            ("Medicamentos", lambda: self.show_view(MedicamentosView)),
            ("Alertas", lambda: self.show_view(AlertasView)),
            ("Estadisticas", lambda: self.show_view(EstadisticasView)),
        ]
        nombre = usuario.get("username") or "Administrador"
        self.build_shell(f"Admin\n{nombre}", items)
        self.show_view(DashboardView)

    def show_student_panel(self, session_data) -> None:
        estudiante = session_data.get("estudiante", {})
        estudiante_id = estudiante.get("id")
        if not estudiante_id:
            messagebox.showerror("Error", "No se pudo identificar al estudiante.")
            self.show_login()
            return

        def student_view(view_class):
            return lambda parent: view_class(parent, estudiante_id)

        items = [
            ("Mi panel", lambda: self.show_view(student_view(DashboardEstudianteView))),
            ("Perfil", lambda: self.show_view(student_view(PerfilView))),
            ("Historial", lambda: self.show_view(student_view(HistorialView))),
            (
                "Evolucion",
                lambda: self.show_view(student_view(EvolucionNutricionalView)),
            ),
            ("Citas", lambda: self.show_view(student_view(CitasEstudianteView))),
            ("Notificaciones", lambda: self.show_view(student_view(NotificacionesView))),
            ("Reclamos", lambda: self.show_view(student_view(ReclamosView))),
        ]
        nombre = estudiante.get("nombre") or "Estudiante"
        self.build_shell(f"Estudiante\n{nombre}", items)
        self.show_view(student_view(DashboardEstudianteView))

    def close(self) -> None:
        try:
            get_db().close()
        finally:
            self.root.destroy()


def main() -> None:
    app = SaludEscolarApp()
    app.run()


if __name__ == "__main__":
    main()
