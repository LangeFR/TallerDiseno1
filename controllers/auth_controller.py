import json
import os
from modelos import Usuario

# Ruta al archivo de usuarios
DB_FILE = "base_de_datos/usuarios.json"


def leer_usuarios():
    """
    Lee el archivo JSON de usuarios y retorna una lista de diccionarios.
    Si el archivo no existe o está vacío, retorna una lista vacía.
    """
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    else:
        return []


def guardar_usuarios(usuarios):
    """
    Recibe una lista de diccionarios y la guarda en el archivo JSON.
    """
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)


def registrar_usuario(usuario: Usuario) -> bool:
    """
    Registra un usuario nuevo.
    
    Proceso:
      - Lee el archivo de usuarios.
      - Verifica si ya existe un usuario con el mismo correo (o se puede ampliar a otro identificador).
      - Si no existe, agrega el nuevo usuario y guarda la lista actualizada en el JSON.
    
    Retorna:
      - True si el registro fue exitoso.
      - False si ya existe un usuario con ese correo.
    """
    usuarios = leer_usuarios()

    # Verificar si ya existe un usuario con el mismo correo
    for u in usuarios:
        if u.get("correo") == usuario.correo:
            # Ya existe un usuario con ese correo
            return False

    # Agregar el nuevo usuario (convierte a diccionario)
    usuarios.append(usuario.to_dict())
    guardar_usuarios(usuarios)
    return True


def validar_login(correo: str, contrasena: str):
    """
    Valida las credenciales de login.
    
    Proceso:
      - Lee el archivo de usuarios.
      - Busca un usuario cuyo campo 'correo' coincida y cuya 'contrasena' sea igual a la ingresada.
    
    Retorna:
      - El objeto Usuario (utilizando from_dict) si la validación es exitosa.
      - None si las credenciales son incorrectas o el usuario no existe.
    """
    usuarios = leer_usuarios()

    for u in usuarios:
        if u.get("correo") == correo and u.get("contrasena") == contrasena:
            return Usuario.from_dict(u)
    return None
