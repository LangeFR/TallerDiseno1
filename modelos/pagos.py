from dataclasses import dataclass
import json
from datetime import datetime

@dataclass
class Pago:
    id: int
    concepto: str
    fecha: str
    cantidad: float

    @staticmethod
    def nuevo_id():
        try:
            with open("base_de_datos/pagos.json", "r") as archivo:
                pagos = json.load(archivo)
                return max(pago["id"] for pago in pagos) + 1
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return 1

    def guardar(self):
        try:
            with open("base_de_datos/pagos.json", "r") as archivo:
                pagos = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            pagos = []

        pagos.append(self.__dict__)
        with open("base_de_datos/pagos.json", "w") as archivo:
            json.dump(pagos, archivo, indent=4)

    def registrar_pagos(self, concepto, cantidad):
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        pago = Pago(id=self.nuevo_id(), concepto=concepto, fecha=fecha_actual, cantidad=cantidad)
        pago.guardar()
