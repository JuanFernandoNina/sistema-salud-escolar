# =============================================================
# MÓDULO: reclamo.py
# DESCRIPCIÓN: Clase Reclamo — mensaje formal de un estudiante
# =============================================================

from datetime import date


class Reclamo:
    """
    Representa un reclamo enviado por un estudiante.
    El administrador puede visualizarlo y cambiar su estado.
    """

    # Estados posibles de un reclamo (constantes de clase)
    ESTADO_PENDIENTE  = "Pendiente"
    ESTADO_EN_PROCESO = "En proceso"
    ESTADO_RESUELTO   = "Resuelto"
    ESTADO_CERRADO    = "Cerrado"

    def __init__(self, estudiante, mensaje):
        """
        Args:
            estudiante (Estudiante): Quién envía el reclamo
            mensaje (str): Contenido del reclamo
        """
        self.__estudiante = estudiante
        self.__mensaje    = mensaje
        self.__fecha      = date.today()
        self.__estado     = self.ESTADO_PENDIENTE   # estado inicial
        self.__respuesta  = None                    # el admin responde

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
    def estado(self):
        return self.__estado

    @property
    def respuesta(self):
        return self.__respuesta

    # ----------------------------------------------------------
    # SETTER — solo el estado puede cambiar
    # ----------------------------------------------------------

    @estado.setter
    def estado(self, nuevo_estado):
        estados_validos = [
            self.ESTADO_PENDIENTE,
            self.ESTADO_EN_PROCESO,
            self.ESTADO_RESUELTO,
            self.ESTADO_CERRADO
        ]
        if nuevo_estado not in estados_validos:
            raise ValueError(f"Estado inválido. Use: {estados_validos}")
        self.__estado = nuevo_estado

    # ----------------------------------------------------------
    # MÉTODOS
    # ----------------------------------------------------------

    def responder(self, texto_respuesta):
        """
        El administrador agrega una respuesta al reclamo
        y cambia el estado automáticamente a 'Resuelto'.
        """
        if not texto_respuesta or len(texto_respuesta.strip()) < 5:
            raise ValueError("La respuesta debe tener al menos 5 caracteres.")
        self.__respuesta = texto_respuesta.strip()
        self.__estado    = self.ESTADO_RESUELTO

    def to_dict(self):
        """Convierte el reclamo a diccionario para las vistas HTML."""
        return {
            "estudiante": self.__estudiante.nombre,
            "mensaje"   : self.__mensaje,
            "fecha"     : str(self.__fecha),
            "estado"    : self.__estado,
            "respuesta" : self.__respuesta or "Sin respuesta aún",
        }

    def __repr__(self):
        return (f"Reclamo(estudiante='{self.__estudiante.nombre}', "
                f"estado='{self.__estado}', fecha='{self.__fecha}')")