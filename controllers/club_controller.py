# club_controller.py
import json
from modelos.base_model import BaseModel
from modelos.usuario import Usuario
from modelos.Inscripcion import Inscripcion
from modelos.informe import Informe
from modelos.entrenamiento import Entrenamiento
from modelos.torneo import Torneo
from modelos.asistencia_torneos import Asistencia_Torneo
from modelos.asistencia_entrenamientos import Asistencia_Entrenamiento
import flet as ft  # Asegúrate de importar flet aquí

class ClubController:
    def __init__(self):
        self.usuarios = [Usuario.from_dict(u) for u in BaseModel.cargar_datos("usuarios.json")]
        self.entrenamientos = [Entrenamiento.from_dict(e) for e in BaseModel.cargar_datos("entrenamientos.json")]

    def actualizar_estado_usuario(self, usuario_id, nuevo_estado):
        for usuario in self.usuarios:
            if usuario.id == usuario_id:
                usuario.estado = nuevo_estado
        self.guardar_usuarios()

    def existe_usuario(self, num_identificacion):
        for usuario in self.usuarios:
            if usuario.num_identificacion == num_identificacion:
                return True
        return False

    def guardar_usuarios(self):
        BaseModel.guardar_datos("usuarios.json", [u.to_dict() for u in self.usuarios])

    def cargar_pagos(self):
        return BaseModel.cargar_datos("pagos.json")

    def agregar_usuario(self, usuario: Usuario):
        self.usuarios.append(usuario)
        self.guardar_usuarios()


    def cargar_usuarios(self):
        datos = BaseModel.cargar_datos("usuarios.json")
        return [Usuario.from_dict(d) for d in datos]

    def filtrar_usuarios(self, estado: str):
        return [usuario for usuario in self.usuarios if usuario.estado == estado]

    def cargar_torneos(self):
        datos = BaseModel.cargar_datos("torneos.json")
        return [Torneo(**d) for d in datos]

    def cargar_entrenamientos(self):
        return [Entrenamiento.from_dict(e) for e in BaseModel.cargar_datos("entrenamientos.json")]

    def dropdown_usuarios_matriculados(self):
        """
        Retorna un Dropdown con los usuarios que están matriculados en el club.
        """
        usuarios_matriculados = [u for u in self.usuarios if u.estado == "matriculado"]
        return ft.Dropdown(
            label="Seleccionar Usuario",
            options=[ft.dropdown.Option(u.nombre) for u in usuarios_matriculados],
        )
        
    def dropdown_usuarios(self):
        """
        Retorna un Dropdown con los usuarios que están matriculados en el club.
        """
        usuarios_incritos = [u for u in self.usuarios]
        return ft.Dropdown(
            label="Seleccionar Usuario",
            options=[ft.dropdown.Option(u.nombre) for u in usuarios_incritos],
        )

    def usuarios_inscritos_dict(self):
        """
        Retorna un diccionario de usuarios matriculados con {nombre: id}.
        """
        return {u.nombre: u.id for u in self.usuarios}
    def usuarios_matriculados_dict(self):
        """
        Retorna un diccionario de usuarios matriculados con {nombre: id}.
        """
        return {u.nombre: u.id for u in self.usuarios if u.estado == "matriculado"}
    
    def cargar_inscripciones(self):
        """
        Carga las inscripciones desde 'inscripciones.json'.
        """
        try:
            return BaseModel.cargar_datos("inscripciones.json")
        except Exception as e:
            print(f"Error al cargar inscripciones: {e}")
            return []

    def get_inscripciones_by_torneo(self, torneo_id):
        """
        Retorna una lista de inscripciones filtradas por torneo_id.
        """
        inscripciones = self.cargar_inscripciones()
        return [insc for insc in inscripciones if insc['torneo_id'] == torneo_id]

    def get_user_by_id(self, user_id):
        """
        Retorna el objeto Usuario con el ID especificado o None si no existe.
        """
        for u in self.usuarios:
            if u.id == user_id:
                return u
        return None

    def get_asistencias_by_torneo(self, torneo_id):
        """
        Carga de 'asistencia_torneos.json' y filtra las que tengan el 'torneo_id' especificado.
        """
        try:
            asistencias = BaseModel.cargar_datos("asistencia_torneos.json")
        except:
            asistencias = []
        return [a for a in asistencias if a["torneo_id"] == torneo_id]

    def usuarios_matriculados_list(self):
        """
        Retorna una lista de usuarios matriculados en el club.
        """
        return [usuario for usuario in self.usuarios if usuario.estado == "matriculado"]
    
    def usuario_esta_matriculado(self, usuario_id):
        """
        Verifica si el usuario está matriculado.

        Parámetros:
            usuario_id (int): El ID del usuario a verificar.

        Retorna:
            bool: True si el usuario está matriculado, False en caso contrario.
        """
        # Buscamos al usuario por su ID
        usuario = self.get_user_by_id(usuario_id)
        if usuario is not None:
            # Verificamos el estado del usuario
            return usuario.estado == "matriculado"
        # Si no encontramos el usuario, retornamos False
        return False
