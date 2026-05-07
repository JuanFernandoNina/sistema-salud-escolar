# =============================================================
# MÓDULO: estudiante.py
# DESCRIPCIÓN: Clase Estudiante — hereda de Persona
# PATRÓN: Herencia + Polimorfismo + Encapsulamiento
# =============================================================

from app.models.persona import Persona
from datetime import date


class Estudiante(Persona):
    """
    Representa a un estudiante del colegio.
    Hereda todos los atributos y métodos de Persona,
    y agrega atributos y comportamientos propios del estudiante.

    Herencia: Estudiante → Persona (ABC)
    """

    def __init__(self, nombre, edad, sexo, usuario, contrasena,
                 codigo, curso, colegio, fotografia=None):
        # Llamamos al constructor de la clase PADRE (Persona)
        super().__init__(nombre, edad, sexo, usuario, contrasena)

        # Atributos PROPIOS del Estudiante (privados)
        self.__codigo              = codigo       # RUDE o nº de boleta
        self.__curso               = curso        # Ej: "4to A"
        self.__colegio             = colegio
        self.__fotografia          = fotografia   # ruta del archivo
        self.__nutricionista_asignado = None      # se asigna después
        self.__controles           = []           # lista de ControlSalud

    # ----------------------------------------------------------
    # GETTERS
    # ----------------------------------------------------------

    @property
    def codigo(self):
        return self.__codigo

    @property
    def curso(self):
        return self.__curso

    @property
    def colegio(self):
        return self.__colegio

    @property
    def fotografia(self):
        return self.__fotografia

    @property
    def nutricionista_asignado(self):
        return self.__nutricionista_asignado

    @property
    def controles(self):
        # Retorna una COPIA para proteger la lista original
        return list(self.__controles)

    # ----------------------------------------------------------
    # SETTERS
    # ----------------------------------------------------------

    @fotografia.setter
    def fotografia(self, ruta):
        self.__fotografia = ruta

    @nutricionista_asignado.setter
    def nutricionista_asignado(self, nutricionista):
        self.__nutricionista_asignado = nutricionista

    # ----------------------------------------------------------
    # IMPLEMENTACIÓN de métodos abstractos de Persona
    # (Polimorfismo: cada clase los implementa a su manera)
    # ----------------------------------------------------------

    def iniciar_sesion(self, usuario, contrasena):
        """
        El estudiante inicia sesión con RUDE o código + contraseña.
        Retorna True si las credenciales son correctas.
        """
        if self.usuario == usuario and self.verificar_contrasena(contrasena):
            return True
        return False

    def mostrar_perfil(self):
        """
        Retorna un diccionario con la información del estudiante.
        Este diccionario se usará para renderizar la vista HTML.
        """
        return {
            "nombre"    : self.nombre,
            "edad"      : self.edad,
            "sexo"      : self.sexo,
            "usuario"   : self.usuario,
            "codigo"    : self.__codigo,
            "curso"     : self.__curso,
            "colegio"   : self.__colegio,
            "fotografia": self.__fotografia,
            "nutricionista": str(self.__nutricionista_asignado)
                             if self.__nutricionista_asignado else "Sin asignar",
            "total_controles": len(self.__controles),
        }

    # ----------------------------------------------------------
    # MÉTODOS PROPIOS del Estudiante
    # ----------------------------------------------------------

    def agregar_control(self, control):
        """
        Agrega un objeto ControlSalud a la lista de controles.
        Valida que sea una instancia correcta antes de agregar.
        """
        from app.models.control_salud import ControlSalud
        if not isinstance(control, ControlSalud):
            raise TypeError("Solo se pueden agregar objetos de tipo ControlSalud.")
        self.__controles.append(control)

    def obtener_controles(self):
        """Retorna todos los controles médicos del estudiante."""
        return list(self.__controles)

    def calcular_imc(self, peso_kg, talla_m):
        """
        Calcula el Índice de Masa Corporal (IMC).
        Fórmula: IMC = peso(kg) / talla²(m)

        Args:
            peso_kg (float): Peso en kilogramos
            talla_m (float): Talla en metros

        Returns:
            float: Valor del IMC redondeado a 2 decimales
        """
        if talla_m <= 0:
            raise ValueError("La talla debe ser mayor a 0.")
        if peso_kg <= 0:
            raise ValueError("El peso debe ser mayor a 0.")

        imc = peso_kg / (talla_m ** 2)
        return round(imc, 2)

    def obtener_estado_nutricional(self, imc):
        """
        Determina el estado nutricional según el IMC.
        Clasificación para niños/adolescentes (OMS).

        Args:
            imc (float): Valor del IMC calculado

        Returns:
            str: Categoría del estado nutricional
        """
        if imc < 16.0:
            return "Desnutrición severa"
        elif imc < 18.5:
            return "Bajo peso"
        elif imc < 25.0:
            return "Normal"
        elif imc < 30.0:
            return "Sobrepeso"
        else:
            return "Obesidad"

    def enviar_reclamo(self, mensaje):
        """
        Crea un objeto Reclamo asociado a este estudiante.

        Args:
            mensaje (str): Contenido del reclamo

        Returns:
            Reclamo: Objeto reclamo creado
        """
        from app.models.reclamo import Reclamo
        if not mensaje or len(mensaje.strip()) < 10:
            raise ValueError("El reclamo debe tener al menos 10 caracteres.")
        return Reclamo(estudiante=self, mensaje=mensaje)

    def realizar_consulta(self, mensaje):
        """
        Crea un objeto Consulta asociado a este estudiante.

        Args:
            mensaje (str): Pregunta o consulta del estudiante

        Returns:
            Consulta: Objeto consulta creado
        """
        from app.models.consulta import Consulta
        if not mensaje or len(mensaje.strip()) < 5:
            raise ValueError("La consulta debe tener al menos 5 caracteres.")
        return Consulta(estudiante=self, mensaje=mensaje)

    def __repr__(self):
        return f"Estudiante(nombre='{self.nombre}', codigo='{self.__codigo}', curso='{self.__curso}')" 