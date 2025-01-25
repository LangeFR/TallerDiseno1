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

    def cambiar_estado(self, nuevo_estado):
        estados_validos = ["ausente", "presente"]
        if nuevo_estado not in estados_validos:
            print("Error: El estado proporcionado no es válido. Debe ser 'ausente' o 'presente'.")
            return

        # Actualizar el estado de la asistencia
        self.estado = nuevo_estado
        
        # Actualizar la información en el archivo JSON
        self.actualizar_asistencia()

    def actualizar_asistencia(self):
        try:
            with open("base_de_datos/asistencia_entrenamientos.json", "r") as archivo:
                asistencias = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Archivo no encontrado o error al decodificar JSON.")
            return

        # Buscar y actualizar la asistencia en la lista
        for asistencia in asistencias:
            if asistencia["id"] == self.id:
                asistencia["estado"] = self.estado
                break

        # Reescribir el archivo con la información actualizada
        with open("base_de_datos/asistencia_entrenamientos.json", "w") as archivo:
            json.dump(asistencias, archivo, indent=4)
        print(f"Estado de asistencia actualizado a '{self.estado}' para el usuario con ID {self.usuario_id}.")

    @staticmethod
    def find_by_user_and_entrenamiento_id(usuario_id, entrenamiento_id):
        try:
            with open("base_de_datos/asistencia_entrenamientos.json", "r") as archivo:
                asistencias = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Archivo no encontrado o error al decodificar JSON.")
            return None  # Puede devolver None si no se encuentra el archivo o hay un error

        # Buscar la asistencia que coincide con usuario_id y entrenamiento_id
        for asistencia in asistencias:
            if asistencia["usuario_id"] == usuario_id and asistencia["entrenamiento_id"] == entrenamiento_id:
                print(f"Asistencia encontrada: ID {asistencia['id']}")
                return asistencia["id"]

        print("No se encontró una asistencia con los ID especificados.")
        return None  # Devuelve None si no se encuentra una coincidencia


