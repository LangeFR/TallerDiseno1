from dataclasses import dataclass
import json

@dataclass
class Asistencia_Torneo:
    id: int
    usuario_id: int
    torneo_id: int
    puesto: int

    @staticmethod
    def nuevo_id():
        try:
            with open("base_de_datos/asistencia_torneos.json", "r") as archivo:
                asistencias = json.load(archivo)
                return max(asistencia["id"] for asistencia in asistencias) + 1
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return 1

    def guardar(self):
        try:
            with open("base_de_datos/asistencia_torneos.json", "r") as archivo:
                asistencias = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            asistencias = []

        asistencias.append(self.__dict__)
        with open("base_de_datos/asistencia_torneos.json", "w") as archivo:
            json.dump(asistencias, archivo, indent=4)

    @staticmethod
    def crear_asistencia(torneo_id, usuario_id, puesto):
        nueva_asistencia = Asistencia_Torneo(
            id=Asistencia_Torneo.nuevo_id(),
            usuario_id=usuario_id,
            torneo_id=torneo_id,
            puesto=puesto
        )
        nueva_asistencia.guardar()
