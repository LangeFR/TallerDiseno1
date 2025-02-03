# auth_controller.py
from modelos.usuario import Usuario
from club_controller import ClubController

# Instancia global de ClubController 
club_controller = ClubController()

def registrar_usuario(usuario: Usuario) -> bool:
    """
    Registra un nuevo usuario.
    
    Verifica si ya existe un usuario con el mismo correo; de no existir, utiliza
    el método agregar_usuario de club_controller para almacenar el nuevo usuario.
    
    Retorna:
      - True si el registro fue exitoso.
      - False si ya existe un usuario con ese correo.
    """
    for u in club_controller.usuarios:
        if u.correo == usuario.correo:
            return False
    club_controller.agregar_usuario(usuario)
    return True

def validar_login(correo: str, contrasena: str):
    """
    Valida las credenciales del usuario.
    
    Recorre la lista de usuarios de club_controller; si encuentra uno cuyo
    correo y contraseña coincidan, retorna ese objeto Usuario; de lo contrario, retorna None.
    """
    for u in club_controller.usuarios:
        if u.correo == correo and u.contrasena == contrasena:
            return u
    return None
