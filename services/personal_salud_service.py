"""
services/personal_salud_service.py
Lógica de negocio para gestión de personal médico.
"""

from typing import Any, Dict, List, Optional
from services.base_service import BaseService
from database.repositories.personal_salud_repository import PersonalSaludRepository
from models.personal_salud import PersonalSalud
import logging

logger = logging.getLogger(__name__)


class PersonalSaludService(BaseService[PersonalSalud]):

    def __init__(self) -> None:
        super().__init__()
        self._repo = PersonalSaludRepository()

    def crear(self, datos: Dict[str, Any]) -> PersonalSalud:
        personal = PersonalSalud(
            nombre=datos["nombre"],
            apellido=datos["apellido"],
            especialidad=datos["especialidad"],
            matricula=datos.get("matricula"),
            telefono=datos.get("telefono"),
            email=datos.get("email"),
        )
        return self._repo.guardar(personal)

    def actualizar(self, id: int, datos: Dict[str, Any]) -> PersonalSalud:
        personal = self._repo.obtener_por_id(id)
        if not personal:
            raise ValueError(f"Personal id={id} no encontrado.")
        for campo in ("nombre", "apellido", "especialidad",
                      "matricula", "telefono", "email"):
            if campo in datos:
                personal.__dict__[f"_{campo}"] = datos[campo]
        return self._repo.guardar(personal)

    def eliminar(self, id: int) -> bool:
        if not self._repo.existe(id):
            raise ValueError(f"Personal id={id} no encontrado.")
        return self._repo.eliminar(id)

    def obtener_por_id(self, id: int) -> Optional[PersonalSalud]:
        return self._repo.obtener_por_id(id)

    def obtener_todos(self) -> List[PersonalSalud]:
        return self._repo.obtener_todos()

    def obtener_por_especialidad(self, especialidad: str) -> List[PersonalSalud]:
        return self._repo.obtener_por_especialidad(especialidad)

    def buscar(self, termino: str) -> List[PersonalSalud]:
        return self._repo.buscar(termino)
