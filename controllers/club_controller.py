import json
from modelos.base_model import BaseModel
from modelos.usuario import Usuario
from modelos.Inscripcion import Inscripcion
from modelos.informe import Informe
from modelos.entrenamiento import Entrenamiento
from modelos.torneo import Torneo
from modelos.asistencia_torneos import Asistencia_Torneo
from modelos.asistencia_entrenamientos import Asistencia_Entrenamiento

class ClubController:
    def __init__(self):
        self.usuarios = [Usuario.from_dict(u) for u in BaseModel.cargar_datos("usuarios.json")]

    def actualizar_estado_usuario(self, usuario_id, nuevo_estado):
        for usuario in self.usuarios:
            if usuario.id == usuario_id:
                usuario.estado = nuevo_estado
        self.guardar_usuarios()

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
