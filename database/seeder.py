"""
database/seeder.py
Inserta datos iniciales (semilla) para arrancar el sistema.

Incluye:
  - Usuario administrador por defecto
  - 3 estudiantes de ejemplo con sus usuarios RUAT
  - 2 personal de salud
  - 5 medicamentos básicos
  - Controles de salud de ejemplo
  - 2 citas de ejemplo

Principio SRP: solo responsable de poblar datos iniciales.
"""

import logging
import bcrypt
from database.connection import get_db

logger = logging.getLogger(__name__)


def _hash(password: str) -> str:
    """Genera hash bcrypt de una contraseña."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(12)).decode()


def seeder() -> None:
    """Inserta datos semilla si la BD está vacía."""
    db = get_db()
    conn = db.get_connection()
    cur = conn.cursor()

    try:
        # ── Verificar si ya hay datos ─────────────────────────────────────────
        cur.execute("SELECT COUNT(*) FROM usuarios")
        if cur.fetchone()[0] > 0:
            logger.info("Seeder omitido: la BD ya contiene datos.")
            return

        logger.info("Ejecutando seeder...")

        # ── 1. Usuarios ───────────────────────────────────────────────────────
        usuarios = [
            ("admin",    _hash("Admin123!"),  "admin"),
            ("RUAT-001", _hash("est001"),     "estudiante"),
            ("RUAT-002", _hash("est002"),     "estudiante"),
            ("RUAT-003", _hash("est003"),     "estudiante"),
        ]
        cur.executemany(
            "INSERT INTO usuarios (username, password_hash, rol) VALUES (?,?,?)",
            usuarios
        )
        logger.info("  ✔ Usuarios insertados.")

        # ── 2. Estudiantes ────────────────────────────────────────────────────
        cur.execute("SELECT id FROM usuarios WHERE username='RUAT-001'")
        uid1 = cur.fetchone()[0]
        cur.execute("SELECT id FROM usuarios WHERE username='RUAT-002'")
        uid2 = cur.fetchone()[0]
        cur.execute("SELECT id FROM usuarios WHERE username='RUAT-003'")
        uid3 = cur.fetchone()[0]

        estudiantes = [
            ("RUAT-001","Juan","Pérez",    "2012-03-15","M","4to","A",
             "Av. Heroínas 123","70011111","María Pérez", uid1),
            ("RUAT-002","Ana","Mamani",    "2013-07-22","F","3ro","B",
             "Calle Sucre 456", "70022222","Carlos Mamani", uid2),
            ("RUAT-003","Luis","Flores",   "2011-11-05","M","5to","A",
             "Av. Blanco 789",  "70033333","Rosa Flores", uid3),
        ]
        cur.executemany(
            """INSERT INTO estudiantes
               (codigo_ruat,nombre,apellido,fecha_nacimiento,sexo,
                grado,seccion,direccion,telefono_tutor,nombre_tutor,usuario_id)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            estudiantes
        )
        logger.info("  ✔ Estudiantes insertados.")

        # ── 3. Personal de salud ──────────────────────────────────────────────
        personal = [
            ("Dra. Carmen","Vásquez","Médico General","MP-1001",
             "70099001","carmen@escuela.bo"),
            ("Lic. Pedro","Quispe","Nutricionista","NP-2001",
             "70099002","pedro@escuela.bo"),
        ]
        cur.executemany(
            """INSERT INTO personal_salud
               (nombre,apellido,especialidad,matricula,telefono,email)
               VALUES (?,?,?,?,?,?)""",
            personal
        )
        logger.info("  ✔ Personal de salud insertado.")

        # ── 4. Medicamentos ───────────────────────────────────────────────────
        medicamentos = [
            ("Paracetamol 500mg", "Analgésico y antipirético",     50, "tabletas", 10),
            ("Ibuprofeno 200mg",  "Antiinflamatorio y analgésico", 30, "tabletas", 10),
            ("Suero Oral",        "Rehidratación oral",            20, "sobres",    5),
            ("Vitamina C 250mg",  "Suplemento vitamínico",         40, "tabletas",  8),
            ("Alcohol 70°",       "Antiséptico de uso externo",    10, "litros",    2),
        ]
        cur.executemany(
            """INSERT INTO medicamentos
               (nombre,descripcion,stock,unidad,stock_minimo)
               VALUES (?,?,?,?,?)""",
            medicamentos
        )
        logger.info("  ✔ Medicamentos insertados.")

        # ── 5. Controles de salud ─────────────────────────────────────────────
        # Recuperar IDs
        cur.execute("SELECT id FROM estudiantes WHERE codigo_ruat='RUAT-001'")
        eid1 = cur.fetchone()[0]
        cur.execute("SELECT id FROM estudiantes WHERE codigo_ruat='RUAT-002'")
        eid2 = cur.fetchone()[0]
        cur.execute("SELECT id FROM estudiantes WHERE codigo_ruat='RUAT-003'")
        eid3 = cur.fetchone()[0]
        cur.execute("SELECT id FROM personal_salud WHERE matricula='MP-1001'")
        pid1 = cur.fetchone()[0]

        controles = [
            # (estudiante_id, personal_id, fecha, peso_kg, talla_m, obs)
            (eid1, pid1, "2025-03-10", 32.5, 1.40, "Control rutinario. Normal."),
            (eid1, pid1, "2025-06-15", 33.0, 1.41, "Leve mejoría de peso."),
            (eid1, pid1, "2025-09-20", 33.8, 1.42, "Evolución favorable."),
            (eid2, pid1, "2025-03-12", 28.0, 1.35, "Peso ligeramente bajo."),
            (eid2, pid1, "2025-06-18", 27.5, 1.35, "Sin aumento de peso. Derivar nutricionista."),
            (eid2, pid1, "2025-09-22", 27.0, 1.36, "Bajo peso consecutivo. Alerta generada."),
            (eid3, pid1, "2025-03-08", 45.0, 1.55, "Sobrepeso detectado."),
            (eid3, pid1, "2025-06-10", 46.5, 1.55, "Sin cambio de talla. Derivar."),
            (eid3, pid1, "2025-09-15", 47.0, 1.56, "Mejora leve de talla."),
        ]
        cur.executemany(
            """INSERT INTO controles_salud
               (estudiante_id,personal_id,fecha_control,peso_kg,talla_m,observaciones)
               VALUES (?,?,?,?,?,?)""",
            controles
        )
        logger.info("  ✔ Controles de salud insertados.")

        # ── 6. Citas ──────────────────────────────────────────────────────────
        citas = [
            (eid1, pid1, "2026-07-05", "09:00",
             "Control semestral",    "confirmada",  None),
            (eid2, pid1, "2026-07-06", "10:00",
             "Seguimiento bajo peso","pendiente",   None),
            (eid3, pid1, "2026-07-07", "11:00",
             "Control de sobrepeso", "pendiente",   None),
        ]
        cur.executemany(
            """INSERT INTO citas
               (estudiante_id,personal_id,fecha_cita,hora_cita,
                motivo,estado,observaciones)
               VALUES (?,?,?,?,?,?,?)""",
            citas
        )
        logger.info("  ✔ Citas insertadas.")

        conn.commit()
        logger.info("✅ Seeder completado exitosamente.")
        logger.info("   Admin → usuario: admin  |  contraseña: Admin123!")
        logger.info("   Estudiante 1 → RUAT-001 |  contraseña: est001")
        logger.info("   Estudiante 2 → RUAT-002 |  contraseña: est002")
        logger.info("   Estudiante 3 → RUAT-003 |  contraseña: est003")

    except Exception as e:
        conn.rollback()
        logger.error(f"Error en seeder: {e}")
        raise
