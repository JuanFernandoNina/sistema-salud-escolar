"""
controllers/base_controller.py
Utilidades comunes para la capa de controladores.
"""

from typing import Any, Callable, Dict, Iterable, Optional
import logging


class BaseController:
    """Base ligera para manejar errores y serializacion de respuestas."""

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    def _ok(self, data: Any = None, message: str = "") -> Dict[str, Any]:
        return {
            "success": True,
            "data": self._serialize(data),
            "message": message,
            "error": None,
        }

    def _fail(self, error: str) -> Dict[str, Any]:
        return {
            "success": False,
            "data": None,
            "message": "",
            "error": error,
        }

    def _handle(
        self,
        action: Callable[[], Any],
        message: str = "",
        not_found_message: Optional[str] = None,
    ) -> Dict[str, Any]:
        try:
            data = action()
            if data is None and not_found_message:
                return self._fail(not_found_message)
            return self._ok(data, message)
        except ValueError as exc:
            return self._fail(str(exc))
        except Exception as exc:
            self._logger.exception("Error inesperado en controlador")
            return self._fail(f"Error inesperado: {exc}")

    def _require_id(self, id_value: Any, field_name: str = "id") -> int:
        try:
            value = int(id_value)
        except (TypeError, ValueError):
            raise ValueError(f"{field_name} debe ser un numero entero.")
        if value <= 0:
            raise ValueError(f"{field_name} debe ser mayor a cero.")
        return value

    def _serialize(self, value: Any) -> Any:
        if hasattr(value, "to_dict"):
            return value.to_dict()
        if isinstance(value, dict):
            return {k: self._serialize(v) for k, v in value.items()}
        if isinstance(value, (list, tuple, set)):
            return [self._serialize(item) for item in value]
        if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
            return [self._serialize(item) for item in value]
        return value
