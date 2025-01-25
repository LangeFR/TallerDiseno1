from dataclasses import dataclass
import json
from typing import List

@dataclass
class Informe:
    id: int
    miembro_id: int
    mes: str
    anio: int
    clases_mes: int
    clases_asistidas: int
    torneos_asistidos: int
    top_torneos: List[dict]

    def __init__(self, id, miembro_id, mes, anio, clases_mes, clases_asistidas, torneos_asistidos, top_torneos):
        self.id = id
        self.miembro_id = miembro_id
        self.mes = mes
        self.anio = anio
        self.clases_mes = clases_mes
        self.clases_asistidas = clases_asistidas
        self.torneos_asistidos = torneos_asistidos
        self.top_torneos = top_torneos

def crear_informe(id_miembro, mes, anio):
    clases_asignadas = contar_clases_asignadas(id_miembro, mes, anio)
    clases_asistidas = contar_clases_asistidas(id_miembro, mes, anio)
    torneos_asistidos = contar_torneos_asistidos(id_miembro, mes, anio)
    top_torneos = encontrar_top_3_torneos(id_miembro, mes, anio)
    
    nuevo_informe = Informe(
        id=nuevo_id(),
        miembro_id=id_miembro,
        mes=mes,
        anio=anio,
        clases_mes=clases_asignadas,
        clases_asistidas=clases_asistidas,
        torneos_asistidos=torneos_asistidos,
        top_torneos=top_torneos
    )
    
    guardar_informe(nuevo_informe)

def contar_clases_asignadas(id_miembro, mes, anio):
    with open("base_de_datos/asistencia_entrenamientos.json", "r") as archivo:
        entrenamientos = json.load(archivo)
        return sum(1 for e in entrenamientos if e["miembro_id"] == id_miembro and e["fecha"].startswith(f"{anio}-{mes}"))

def contar_clases_asistidas(id_miembro, mes, anio):
    with open("base_de_datos/asistencia_entrenamientos.json", "r") as archivo:
        entrenamientos = json.load(archivo)
        return sum(1 for e in entrenamientos if e["miembro_id"] == id_miembro and e["fecha"].startswith(f"{anio}-{mes}") and e["estado"] == "verde")

def contar_torneos_asistidos(id_miembro, mes, anio):
    with open("base_de_datos/asistencia_torneos.json", "r") as archivo:
        torneos = json.load(archivo)
        return sum(1 for t in torneos if t["miembro_id"] == id_miembro and t["fecha"].startswith(f"{anio}-{mes}"))

def encontrar_top_3_torneos(id_miembro, mes, anio):
    with open("base_de_datos/asistencia_torneos.json", "r") as archivo_asistencia, \
         open("base_de_datos/torneos.json", "r") as archivo_torneos:
        asistencia = json.load(archivo_asistencia)
        torneos = json.load(archivo_torneos)
        resultados = [
            (t["nombre"], a["puesto"])
            for a in asistencia if a["miembro_id"] == id_miembro and a["fecha"].startswith(f"{anio}-{mes}")
            for t in torneos if t["id"] == a["torneo_id"]
        ]
        resultados.sort(key=lambda x: x[1])  # Ordenar por el puesto, ascendente
        return resultados[:3]  # Devolver solo los 3 mejores

def guardar_informe(informe):
    with open("base_de_datos/informes.json", "a") as archivo:
        json.dump(informe.__dict__, archivo, ensure_ascii=False, indent=4)
        archivo.write("\n")

def nuevo_id():
    with open("base_de_datos/informes.json", "r") as archivo:
        try:
            informes = json.load(archivo)
            return max(informe["id"] for informe in informes) + 1
        except ValueError:
            return 1  # Retorna 1 si el archivo está vacío o no se puede cargar
