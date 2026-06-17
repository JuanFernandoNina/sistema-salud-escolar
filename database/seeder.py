"""
database/seeder.py
Inserta datos iniciales para arrancar el sistema.

Incluye usuarios, estudiantes con RUAT numerico de 8 digitos,
personal de salud, medicamentos, controles, citas y reclamos.
"""

import logging

import bcrypt

from database.connection import get_db

logger = logging.getLogger(__name__)


def _hash(password: str) -> str:
    """Genera hash bcrypt de una contrasena."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12)).decode("utf-8")


ESTUDIANTES = [
    ("12345678", "Juan", "Perez", "2018-03-15", "M", "1ro", "A", "Av. Heroenas 123", "70011111", "Maria Perez", "12345678"),
    ("23456781", "Ana", "Mamani", "2018-07-22", "F", "1ro", "B", "Calle Sucre 456", "70022222", "Carlos Mamani", "23456781"),
    ("34567812", "Diego", "Quispe", "2017-11-05", "M", "1ro", "A", "Av. Blanco 789", "70033333", "Rosa Quispe", "34567812"),
    ("45678123", "Lucia", "Flores", "2017-02-10", "F", "1ro", "B", "Zona Norte 10", "70044444", "Elena Flores", "45678123"),
    ("56781234", "Mario", "Rojas", "2016-04-12", "M", "2do", "A", "Barrio Lindo 22", "70055555", "Marta Rojas", "56781234"),
    ("67812345", "Camila", "Vargas", "2016-08-30", "F", "2do", "B", "Calle Junin 18", "70066666", "Jose Vargas", "67812345"),
    ("78123456", "Sofia", "Torres", "2015-01-19", "F", "2do", "A", "Av. America 44", "70077777", "Laura Torres", "78123456"),
    ("81234567", "Mateo", "Cruz", "2015-10-03", "M", "2do", "B", "Calle Potosi 90", "70088888", "Pedro Cruz", "81234567"),
    ("13572468", "Valeria", "Aguilar", "2014-03-24", "F", "3ro", "A", "Villa Esperanza 6", "70111111", "Patricia Aguilar", "13572468"),
    ("24681357", "Andres", "Gutierrez", "2014-09-14", "M", "3ro", "B", "Calle Aroma 13", "70122222", "Hugo Gutierrez", "24681357"),
    ("31415926", "Natalia", "Soto", "2013-06-08", "F", "3ro", "A", "Av. Circunvalacion", "70133333", "Claudia Soto", "31415926"),
    ("27182818", "Bruno", "Lopez", "2013-12-01", "M", "3ro", "B", "Calle Beni 7", "70144444", "Ruben Lopez", "27182818"),
    ("10293847", "Daniela", "Rivera", "2012-05-05", "F", "4to", "A", "Av. Libertad 30", "70211111", "Gabriela Rivera", "10293847"),
    ("56473829", "Samuel", "Condori", "2012-11-16", "M", "4to", "B", "Calle La Paz 12", "70222222", "Felipe Condori", "56473829"),
    ("91827364", "Paola", "Mendoza", "2011-02-27", "F", "4to", "A", "Barrio Central 5", "70233333", "Silvia Mendoza", "91827364"),
    ("82736451", "Kevin", "Salazar", "2011-07-09", "M", "4to", "B", "Av. Petrolera 77", "70244444", "Nelson Salazar", "82736451"),
    ("19283746", "Gabriel", "Castro", "2010-04-18", "M", "5to", "A", "Calle Oruro 31", "70311111", "Carmen Castro", "19283746"),
    ("65748392", "Mariana", "Nina", "2010-09-26", "F", "5to", "B", "Av. Universitaria 15", "70322222", "Victor Nina", "65748392"),
    ("47382910", "Sebastian", "Herrera", "2009-01-12", "M", "5to", "A", "Calle Tarija 3", "70333333", "Teresa Herrera", "47382910"),
    ("83920174", "Eliana", "Choque", "2009-06-21", "F", "5to", "B", "Zona Sur 40", "70344444", "Miguel Choque", "83920174"),
    ("90817263", "Rodrigo", "Paz", "2008-02-02", "M", "6to", "A", "Av. Santa Cruz 55", "70411111", "Diana Paz", "90817263"),
    ("74635281", "Fernanda", "Molina", "2008-08-11", "F", "6to", "B", "Calle Cochabamba 20", "70422222", "Raul Molina", "74635281"),
    ("62514387", "Alvaro", "Medina", "2007-03-29", "M", "6to", "A", "Villa Fatima 8", "70433333", "Beatriz Medina", "62514387"),
    ("51428736", "Carla", "Arce", "2007-10-17", "F", "6to", "B", "Calle Murillo 60", "70444444", "Oscar Arce", "51428736"),
]


def seeder() -> None:
    """Inserta datos semilla si la BD esta vacia."""
    db = get_db()
    conn = db.get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT COUNT(*) FROM usuarios")
        if cur.fetchone()[0] > 0:
            _migrar_credenciales_estudiantes(cur)
            conn.commit()
            logger.info("Seeder omitido: la BD ya contiene datos.")
            return

        logger.info("Ejecutando seeder...")

        usuarios = [("admin", _hash("Admin123!"), "admin")]
        usuarios += [(nombre, _hash(password), "estudiante") for _ruat, nombre, *_rest, password in ESTUDIANTES]
        cur.executemany(
            "INSERT INTO usuarios (username, password_hash, rol) VALUES (?,?,?)",
            usuarios,
        )

        usuarios_por_nombre = {
            row["username"]: row["id"]
            for row in cur.execute("SELECT id, username FROM usuarios").fetchall()
        }

        estudiantes = [
            (
                ruat,
                nombre,
                apellido,
                fecha_nacimiento,
                sexo,
                grado,
                seccion,
                direccion,
                telefono_tutor,
                nombre_tutor,
                usuarios_por_nombre[nombre],
            )
            for (
                ruat,
                nombre,
                apellido,
                fecha_nacimiento,
                sexo,
                grado,
                seccion,
                direccion,
                telefono_tutor,
                nombre_tutor,
                _password,
            ) in ESTUDIANTES
        ]
        cur.executemany(
            """INSERT INTO estudiantes
               (codigo_ruat,nombre,apellido,fecha_nacimiento,sexo,
                grado,seccion,direccion,telefono_tutor,nombre_tutor,usuario_id)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            estudiantes,
        )

        personal = [
            ("Dra. Carmen", "Vasquez", "Medico General", "MP-1001", "70099001", "carmen@escuela.bo"),
            ("Lic. Pedro", "Quispe", "Nutricionista", "NP-2001", "70099002", "pedro@escuela.bo"),
            ("Enf. Julia", "Ramos", "Enfermeria Escolar", "EN-3001", "70099003", "julia@escuela.bo"),
        ]
        cur.executemany(
            """INSERT INTO personal_salud
               (nombre,apellido,especialidad,matricula,telefono,email)
               VALUES (?,?,?,?,?,?)""",
            personal,
        )

        medicamentos = [
            ("Paracetamol 500mg", "Analgesico y antipiretico", 50, "tabletas", 10),
            ("Ibuprofeno 200mg", "Antiinflamatorio y analgesico", 30, "tabletas", 10),
            ("Suero Oral", "Rehidratacion oral", 20, "sobres", 5),
            ("Vitamina C 250mg", "Suplemento vitaminico", 40, "tabletas", 8),
            ("Alcohol 70", "Antiseptico de uso externo", 10, "litros", 2),
            ("Gasas esteriles", "Material de curacion", 15, "paquetes", 5),
            ("Termometro digital", "Control de temperatura", 4, "unidades", 2),
            ("Jarabe para tos", "Alivio de tos seca", 3, "frascos", 5),
        ]
        cur.executemany(
            """INSERT INTO medicamentos
               (nombre,descripcion,stock,unidad,stock_minimo)
               VALUES (?,?,?,?,?)""",
            medicamentos,
        )

        estudiantes_db = cur.execute(
            "SELECT id, codigo_ruat, grado FROM estudiantes ORDER BY id"
        ).fetchall()
        personal_id = cur.execute(
            "SELECT id FROM personal_salud WHERE matricula='MP-1001'"
        ).fetchone()[0]

        controles = []
        citas = []
        reclamos = []
        for idx, est in enumerate(estudiantes_db):
            base_peso = 21 + idx * 1.7
            base_talla = 1.18 + min(idx * 0.025, 0.42)
            if idx % 6 == 1:
                pesos = [base_peso - 1.5, base_peso - 1.8, base_peso - 2.0]
                tallas = [base_talla, base_talla, base_talla + 0.01]
                obs = ["Peso bajo inicial.", "Bajo peso, derivar nutricionista.", "Bajo peso consecutivo."]
            elif idx % 6 == 4:
                pesos = [base_peso + 8.0, base_peso + 9.4, base_peso + 10.2]
                tallas = [base_talla, base_talla + 0.01, base_talla + 0.02]
                obs = ["Sobrepeso detectado.", "Seguimiento nutricional.", "Mantener control alimentario."]
            elif idx % 6 == 5:
                pesos = [base_peso, base_peso + 6.2, base_peso + 6.7]
                tallas = [base_talla, base_talla + 0.01, base_talla + 0.02]
                obs = ["Control normal.", "Variacion brusca de peso.", "Revisar habitos alimentarios."]
            else:
                pesos = [base_peso, base_peso + 0.8, base_peso + 1.3]
                tallas = [base_talla, base_talla + 0.02, base_talla + 0.04]
                obs = ["Control rutinario.", "Evolucion favorable.", "Estado general estable."]

            for fecha, peso, talla, observacion in zip(
                ("2026-02-15", "2026-04-15", "2026-06-15"),
                pesos,
                tallas,
                obs,
            ):
                controles.append((est["id"], personal_id, fecha, round(peso, 1), round(talla, 2), observacion))

            estado = "pendiente" if idx % 3 else "confirmada"
            citas.append(
                (
                    est["id"],
                    personal_id,
                    f"2026-07-{(idx % 24) + 1:02d}",
                    f"{8 + (idx % 8):02d}:00",
                    "Control de seguimiento escolar",
                    estado,
                    None,
                )
            )
            if idx % 5 == 0:
                reclamos.append(
                    (
                        est["id"],
                        "Consulta de seguimiento",
                        "Solicita revision del ultimo control de salud.",
                        "pendiente",
                        None,
                    )
                )

        cur.executemany(
            """INSERT INTO controles_salud
               (estudiante_id,personal_id,fecha_control,peso_kg,talla_m,observaciones)
               VALUES (?,?,?,?,?,?)""",
            controles,
        )
        cur.executemany(
            """INSERT INTO citas
               (estudiante_id,personal_id,fecha_cita,hora_cita,motivo,estado,observaciones)
               VALUES (?,?,?,?,?,?,?)""",
            citas,
        )
        cur.executemany(
            """INSERT INTO reclamos
               (estudiante_id,asunto,descripcion,estado,respuesta)
               VALUES (?,?,?,?,?)""",
            reclamos,
        )

        conn.commit()
        logger.info("Seeder completado exitosamente.")
        logger.info("Admin: admin / Admin123!")
        logger.info("Estudiante de prueba: Juan / 12345678")

    except Exception as e:
        conn.rollback()
        logger.error(f"Error en seeder: {e}")
        raise


