"""
database/repositories/base_repository.py
Repositorio abstracto genérico (interfaz CRUD).

Patrones y principios aplicados:
  - Repository Pattern : abstrae el acceso a datos del resto del sistema.
  - Generics (TypeVar) : tipado fuerte sin perder flexibilidad.
  - ISP  : interfaz mínima — cada repositorio concreto agrega lo que necesita.
  - DIP  : capas superiores dependen de esta abstracción, no de SQLite directo.
  - SRP  : solo define el contrato de acceso a datos.
"""

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar
from models.base_model import BaseModel
from database.connection import get_db
import logging

logger = logging.getLogger(__name__)

# TypeVar ligado a BaseModel — garantiza que T siempre es un modelo del dominio
T = TypeVar("T", bound=BaseModel)


class BaseRepository(ABC, Generic[T]):
    """
    Interfaz abstracta CRUD para todos los repositorios.
    Cada repositorio concreto hereda de BaseRepository[ModeloConcreto].

    Ejemplo:
        class EstudianteRepository(BaseRepository[Estudiante]):
            ...
    """

    def __init__(self, tabla: str) -> None:
        """
        Args:
            tabla: nombre exacto de la tabla SQLite que gestiona este repo.
        """
        self._tabla = tabla
        self._db = get_db()

    # ── Propiedades de acceso a BD ────────────────────────────────────────────

    @property
    def connection(self):
        return self._db.get_connection()

    @property
    def cursor(self):
        return self._db.get_cursor()

    # ── Contrato CRUD abstracto ───────────────────────────────────────────────

    @abstractmethod
    def guardar(self, modelo: T) -> T:
        """
        INSERT si el modelo no tiene ID, UPDATE si ya lo tiene.
        Retorna el modelo con el ID asignado.
        """
        ...

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[T]:
        """Busca un registro por su clave primaria. None si no existe."""
        ...

    @abstractmethod
    def obtener_todos(self) -> List[T]:
        """Retorna todos los registros activos de la tabla."""
        ...

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """
        Elimina lógicamente (activo=0) o físicamente según el modelo.
        Retorna True si se eliminó correctamente.
        """
        ...

    @abstractmethod
    def _fila_a_modelo(self, fila) -> T:
        """
        Convierte una fila SQLite (sqlite3.Row) en una instancia del modelo.
        Cada repositorio concreto implementa el mapeo de columnas.
        """
        ...

    # ── Métodos concretos reutilizables ───────────────────────────────────────

    def existe(self, id: int) -> bool:
        """Verifica si existe un registro con el ID dado."""
        cur = self.cursor
        cur.execute(
            f"SELECT COUNT(*) FROM {self._tabla} WHERE id = ?", (id,)
        )
        return cur.fetchone()[0] > 0

    def contar(self) -> int:
        """Retorna el total de registros en la tabla."""
        cur = self.cursor
        cur.execute(f"SELECT COUNT(*) FROM {self._tabla}")
        return cur.fetchone()[0]

    def _commit(self) -> None:
        """Confirma la transacción activa."""
        self._db.commit()

    def _rollback(self) -> None:
        """Revierte la transacción activa."""
        self._db.rollback()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} tabla='{self._tabla}'>"
