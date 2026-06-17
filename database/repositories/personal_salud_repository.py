"""
database/repositories/personal_salud_repository.py
Repositorio para la tabla `personal_salud`.
"""

from typing import List, Optional
from database.repositories.base_repository import BaseRepository
from models.personal_salud import PersonalSalud
import logging

logger = logging.getLogger(__name__)


class PersonalSaludRepository(BaseRepository[PersonalSalud]):

    def __init__(self) -> None:
        super().__init__("personal_salud")

    def guardar(self, modelo: PersonalSalud) -> PersonalSalud:
        modelo.validate()
        if modelo.id is None:
            cur = self.cursor
            cur.execute(
                """INSERT INTO personal_salud
                   (nombre, apellido, especialidad, matricula,
                    telefono, email, activo)
                   VALUES (?,?,?,?,?,?,?)""",
                (modelo.nombre, modelo.apellido, modelo.especialidad,
                 modelo.matricula, modelo.telefono,
                 modelo.email, int(modelo.activo)),
            )
            self._commit()
            modelo._id = cur.lastrowid
        else:
            self.cursor.execute(
                """UPDATE personal_salud
                   SET nombre=?, apellido=?, especialidad=?,
                       matricula=?, telefono=?, email=?, activo=?
                   WHERE id=?""",
                (modelo.nombre, modelo.apellido, modelo.especialidad,
                 modelo.matricula, modelo.telefono,
                 modelo.email, int(modelo.activo), modelo.id),
            )
            self._commit()
        return modelo

    def obtener_por_id(self, id: int) -> Optional[PersonalSalud]:
        cur = self.cursor
        cur.execute("SELECT * FROM personal_salud WHERE id=?", (id,))
        fila = cur.fetchone()
        return self._fila_a_modelo(fila) if fila else None

    def obtener_todos(self) -> List[PersonalSalud]:
        cur = self.cursor
        cur.execute(
            "SELECT * FROM personal_salud WHERE activo=1 ORDER BY apellido"
        )
        return [self._fila_a_modelo(f) for f in cur.fetchall()]

    def eliminar(self, id: int) -> bool:
        self.cursor.execute(
            "UPDATE personal_salud SET activo=0 WHERE id=?", (id,)
        )
        self._commit()
        return True

    def _fila_a_modelo(self, fila) -> PersonalSalud:
        return PersonalSalud(
            id=fila["id"],
            nombre=fila["nombre"],
            apellido=fila["apellido"],
            especialidad=fila["especialidad"],
            matricula=fila["matricula"],
            telefono=fila["telefono"],
            email=fila["email"],
            activo=fila["activo"],
            creado_en=fila["creado_en"],
        )

    # ── Consultas específicas ─────────────────────────────────────────────────

    def obtener_por_especialidad(self, especialidad: str) -> List[PersonalSalud]:
        cur = self.cursor
        cur.execute(
            """SELECT * FROM personal_salud
               WHERE especialidad=? AND activo=1 ORDER BY apellido""",
            (especialidad,),
        )
        return [self._fila_a_modelo(f) for f in cur.fetchall()]

    def buscar(self, termino: str) -> List[PersonalSalud]:
        like = f"%{termino}%"
        cur = self.cursor
        cur.execute(
            """SELECT * FROM personal_salud
               WHERE activo=1 AND (
                 nombre LIKE ? OR apellido LIKE ? OR especialidad LIKE ?
               )
               ORDER BY apellido""",
            (like, like, like),
        )
        return [self._fila_a_modelo(f) for f in cur.fetchall()]
