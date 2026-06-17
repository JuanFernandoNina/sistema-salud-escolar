"""Vista administrativa de personal de salud."""

from controllers.personal_salud_controller import PersonalSaludController
from views.crud_view import CrudView


class PersonalSaludView(CrudView):
    title = "Personal de salud"
    subtitle = "Profesionales vinculados a controles y citas."
    columns = (
        ("id", "ID", 50),
        ("nombre", "Nombre", 130),
        ("apellido", "Apellido", 130),
        ("especialidad", "Especialidad", 150),
        ("matricula", "Matricula", 120),
        ("telefono", "Telefono", 120),
        ("email", "Email", 180),
    )
    fields = (
        ("nombre", "Nombre", "entry", None),
        ("apellido", "Apellido", "entry", None),
        ("especialidad", "Especialidad", "entry", None),
        ("matricula", "Matricula", "entry", None),
        ("telefono", "Telefono", "entry", None),
        ("email", "Email", "entry", None),
    )

    def __init__(self, parent, controller=None):
        super().__init__(parent, controller or PersonalSaludController())

    def list_action(self):
        return self.controller.listar_personal()

    def create_action(self, data):
        return self.controller.crear_personal(data)

    def update_action(self, item_id, data):
        return self.controller.actualizar_personal(item_id, data)

    def delete_action(self, item_id):
        return self.controller.eliminar_personal(item_id)
