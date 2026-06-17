"""
services/base_service.py
Clase abstracta base para todos los servicios del sistema.

Patrones y principios aplicados:
  - Facade    : los servicios simplifican la interacción con repositorios.
  - Template Method: define el esqueleto de operaciones con pasos abstractos.
  - SRP       : cada servicio concreto gestiona la lógica de un solo dominio.
  - DIP       : los servicios dependen de abstracciones (repositorios), no
                de implementaciones concretas.
  - LSP       : cualquier servicio concreto puede sustituir a BaseService.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, TypeVar
from models.base_model import BaseModel
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class BaseService(ABC, Generic[T]):
    """
    Clase abstracta base para la capa de servicios.
    Implementa el patrón Template Method: define el flujo de
    crear/actualizar/eliminar con pasos que las subclases completan.

    Cada servicio concreto hereda de BaseService[ModeloConcreto] e inyecta
    su propio repositorio en el constructor.
    """

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    # ── Contrato abstracto — cada servicio debe implementar ───────────────────

    @abstractmethod
    def crear(self, datos: Dict[str, Any]) -> T:
        """
        Valida los datos, construye el modelo y lo persiste.
        Lanza ValueError si los datos son inválidos.
        Retorna el modelo guardado con su ID.
        """
        ...

    @abstractmethod
    def actualizar(self, id: int, datos: Dict[str, Any]) -> T:
        """
        Actualiza un registro existente.
        Lanza ValueError si el ID no existe o los datos son inválidos.
        """
        ...

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """
        Elimina (lógica o físicamente) un registro.
        Lanza ValueError si el ID no existe.
        """
        ...

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[T]:
        """Recupera un modelo por su ID. Retorna None si no existe."""
        ...

    @abstractmethod
    def obtener_todos(self) -> List[T]:
        """Retorna todos los registros del dominio."""
        ...

    # ── Template Methods — flujo con pasos reutilizables ─────────────────────

    def _antes_de_guardar(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Hook ejecutado antes de guardar/actualizar.
        Las subclases pueden sobreescribir para limpiar o enriquecer datos.
        Por defecto, elimina espacios en strings.
        """
        return {
            k: v.strip() if isinstance(v, str) else v
            for k, v in datos.items()
        }

    def _despues_de_guardar(self, modelo: T) -> None:
        """
        Hook ejecutado tras guardar exitosamente.
        Las subclases pueden sobreescribir para enviar notificaciones,
        generar alertas, registrar auditoría, etc.
        Por defecto solo registra en log.
        """
        self._logger.info(
            f"{self.__class__.__name__}: guardado → {modelo}"
        )

    def _validar_id_existe(self, id: int,
                            obtener_fn) -> T:
        """
        Verifica que el ID existe antes de actualizar/eliminar.
        Lanza ValueError si no se encuentra.
        """
        modelo = obtener_fn(id)
        if modelo is None:
            raise ValueError(
                f"Registro con ID {id} no encontrado en "
                f"{self.__class__.__name__}."
            )
        return modelo

    # ── Utilidades de log ─────────────────────────────────────────────────────

    def _log_info(self, mensaje: str) -> None:
        self._logger.info(mensaje)

    def _log_error(self, mensaje: str) -> None:
        self._logger.error(mensaje)

    def _log_warning(self, mensaje: str) -> None:
        self._logger.warning(mensaje)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
