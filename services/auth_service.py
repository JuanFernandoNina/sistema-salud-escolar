"""
services/auth_service.py
Servicio de autenticación: login Admin y login de Estudiante.

Principios:
  - SRP  : única responsabilidad — autenticar usuarios.
  - DIP  : depende de UsuarioRepository y EstudianteRepository (abstracciones).
"""

import bcrypt
import logging
from typing import Optional, Tuple
from database.repositories.usuario_repository import UsuarioRepository
from database.repositories.estudiante_repository import EstudianteRepository
from models.usuario import Usuario
from models.estudiante import Estudiante

logger = logging.getLogger(__name__)


class AuthService:
    """Gestiona la autenticación de administradores y estudiantes."""

    def __init__(self) -> None:
        self._usuario_repo   = UsuarioRepository()
        self._estudiante_repo = EstudianteRepository()

    # ── Login Administrador ───────────────────────────────────────────────────

    def login_admin(
        self, username: str, password: str
    ) -> Optional[Usuario]:
        """
        Autentica un usuario administrador.
        Retorna el Usuario si las credenciales son válidas, None si no.
        """
        if not username or not password:
            return None
        usuario = self._usuario_repo.obtener_por_username(username)
        if not usuario:
            logger.warning(f"Login fallido — usuario no encontrado: {username}")
            return None
        if not usuario.es_admin():
            logger.warning(f"Login fallido — no es admin: {username}")
            return None
        if not self._verificar_password(password, usuario.password_hash):
            logger.warning(f"Login fallido — contraseña incorrecta: {username}")
            return None
        self._usuario_repo.actualizar_ultimo_acceso(usuario.id)
        logger.info(f"Login admin exitoso: {username}")
        return usuario

    # ── Login Estudiante (nombre / RUAT) ─────────────────────────────────────

    def login_estudiante(
        self, username: str, password: str
    ) -> Optional[Tuple[Usuario, Estudiante]]:
        """
        Autentica un estudiante por nombre de usuario.
        La contraseña del estudiante es su código RUAT.
        Retorna (Usuario, Estudiante) si es válido, None si no.
        """
        if not username or not password:
            return None
        usuario = self._usuario_repo.obtener_por_username(username)
        if not usuario or not usuario.es_estudiante():
            logger.warning(f"Login estudiante fallido — usuario: {username}")
            return None
        if not self._verificar_password(password, usuario.password_hash):
            logger.warning(f"Login estudiante fallido — password: {username}")
            return None
        estudiante = self._estudiante_repo.obtener_por_usuario_id(usuario.id)
        if not estudiante:
            logger.error(f"Usuario estudiante sin perfil: {username}")
            return None
        self._usuario_repo.actualizar_ultimo_acceso(usuario.id)
        logger.info(f"Login estudiante exitoso: {username}")
        return (usuario, estudiante)

    # ── Gestión de contraseñas ────────────────────────────────────────────────

    def hashear_password(self, password: str) -> str:
        """Genera el hash bcrypt de una contraseña en texto plano."""
        return bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def _verificar_password(self, password: str, hash_guardado: str) -> bool:
        """Verifica una contraseña contra su hash bcrypt."""
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"),
                hash_guardado.encode("utf-8"),
            )
        except Exception as e:
            logger.error(f"Error verificando contraseña: {e}")
            return False

    def cambiar_password(
        self, usuario_id: int, password_actual: str, password_nueva: str
    ) -> bool:
        """
        Cambia la contraseña de un usuario tras verificar la actual.
        Retorna True si el cambio fue exitoso.
        """
        usuario = self._usuario_repo.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado.")
        if not self._verificar_password(password_actual, usuario.password_hash):
            raise ValueError("La contraseña actual es incorrecta.")
        if len(password_nueva) < 6:
            raise ValueError("La nueva contraseña debe tener al menos 6 caracteres.")
        usuario.password_hash = self.hashear_password(password_nueva)
        self._usuario_repo.guardar(usuario)
        return True
