from dataclasses import dataclass, field
import json

@dataclass
class Usuario:
    id: int
    nombre: str
    apellidos: str
    num_identificacion: str
    correo: str
    telefono: str
    estado: str

    def guardar_usuario(self):
        nuevo_usuario = self.__dict__
        with open("base_de_datos/usuarios.json", "a") as archivo:
            json.dump(nuevo_usuario, archivo, ensure_ascii=False, indent=4)
            archivo.write("\n")

def nuevo_usuario_id():
    with open("base_de_datos/usuarios.json", "r") as archivo:
        try:
            usuarios = json.load(archivo)
            return max(usuario["id"] for usuario in usuarios) + 1
        except ValueError:
            return 1  # Retorna 1 si el archivo está vacío o no se puede cargar

def crear_usuario(nombre, apellidos, num_identificacion, correo, telefono, estado):
    id_usuario = nuevo_usuario_id()
    usuario = Usuario(
        id=id_usuario,
        nombre=nombre,
        apellidos=apellidos,
        num_identificacion=num_identificacion,
        correo=correo,
        telefono=telefono,
        estado=estado
    )
    usuario.guardar_usuario()
    return usuario
