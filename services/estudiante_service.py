"""
services/estudiante_service.py
Lógica de negocio para gestión de estudiantes (RF01, RF02).
"""

from typing import Any, Dict, List, Optional
from services.base_service import BaseService
from database.repositories.estudiante_repository import EstudianteRepository
from database.repositories.usuario_repository import UsuarioRepository
from models.estudiante import Estudiante
import bcrypt
import logging

logger = logging.getLogger(__name__)


class EstudianteService(BaseService[Estudiante]):

    def __init__(self) -> None:
        super().__init__()
        self._repo         = EstudianteRepository()
        self._usuario_repo = UsuarioRepository()

    # ── Contrato BaseService ──────────────────────────────────────────────────

    def crear(self, datos: Dict[str, Any]) -> Estudiante:
        """
        Crea un estudiante y su usuario asociado (login nombre / RUAT).
        datos debe incluir: codigo_ruat, nombre, apellido,
        fecha_nacimiento, sexo, grado, seccion, password (opcional).
        """
        if self._repo.existe_ruat(datos.get("codigo_ruat", "")):
            raise ValueError(f"El código RUAT '{datos['codigo_ruat']}' ya existe.")

        # Crear usuario de acceso para el estudiante
        username = self._normalizar_username_estudiante(datos["nombre"])
        if self._usuario_repo.existe_username(username):
            raise ValueError(f"El usuario estudiante '{username}' ya existe.")

        password = datos.get("password") or datos.get("codigo_ruat", "est123")
        password_hash = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()
        ).decode()

        from models.usuario import Usuario
        usuario = Usuario(
            username=username,
            password_hash=password_hash,
            rol="estudiante",
        )
        usuario = self._usuario_repo.guardar(usuario)

        estudiante = Estudiante(
            codigo_ruat=datos["codigo_ruat"],
            nombre=datos["nombre"],
            apellido=datos["apellido"],
            fecha_nacimiento=datos["fecha_nacimiento"],
            sexo=datos["sexo"],
            grado=datos["grado"],
            seccion=datos.get("seccion", "A"),
            direccion=datos.get("direccion"),
            telefono_tutor=datos.get("telefono_tutor"),
            nombre_tutor=datos.get("nombre_tutor"),
            usuario_id=usuario.id,
        )
        return self._repo.guardar(estudiante)

    def actualizar(self, id: int, datos: Dict[str, Any]) -> Estudiante:
        estudiante = self._repo.obtener_por_id(id)
        if not estudiante:
            raise ValueError(f"Estudiante con id={id} no encontrado.")
        if "nombre" in datos and estudiante.usuario_id:
            username = self._normalizar_username_estudiante(datos["nombre"])
            if self._usuario_repo.existe_username(username, excluir_id=estudiante.usuario_id):
                raise ValueError(f"El usuario estudiante '{username}' ya existe.")
        for campo in ("nombre", "apellido", "fecha_nacimiento",
                      "sexo", "grado", "seccion",
                      "direccion", "telefono_tutor", "nombre_tutor"):
            if campo in datos:
                setattr(estudiante, f"_{campo}", datos[campo])
        estudiante = self._repo.guardar(estudiante)
        self._sincronizar_usuario_estudiante(estudiante)
        return estudiante

    def eliminar(self, id: int) -> bool:
        estudiante = self._repo.obtener_por_id(id)
        if not estudiante:
            raise ValueError(f"Estudiante con id={id} no encontrado.")
        eliminado = self._repo.eliminar(id)
        if eliminado and estudiante.usuario_id:
            usuario = self._usuario_repo.obtener_por_id(estudiante.usuario_id)
            if usuario:
                usuario.username = f"{usuario.username}_eliminado_{usuario.id}"
                self._usuario_repo.guardar(usuario)
            self._usuario_repo.eliminar(estudiante.usuario_id)
        return eliminado

    def obtener_por_id(self, id: int) -> Optional[Estudiante]:
        return self._repo.obtener_por_id(id)

    def obtener_todos(self) -> List[Estudiante]:
        return self._repo.obtener_todos()

    # ── Métodos adicionales ───────────────────────────────────────────────────

    def obtener_por_grado(self, grado: str) -> List[Estudiante]:
        return self._repo.obtener_por_grado(grado)

    def buscar(self, termino: str) -> List[Estudiante]:
        return self._repo.buscar(termino)

    def obtener_por_ruat(self, ruat: str) -> Optional[Estudiante]:
        return self._repo.obtener_por_ruat(ruat)

    def _normalizar_username_estudiante(self, nombre: str) -> str:
        username = (nombre or "").strip()
        if not username:
            raise ValueError("El nombre del estudiante es obligatorio para crear su usuario.")
        return username

    def _sincronizar_usuario_estudiante(self, estudiante: Estudiante) -> None:
        if not estudiante.usuario_id:
            return
        usuario = self._usuario_repo.obtener_por_id(estudiante.usuario_id)
        if not usuario:
            return
        username = self._normalizar_username_estudiante(estudiante.nombre)
        if self._usuario_repo.existe_username(username, excluir_id=usuario.id):
            raise ValueError(f"El usuario estudiante '{username}' ya existe.")
        if usuario.username != username:
            usuario.username = username
            self._usuario_repo.guardar(usuario)
