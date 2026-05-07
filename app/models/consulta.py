# =============================================================
# MÓDULO: consulta.py
# DESCRIPCIÓN: Clase Consulta — pregunta médica de un estudiante
# =============================================================

from datetime import date


class Consulta:
    """
    Representa una consulta médica o duda enviada por un estudiante.
    Un doctor o el administrador puede responderla.
    """

    def __init__(self, estudiante, mensaje):
        """
        Args:
            estudiante (Estudiante): Quién realiza la consulta
            mensaje (str): Contenido de la consulta
        """
        self.__estudiante     = estudiante
        self.__mensaje        = mensaje
        self.__fecha          = date.today()
        self.__respuesta      = None    # texto de la respuesta
        self.__respondido_por = None    # Doctor o admin que respondió
        self.__respondida     = False   # bandera de estado

    # ----------------------------------------------------------
    # GETTERS
    # ----------------------------------------------------------

    @property
    def estudiante(self):
        return self.__estudiante

    @property
    def mensaje(self):
        return self.__mensaje

    @property
    def fecha(self):
        return self.__fecha

    @property
    def respuesta(self):
        return self.__respuesta

    @property
    def respondido_por(self):
        return self.__respondido_por

    @property
    def respondida(self):
        return self.__respondida

    # ----------------------------------------------------------
    # MÉTODOS
    # ----------------------------------------------------------

    def agregar_respuesta(self, texto, respondido_por=None):
        """
        Agrega la respuesta a esta consulta.
        Marca la consulta como respondida.

        Args:
            texto (str): Texto de la respuesta médica
            respondido_por: Objeto Doctor o nombre del admin
        """
        if self.__respondida:
            raise Exception("Esta consulta ya fue respondida.")
        if not texto or len(texto.strip()) < 5:
            raise ValueError("La respuesta debe tener al menos 5 caracteres.")

        self.__respuesta      = texto.strip()
        self.__respondido_por = respondido_por
        self.__respondida     = True

    def to_dict(self):
        """Convierte la consulta a diccionario para las vistas HTML."""
        respondido_por_nombre = None
        if self.__respondido_por:
            # Puede ser un objeto Doctor o un string (nombre del admin)
            if hasattr(self.__respondido_por, 'nombre'):
                respondido_por_nombre = self.__respondido_por.nombre
            else:
                respondido_por_nombre = str(self.__respondido_por)

        return {
            "estudiante"     : self.__estudiante.nombre,
            "mensaje"        : self.__mensaje,
            "fecha"          : str(self.__fecha),
            "respondida"     : self.__respondida,
            "respuesta"      : self.__respuesta or "Pendiente de respuesta",
            "respondido_por" : respondido_por_nombre or "Sin asignar",
        }

    def __repr__(self):
        estado = "Respondida" if self.__respondida else "Pendiente"
        return f"Consulta(estudiante='{self.__estudiante.nombre}', estado='{estado}')"