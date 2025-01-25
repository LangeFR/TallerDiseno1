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

    def registrar_matriculas(self):
        try:
            with open("base_de_datos/usuarios.json", "r") as archivo:
                usuarios = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            usuarios = []

        for usuario in usuarios:
            # asignamos un nuevo pago_id
            nuevo_pago_id = self.nuevo_id()  # Esto puede cambiarse según cómo se manejen los pagos
            matricula = Matricula(id=self.nuevo_id(), usuario_id=usuario['id'], pago_id=nuevo_pago_id)
            matricula.guardar()
