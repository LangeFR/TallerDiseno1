from dataclasses import dataclass
import json
from datetime import datetime

@dataclass
class Pago:
    id: int
    usuario_id: int
    concepto: str
    fecha: str
    cantidad: float

# Función para cargar usuarios desde un archivo JSON
def cargar_usuarios(archivo):
    try:
        with open(archivo, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("El archivo no fue encontrado.")
        return []
    except json.JSONDecodeError:
        print("Error al decodificar el archivo JSON.")
        return []

# Función para crear pagos para cada usuario
def crear_pagos(usuarios, concepto, cantidad):
    pagos = []
    fecha_actual = datetime.now().strftime("%Y-%m-%d")  # Formato de fecha como AAAA-MM-DD
    id_pago = 1  # Iniciar un contador para los ID de los pagos

    for usuario in usuarios:
        pago = Pago(
            id=id_pago,
            usuario_id=usuario['id'],  # Asumiendo que cada usuario tiene un 'id'
            concepto=concepto,
            fecha=fecha_actual,
            cantidad=cantidad
        )
        pagos.append(pago)
        id_pago += 1  # Incrementar ID para el siguiente pago

    return pagos

# Función principal para ejecutar el programa
def main():
    archivo_usuarios = "base_de_datos/usuarios.json"  # Actualizado para apuntar a la carpeta correcta
    usuarios = cargar_usuarios(archivo_usuarios)
    if usuarios:
        pagos_de_matricula = crear_pagos(usuarios, "matricula", 100.00)  # $100 para la matrícula de cada usuario

        # Imprimir los pagos generados
        for pago in pagos_de_matricula:
            print(pago)
    else:
        print("No se encontraron usuarios para procesar pagos.")

# Ejecutar el programa
if __name__ == "__main__":
    main()
