"""Vista administrativa de estudiantes."""

from controllers.estudiante_controller import EstudianteController
from views.crud_view import CrudView


class EstudiantesView(CrudView):
    title = "Estudiantes"
    subtitle = "Registro, actualizacion y busqueda de estudiantes."
    columns = (
        ("id", "ID", 50),
        ("codigo_ruat", "RUAT", 110),
        ("nombre", "Nombre", 130),
        ("apellido", "Apellido", 130),
        ("grado", "Grado", 80),
        ("seccion", "Seccion", 80),
        ("telefono_tutor", "Telefono tutor", 130),
    )
    fields = (
        ("codigo_ruat", "Codigo RUAT", "entry", None),
        ("nombre", "Nombre", "entry", None),
        ("apellido", "Apellido", "entry", None),
        ("fecha_nacimiento", "Fecha nacimiento (YYYY-MM-DD)", "entry", None),
        ("sexo", "Sexo", "combo", ("M", "F")),
        ("grado", "Grado", "combo", ("1ro", "2do", "3ro", "4to", "5to", "6to")),
        ("seccion", "Seccion", "entry", None),
        ("direccion", "Direccion", "entry", None),
        ("telefono_tutor", "Telefono tutor", "entry", None),
        ("nombre_tutor", "Nombre tutor", "entry", None),
        ("password", "Password inicial", "password", None),
    )

    def __init__(self, parent, controller=None):
        super().__init__(parent, controller or EstudianteController())

    def list_action(self):
        return self.controller.listar_estudiantes()

    def create_action(self, data):
        return self.controller.crear_estudiante(data)

    def update_action(self, item_id, data):
        data.pop("codigo_ruat", None)
        data.pop("password", None)
        return self.controller.actualizar_estudiante(item_id, data)

    def delete_action(self, item_id):
        return self.controller.eliminar_estudiante(item_id)
