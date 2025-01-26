from dataclasses import dataclass
import json


@dataclass
class Inscripcion:
    usuario: str
    torneo_id: int

    @staticmethod
    def cargar_inscripciones():
        try:
            with open("base_de_datos/inscripciones.json", "r") as archivo:
                return json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def guardar_inscripciones(inscripciones):
        with open("base_de_datos/inscripciones.json", "w") as archivo:
            json.dump(inscripciones, archivo, indent=4)

    def guardar(self):
        inscripciones = self.cargar_inscripciones()

        # Validar si ya existe la inscripción
        if any(
            inscripcion["usuario"] == self.usuario and inscripcion["torneo_id"] == self.torneo_id
            for inscripcion in inscripciones
        ):
            raise ValueError("El usuario ya está inscrito en este torneo.")

        inscripciones.append(self.__dict__)
        self.guardar_inscripciones(inscripciones)
