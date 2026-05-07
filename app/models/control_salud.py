# =============================================================
# MÓDULO: control_salud.py
# DESCRIPCIÓN: Clase ControlSalud — registro médico de un
#              estudiante en una fecha determinada
# =============================================================

from datetime import date


class ControlSalud:
    """
    Representa un control médico realizado a un estudiante.
    Almacena datos de peso, talla, IMC y estado nutricional.
    No hereda de Persona — es una entidad de datos independiente.
    """

    def __init__(self, peso, talla, imc, estado_nutricional,
                 observaciones="", doctor=None):
        """
        Args:
            peso (float): Peso del estudiante en kg
            talla (float): Talla en metros
            imc (float): IMC ya calculado
            estado_nutricional (str): Clasificación nutricional
            observaciones (str): Notas del médico
            doctor (Doctor): Médico que realizó el control
        """
        self.__fecha              = date.today()    # Se registra la fecha actual
        self.__peso               = peso
        self.__talla              = talla
        self.__imc                = imc
        self.__estado_nutricional = estado_nutricional
        self.__observaciones      = observaciones
        self.__doctor             = doctor          # referencia al Doctor

    # ----------------------------------------------------------
    # GETTERS (todos de solo lectura — el control no se modifica)
    # ----------------------------------------------------------

    @property
    def fecha(self):
        return self.__fecha

    @property
    def peso(self):
        return self.__peso

    @property
    def talla(self):
        return self.__talla

    @property
    def imc(self):
        return self.__imc

    @property
    def estado_nutricional(self):
        return self.__estado_nutricional

    @property
    def observaciones(self):
        return self.__observaciones

    @property
    def doctor(self):
        return self.__doctor

    # ----------------------------------------------------------
    # MÉTODOS
    # ----------------------------------------------------------

    def to_dict(self):
        """
        Convierte el control a diccionario.
        Útil para enviar los datos a las plantillas HTML (Jinja2)
        o para serializar a JSON en la API.
        """
        return {
            "fecha"             : str(self.__fecha),
            "peso"              : self.__peso,
            "talla"             : self.__talla,
            "imc"               : self.__imc,
            "estado_nutricional": self.__estado_nutricional,
            "observaciones"     : self.__observaciones,
            "doctor"            : self.__doctor.nombre if self.__doctor else "Sin asignar",
        }

    def __repr__(self):
        return (f"ControlSalud(fecha='{self.__fecha}', "
                f"peso={self.__peso}kg, talla={self.__talla}m, "
                f"imc={self.__imc}, estado='{self.__estado_nutricional}')")