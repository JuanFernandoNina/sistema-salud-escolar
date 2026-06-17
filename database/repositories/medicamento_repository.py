"""
database/repositories/medicamento_repository.py
Repositorio para la tabla `medicamentos`.
"""

from typing import List, Optional
from database.repositories.base_repository import BaseRepository
from models.medicamento import Medicamento
import logging

logger = logging.getLogger(__name__)


class MedicamentoRepository(BaseRepository[Medicamento]):

    def __init__(self) -> None:
        super().__init__("medicamentos")

    def guardar(self, modelo: Medicamento) -> Medicamento:
        modelo.validate()
        if modelo.id is None:
            cur = self.cursor
            cur.execute(
                """INSERT INTO medicamentos
                   (nombre, descripcion, stock, unidad, stock_minimo, activo)
                   VALUES (?,?,?,?,?,?)""",
                (modelo.nombre, modelo.descripcion, modelo.stock,
                 modelo.unidad, modelo.stock_minimo, int(modelo.activo)),
            )
            self._commit()
            modelo._id = cur.lastrowid
        else:
            self.cursor.execute(
                """UPDATE medicamentos
                   SET nombre=?, descripcion=?, stock=?, unidad=?,
                       stock_minimo=?, activo=?
                   WHERE id=?""",
                (modelo.nombre, modelo.descripcion, modelo.stock,
                 modelo.unidad, modelo.stock_minimo,
                 int(modelo.activo), modelo.id),
            )
            self._commit()
        return modelo

    def obtener_por_id(self, id: int) -> Optional[Medicamento]:
        cur = self.cursor
        cur.execute("SELECT * FROM medicamentos WHERE id=?", (id,))
        fila = cur.fetchone()
        return self._fila_a_modelo(fila) if fila else None

    def obtener_todos(self) -> List[Medicamento]:
        cur = self.cursor
        cur.execute(
            "SELECT * FROM medicamentos WHERE activo=1 ORDER BY nombre"
        )
        return [self._fila_a_modelo(f) for f in cur.fetchall()]

    def eliminar(self, id: int) -> bool:
        self.cursor.execute(
            "UPDATE medicamentos SET activo=0 WHERE id=?", (id,)
        )
        self._commit()
        return True

    def _fila_a_modelo(self, fila) -> Medicamento:
        return Medicamento(
            id=fila["id"],
            nombre=fila["nombre"],
            descripcion=fila["descripcion"],
            stock=fila["stock"],
            unidad=fila["unidad"],
            stock_minimo=fila["stock_minimo"],
            activo=fila["activo"],
            creado_en=fila["creado_en"],
        )

    # ── Consultas específicas ─────────────────────────────────────────────────

    def obtener_con_stock_bajo(self) -> List[Medicamento]:
        """Retorna medicamentos donde stock <= stock_minimo."""
        cur = self.cursor
        cur.execute(
            """SELECT * FROM medicamentos
               WHERE activo=1 AND stock <= stock_minimo
               ORDER BY stock ASC""",
        )
        return [self._fila_a_modelo(f) for f in cur.fetchall()]

    def actualizar_stock(self, id: int, nuevo_stock: int) -> bool:
        self.cursor.execute(
            "UPDATE medicamentos SET stock=? WHERE id=?", (nuevo_stock, id)
        )
        self._commit()
        return True

    def buscar(self, termino: str) -> List[Medicamento]:
        like = f"%{termino}%"
        cur = self.cursor
        cur.execute(
            """SELECT * FROM medicamentos
               WHERE activo=1 AND (nombre LIKE ? OR descripcion LIKE ?)
               ORDER BY nombre""",
            (like, like),
        )
        return [self._fila_a_modelo(f) for f in cur.fetchall()]
