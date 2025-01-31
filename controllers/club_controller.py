# club_controller.py
import json
import requests
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
        
    
    
    @staticmethod
    def obtener_usuarios_pendientes():
        
        GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1IMtHvmvLf4tFan7E0SJgvXMXlTRSk3HchdqJAsKnEbA/gviz/tq?tqx=out:json"
        """
        Obtiene la lista de usuarios preinscritos desde Google Sheets.
        """
        try:
            response = requests.get(GOOGLE_SHEETS_URL)
            raw_data = response.text.strip()  # Eliminar espacios en blanco

            # Imprimir la respuesta cruda para verificar
            print("🔹 Respuesta cruda de Google Sheets:")
            print(raw_data[:500])  # Solo imprimimos los primeros 500 caracteres para depuración

            # Limpiar la respuesta JSON eliminando los caracteres no válidos
            if raw_data.startswith("/*O_o*/"):
                json_str = raw_data.replace("/*O_o*/", "").replace("google.visualization.Query.setResponse(", "")[:-2]
            else:
                print("❌ Error: La respuesta no tiene el formato esperado de Google Sheets.")
                return []

            json_data = json.loads(json_str)  # Convertir en JSON limpio
            filas = json_data.get("table", {}).get("rows", [])

            usuarios = []
            for fila in filas:
                valores = [col["v"] if col and "v" in col else "" for col in fila["c"]]

                # Convertir edad en entero, manejando errores
                try:
                    edad = int(valores[3]) if isinstance(valores[3], (int, float)) else 0
                except ValueError:
                    edad = 0

                # Convertir número de identificación y teléfono en cadenas para evitar errores de notación científica
                num_identificacion = str(valores[4]) if valores[4] else ""
                telefono = str(valores[6]) if valores[6] else ""

                usuario = {
                    "id":"",
                    "nombre": valores[1],  
                    "apellidos": valores[2],  
                    "edad": edad,
                    "num_identificacion": num_identificacion,  
                    "correo": valores[5],  
                    "telefono": telefono,  
                    "estado": "pendiente"
                }
                usuarios.append(usuario)

            return usuarios

        except json.JSONDecodeError as e:
            print(f"❌ Error al decodificar JSON: {e}")
            return []
        except Exception as e:
            print(f"❌ Error obteniendo inscripciones: {e}")
            return []
    def actualizar_estado_usuario(self, usuario_id, nuevo_estado):
        for usuario in self.usuarios:
            if usuario.id == usuario_id:
                usuario.estado = nuevo_estado
        self.guardar_usuarios()

    def existe_usuario(self, num_identificacion, nombre):
        for usuario in self.usuarios:
            if usuario.num_identificacion == num_identificacion and usuario.nombre == nombre:
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
