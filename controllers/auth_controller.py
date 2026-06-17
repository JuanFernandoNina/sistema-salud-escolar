"""
controllers/auth_controller.py
Controlador de autenticacion para administradores y estudiantes.
"""

from typing import Any, Dict
from controllers.base_controller import BaseController
from services.auth_service import AuthService


class AuthController(BaseController):
    """Coordina el login y cambio de password desde las vistas."""

    def __init__(self) -> None:
        super().__init__()
        self._service = AuthService()

    def login_admin(self, username: str, password: str) -> Dict[str, Any]:
        def action():
            usuario = self._service.login_admin(username.strip(), password)
            if not usuario:
                return None
            data = usuario.to_dict()
            data.pop("password_hash", None)
            return data

        return self._handle(
            action,
            message="Login de administrador exitoso.",
            not_found_message="Credenciales de administrador invalidas.",
        )

    def login_estudiante(self, username: str, password: str) -> Dict[str, Any]:
        def action():
            resultado = self._service.login_estudiante(username.strip(), password)
            if not resultado:
                return None
            usuario, estudiante = resultado
            usuario_data = usuario.to_dict()
            usuario_data.pop("password_hash", None)
            return {"usuario": usuario_data, "estudiante": estudiante.to_dict()}

        return self._handle(
            action,
            message="Login de estudiante exitoso.",
            not_found_message="Usuario o password invalidos.",
        )

    def cambiar_password(
        self, usuario_id: int, password_actual: str, password_nueva: str
    ) -> Dict[str, Any]:
        return self._handle(
            lambda: self._service.cambiar_password(
                self._require_id(usuario_id, "usuario_id"),
                password_actual,
                password_nueva,
            ),
            message="Password actualizado correctamente.",
        )
