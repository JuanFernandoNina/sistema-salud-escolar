"""
database/repositories/usuario_repository.py
Repositorio para la tabla `usuarios`.

Principios:
  - SRP        : solo acceso a datos de usuarios.
  - Repository : abstrae SQLite del resto del sistema.
  - DIP        : AuthService depende de esta abstracción.
"""

from typing import List, Optional
from database.repositories.base_repository import BaseRepository
from models.usuario import Usuario
import logging

logger = logging.getLogger(__name__)


class UsuarioRepository(BaseRepository[Usuario]):

    def __init__(self) -> None:
        super().__init__("usuarios")

    # ── Contrato BaseRepository ───────────────────────────────────────────────

    def guardar(self, modelo: Usuario) -> Usuario:
        modelo.validate()
        if modelo.id is None:
            cur = self.cursor
            cur.execute(
                """INSERT INTO usuarios (username, password_hash, rol, activo)
                   VALUES (?, ?, ?, ?)""",
                (modelo.username, modelo.password_hash,
                 modelo.rol, int(modelo.activo)),
            )
            self._commit()
            modelo._id = cur.lastrowid
            logger.info(f"Usuario creado id={modelo.id}")
        else:
            self.cursor.execute(
                """UPDATE usuarios
                   SET username=?, password_hash=?, rol=?, activo=?,
                       ultimo_acceso=?
                   WHERE id=?""",
                (modelo.username, modelo.password_hash, modelo.rol,
                 int(modelo.activo), modelo.ultimo_acceso, modelo.id),
            )
            self._commit()
            logger.info(f"Usuario actualizado id={modelo.id}")
        return modelo

    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        cur = self.cursor
        cur.execute("SELECT * FROM usuarios WHERE id=?", (id,))
        fila = cur.fetchone()
        return self._fila_a_modelo(fila) if fila else None

    def obtener_todos(self) -> List[Usuario]:
        cur = self.cursor
        cur.execute("SELECT * FROM usuarios WHERE activo=1 ORDER BY username")
        return [self._fila_a_modelo(f) for f in cur.fetchall()]

    def eliminar(self, id: int) -> bool:
        self.cursor.execute(
            "UPDATE usuarios SET activo=0 WHERE id=?", (id,)
        )
        self._commit()
        return True

    def _fila_a_modelo(self, fila) -> Usuario:
        return Usuario(
            id=fila["id"],
            username=fila["username"],
            password_hash=fila["password_hash"],
            rol=fila["rol"],
            activo=fila["activo"],
            creado_en=fila["creado_en"],
            ultimo_acceso=fila["ultimo_acceso"],
        )

    # ── Consultas específicas ─────────────────────────────────────────────────

    def obtener_por_username(self, username: str) -> Optional[Usuario]:
        cur = self.cursor
        cur.execute(
            "SELECT * FROM usuarios WHERE username=? AND activo=1", (username,)
        )
        fila = cur.fetchone()
        return self._fila_a_modelo(fila) if fila else None

    def existe_username(self, username: str, excluir_id: int = None) -> bool:
        cur = self.cursor
        if excluir_id:
            cur.execute(
                "SELECT COUNT(*) FROM usuarios WHERE username=? AND id!=?",
                (username, excluir_id),
            )
        else:
            cur.execute(
                "SELECT COUNT(*) FROM usuarios WHERE username=?", (username,)
            )
        return cur.fetchone()[0] > 0

    def actualizar_ultimo_acceso(self, id: int) -> None:
        self.cursor.execute(
            "UPDATE usuarios SET ultimo_acceso=datetime('now') WHERE id=?",
            (id,),
        )
        self._commit()
