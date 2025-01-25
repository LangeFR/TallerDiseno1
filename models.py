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



