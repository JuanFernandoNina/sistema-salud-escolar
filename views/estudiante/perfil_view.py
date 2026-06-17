"""Vista de perfil del estudiante."""

from controllers.estudiante_controller import EstudianteController
from views.base_view import BaseView
from views.components import header, info_panel


class PerfilView(BaseView):
    def __init__(self, parent, estudiante_id: int, controller=None):
        self.estudiante_id = estudiante_id
        super().__init__(parent, controller or EstudianteController())

    def _build_ui(self):
        header(self._frame, "Mi perfil", "Datos personales y tutor registrados.")
        self.content = info_panel(self._frame, "Cargando", ["Espere..."])
        self.content.pack(fill="x", padx=20, pady=10)
        self.load_data()

    def load_data(self):
        self.content.destroy()
        response = self.controller.obtener_perfil_estudiante(self.estudiante_id)
        if not response.get("success"):
            self.content = info_panel(self._frame, "Perfil", [response.get("error") or "No disponible"])
            self.content.pack(fill="x", padx=20, pady=10)
            return
        est = response["data"]["estudiante"]
        lines = [
            f"Nombre: {est.get('nombre')} {est.get('apellido')}",
            f"RUAT: {est.get('codigo_ruat')}",
            f"Edad: {response['data'].get('edad')} anos",
            f"Grado y seccion: {est.get('grado')} {est.get('seccion')}",
            f"Direccion: {est.get('direccion') or ''}",
            f"Tutor: {est.get('nombre_tutor') or ''}",
            f"Telefono tutor: {est.get('telefono_tutor') or ''}",
        ]
        self.content = info_panel(self._frame, "Datos del estudiante", lines)
        self.content.pack(fill="x", padx=20, pady=10)
