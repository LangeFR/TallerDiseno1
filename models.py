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

