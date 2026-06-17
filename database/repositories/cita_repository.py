"""
database/repositories/cita_repository.py
Repositorio para la tabla `citas`.
"""

from typing import List, Optional
from database.repositories.base_repository import BaseRepository
from models.cita import Cita
import logging

logger = logging.getLogger(__name__)


class CitaRepository(BaseRepository[Cita]):

    def __init__(self) -> None:
        super().__init__("citas")

    # ── Contrato BaseRepository ───────────────────────────────────────────────

    def guardar(self, modelo: Cita) -> Cita:
        modelo.validate()
        if modelo.id is None:
            cur = self.cursor
            cur.execute(
                """INSERT INTO citas
                   (estudiante_id, personal_id, fecha_cita, hora_cita,
                    motivo, estado, observaciones)
                   VALUES (?,?,?,?,?,?,?)""",
                (modelo.estudiante_id, modelo.personal_id,
                 modelo.fecha_cita, modelo.hora_cita,
                 modelo.motivo, modelo.estado, modelo.observaciones),
            )
            self._commit()
            modelo._id = cur.lastrowid
        else:
            self.cursor.execute(
                """UPDATE citas
                   SET personal_id=?, fecha_cita=?, hora_cita=?,
                       motivo=?, estado=?, observaciones=?
                   WHERE id=?""",
                (modelo.personal_id, modelo.fecha_cita, modelo.hora_cita,
                 modelo.motivo, modelo.estado, modelo.observaciones,
                 modelo.id),
            )
            self._commit()
        return modelo

    def obtener_por_id(self, id: int) -> Optional[Cita]:
        cur = self.cursor
        cur.execute("SELECT * FROM citas WHERE id=?", (id,))
        fila = cur.fetchone()
        return self._fila_a_modelo(fila) if fila else None

    def obtener_todos(self) -> List[Cita]:
        cur = self.cursor
        cur.execute("SELECT * FROM citas ORDER BY fecha_cita DESC, hora_cita")
        return [self._fila_a_modelo(f) for f in cur.fetchall()]

    def eliminar(self, id: int) -> bool:
        self.cursor.execute("DELETE FROM citas WHERE id=?", (id,))
        self._commit()
        return True

    def _fila_a_modelo(self, fila) -> Cita:
        return Cita(
            id=fila["id"],
            estudiante_id=fila["estudiante_id"],
            personal_id=fila["personal_id"],
            fecha_cita=fila["fecha_cita"],
            hora_cita=fila["hora_cita"],
            motivo=fila["motivo"],
            estado=fila["estado"],
            observaciones=fila["observaciones"],
            creado_en=fila["creado_en"],
        )

    # ── Consultas específicas ─────────────────────────────────────────────────

    def obtener_por_estudiante(self, estudiante_id: int) -> List[Cita]:
        cur = self.cursor
        cur.execute(
            """SELECT * FROM citas WHERE estudiante_id=?
               ORDER BY fecha_cita DESC""",
            (estudiante_id,),
        )
        return [self._fila_a_modelo(f) for f in cur.fetchall()]

    def obtener_por_estado(self, estado: str) -> List[Cita]:
        cur = self.cursor
        cur.execute(
            "SELECT * FROM citas WHERE estado=? ORDER BY fecha_cita",
            (estado,),
        )
        return [self._fila_a_modelo(f) for f in cur.fetchall()]

    def obtener_pendientes(self) -> List[Cita]:
        return self.obtener_por_estado("pendiente")

    def obtener_por_fecha(self, fecha: str) -> List[Cita]:
        cur = self.cursor
        cur.execute(
            "SELECT * FROM citas WHERE fecha_cita=? ORDER BY hora_cita",
            (fecha,),
        )
        return [self._fila_a_modelo(f) for f in cur.fetchall()]

    def cambiar_estado(self, id: int, estado: str) -> bool:
        self.cursor.execute(
            "UPDATE citas SET estado=? WHERE id=?", (estado, id)
        )
        self._commit()
        return True
