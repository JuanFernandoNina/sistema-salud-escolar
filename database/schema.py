"""
database/schema.py
Define y ejecuta la creación de todas las tablas del sistema.

Principio SRP: este módulo solo se ocupa de la estructura de la BD.
Patrón: Script de migración / DDL centralizado.
"""

import logging
from database.connection import get_db

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
#  DDL — Sentencias CREATE TABLE
# ═══════════════════════════════════════════════════════════════════════════════

TABLAS = [

    # ── 1. usuarios ────────────────────────────────────────────────────────────
    """
    CREATE TABLE IF NOT EXISTS usuarios (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        username        TEXT    NOT NULL UNIQUE,
        password_hash   TEXT    NOT NULL,
        rol             TEXT    NOT NULL CHECK(rol IN ('admin','estudiante')),
        activo          INTEGER NOT NULL DEFAULT 1 CHECK(activo IN (0,1)),
        creado_en       TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
        ultimo_acceso   TEXT
    )
    """,

    # ── 2. estudiantes ─────────────────────────────────────────────────────────
    """
    CREATE TABLE IF NOT EXISTS estudiantes (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_ruat     TEXT    NOT NULL UNIQUE,
        nombre          TEXT    NOT NULL,
        apellido        TEXT    NOT NULL,
        fecha_nacimiento TEXT   NOT NULL,
        sexo            TEXT    NOT NULL CHECK(sexo IN ('M','F')),
        grado           TEXT    NOT NULL,
        seccion         TEXT    NOT NULL DEFAULT 'A',
        direccion       TEXT,
        telefono_tutor  TEXT,
        nombre_tutor    TEXT,
        usuario_id      INTEGER UNIQUE,
        activo          INTEGER NOT NULL DEFAULT 1 CHECK(activo IN (0,1)),
        creado_en       TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
    )
    """,

    # ── 3. personal_salud ──────────────────────────────────────────────────────
    """
    CREATE TABLE IF NOT EXISTS personal_salud (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre          TEXT    NOT NULL,
        apellido        TEXT    NOT NULL,
        especialidad    TEXT    NOT NULL,
        matricula       TEXT    UNIQUE,
        telefono        TEXT,
        email           TEXT,
        activo          INTEGER NOT NULL DEFAULT 1 CHECK(activo IN (0,1)),
        creado_en       TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
    )
    """,

    # ── 4. controles_salud ─────────────────────────────────────────────────────
    """
    CREATE TABLE IF NOT EXISTS controles_salud (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        estudiante_id   INTEGER NOT NULL,
        personal_id     INTEGER,
        fecha_control   TEXT    NOT NULL DEFAULT (date('now','localtime')),
        peso_kg         REAL    NOT NULL CHECK(peso_kg > 0),
        talla_m         REAL    NOT NULL CHECK(talla_m > 0),
        imc             REAL    GENERATED ALWAYS AS
                            (ROUND(peso_kg / (talla_m * talla_m), 2)) STORED,
        estado_nutricional TEXT GENERATED ALWAYS AS (
            CASE
                WHEN (peso_kg / (talla_m * talla_m)) < 18.5  THEN 'Bajo peso'
                WHEN (peso_kg / (talla_m * talla_m)) <= 24.9 THEN 'Normal'
                WHEN (peso_kg / (talla_m * talla_m)) <= 29.9 THEN 'Sobrepeso'
                ELSE 'Obesidad'
            END
        ) STORED,
        observaciones   TEXT,
        creado_en       TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
        FOREIGN KEY (personal_id)   REFERENCES personal_salud(id) ON DELETE SET NULL
    )
    """,

    # ── 5. medicamentos ────────────────────────────────────────────────────────
    """
    CREATE TABLE IF NOT EXISTS medicamentos (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre          TEXT    NOT NULL UNIQUE,
        descripcion     TEXT,
        stock           INTEGER NOT NULL DEFAULT 0 CHECK(stock >= 0),
        unidad          TEXT    NOT NULL DEFAULT 'unidades',
        stock_minimo    INTEGER NOT NULL DEFAULT 5,
        activo          INTEGER NOT NULL DEFAULT 1 CHECK(activo IN (0,1)),
        creado_en       TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
    )
    """,

    # ── 6. citas ───────────────────────────────────────────────────────────────
    """
    CREATE TABLE IF NOT EXISTS citas (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        estudiante_id   INTEGER NOT NULL,
        personal_id     INTEGER,
        fecha_cita      TEXT    NOT NULL,
        hora_cita       TEXT    NOT NULL DEFAULT '08:00',
        motivo          TEXT    NOT NULL,
        estado          TEXT    NOT NULL DEFAULT 'pendiente'
                            CHECK(estado IN ('pendiente','confirmada',
                                             'realizada','cancelada')),
        observaciones   TEXT,
        creado_en       TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
        FOREIGN KEY (personal_id)   REFERENCES personal_salud(id) ON DELETE SET NULL
    )
    """,

    # ── 7. reclamos ────────────────────────────────────────────────────────────
    """
    CREATE TABLE IF NOT EXISTS reclamos (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        estudiante_id   INTEGER NOT NULL,
        asunto          TEXT    NOT NULL,
        descripcion     TEXT    NOT NULL,
        estado          TEXT    NOT NULL DEFAULT 'pendiente'
                            CHECK(estado IN ('pendiente','en_revision',
                                             'resuelto','rechazado')),
        respuesta       TEXT,
        creado_en       TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
        resuelto_en     TEXT,
        FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE
    )
    """,
]

# ═══════════════════════════════════════════════════════════════════════════════
#  DDL — Índices para optimizar consultas frecuentes
# ═══════════════════════════════════════════════════════════════════════════════

INDICES = [
    "CREATE INDEX IF NOT EXISTS idx_estudiantes_ruat     ON estudiantes(codigo_ruat)",
    "CREATE INDEX IF NOT EXISTS idx_estudiantes_grado    ON estudiantes(grado)",
    "CREATE INDEX IF NOT EXISTS idx_controles_estudiante ON controles_salud(estudiante_id)",
    "CREATE INDEX IF NOT EXISTS idx_controles_fecha      ON controles_salud(fecha_control)",
    "CREATE INDEX IF NOT EXISTS idx_citas_estudiante     ON citas(estudiante_id)",
    "CREATE INDEX IF NOT EXISTS idx_citas_fecha          ON citas(fecha_cita)",
    "CREATE INDEX IF NOT EXISTS idx_citas_estado         ON citas(estado)",
    "CREATE INDEX IF NOT EXISTS idx_reclamos_estudiante  ON reclamos(estudiante_id)",
    "CREATE INDEX IF NOT EXISTS idx_reclamos_estado      ON reclamos(estado)",
    "CREATE INDEX IF NOT EXISTS idx_usuarios_rol         ON usuarios(rol)",
]

# ═══════════════════════════════════════════════════════════════════════════════
#  Función principal
# ═══════════════════════════════════════════════════════════════════════════════

def crear_tablas() -> None:
    """Crea todas las tablas e índices si no existen."""
    db = get_db()
    conn = db.get_connection()
    cursor = conn.cursor()

    try:
        logger.info("Iniciando creación de tablas...")
        for ddl in TABLAS:
            cursor.execute(ddl)
        logger.info(f"  ✔ {len(TABLAS)} tablas verificadas/creadas.")

        for idx in INDICES:
            cursor.execute(idx)
        logger.info(f"  ✔ {len(INDICES)} índices verificados/creados.")

        conn.commit()
        logger.info("Esquema de BD listo.")

    except Exception as e:
        conn.rollback()
        logger.error(f"Error creando tablas: {e}")
        raise
