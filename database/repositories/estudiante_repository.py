"""
database/repositories/estudiante_repository.py
Repositorio para la tabla `estudiantes`.
"""

from typing import List, Optional
from database.repositories.base_repository import BaseRepository
from models.estudiante import Estudiante
import logging

logger = logging.getLogger(__name__)


class EstudianteRepository(BaseRepository[Estudiante]):

    def __init__(self) -> None:
        super().__init__("estudiantes")

    # ── Contrato BaseRepository ───────────────────────────────────────────────

    def guardar(self, modelo: Estudiante) -> Estudiante:
        modelo.validate()
        if modelo.id is None:
            cur = self.cursor
            cur.execute(
                """INSERT INTO estudiantes
                   (codigo_ruat, nombre, apellido, fecha_nacimiento, sexo,
                    grado, seccion, direccion, telefono_tutor, nombre_tutor,
                    usuario_id, activo)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (modelo.codigo_ruat, modelo.nombre, modelo.apellido,
                 modelo.fecha_nacimiento, modelo.sexo, modelo.grado,
                 modelo.seccion, modelo.direccion, modelo.telefono_tutor,
                 modelo.nombre_tutor, modelo.usuario_id, int(modelo.activo)),
            )
            self._commit()
            modelo._id = cur.lastrowid
        else:
            self.cursor.execute(
                """UPDATE estudiantes
                   SET nombre=?, apellido=?, fecha_nacimiento=?, sexo=?,
                       grado=?, seccion=?, direccion=?, telefono_tutor=?,
                       nombre_tutor=?, activo=?
                   WHERE id=?""",
                (modelo.nombre, modelo.apellido, modelo.fecha_nacimiento,
                 modelo.sexo, modelo.grado, modelo.seccion, modelo.direccion,
                 modelo.telefono_tutor, modelo.nombre_tutor,
                 int(modelo.activo), modelo.id),
            )
            self._commit()
        return modelo

    def obtener_por_id(self, id: int) -> Optional[Estudiante]:
        cur = self.cursor
        cur.execute("SELECT * FROM estudiantes WHERE id=?", (id,))
        fila = cur.fetchone()
        return self._fila_a_modelo(fila) if fila else None

    def obtener_todos(self) -> List[Estudiante]:
        cur = self.cursor
        cur.execute(
            "SELECT * FROM estudiantes WHERE activo=1 ORDER BY apellido, nombre"
        )
        return [self._fila_a_modelo(f) for f in cur.fetchall()]

    def eliminar(self, id: int) -> bool:
        self.cursor.execute(
            "UPDATE estudiantes SET activo=0 WHERE id=?", (id,)
        )
        self._commit()
        return True

    def _fila_a_modelo(self, fila) -> Estudiante:
        return Estudiante(
            id=fila["id"],
            codigo_ruat=fila["codigo_ruat"],
            nombre=fila["nombre"],
            apellido=fila["apellido"],
            fecha_nacimiento=fila["fecha_nacimiento"],
            sexo=fila["sexo"],
            grado=fila["grado"],
            seccion=fila["seccion"],
            direccion=fila["direccion"],
            telefono_tutor=fila["telefono_tutor"],
            nombre_tutor=fila["nombre_tutor"],
            usuario_id=fila["usuario_id"],
            activo=fila["activo"],
            creado_en=fila["creado_en"],
        )

    # ── Consultas específicas ─────────────────────────────────────────────────

    def obtener_por_ruat(self, codigo_ruat: str) -> Optional[Estudiante]:
        cur = self.cursor
        cur.execute(
            "SELECT * FROM estudiantes WHERE codigo_ruat=? AND activo=1",
            (codigo_ruat,),
        )
        fila = cur.fetchone()
        return self._fila_a_modelo(fila) if fila else None

    def obtener_por_usuario_id(self, usuario_id: int) -> Optional[Estudiante]:
        cur = self.cursor
        cur.execute(
            "SELECT * FROM estudiantes WHERE usuario_id=? AND activo=1",
            (usuario_id,),
        )
        fila = cur.fetchone()
        return self._fila_a_modelo(fila) if fila else None

    def obtener_por_grado(self, grado: str) -> List[Estudiante]:
        cur = self.cursor
        cur.execute(
            "SELECT * FROM estudiantes WHERE grado=? AND activo=1 ORDER BY apellido",
            (grado,),
        )
        return [self._fila_a_modelo(f) for f in cur.fetchall()]

    def buscar(self, termino: str) -> List[Estudiante]:
        like = f"%{termino}%"
        cur = self.cursor
        cur.execute(
            """SELECT * FROM estudiantes
               WHERE activo=1 AND (
                 nombre LIKE ? OR apellido LIKE ? OR codigo_ruat LIKE ?
               )
               ORDER BY apellido, nombre""",
            (like, like, like),
        )
        return [self._fila_a_modelo(f) for f in cur.fetchall()]

    def existe_ruat(self, codigo_ruat: str, excluir_id: int = None) -> bool:
        cur = self.cursor
        if excluir_id:
            cur.execute(
                "SELECT COUNT(*) FROM estudiantes WHERE codigo_ruat=? AND id!=?",
                (codigo_ruat, excluir_id),
            )
        else:
            cur.execute(
                "SELECT COUNT(*) FROM estudiantes WHERE codigo_ruat=?",
                (codigo_ruat,),
            )
        return cur.fetchone()[0] > 0
