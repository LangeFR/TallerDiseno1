from dataclasses import dataclass
import json

@dataclass
class Asistencia_Entrenamiento:
    id: int
    usuario_id: int
    entrenamiento_id: int
    estado: str

    @staticmethod
    def nuevo_id():
        try:
            with open("base_de_datos/asistencia_entrenamientos.json", "r") as archivo:
                asistencias = json.load(archivo)
                return max(asistencia["id"] for asistencia in asistencias) + 1
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return 1

    def guardar(self):
        try:
            with open("base_de_datos/asistencia_entrenamientos.json", "r") as archivo:
                asistencias = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            asistencias = []

        asistencias.append(self.__dict__)
        with open("base_de_datos/asistencia_entrenamientos.json", "w") as archivo:
            json.dump(asistencias, archivo, indent=4)
