"""
config/settings.py
Configuración central del sistema.
Principio: SRP — un único lugar para todas las constantes de configuración.
"""

import os

# ── Rutas base ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# ── Base de datos ────────────────────────────────────────────────────────────
DB_NAME = "salud_escolar.db"
DB_PATH = os.path.join(DATA_DIR, DB_NAME)

# ── Aplicación ───────────────────────────────────────────────────────────────
APP_NAME = "Sistema de Seguimiento de Salud Escolar"
APP_VERSION = "1.0.0"
APP_WIDTH = 1200
APP_HEIGHT = 700

# ── Colores UI ───────────────────────────────────────────────────────────────
COLOR_PRIMARY   = "#1E3A5F"   # Azul oscuro — sidebar, headers
COLOR_WHITE     = "#FFFFFF"   # Blanco — fondo principal
COLOR_GRAY      = "#F5F5F5"   # Gris claro — fondo secundario
COLOR_ACCENT    = "#2E86AB"   # Azul medio — botones activos
COLOR_DANGER    = "#E63946"   # Rojo — alertas y eliminar
COLOR_SUCCESS   = "#2A9D8F"   # Verde — éxito / estado normal
COLOR_WARNING   = "#E9C46A"   # Amarillo — advertencias
COLOR_TEXT_DARK = "#212121"   # Texto oscuro
COLOR_TEXT_LIGHT= "#ECEFF1"   # Texto sobre fondo oscuro

# ── Fuentes ───────────────────────────────────────────────────────────────────
FONT_FAMILY   = "Segoe UI"
FONT_TITLE    = (FONT_FAMILY, 18, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 13, "bold")
FONT_NORMAL   = (FONT_FAMILY, 11)
FONT_SMALL    = (FONT_FAMILY, 9)
FONT_BUTTON   = (FONT_FAMILY, 11, "bold")

# ── Seguridad ─────────────────────────────────────────────────────────────────
BCRYPT_ROUNDS = 12
SESSION_TIMEOUT_MIN = 30        # minutos de inactividad antes de cerrar sesión

# ── IMC — rangos simplificados para escolares ─────────────────────────────────
IMC_BAJO_PESO   = 18.5
IMC_NORMAL_MAX  = 24.9
IMC_SOBREPESO   = 29.9
# >= 30 → Obesidad

# ── Alertas ───────────────────────────────────────────────────────────────────
ALERTA_CONTROLES_SIN_CRECIMIENTO = 3   # controles sin aumento de talla
ALERTA_VARIACION_PESO_KG         = 5   # kg de variación brusca entre controles
ALERTA_BAJO_PESO_CONSECUTIVO     = 2   # controles consecutivos con bajo peso
