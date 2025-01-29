from dataclasses import dataclass
import json

@dataclass
class Usuario:
    id: int
    nombre: str
    apellidos: str
    edad: int  # Añadido 'edad'
    num_identificacion: str
    correo: str
    telefono: str
    estado: str

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "edad": self.edad,  # Incluir 'edad'
            "num_identificacion": self.num_identificacion,
            "correo": self.correo,
            "telefono": self.telefono,
            "estado": self.estado,
        }

    @staticmethod
    def from_dict(data):
        return Usuario(
            id=data["id"],
            nombre=data["nombre"],
            apellidos=data.get("apellidos", ""),
            edad=data.get("edad", 0),  # Manejar ausencia de 'edad'
            num_identificacion=data["num_identificacion"],
            correo=data["correo"],
            telefono=data["telefono"],
            estado=data.get("estado", "inscrito")
        )

    @staticmethod
    def nuevo_id():
        try:
            with open("base_de_datos/usuarios.json", "r") as archivo:
                usuarios = json.load(archivo)
                if not usuarios:
                    return 1
                return max(usuario["id"] for usuario in usuarios) + 1
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return 1
