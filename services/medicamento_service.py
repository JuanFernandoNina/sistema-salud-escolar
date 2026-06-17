"""
services/medicamento_service.py
Lógica de negocio para inventario de medicamentos.
"""

from typing import Any, Dict, List, Optional
from services.base_service import BaseService
from database.repositories.medicamento_repository import MedicamentoRepository
from models.medicamento import Medicamento
import logging

logger = logging.getLogger(__name__)


class MedicamentoService(BaseService[Medicamento]):

    def __init__(self) -> None:
        super().__init__()
        self._repo = MedicamentoRepository()

    def crear(self, datos: Dict[str, Any]) -> Medicamento:
        med = Medicamento(
            nombre=datos["nombre"],
            descripcion=datos.get("descripcion"),
            stock=int(datos.get("stock", 0)),
            unidad=datos.get("unidad", "unidades"),
            stock_minimo=int(datos.get("stock_minimo", 5)),
        )
        return self._repo.guardar(med)

    def actualizar(self, id: int, datos: Dict[str, Any]) -> Medicamento:
        med = self._repo.obtener_por_id(id)
        if not med:
            raise ValueError(f"Medicamento id={id} no encontrado.")
        for campo in ("nombre", "descripcion", "stock",
                      "unidad", "stock_minimo"):
            if campo in datos:
                med.__dict__[f"_{campo}"] = datos[campo]
        return self._repo.guardar(med)

    def eliminar(self, id: int) -> bool:
        if not self._repo.existe(id):
            raise ValueError(f"Medicamento id={id} no encontrado.")
        return self._repo.eliminar(id)

    def obtener_por_id(self, id: int) -> Optional[Medicamento]:
        return self._repo.obtener_por_id(id)

    def obtener_todos(self) -> List[Medicamento]:
        return self._repo.obtener_todos()

    # ── Métodos específicos ───────────────────────────────────────────────────

    def ajustar_stock(self, id: int, cantidad: int) -> Medicamento:
        """Suma o resta cantidad al stock. Lanza ValueError si queda negativo."""
        med = self._repo.obtener_por_id(id)
        if not med:
            raise ValueError(f"Medicamento id={id} no encontrado.")
        med.ajustar_stock(cantidad)
        return self._repo.guardar(med)

    def obtener_con_stock_bajo(self) -> List[Medicamento]:
        return self._repo.obtener_con_stock_bajo()

    def buscar(self, termino: str) -> List[Medicamento]:
        return self._repo.buscar(termino)
