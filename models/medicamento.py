"""
models/medicamento.py
Modelo de dominio para la tabla `medicamentos`.

Principios aplicados:
  - Encapsulamiento : stock protegido, no puede ser negativo.
  - SRP             : representa únicamente un medicamento del botiquín.
  - Herencia        : extiende BaseModel.
"""

from typing import Any, Dict, Optional
from models.base_model import BaseModel


class Medicamento(BaseModel):
    """Representa un medicamento del inventario escolar."""

    def __init__(
        self,
        nombre:       str,
        stock:        int  = 0,
        unidad:       str  = "unidades",
        stock_minimo: int  = 5,
        descripcion:  Optional[str] = None,
        id:           Optional[int] = None,
        activo:       int  = 1,
        creado_en:    Optional[str] = None,
    ) -> None:
        super().__init__(id, creado_en)
        self._nombre       = nombre
        self._descripcion  = descripcion
        self._stock        = stock
        self._unidad       = unidad
        self._stock_minimo = stock_minimo
        self._activo       = bool(activo)

    # ── Propiedades ───────────────────────────────────────────────────────────

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, v: str) -> None:
        if not v or not v.strip():
            raise ValueError("El nombre del medicamento no puede estar vacío.")
        self._nombre = v.strip()

    @property
    def descripcion(self) -> Optional[str]:
        return self._descripcion

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, v: int) -> None:
        if v < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._stock = v

    @property
    def unidad(self) -> str:
        return self._unidad

    @property
    def stock_minimo(self) -> int:
        return self._stock_minimo

    @property
    def activo(self) -> bool:
        return self._activo

    # ── Contrato BaseModel ────────────────────────────────────────────────────

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":           self._id,
            "nombre":       self._nombre,
            "descripcion":  self._descripcion,
            "stock":        self._stock,
            "unidad":       self._unidad,
            "stock_minimo": self._stock_minimo,
            "activo":       int(self._activo),
            "creado_en":    self._creado_en,
        }

    def validate(self) -> bool:
        if not self._nombre or not self._nombre.strip():
            raise ValueError("El nombre del medicamento es obligatorio.")
        if self._stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        if self._stock_minimo < 0:
            raise ValueError("El stock mínimo no puede ser negativo.")
        return True

    # ── Helpers ───────────────────────────────────────────────────────────────

    def tiene_stock_bajo(self) -> bool:
        """Retorna True si el stock está por debajo del mínimo."""
        return self._stock <= self._stock_minimo

    def ajustar_stock(self, cantidad: int) -> None:
        """
        Ajusta el stock sumando o restando.
        Lanza ValueError si el resultado es negativo.
        """
        nuevo = self._stock + cantidad
        if nuevo < 0:
            raise ValueError(
                f"Stock insuficiente. Disponible: {self._stock}, "
                f"solicitado: {abs(cantidad)}"
            )
        self._stock = nuevo

    def __repr__(self) -> str:
        return (f"<Medicamento id={self._id} "
                f"nombre='{self._nombre}' stock={self._stock}>")
