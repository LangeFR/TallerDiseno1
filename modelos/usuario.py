from dataclasses import dataclass
import json

@dataclass
class Usuario:
    id: int
    nombre: str
    apellidos: str
    edad: int 
    num_identificacion: str
    correo: str
    telefono: str
    estado: str
    rol: str         # Nuevo campo: indica el rol del usuario ("admin", "coach", "user", etc.)
    contrasena: str  # Nuevo campo: almacena la contraseña (idealmente, un hash)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "edad": self.edad,
            "num_identificacion": self.num_identificacion,
            "correo": self.correo,
            "telefono": self.telefono,
            "estado": self.estado,
            "rol": self.rol,
            "contrasena": self.contrasena,
        }

    @staticmethod
    def from_dict(data):
        return Usuario(
            id=data["id"],
            nombre=data["nombre"],
            apellidos=data.get("apellidos", ""),
            edad=data.get("edad", 0),
            num_identificacion=data["num_identificacion"],
            correo=data["correo"],
            telefono=data["telefono"],
            estado=data.get("estado", "inscrito"),
            rol=data.get("rol", "user"),         # Valor por defecto "user" si no está especificado
            contrasena=data.get("contrasena", "")  # Valor por defecto vacío
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
