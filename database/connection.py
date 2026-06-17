"""
database/connection.py
Gestión de la conexión SQLite mediante Singleton.

Patrones aplicados:
  - Singleton     : una sola instancia de DatabaseConnection en todo el sistema.
  - Context Manager: permite usar `with DatabaseConnection.get_instance() as conn`
                     para commits/rollbacks automáticos.

Principios SOLID:
  - SRP : solo gestiona la conexión, nada más.
  - OCP : extensible sin modificar (se puede heredar para otros motores).
"""

import sqlite3
import os
import logging
from typing import Optional
from config.settings import DB_PATH, DATA_DIR

# ── Logger ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


class DatabaseConnection:
    """
    Singleton que mantiene una única conexión SQLite activa.
    Thread-safe para uso en Tkinter (hilo principal único).
    """

    _instance: Optional["DatabaseConnection"] = None
    _connection: Optional[sqlite3.Connection] = None

    def __new__(cls) -> "DatabaseConnection":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # ── Interfaz pública ──────────────────────────────────────────────────────

    @classmethod
    def get_instance(cls) -> "DatabaseConnection":
        """Devuelve la única instancia del Singleton."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_connection(self) -> sqlite3.Connection:
        """
        Devuelve la conexión activa.
        La crea si no existe o si fue cerrada previamente.
        """
        if self._connection is None:
            self._connection = self._create_connection()
        return self._connection

    def get_cursor(self) -> sqlite3.Cursor:
        """Devuelve un cursor listo para ejecutar consultas."""
        return self.get_connection().cursor()

    def commit(self) -> None:
        """Confirma la transacción activa."""
        if self._connection:
            self._connection.commit()

    def rollback(self) -> None:
        """Revierte la transacción activa."""
        if self._connection:
            self._connection.rollback()
            logger.warning("Transacción revertida (rollback).")

    def close(self) -> None:
        """Cierra la conexión y limpia el Singleton."""
        if self._connection:
            self._connection.close()
            self._connection = None
            logger.info("Conexión SQLite cerrada.")

    # ── Context Manager ───────────────────────────────────────────────────────

    def __enter__(self) -> sqlite3.Connection:
        return self.get_connection()

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
            logger.error(f"Error en transacción: {exc_val}")
        return False   # no suprime la excepción

    # ── Método privado de creación ────────────────────────────────────────────

    def _create_connection(self) -> sqlite3.Connection:
        """
        Crea y configura la conexión SQLite.
        - Crea el directorio /data/ si no existe.
        - Activa claves foráneas (PRAGMA foreign_keys = ON).
        - Activa WAL para mejor concurrencia de lectura.
        - Devuelve filas como diccionarios (Row Factory).
        """
        os.makedirs(DATA_DIR, exist_ok=True)

        try:
            conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            conn.row_factory = sqlite3.Row          # acceso por nombre de columna
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA synchronous = NORMAL")
            conn.commit()
            logger.info(f"Conexión SQLite establecida → {DB_PATH}")
            return conn

        except sqlite3.Error as e:
            logger.critical(f"No se pudo conectar a la BD: {e}")
            raise


# ── Función de conveniencia ───────────────────────────────────────────────────

def get_db() -> DatabaseConnection:
    """
    Atajo global para obtener la instancia de la conexión.
    Uso: conn = get_db().get_connection()
         cursor = get_db().get_cursor()
    """
    return DatabaseConnection.get_instance()
