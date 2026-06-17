"""Vista administrativa de controles de salud."""

from controllers.control_salud_controller import ControlSaludController
from views.crud_view import CrudView


class ControlesSaludView(CrudView):
    title = "Controles de salud"
    subtitle = "Peso, talla, IMC y observaciones de cada estudiante."
    columns = (
        ("id", "ID", 50),
        ("estudiante_id", "Estudiante", 90),
        ("fecha_control", "Fecha", 110),
        ("peso_kg", "Peso kg", 90),
        ("talla_m", "Talla m", 90),
        ("imc", "IMC", 80),
        ("estado_nutricional", "Estado", 140),
        ("observaciones", "Observaciones", 220),
    )
    fields = (
        ("estudiante_id", "ID estudiante", "entry", None),
        ("peso_kg", "Peso kg", "entry", None),
        ("talla_m", "Talla m", "entry", None),
        ("fecha_control", "Fecha control (YYYY-MM-DD)", "entry", None),
        ("personal_id", "ID personal salud", "entry", None),
        ("observaciones", "Observaciones", "text", None),
    )

    def __init__(self, parent, controller=None):
        super().__init__(parent, controller or ControlSaludController())

    def list_action(self):
        return self.controller.listar_controles()

    def create_action(self, data):
        return self.controller.crear_control(data)

    def update_action(self, item_id, data):
        data.pop("estudiante_id", None)
        return self.controller.actualizar_control(item_id, data)

    def delete_action(self, item_id):
        return self.controller.eliminar_control(item_id)
