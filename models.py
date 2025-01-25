import json
from dataclasses import dataclass, field
from typing import List

@dataclass
class Miembro:
    id: int
    nombre: str
    apellidos: str
    num_identificacion: str
    correo: str
    telefono: str
    estado: str

@dataclass
class Informe:
    id: int
    miembro_id: int
    clases_mes: int
    clases_asistidas: int
    torneos_asistidos: int
    asistencia_torneo1_id: int
    asistencia_torneo2_id: int
    asistencia_torneo3_id: int

@dataclass
class Entrenamiento:
    id: int
    fecha: str

@dataclass
class Asistencia_Entrenamiento:
    id: int
    miembro_id: int
    entrenamiento_id: int
    estado: str  # 'verde' o 'rojo'

@dataclass
class Torneo:
    id: int
    nombre: str
    fecha: str

@dataclass
class Asistencia_Torneo:
    id: int
    miembro_id: int
    torneo_id: int
    puesto: int

@dataclass
class Inscripcion:
    id: int
    miembro_id: int
    pago_id: int

@dataclass
class Pago:
    id: int
    estado: str
    concepto: str
    fecha: str
    cantidad: int
