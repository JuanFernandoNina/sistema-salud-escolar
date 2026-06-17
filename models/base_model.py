"""
models/base_model.py
Clase abstracta base para todos los modelos del sistema.

Patrones y principios aplicados:
  - Abstracción   : define la interfaz mínima que todo modelo debe cumplir.
  - Encapsulamiento: atributos protegidos con propiedades.
  - SRP           : solo representa y valida la estructura de un modelo.
  - OCP           : abierto para extensión, cerrado para modificación.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Optional


class BaseModel(ABC):
    """
    Clase abstracta base para todos los modelos del dominio.
    Todo modelo hereda de aquí y debe implementar to_dict() y validate().
    """

    def __init__(self, id: Optional[int] = None,
                 creado_en: Optional[str] = None):
        self._id: Optional[int] = id
        self._creado_en: str = creado_en or datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    # ── Propiedades comunes ───────────────────────────────────────────────────

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        if value is not None and value <= 0:
            raise ValueError("El ID debe ser un entero positivo.")
        self._id = value

    @property
    def creado_en(self) -> str:
        return self._creado_en

    # ── Métodos abstractos — contrato obligatorio ─────────────────────────────

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Serializa el modelo a diccionario.
        Usado por repositorios y vistas para mapear datos.
        """
        ...

    @abstractmethod
    def validate(self) -> bool:
        """
        Valida la integridad de los datos del modelo.
        Debe lanzar ValueError si algo es inválido.
        Retorna True si todo es correcto.
        """
        ...

    # ── Métodos concretos comunes ─────────────────────────────────────────────

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseModel":
        """
        Método de fábrica: crea una instancia desde un diccionario.
        Cada subclase puede sobreescribir si necesita lógica especial.
        """
        return cls(**data)

    def is_persisted(self) -> bool:
        """Retorna True si el modelo ya fue guardado en la BD (tiene ID)."""
        return self._id is not None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self._id}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseModel):
            return False
        return self._id is not None and self._id == other._id
