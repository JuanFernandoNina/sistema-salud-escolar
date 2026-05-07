# =============================================================
# MÓDULO: doctor.py
# DESCRIPCIÓN: Clase Doctor — hereda de Persona
# PATRÓN: Herencia + Polimorfismo
# =============================================================

from app.models.persona import Persona


class Doctor(Persona):
    """
    Representa a un médico o doctor del sistema escolar.
    Puede registrar controles, responder consultas y gestionar citas.

    Herencia: Doctor → Persona (ABC)
    """

    def __init__(self, nombre, edad, sexo, usuario, contrasena,
                 especialidad, matricula):
        super().__init__(nombre, edad, sexo, usuario, contrasena)

        # Atributos propios del Doctor
        self.__especialidad = especialidad   # Ej: "Pediatría", "Medicina General"
        self.__matricula    = matricula      # Número de matrícula profesional
        self.__citas        = []             # Lista de citas del doctor

    # ----------------------------------------------------------
    # GETTERS
    # ----------------------------------------------------------

    @property
    def especialidad(self):
        return self.__especialidad

    @property
    def matricula(self):
        return self.__matricula

    @property
    def citas(self):
        return list(self.__citas)

    # ----------------------------------------------------------
    # IMPLEMENTACIÓN de métodos abstractos (Polimorfismo)
    # ----------------------------------------------------------

    def iniciar_sesion(self, usuario, contrasena):
        """
        El doctor inicia sesión con usuario y contraseña institucional.
        """
        return self.usuario == usuario and self.verificar_contrasena(contrasena)

    def mostrar_perfil(self):
        """
        Retorna el perfil médico del doctor.
        """
        return {
            "nombre"      : self.nombre,
            "edad"        : self.edad,
            "sexo"        : self.sexo,
            "usuario"     : self.usuario,
            "especialidad": self.__especialidad,
            "matricula"   : self.__matricula,
            "rol"         : "Doctor",
        }

    # ----------------------------------------------------------
    # MÉTODOS PROPIOS del Doctor
    # ----------------------------------------------------------

    def registrar_control(self, estudiante, peso, talla, observaciones=""):
        """
        Registra un control de salud para un estudiante.
        Calcula automáticamente el IMC y estado nutricional.

        Args:
            estudiante (Estudiante): El estudiante a controlar
            peso (float): Peso en kg
            talla (float): Talla en metros
            observaciones (str): Notas médicas adicionales

        Returns:
            ControlSalud: El objeto control creado
        """
        from app.models.control_salud import ControlSalud
        from app.models.estudiante import Estudiante

        if not isinstance(estudiante, Estudiante):
            raise TypeError("Se requiere un objeto Estudiante.")

        # Calcular IMC usando el método del estudiante
        imc = estudiante.calcular_imc(peso, talla)
        estado = estudiante.obtener_estado_nutricional(imc)

        control = ControlSalud(
            peso=peso,
            talla=talla,
            imc=imc,
            estado_nutricional=estado,
            observaciones=observaciones,
            doctor=self
        )

        # Agregar el control al historial del estudiante
        estudiante.agregar_control(control)
        return control

    def responder_consulta(self, consulta, respuesta):
        """
        Responde una consulta enviada por un estudiante.

        Args:
            consulta (Consulta): Objeto consulta a responder
            respuesta (str): Texto de la respuesta médica
        """
        from app.models.consulta import Consulta

        if not isinstance(consulta, Consulta):
            raise TypeError("Se requiere un objeto Consulta.")
        if not respuesta or len(respuesta.strip()) < 5:
            raise ValueError("La respuesta debe tener al menos 5 caracteres.")

        consulta.agregar_respuesta(respuesta, respondido_por=self)

    def gestionar_citas(self, accion, cita):
        """
        Gestiona el estado de una cita médica.

        Args:
            accion (str): 'confirmar', 'cancelar' o 'completar'
            cita (Cita): Objeto cita a gestionar
        """
        from app.models.cita import Cita

        acciones_validas = ['confirmar', 'cancelar', 'completar']
        if accion not in acciones_validas:
            raise ValueError(f"Acción inválida. Use: {acciones_validas}")

        if accion == 'confirmar':
            cita.estado = 'Confirmada'
        elif accion == 'cancelar':
            cita.estado = 'Cancelada'
        elif accion == 'completar':
            cita.estado = 'Completada'

    def __repr__(self):
        return f"Doctor(nombre='{self.nombre}', especialidad='{self.__especialidad}')"