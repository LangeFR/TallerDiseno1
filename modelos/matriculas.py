from dataclasses import dataclass
import json

@dataclass
class Matricula:
    id: int
    usuario_id: int
    pago_id: int

    @staticmethod
    def nuevo_id():
        try:
            with open("base_de_datos/matriculas.json", "r") as archivo:
                matriculas = json.load(archivo)
                return max(matricula["id"] for matricula in matriculas) + 1
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return 1

    def guardar(self):
        try:
            with open("base_de_datos/matriculas.json", "r") as archivo:
                matriculas = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            matriculas = []

        matriculas.append(self.__dict__)
        with open("base_de_datos/matriculas.json", "w") as archivo:
            json.dump(matriculas, archivo, indent=4)

