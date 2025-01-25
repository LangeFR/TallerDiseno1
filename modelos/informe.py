from dataclasses import dataclass
import json
from typing import List

@dataclass
class Informe:
    id: int
    usuario_id: int
    mes: str
    anio: int
    clases_mes: int
    clases_asistidas: int
    torneos_asistidos: int
    top_torneos: List[dict]

    def __init__(self, id, usuario_id, mes, anio, clases_mes, clases_asistidas, torneos_asistidos, top_torneos):
        self.id = id
        self.usuario_id = usuario_id
        self.mes = mes
        self.anio = anio
        self.clases_mes = clases_mes
        self.clases_asistidas = clases_asistidas
        self.torneos_asistidos = torneos_asistidos
        self.top_torneos = top_torneos

    def crear_informe(id_usuario, mes, anio):
        clases_asignadas = contar_clases_asignadas(id_usuario, mes, anio)
        clases_asistidas = contar_clases_asistidas(id_usuario, mes, anio)
        torneos_asistidos = contar_torneos_asistidos(id_usuario, mes, anio)
        top_torneos = encontrar_top_3_torneos(id_usuario, mes, anio)
        
        nuevo_informe = Informe(
            id=nuevo_id(),
            usuario_id=id_usuario,
            mes=mes,
            anio=anio,
            clases_mes=clases_asignadas,
            clases_asistidas=clases_asistidas,
            torneos_asistidos=torneos_asistidos,
            top_torneos=top_torneos
        )
        
        guardar_informe(nuevo_informe)

def contar_clases_asignadas(id_usuario, mes, anio):
    with open("base_de_datos/asistencia_entrenamientos.json", "r") as archivo:
        entrenamientos = json.load(archivo)
        with open("base_de_datos/entrenamientos.json", "r") as archivo_ent:
            lista_entrenamientos = json.load(archivo_ent)
            return sum(1 for e in entrenamientos if any(ent["id"] == e["entrenamiento_id"] and ent["fecha"].startswith(f"{anio}-{mes}") for ent in lista_entrenamientos) and e["usuario_id"] == id_usuario)

def contar_clases_asistidas(id_usuario, mes, anio):
    with open("base_de_datos/asistencia_entrenamientos.json", "r") as archivo:
        entrenamientos = json.load(archivo)
        with open("base_de_datos/entrenamientos.json", "r") as archivo_ent:
            lista_entrenamientos = json.load(archivo_ent)
            return sum(1 for e in entrenamientos if any(ent["id"] == e["entrenamiento_id"] and ent["fecha"].startswith(f"{anio}-{mes}") for ent in lista_entrenamientos) and e["usuario_id"] == id_usuario and e["estado"] == "presente")


def contar_torneos_asistidos(id_usuario, mes, anio):
    with open("base_de_datos/asistencia_torneos.json", "r") as archivo:
        torneos_asistidos = json.load(archivo)
        with open("base_de_datos/torneos.json", "r") as archivo_tor:
            lista_torneos = json.load(archivo_tor)
            return sum(1 for t in torneos_asistidos if any(tor["id"] == t["torneo_id"] and tor["fecha"].startswith(f"{anio}-{mes}") for tor in lista_torneos) and t["usuario_id"] == id_usuario)

def encontrar_top_3_torneos(id_usuario, mes, anio):
    with open("base_de_datos/asistencia_torneos.json", "r") as archivo_asistencia, open("base_de_datos/torneos.json", "r") as archivo_torneos:
        asistencia = json.load(archivo_asistencia)
        torneos = json.load(archivo_torneos)
        resultados = [(tor["nombre"], a["puesto"]) for a in asistencia for tor in torneos if a["usuario_id"] == id_usuario and tor["id"] == a["torneo_id"] and tor["fecha"].startswith(f"{anio}-{mes}")]
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
