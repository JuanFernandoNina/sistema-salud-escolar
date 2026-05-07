# =============================================================
# MÓDULO: cita.py
# DESCRIPCIÓN: Clase Cita — agendamiento médico entre
#              un estudiante y un doctor
# =============================================================

from datetime import date, time


class Cita:
    """
    Representa una cita médica agendada.
    Relaciona a un Estudiante con un Doctor en fecha y hora específica.
    """

    # Estados posibles de una cita
    ESTADO_PENDIENTE  = "Pendiente"
    ESTADO_CONFIRMADA = "Confirmada"
    ESTADO_CANCELADA  = "Cancelada"
    ESTADO_COMPLETADA = "Completada"

    def __init__(self, estudiante, doctor, fecha, hora, motivo=""):
        """
        Args:
            estudiante (Estudiante): Paciente de la cita
            doctor (Doctor): Médico responsable
            fecha (date): Fecha de la cita
            hora (str): Hora en formato "HH:MM"
            motivo (str): Motivo de la consulta
        """
        self.__estudiante = estudiante
        self.__doctor     = doctor
        self.__fecha      = fecha
        self.__hora       = hora
        self.__motivo     = motivo
        self.__estado     = self.ESTADO_PENDIENTE   # estado inicial
        self.__creada_en  = date.today()

    # ----------------------------------------------------------
    # GETTERS
    # ----------------------------------------------------------

    @property
    def estudiante(self):
        return self.__estudiante

    @property
    def doctor(self):
        return self.__doctor

    @property
    def fecha(self):
        return self.__fecha

    @property
    def hora(self):
        return self.__hora

    @property
    def motivo(self):
        return self.__motivo

    @property
    def estado(self):
        return self.__estado

    @property
    def creada_en(self):
        return self.__creada_en

    # ----------------------------------------------------------
    # SETTER — solo el estado puede cambiar tras crear la cita
    # ----------------------------------------------------------

    @estado.setter
    def estado(self, nuevo_estado):
        estados_validos = [
            self.ESTADO_PENDIENTE,
            self.ESTADO_CONFIRMADA,
            self.ESTADO_CANCELADA,
            self.ESTADO_COMPLETADA
        ]
        if nuevo_estado not in estados_validos:
            raise ValueError(f"Estado inválido. Use uno de: {estados_validos}")
        self.__estado = nuevo_estado

    # ----------------------------------------------------------
    # MÉTODOS
    # ----------------------------------------------------------

    def cancelar(self):
        """Cancela la cita si no está ya completada."""
        if self.__estado == self.ESTADO_COMPLETADA:
            raise Exception("No se puede cancelar una cita ya completada.")
        self.__estado = self.ESTADO_CANCELADA

    def confirmar(self):
        """Confirma la cita si está pendiente."""
        if self.__estado != self.ESTADO_PENDIENTE:
            raise Exception("Solo se pueden confirmar citas pendientes.")
        self.__estado = self.ESTADO_CONFIRMADA

    def completar(self):
        """Marca la cita como completada."""
        if self.__estado == self.ESTADO_CANCELADA:
            raise Exception("No se puede completar una cita cancelada.")
        self.__estado = self.ESTADO_COMPLETADA

    def esta_activa(self):
        """Retorna True si la cita está pendiente o confirmada."""
        return self.__estado in [self.ESTADO_PENDIENTE, self.ESTADO_CONFIRMADA]

    def to_dict(self):
        """Convierte la cita a diccionario para las vistas HTML."""
        return {
            "estudiante": self.__estudiante.nombre,
            "doctor"    : self.__doctor.nombre,
            "fecha"     : str(self.__fecha),
            "hora"      : self.__hora,
            "motivo"    : self.__motivo or "Sin motivo especificado",
            "estado"    : self.__estado,
            "creada_en" : str(self.__creada_en),
        }

    def __repr__(self):
        return (f"Cita(estudiante='{self.__estudiante.nombre}', "
                f"doctor='{self.__doctor.nombre}', "
                f"fecha='{self.__fecha}', estado='{self.__estado}')")