# =============================================================
# MÓDULO: persona.py
# DESCRIPCIÓN: Clase abstracta base para todos los usuarios
#              del sistema (Estudiante, Doctor, Nutricionista)
# PATRÓN: Abstracción + Herencia (POO)
# =============================================================

from abc import ABC, abstractmethod  # ABC = Abstract Base Class


class Persona(ABC):
    """
    Clase ABSTRACTA que representa a cualquier persona del sistema.
    No se puede instanciar directamente — solo sirve como plantilla
    para las clases derivadas: Estudiante, Doctor, Nutricionista.

    Principios aplicados:
        - Abstracción: define la estructura sin implementar todo
        - Encapsulamiento: atributos privados con getters/setters
        - Herencia: las clases hijas heredan atributos y métodos
    """

    def __init__(self, nombre, edad, sexo, usuario, contrasena):
        # Atributos PRIVADOS (encapsulamiento)
        # El doble guion bajo (__) indica que son privados
        self.__nombre    = nombre
        self.__edad      = edad
        self.__sexo      = sexo      # 'M' o 'F'
        self.__usuario   = usuario
        self.__contrasena = contrasena

    # ----------------------------------------------------------
    # GETTERS — permiten leer los atributos privados
    # ----------------------------------------------------------

    @property
    def nombre(self):
        return self.__nombre

    @property
    def edad(self):
        return self.__edad

    @property
    def sexo(self):
        return self.__sexo

    @property
    def usuario(self):
        return self.__usuario

    # Nota: la contraseña NO tiene getter por seguridad

    # ----------------------------------------------------------
    # SETTERS — permiten modificar los atributos con validación
    # ----------------------------------------------------------

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres.")
        self.__nombre = valor.strip()

    @edad.setter
    def edad(self, valor):
        if not isinstance(valor, int) or valor < 0 or valor > 120:
            raise ValueError("La edad debe ser un número entre 0 y 120.")
        self.__edad = valor

    @usuario.setter
    def usuario(self, valor):
        if not valor or len(valor.strip()) < 3:
            raise ValueError("El usuario debe tener al menos 3 caracteres.")
        self.__usuario = valor.strip()

    def set_contrasena(self, nueva):
        """Método para cambiar la contraseña con validación mínima."""
        if len(nueva) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")
        self.__contrasena = nueva

    def verificar_contrasena(self, intento):
        """Verifica si la contraseña ingresada es correcta."""
        return self.__contrasena == intento

    # ----------------------------------------------------------
    # MÉTODOS ABSTRACTOS — OBLIGATORIOS en las clases hijas
    # Cada clase derivada DEBE implementar estos métodos
    # ----------------------------------------------------------

    @abstractmethod
    def iniciar_sesion(self, usuario, contrasena):
        """
        Lógica de autenticación.
        Cada tipo de usuario (admin, estudiante) tiene su propia lógica.
        """
        pass

    @abstractmethod
    def mostrar_perfil(self):
        """
        Retorna los datos del perfil del usuario.
        Cada tipo de usuario muestra información diferente.
        """
        pass

    # ----------------------------------------------------------
    # MÉTODO CONCRETO — disponible para todas las clases hijas
    # ----------------------------------------------------------

    def __repr__(self):
        """Representación legible del objeto (para debugging)."""
        return f"{self.__class__.__name__}(nombre='{self.__nombre}', usuario='{self.__usuario}')"