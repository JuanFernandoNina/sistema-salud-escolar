"""
services/reporte_service.py
Generación de reportes individuales y por curso (RF07).
"""

from typing import Any, Dict, List, Optional
from database.repositories.estudiante_repository import EstudianteRepository
from database.repositories.control_salud_repository import ControlSaludRepository
from services.alerta_service import AlertaService
import logging

logger = logging.getLogger(__name__)


class ReporteService:
    """Genera reportes individuales y generales (RF07)."""

    def __init__(self) -> None:
        self._est_repo     = EstudianteRepository()
        self._control_repo = ControlSaludRepository()
        self._alerta_svc   = AlertaService()

    # ── Reporte individual (RF07) ─────────────────────────────────────────────

    def reporte_individual(self, estudiante_id: int) -> Dict[str, Any]:
        """
        Reporte completo de un estudiante:
        datos personales + historial de controles + alertas activas.
        """
        estudiante = self._est_repo.obtener_por_id(estudiante_id)
        if not estudiante:
            raise ValueError(f"Estudiante id={estudiante_id} no encontrado.")

        controles = self._control_repo.obtener_por_estudiante(estudiante_id)
        alertas   = self._alerta_svc.obtener_alertas_estudiante(estudiante_id)

        ultimo  = controles[-1] if controles else None
        evoluc  = [
            {
                "fecha":              c.fecha_control,
                "peso_kg":            c.peso_kg,
                "talla_m":            c.talla_m,
                "imc":                c.imc,
                "estado_nutricional": c.estado_nutricional,
            }
            for c in controles
        ]

        return {
            "estudiante":          estudiante.to_dict(),
            "edad":                estudiante.calcular_edad(),
            "total_controles":     len(controles),
            "ultimo_control":      ultimo.to_dict() if ultimo else None,
            "estado_nutricional":  ultimo.estado_nutricional if ultimo else "Sin datos",
            "imc_actual":          ultimo.imc if ultimo else None,
            "evolucion":           evoluc,
            "alertas":             alertas,
            "total_alertas":       len(alertas),
        }

    # ── Reporte por curso (RF07) ──────────────────────────────────────────────

    def reporte_por_curso(self, grado: str) -> Dict[str, Any]:
        """
        Reporte estadístico de todos los estudiantes de un grado.
        """
        estudiantes = self._est_repo.obtener_por_grado(grado)
        filas = []
        total_imc = 0.0
        conteo_imc = 0
        distribucion = {
            "Bajo peso": 0, "Normal": 0,
            "Sobrepeso": 0, "Obesidad": 0, "Sin datos": 0,
        }

        for est in estudiantes:
            ultimo = self._control_repo.obtener_ultimo_por_estudiante(est.id)
            alertas = self._alerta_svc.obtener_alertas_estudiante(est.id)
            estado = ultimo.estado_nutricional if ultimo else "Sin datos"
            imc    = ultimo.imc if ultimo else None

            distribucion[estado] = distribucion.get(estado, 0) + 1
            if imc:
                total_imc  += imc
                conteo_imc += 1

            filas.append({
                "id":                 est.id,
                "nombre_completo":    est.nombre_completo,
                "codigo_ruat":        est.codigo_ruat,
                "edad":               est.calcular_edad(),
                "sexo":               est.sexo,
                "ultimo_control":     ultimo.fecha_control if ultimo else "—",
                "imc":                imc,
                "estado_nutricional": estado,
                "total_alertas":      len(alertas),
            })

        return {
            "grado":              grado,
            "total_estudiantes":  len(estudiantes),
            "estudiantes":        filas,
            "distribucion_nutricional": distribucion,
            "imc_promedio":       round(total_imc / conteo_imc, 2)
                                  if conteo_imc else None,
        }

    # ── Resumen general para Dashboard ───────────────────────────────────────

    def resumen_dashboard(self) -> Dict[str, Any]:
        """Estadísticas rápidas para el panel del administrador."""
        from database.repositories.cita_repository import CitaRepository
        from database.repositories.medicamento_repository import MedicamentoRepository
        from database.repositories.reclamo_repository import ReclamoRepository

        est_total    = self._est_repo.contar()
        alertas_tot  = self._alerta_svc.contar_alertas_activas()
        citas_pend   = len(CitaRepository().obtener_pendientes())
        stock_bajo   = len(MedicamentoRepository().obtener_con_stock_bajo())
        reclamos_p   = len(ReclamoRepository().obtener_pendientes())

        return {
            "total_estudiantes":  est_total,
            "alertas_activas":    alertas_tot,
            "citas_pendientes":   citas_pend,
            "medicamentos_bajos": stock_bajo,
            "reclamos_pendientes": reclamos_p,
        }