def _migrar_credenciales_estudiantes(cur) -> None:
    """Alinea usuarios existentes al login nombre / RUAT."""
    filas = cur.execute(
        """SELECT e.id, e.codigo_ruat, e.nombre, e.usuario_id,
                  u.username, u.password_hash
           FROM estudiantes e
           JOIN usuarios u ON u.id = e.usuario_id
           WHERE e.activo=1 AND u.rol='estudiante' AND u.activo=1"""
    ).fetchall()

    for fila in filas:
        username = (fila["nombre"] or "").strip()
        if not username:
            continue

        existe = cur.execute(
            "SELECT id FROM usuarios WHERE username=? AND id!=?",
            (username, fila["usuario_id"]),
        ).fetchone()
        if existe:
            logger.warning(
                "No se migro usuario del estudiante id=%s: username duplicado '%s'.",
                fila["id"],
                username,
            )
            continue

        password_hash = fila["password_hash"]
        try:
            password_ok = bcrypt.checkpw(
                fila["codigo_ruat"].encode("utf-8"),
                password_hash.encode("utf-8"),
            )
        except Exception:
            password_ok = False
        if not password_ok:
            password_hash = _hash(fila["codigo_ruat"])

        cur.execute(
            "UPDATE usuarios SET username=?, password_hash=? WHERE id=?",
            (username, password_hash, fila["usuario_id"]),
        )
