# 📁 app/models — Documentación de Modelos

Este módulo contiene todas las **clases del sistema** organizadas con
Programación Orientada a Objetos (POO). Aquí vive la lógica de negocio
pura, separada completamente de la base de datos y las vistas.

---

## 📌 Índice

- [Estructura del módulo](#estructura-del-módulo)
- [Principios de POO aplicados](#principios-de-poo-aplicados)
- [Jerarquía de clases](#jerarquía-de-clases)
- [Clases con herencia](#clases-con-herencia)
  - [Persona (abstracta)](#1-persona--abstracta)
  - [Estudiante](#2-estudiante)
  - [Doctor](#3-doctor)
  - [Nutricionista](#4-nutricionista)
- [Clases de entidad](#clases-de-entidad)
  - [ControlSalud](#5-controlsalud)
  - [Reclamo](#6-reclamo)
  - [Consulta](#7-consulta)
  - [Cita](#8-cita)
- [Cómo importar las clases](#cómo-importar-las-clases)
- [Ejemplos de uso](#ejemplos-de-uso)

---

## Estructura del módulo

```
app/models/
│
├── __init__.py        ← Exporta todas las clases (punto de entrada)
├── persona.py         ← Clase abstracta base (ABC)
├── estudiante.py      ← Hereda de Persona
├── doctor.py          ← Hereda de Persona
├── nutricionista.py   ← Hereda de Persona
├── control_salud.py   ← Entidad de datos
├── reclamo.py         ← Entidad de datos
├── consulta.py        ← Entidad de datos
└── cita.py            ← Entidad de datos
```

---

## Principios de POO aplicados

### 🔷 Abstracción
`Persona` es una clase abstracta (`ABC`). No se puede instanciar directamente.
Solo define la **estructura obligatoria** que deben cumplir las clases derivadas.
Esto garantiza que todo usuario del sistema tenga al menos nombre, usuario,
contraseña y sepa iniciar sesión.

```python
# ESTO genera error — Persona es abstracta:
p = Persona("Juan", 20, "M", "juan01", "1234")  # ❌ TypeError

# ESTO sí funciona — se usa una clase concreta:
e = Estudiante("Juan", 15, "M", "juan01", "1234", "RUD-001", "3ro A", "Colegio Bolívar")  # ✅
```

### 🔷 Herencia
`Estudiante`, `Doctor` y `Nutricionista` **heredan** de `Persona`.
Esto significa que reciben automáticamente todos los atributos y métodos
de `Persona` sin tener que reescribirlos.

```
Persona (abstracta)
    ├── Estudiante
    ├── Doctor
    └── Nutricionista
```

### 🔷 Encapsulamiento
Todos los atributos son **privados** (doble guion bajo `__`).
Solo se accede a ellos a través de `@property` (getters) y setters con validación.

```python
# Acceso correcto mediante getter:
print(estudiante.nombre)       # ✅ "Juan"

# Acceso directo está bloqueado por Python:
print(estudiante.__nombre)     # ❌ AttributeError
```

### 🔷 Polimorfismo
`iniciar_sesion()` y `mostrar_perfil()` están definidos en `Persona` como abstractos,
pero **cada clase los implementa de forma diferente**:

| Clase         | `iniciar_sesion()`                        | `mostrar_perfil()`                        |
|---------------|-------------------------------------------|-------------------------------------------|
| `Estudiante`  | Valida con código/RUDE + contraseña       | Devuelve datos + curso + controles        |
| `Doctor`      | Valida con usuario institucional          | Devuelve datos + especialidad + matrícula |
| `Nutricionista` | Valida con usuario institucional        | Devuelve datos + estudiantes a cargo      |

---

## Jerarquía de clases

```
                    ┌─────────────────────┐
                    │   Persona  «ABC»    │
                    │─────────────────────│
                    │ - nombre            │
                    │ - edad              │
                    │ - sexo              │
                    │ - usuario           │
                    │ - contraseña        │
                    │─────────────────────│
                    │ + iniciar_sesion()  │  ← abstracto
                    │ + mostrar_perfil()  │  ← abstracto
                    │ + verificar_clave() │  ← concreto
                    └──────────┬──────────┘
                               │  hereda
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
     ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
     │  Estudiante  │  │    Doctor    │  │  Nutricionista   │
     └──────────────┘  └──────────────┘  └──────────────────┘

  Clases de entidad (independientes, sin herencia):

  ┌──────────────┐  ┌──────────┐  ┌──────────┐  ┌──────┐
  │ ControlSalud │  │ Reclamo  │  │ Consulta │  │ Cita │
  └──────────────┘  └──────────┘  └──────────┘  └──────┘
```

---

## Clases con herencia

### 1. `Persona` — Abstracta

**Archivo:** `persona.py`

Clase base de todo el sistema. Nadie puede ser usuario sin pasar por esta clase.

#### Atributos privados

| Atributo       | Tipo   | Descripción                        |
|----------------|--------|------------------------------------|
| `__nombre`     | `str`  | Nombre completo                    |
| `__edad`       | `int`  | Edad en años                       |
| `__sexo`       | `str`  | `'M'` o `'F'`                      |
| `__usuario`    | `str`  | Nombre de usuario para login       |
| `__contrasena` | `str`  | Contraseña (sin getter por seguridad) |

#### Métodos abstractos (obligatorios en hijas)

| Método                          | Descripción                                      |
|---------------------------------|--------------------------------------------------|
| `iniciar_sesion(usuario, clave)` | Autenticación. Cada clase lo implementa distinto |
| `mostrar_perfil()`              | Retorna dict con datos del usuario               |

#### Métodos concretos (disponibles para todas las hijas)

| Método                    | Descripción                                    |
|---------------------------|------------------------------------------------|
| `verificar_contrasena(x)` | Compara `x` con la contraseña almacenada       |
| `set_contrasena(nueva)`   | Cambia la contraseña con validación de longitud |

---

### 2. `Estudiante`

**Archivo:** `estudiante.py`  
**Hereda de:** `Persona`

Representa a un alumno del colegio. Es el usuario principal del sistema.

#### Atributos propios

| Atributo                    | Tipo           | Descripción                             |
|-----------------------------|----------------|-----------------------------------------|
| `__codigo`                  | `str`          | RUDE o número de boleta                 |
| `__curso`                   | `str`          | Ej: `"4to A"`                           |
| `__colegio`                 | `str`          | Nombre del colegio                      |
| `__fotografia`              | `str` / `None` | Ruta al archivo de foto en `uploads/`   |
| `__nutricionista_asignado`  | `Nutricionista` / `None` | Nutricionista responsable  |
| `__controles`               | `list`         | Lista de objetos `ControlSalud`         |

#### Métodos

| Método                              | Retorna        | Descripción                                           |
|-------------------------------------|----------------|-------------------------------------------------------|
| `iniciar_sesion(usuario, clave)`    | `bool`         | Valida credenciales del estudiante                    |
| `mostrar_perfil()`                  | `dict`         | Devuelve todos los datos del perfil                   |
| `agregar_control(control)`          | `None`         | Agrega un `ControlSalud` a su historial               |
| `obtener_controles()`               | `list`         | Retorna copia de la lista de controles                |
| `calcular_imc(peso_kg, talla_m)`    | `float`        | Fórmula: `peso / talla²`                              |
| `obtener_estado_nutricional(imc)`   | `str`          | Clasifica según OMS (Normal, Sobrepeso, etc.)         |
| `enviar_reclamo(mensaje)`           | `Reclamo`      | Crea y retorna un objeto `Reclamo`                    |
| `realizar_consulta(mensaje)`        | `Consulta`     | Crea y retorna un objeto `Consulta`                   |

#### Clasificación de IMC (OMS)

| IMC            | Estado nutricional    |
|----------------|-----------------------|
| `< 16.0`       | Desnutrición severa   |
| `16.0 – 18.4`  | Bajo peso             |
| `18.5 – 24.9`  | Normal                |
| `25.0 – 29.9`  | Sobrepeso             |
| `≥ 30.0`       | Obesidad              |

---

### 3. `Doctor`

**Archivo:** `doctor.py`  
**Hereda de:** `Persona`

Representa al médico del sistema. Registra controles y responde consultas.

#### Atributos propios

| Atributo        | Tipo   | Descripción                         |
|-----------------|--------|-------------------------------------|
| `__especialidad`| `str`  | Ej: `"Pediatría"`, `"Medicina General"` |
| `__matricula`   | `str`  | Número de matrícula profesional     |
| `__citas`       | `list` | Lista de objetos `Cita`             |

#### Métodos

| Método                                         | Retorna       | Descripción                                                  |
|------------------------------------------------|---------------|--------------------------------------------------------------|
| `iniciar_sesion(usuario, clave)`               | `bool`        | Valida credenciales del doctor                               |
| `mostrar_perfil()`                             | `dict`        | Devuelve datos médicos del perfil                            |
| `registrar_control(estudiante, peso, talla, obs)` | `ControlSalud` | Crea control, calcula IMC y lo agrega al estudiante     |
| `responder_consulta(consulta, respuesta)`      | `None`        | Llama a `consulta.agregar_respuesta()` con su autoría        |
| `gestionar_citas(accion, cita)`                | `None`        | Cambia estado de cita: `confirmar`, `cancelar`, `completar`  |

---

### 4. `Nutricionista`

**Archivo:** `nutricionista.py`  
**Hereda de:** `Persona`

Especialista en seguimiento nutricional. Puede tener varios estudiantes a cargo.

#### Atributos propios

| Atributo                    | Tipo   | Descripción                          |
|-----------------------------|--------|--------------------------------------|
| `__matricula`               | `str`  | Matrícula profesional                |
| `__estudiantes_asignados`   | `list` | Lista de `Estudiante` bajo su cargo  |

#### Métodos

| Método                                  | Retorna | Descripción                                              |
|-----------------------------------------|---------|----------------------------------------------------------|
| `iniciar_sesion(usuario, clave)`        | `bool`  | Valida credenciales                                      |
| `mostrar_perfil()`                      | `dict`  | Devuelve datos del perfil con cantidad de estudiantes    |
| `asignar_estudiante(estudiante)`        | `None`  | Agrega estudiante a su lista y se asigna en el objeto    |
| `evaluar_nutricion(estudiante)`         | `dict`  | Analiza el último control del estudiante                 |
| `generar_reporte(estudiante)`           | `dict`  | Genera historial nutricional completo                    |
| `asignar_dieta(estudiante, descripcion)`| `dict`  | Registra un plan alimentario para el estudiante          |

---

## Clases de entidad

Estas clases **no heredan de `Persona`**. Son objetos de datos que representan
registros del sistema. Cada una tiene un método `to_dict()` para enviar sus datos
a las vistas HTML.

---

### 5. `ControlSalud`

**Archivo:** `control_salud.py`

Registro médico tomado en una fecha. Es de **solo lectura** una vez creado
(ningún atributo tiene setter — un control no se edita, se crea uno nuevo).

#### Atributos

| Atributo              | Tipo    | Descripción                                          |
|-----------------------|---------|------------------------------------------------------|
| `__fecha`             | `date`  | Fecha del control (se asigna automáticamente)        |
| `__peso`              | `float` | Peso en kilogramos                                   |
| `__talla`             | `float` | Talla en metros                                      |
| `__imc`               | `float` | IMC calculado por `Estudiante.calcular_imc()`        |
| `__estado_nutricional`| `str`   | Clasificación OMS                                    |
| `__observaciones`     | `str`   | Notas del médico (opcional)                          |
| `__doctor`            | `Doctor`| Doctor que realizó el control                        |

---

### 6. `Reclamo`

**Archivo:** `reclamo.py`

Mensaje formal enviado por un estudiante. El administrador puede responderlo
y cambiar su estado.

#### Atributos

| Atributo      | Tipo         | Descripción                              |
|---------------|--------------|------------------------------------------|
| `__estudiante`| `Estudiante` | Quién envió el reclamo                   |
| `__mensaje`   | `str`        | Contenido del reclamo                    |
| `__fecha`     | `date`       | Fecha de envío (automática)              |
| `__estado`    | `str`        | `Pendiente` → `En proceso` → `Resuelto`  |
| `__respuesta` | `str` / `None` | Respuesta del administrador            |

#### Estados posibles

```
Pendiente  →  En proceso  →  Resuelto  →  Cerrado
```

---

### 7. `Consulta`

**Archivo:** `consulta.py`

Pregunta médica enviada por un estudiante. Un `Doctor` o el administrador
puede responderla. Solo puede responderse **una vez**.

#### Atributos

| Atributo          | Tipo           | Descripción                           |
|-------------------|----------------|---------------------------------------|
| `__estudiante`    | `Estudiante`   | Quién realizó la consulta             |
| `__mensaje`       | `str`          | Texto de la consulta                  |
| `__fecha`         | `date`         | Fecha de envío (automática)           |
| `__respuesta`     | `str` / `None` | Texto de la respuesta                 |
| `__respondido_por`| `Doctor` / `str` / `None` | Quién respondió            |
| `__respondida`    | `bool`         | `False` hasta que se responda         |

---

### 8. `Cita`

**Archivo:** `cita.py`

Agendamiento médico entre un `Estudiante` y un `Doctor` en fecha y hora definidas.

#### Atributos

| Atributo      | Tipo         | Descripción                          |
|---------------|--------------|--------------------------------------|
| `__estudiante`| `Estudiante` | Paciente de la cita                  |
| `__doctor`    | `Doctor`     | Médico responsable                   |
| `__fecha`     | `date`       | Fecha de la cita                     |
| `__hora`      | `str`        | Hora en formato `"HH:MM"`            |
| `__motivo`    | `str`        | Motivo de la consulta (opcional)     |
| `__estado`    | `str`        | Estado actual de la cita             |
| `__creada_en` | `date`       | Fecha en que se registró             |

#### Estados posibles

```
Pendiente  →  Confirmada  →  Completada
                ↓
            Cancelada
```

---

## Cómo importar las clases

Gracias al archivo `__init__.py`, puedes importar cualquier clase
desde una sola línea:

```python
# Importar clases individuales
from app.models import Estudiante
from app.models import Doctor, Nutricionista

# Importar varias a la vez
from app.models import Estudiante, ControlSalud, Cita, Reclamo
```

También puedes importar directamente desde el archivo específico:

```python
from app.models.estudiante import Estudiante
from app.models.control_salud import ControlSalud
```

---

## Ejemplos de uso

### Crear un estudiante y calcular su IMC

```python
from app.models import Estudiante

alumno = Estudiante(
    nombre    = "María López",
    edad      = 14,
    sexo      = "F",
    usuario   = "maria.lopez",
    contrasena= "segura123",
    codigo    = "RUD-2024-001",
    curso     = "3ro B",
    colegio   = "Unidad Educativa Simón Bolívar"
)

imc    = alumno.calcular_imc(peso_kg=52.0, talla_m=1.58)
estado = alumno.obtener_estado_nutricional(imc)

print(imc)     # 20.83
print(estado)  # Normal
```

### Doctor registra un control para un estudiante

```python
from app.models import Doctor, Estudiante

medico = Doctor(
    nombre     = "Dr. Carlos Ramos",
    edad       = 42,
    sexo       = "M",
    usuario    = "c.ramos",
    contrasena = "doctor456",
    especialidad = "Medicina General",
    matricula  = "MED-0042"
)

# El doctor registra el control — calcula IMC automáticamente
control = medico.registrar_control(
    estudiante   = alumno,
    peso         = 52.0,
    talla        = 1.58,
    observaciones= "Estudiante en buen estado general."
)

print(control)
# ControlSalud(fecha='2024-05-06', peso=52.0kg, talla=1.58m, imc=20.83, estado='Normal')
```

### Estudiante envía un reclamo

```python
reclamo = alumno.enviar_reclamo(
    "No recibí los resultados de mi último control médico."
)

print(reclamo.estado)   # Pendiente
reclamo.responder("Los resultados ya fueron enviados a su correo.")
print(reclamo.estado)   # Resuelto
```

### Nutricionista evalúa y asigna dieta

```python
from app.models import Nutricionista

nut = Nutricionista(
    nombre     = "Lic. Ana Torres",
    edad       = 35,
    sexo       = "F",
    usuario    = "a.torres",
    contrasena = "nutri789",
    matricula  = "NUT-0015"
)

nut.asignar_estudiante(alumno)
evaluacion = nut.evaluar_nutricion(alumno)
print(evaluacion["estado"])  # Normal

nut.asignar_dieta(alumno, "Dieta equilibrada: 3 comidas principales y 2 meriendas.")
```

### Agendar una cita médica

```python
from app.models import Cita
from datetime import date

cita = Cita(
    estudiante = alumno,
    doctor     = medico,
    fecha      = date(2024, 6, 15),
    hora       = "10:30",
    motivo     = "Control de rutina semestral"
)

print(cita.estado)   # Pendiente
cita.confirmar()
print(cita.estado)   # Confirmada
cita.completar()
print(cita.estado)   # Completada
```

---

## Notas importantes

- Ningún atributo privado debe accederse con `__` directamente. Siempre usar las `@property`.
- La contraseña **no tiene getter** por seguridad. Solo se puede verificar con `verificar_contrasena()`.
- `ControlSalud` es inmutable una vez creado. Para corregir datos, se crea un nuevo control.
- `Consulta` solo puede responderse una vez. Si ya fue respondida, lanza una excepción.
- Todos los objetos tienen `to_dict()` para pasar sus datos a las vistas HTML de Flask/Jinja2.

---

*Módulo creado como parte del Sistema Web de Seguimiento de Salud Escolar.*  
*Paso 2 de 8 — Modelos y Programación Orientada a Objetos.*