from dataclasses import dataclass
import json

@dataclass
class Torneo:
    id: int
    nombre: str
    fecha: str

    @staticmethod
    def nuevo_id():
        try:
            with open("base_de_datos/torneos.json", "r") as archivo:
                torneos = json.load(archivo)
                return max(torneo["id"] for torneo in torneos) + 1
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return 1

    def guardar(self):
        try:
            with open("base_de_datos/torneos.json", "r") as archivo:
                torneos = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            torneos = []
        
        torneos.append(self.__dict__)
        with open("base_de_datos/torneos.json", "w") as archivo:
            json.dump(torneos, archivo, indent=4)
