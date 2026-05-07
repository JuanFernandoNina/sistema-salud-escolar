# =============================================================
# MÓDULO: models/__init__.py
# DESCRIPCIÓN: Punto de entrada del módulo models.
#              Exporta todas las clases para importarlas fácil:
#
#              from app.models import Estudiante, Doctor, Cita
# =============================================================

from app.models.persona       import Persona
from app.models.estudiante    import Estudiante
from app.models.doctor        import Doctor
from app.models.nutricionista import Nutricionista
from app.models.control_salud import ControlSalud
from app.models.reclamo       import Reclamo
from app.models.consulta      import Consulta
from app.models.cita          import Cita

# Lista de todos los modelos disponibles (útil para documentación)
__all__ = [
    "Persona",
    "Estudiante",
    "Doctor",
    "Nutricionista",
    "ControlSalud",
    "Reclamo",
    "Consulta",
    "Cita",
]