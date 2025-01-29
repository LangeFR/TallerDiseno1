import json
import os

class BaseModel:
    @staticmethod
    def guardar_datos(nombre_archivo, datos):
        base_path = os.path.join('base_de_datos', nombre_archivo) 
        with open(base_path, 'w') as file:
            json.dump(datos, file, indent=4)

    @staticmethod
    def cargar_datos(nombre_archivo):
        base_path = os.path.join('base_de_datos', nombre_archivo)  
        try:
            with open(base_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
