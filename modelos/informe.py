from dataclasses import dataclass, field
from typing import List

@dataclass
class Informe:
    def __init__(self, id, miembro_id, clases_mes, clases_asistidas, torneos_asistidos, asistencia_torneo1_id, asistencia_torneo2_id, asistencia_torneo3_id):
        self.id = id
        self.miembro_id = miembro_id
        self.clases_mes = clases_mes
        self.clases_asistidas = clases_asistidas
        self.torneos_asistidos = torneos_asistidos
        self.asistencia_torneo1_id = asistencia_torneo1_id
        self.asistencia_torneo2_id = asistencia_torneo2_id
        self.asistencia_torneo3_id = asistencia_torneo3_id

    def crear_informe(id_miembro, mes):
        clases_asignadas = contar_clases_asignadas(id_miembro, mes)
        clases_asistidas = contar_clases_asistidas(id_miembro, mes)
        torneos_asistidos = contar_torneos_asistidos(id_miembro, mes)
        top_torneos = encontrar_top_3_torneos(id_miembro, mes)
        
        # Asumiendo una lógica para asignar un ID único al nuevo informe
        nuevo_informe = Informe(
            id=nuevo_id(),
            miembro_id=id_miembro,
            clases_mes=clases_asignadas,
            clases_asistidas=clases_asistidas,
            torneos_asistidos=torneos_asistidos,
            asistencia_torneo1_id=top_torneos[0] if len(top_torneos) > 0 else None,
            asistencia_torneo2_id=top_torneos[1] if len(top_torneos) > 1 else None,
            asistencia_torneo3_id=top_torneos[2] if len(top_torneos) > 2 else None
        )
        
        # Guardar el nuevo informe en el archivo JSON
        guardar_informe(nuevo_informe)

def contar_clases_asignadas(id_miembro, mes):
    return None

def contar_clases_asistidas(id_miembro, mes):
    return None

def contar_torneos_asistidos(id_miembro, mes):
    return None

def encontrar_top_3_torneos(id_miembro, mes):
    return None



