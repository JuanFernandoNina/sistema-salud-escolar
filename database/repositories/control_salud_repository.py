"""
database/repositories/control_salud_repository.py
Repositorio para la tabla `controles_salud`.
"""

from typing import List, Optional
from database.repositories.base_repository import BaseRepository
from models.control_salud import ControlSalud
import logging

logger = logging.getLogger(__name__)


class ControlSaludRepository(BaseRepository[ControlSalud]):

    def __init__(self) -> None:
        super().__init__("controles_salud")

    # ── Contrato BaseRepository ───────────────────────────────────────────────

    def guardar(self, modelo: ControlSalud) -> ControlSalud:
        modelo.validate()
        if modelo.id is None:
            cur = self.cursor
            cur.execute(
                """INSERT INTO controles_salud
                   (estudiante_id, personal_id, fecha_control,
                    peso_kg, talla_m, observaciones)
                   VALUES (?,?,?,?,?,?)""",
                (modelo.estudiante_id, modelo.personal_id,
                 modelo.fecha_control, modelo.peso_kg,
                 modelo.talla_m, modelo.observaciones),
            )
            self._commit()
            modelo._id = cur.lastrowid
        else:
            self.cursor.execute(
                """UPDATE controles_salud
                   SET personal_id=?, fecha_control=?, peso_kg=?,
                       talla_m=?, observaciones=?
                   WHERE id=?""",
                (modelo.personal_id, modelo.fecha_control,
                 modelo.peso_kg, modelo.talla_m,
                 modelo.observaciones, modelo.id),
            )
            self._commit()
        return modelo

    def obtener_por_id(self, id: int) -> Optional[ControlSalud]:
        cur = self.cursor
        cur.execute("SELECT * FROM controles_salud WHERE id=?", (id,))
        fila = cur.fetchone()
        return self._fila_a_modelo(fila) if fila else None

    def obtener_todos(self) -> List[ControlSalud]:
        cur = self.cursor
        cur.execute(
            "SELECT * FROM controles_salud ORDER BY fecha_control DESC"
        )
        return [self._fila_a_modelo(f) for f in cur.fetchall()]

    def eliminar(self, id: int) -> bool:
        self.cursor.execute("DELETE FROM controles_salud WHERE id=?", (id,))
        self._commit()
        return True

    def _fila_a_modelo(self, fila) -> ControlSalud:
        return ControlSalud(
            id=fila["id"],
            estudiante_id=fila["estudiante_id"],
            personal_id=fila["personal_id"],
            fecha_control=fila["fecha_control"],
            peso_kg=fila["peso_kg"],
            talla_m=fila["talla_m"],
            observaciones=fila["observaciones"],
            creado_en=fila["creado_en"],
        )

    # ── Consultas específicas ─────────────────────────────────────────────────

    def obtener_por_estudiante(self, estudiante_id: int) -> List[ControlSalud]:
        cur = self.cursor
        cur.execute(
            """SELECT * FROM controles_salud
               WHERE estudiante_id=?
               ORDER BY fecha_control ASC""",
            (estudiante_id,),
        )
        return [self._fila_a_modelo(f) for f in cur.fetchall()]

    def obtener_ultimo_por_estudiante(
        self, estudiante_id: int
    ) -> Optional[ControlSalud]:
        cur = self.cursor
        cur.execute(
            """SELECT * FROM controles_salud
               WHERE estudiante_id=?
               ORDER BY fecha_control DESC LIMIT 1""",
            (estudiante_id,),
        )
        fila = cur.fetchone()
        return self._fila_a_modelo(fila) if fila else None

    def obtener_ultimos_n(
        self, estudiante_id: int, n: int = 3
    ) -> List[ControlSalud]:
        cur = self.cursor
        cur.execute(
            """SELECT * FROM controles_salud
               WHERE estudiante_id=?
               ORDER BY fecha_control DESC LIMIT ?""",
            (estudiante_id, n),
        )
        return [self._fila_a_modelo(f) for f in cur.fetchall()]

    def obtener_por_rango_fecha(
        self, fecha_inicio: str, fecha_fin: str
    ) -> List[ControlSalud]:
        cur = self.cursor
        cur.execute(
            """SELECT * FROM controles_salud
               WHERE fecha_control BETWEEN ? AND ?
               ORDER BY fecha_control DESC""",
            (fecha_inicio, fecha_fin),
        )
        return [self._fila_a_modelo(f) for f in cur.fetchall()]
