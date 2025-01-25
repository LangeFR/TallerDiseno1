from dataclasses import dataclass, field
import json
from datetime import datetime

@dataclass
class Pago:
    usuario_id: int
    concepto: str
    fecha: str
    cantidad: float
    id: int = field(default=None, init=False)  # ID se establece automáticamente, no se pasa al constructor

    def __post_init__(self):
        # Asignar un nuevo ID si es la primera vez que se crea el objeto
        if self.id is None:
            self.id = self.nuevo_id()

    def to_dict(self):
        # Retorna un diccionario con los valores actuales de las propiedades
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "concepto": self.concepto,
            "fecha": self.fecha,
            "cantidad": self.cantidad
        }
        
    @staticmethod
    def nuevo_id():
        """Genera un nuevo ID para el pago basado en los pagos existentes en pagos.json."""
        try:
            with open("base_de_datos/pagos.json", "r") as archivo:
                pagos = json.load(archivo)
                if pagos:  # Asegurarse de que hay pagos para calcular el máximo
                    return max(pago["id"] for pago in pagos) + 1
                return 1  # Si el archivo existe pero está vacío, empezamos desde 1
        except (FileNotFoundError, json.JSONDecodeError, ValueError):  # Captura errores de archivo no encontrado y problemas de decodificación JSON, además de un archivo vacío
            return 1

    def guardar(self):
        """Guarda el pago en el archivo JSON de pagos."""
        try:
            with open("base_de_datos/pagos.json", "r") as archivo:
                pagos = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            pagos = []  # Inicializa una lista vacía si el archivo no existe o hay un error de decodificación

        # Agrega el pago actual al listado de pagos
        pagos.append(self.to_dict())

        # Guarda la lista actualizada de pagos en el archivo
        with open("base_de_datos/pagos.json", "w") as archivo:
            json.dump(pagos, archivo, indent=4)
