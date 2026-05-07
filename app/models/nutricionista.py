# =============================================================
# MÓDULO: nutricionista.py
# DESCRIPCIÓN: Clase Nutricionista — hereda de Persona
# PATRÓN: Herencia + Polimorfismo
# =============================================================

from app.models.persona import Persona


class Nutricionista(Persona):
    """
    Representa a un nutricionista del sistema escolar.
    Puede evaluar el estado nutricional, generar reportes
    y asignar dietas a los estudiantes.

    Herencia: Nutricionista → Persona (ABC)
    """

    def __init__(self, nombre, edad, sexo, usuario, contrasena, matricula):
        super().__init__(nombre, edad, sexo, usuario, contrasena)

        self.__matricula          = matricula
        self.__estudiantes_asignados = []   # lista de Estudiantes a su cargo

    # ----------------------------------------------------------
    # GETTERS
    # ----------------------------------------------------------

    @property
    def matricula(self):
        return self.__matricula

    @property
    def estudiantes_asignados(self):
        return list(self.__estudiantes_asignados)

    # ----------------------------------------------------------
    # IMPLEMENTACIÓN de métodos abstractos (Polimorfismo)
    # ----------------------------------------------------------

    def iniciar_sesion(self, usuario, contrasena):
        return self.usuario == usuario and self.verificar_contrasena(contrasena)

    def mostrar_perfil(self):
        return {
            "nombre"      : self.nombre,
            "edad"        : self.edad,
            "sexo"        : self.sexo,
            "usuario"     : self.usuario,
            "matricula"   : self.__matricula,
            "rol"         : "Nutricionista",
            "estudiantes_a_cargo": len(self.__estudiantes_asignados),
        }

    # ----------------------------------------------------------
    # MÉTODOS PROPIOS del Nutricionista
    # ----------------------------------------------------------

    def asignar_estudiante(self, estudiante):
        """
        Asigna un estudiante a este nutricionista.
        También actualiza el nutricionista en el objeto estudiante.
        """
        from app.models.estudiante import Estudiante
        if not isinstance(estudiante, Estudiante):
            raise TypeError("Se requiere un objeto Estudiante.")

        if estudiante not in self.__estudiantes_asignados:
            self.__estudiantes_asignados.append(estudiante)
            estudiante.nutricionista_asignado = self

    def evaluar_nutricion(self, estudiante):
        """
        Evalúa el estado nutricional de un estudiante
        basándose en su último control de salud.

        Args:
            estudiante (Estudiante): Estudiante a evaluar

        Returns:
            dict: Resumen de la evaluación nutricional
        """
        controles = estudiante.obtener_controles()

        if not controles:
            return {
                "estudiante": estudiante.nombre,
                "resultado" : "Sin controles registrados",
                "imc"       : None,
                "estado"    : None,
            }

        # Obtener el control más reciente (el último de la lista)
        ultimo = controles[-1]

        return {
            "estudiante": estudiante.nombre,
            "fecha"     : ultimo.fecha,
            "peso"      : ultimo.peso,
            "talla"     : ultimo.talla,
            "imc"       : ultimo.imc,
            "estado"    : ultimo.estado_nutricional,
            "evaluado_por": self.nombre,
        }

    def generar_reporte(self, estudiante):
        """
        Genera un reporte nutricional completo del estudiante
        con todo su historial de controles.

        Args:
            estudiante (Estudiante): Estudiante del reporte

        Returns:
            dict: Reporte completo con historial
        """
        controles = estudiante.obtener_controles()

        historial = []
        for ctrl in controles:
            historial.append({
                "fecha"  : ctrl.fecha,
                "peso"   : ctrl.peso,
                "talla"  : ctrl.talla,
                "imc"    : ctrl.imc,
                "estado" : ctrl.estado_nutricional,
            })

        return {
            "estudiante"  : estudiante.mostrar_perfil(),
            "nutricionista": self.nombre,
            "historial"   : historial,
            "total_controles": len(historial),
        }

    def asignar_dieta(self, estudiante, descripcion_dieta):
        """
        Registra una recomendación de dieta para un estudiante.

        Args:
            estudiante (Estudiante): El estudiante que recibirá la dieta
            descripcion_dieta (str): Descripción del plan alimentario

        Returns:
            dict: Confirmación de la dieta asignada
        """
        if not descripcion_dieta or len(descripcion_dieta.strip()) < 10:
            raise ValueError("La descripción de la dieta es muy corta.")

        return {
            "estudiante"       : estudiante.nombre,
            "nutricionista"    : self.nombre,
            "dieta"            : descripcion_dieta.strip(),
            "estado_nutricional": self.evaluar_nutricion(estudiante).get("estado"),
        }

    def __repr__(self):
        return f"Nutricionista(nombre='{self.nombre}', estudiantes={len(self.__estudiantes_asignados)})"