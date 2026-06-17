"""
database/repositories/reclamo_repository.py
Repositorio para la tabla `reclamos`.
"""

from typing import List, Optional
from database.repositories.base_repository import BaseRepository
from models.reclamo import Reclamo
import logging

logger = logging.getLogger(__name__)


class ReclamoRepository(BaseRepository[Reclamo]):

    def __init__(self) -> None:
        super().__init__("reclamos")

    def guardar(self, modelo: Reclamo) -> Reclamo:
        modelo.validate()
        if modelo.id is None:
            cur = self.cursor
            cur.execute(
                """INSERT INTO reclamos
                   (estudiante_id, asunto, descripcion, estado,
                    respuesta, resuelto_en)
                   VALUES (?,?,?,?,?,?)""",
                (modelo.estudiante_id, modelo.asunto, modelo.descripcion,
                 modelo.estado, modelo.respuesta, modelo.resuelto_en),
            )
            self._commit()
            modelo._id = cur.lastrowid
        else:
            self.cursor.execute(
                """UPDATE reclamos
                   SET asunto=?, descripcion=?, estado=?,
                       respuesta=?, resuelto_en=?
                   WHERE id=?""",
                (modelo.asunto, modelo.descripcion, modelo.estado,
                 modelo.respuesta, modelo.resuelto_en, modelo.id),
            )
            self._commit()
        return modelo

    def obtener_por_id(self, id: int) -> Optional[Reclamo]:
        cur = self.cursor
        cur.execute("SELECT * FROM reclamos WHERE id=?", (id,))
        fila = cur.fetchone()
        return self._fila_a_modelo(fila) if fila else None

    def obtener_todos(self) -> List[Reclamo]:
        cur = self.cursor
        cur.execute("SELECT * FROM reclamos ORDER BY creado_en DESC")
        return [self._fila_a_modelo(f) for f in cur.fetchall()]

    def eliminar(self, id: int) -> bool:
        self.cursor.execute("DELETE FROM reclamos WHERE id=?", (id,))
        self._commit()
        return True

    def _fila_a_modelo(self, fila) -> Reclamo:
        return Reclamo(
            id=fila["id"],
            estudiante_id=fila["estudiante_id"],
            asunto=fila["asunto"],
            descripcion=fila["descripcion"],
            estado=fila["estado"],
            respuesta=fila["respuesta"],
            resuelto_en=fila["resuelto_en"],
            creado_en=fila["creado_en"],
        )

    # ── Consultas específicas ─────────────────────────────────────────────────

    def obtener_por_estudiante(self, estudiante_id: int) -> List[Reclamo]:
        cur = self.cursor
        cur.execute(
            "SELECT * FROM reclamos WHERE estudiante_id=? ORDER BY creado_en DESC",
            (estudiante_id,),
        )
        return [self._fila_a_modelo(f) for f in cur.fetchall()]

    def obtener_por_estado(self, estado: str) -> List[Reclamo]:
        cur = self.cursor
        cur.execute(
            "SELECT * FROM reclamos WHERE estado=? ORDER BY creado_en DESC",
            (estado,),
        )
        return [self._fila_a_modelo(f) for f in cur.fetchall()]

    def obtener_pendientes(self) -> List[Reclamo]:
        return self.obtener_por_estado("pendiente")

    def resolver(self, id: int, respuesta: str) -> bool:
        self.cursor.execute(
            """UPDATE reclamos
               SET estado='resuelto', respuesta=?,
                   resuelto_en=datetime('now')
               WHERE id=?""",
            (respuesta, id),
        )
        self._commit()
        return True
