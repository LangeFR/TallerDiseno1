from dataclasses import dataclass, asdict, field
import json
from datetime import datetime

@dataclass
class Pago:
    id: int = field(default=None, init=False)
    usuario_id: int
    concepto: str
    fecha: str
    cantidad: float

    def __post_init__(self):
        if self.id is None:
            self.id = self.nuevo_id()
        if not self.validar_fecha(self.fecha):
            raise ValueError(f"Fecha {self.fecha} no es válida. Formato esperado: YYYY-MM-DD.")

    @staticmethod
    def nuevo_id():
        """Genera un nuevo ID para el pago basado en los pagos existentes."""
        try:
            with open("base_de_datos/pagos.json", "r") as archivo:
                pagos = json.load(archivo)
                if pagos:  # Asegúrate de que hay pagos para calcular el máximo
                    return max(pago["id"] for pago in pagos) + 1
                return 1
        except (FileNotFoundError, json.JSONDecodeError):
            return 1

    def guardar(self):
        """Guarda el pago en el archivo JSON de pagos."""
        try:
            with open("base_de_datos/pagos.json", "r") as archivo:
                pagos = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            pagos = []

        pagos.append(asdict(self))  # Correcto uso de asdict para convertir dataclass a dict
        with open("base_de_datos/pagos.json", "w") as archivo:
            json.dump(pagos, archivo, indent=4)

    @staticmethod
    def validar_fecha(fecha):
        """Valida que la fecha esté en el formato correcto (YYYY-MM-DD)."""
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
            return True
        except ValueError:
            return False
