from dataclasses import dataclass
import json
from asistencia_entrenamientos import Asistencia_Entrenamiento

@dataclass
class Entrenamiento:
    id: int
    fecha: str

    @staticmethod
    def nuevo_id():
        try:
            with open("base_de_datos/entrenamientos.json", "r") as archivo:
                entrenamientos = json.load(archivo)
                return max(entrenamiento["id"] for entrenamiento in entrenamientos) + 1
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return 1

    def guardar(self):
        try:
            with open("base_de_datos/entrenamientos.json", "r") as archivo:
                entrenamientos = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            entrenamientos = []
        
        entrenamientos.append(self.__dict__)
        with open("base_de_datos/entrenamientos.json", "w") as archivo:
            json.dump(entrenamientos, archivo, indent=4)

    def crear_asistencia_entrenamientos(self):
        try:
            with open("base_de_datos/usuarios.json", "r") as archivo:
                usuarios = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            usuarios = []

        for usuario in usuarios:
            asistencia = Asistencia_Entrenamiento(entrenamiento_id=self.id, usuario_id=usuario['id'])
            asistencia.guardar()
