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


    def get_asistencias_by_torneo(self, torneo_id):
        """
        Retorna una lista de instancias de Asistencia_Torneo filtradas por torneo_id.
        """
        return Asistencia_Torneo.obtener_asistencias_por_torneo(torneo_id)
    
    def mostrar_formulario_edicion(self, usuario):
        """
        Muestra un formulario para editar los datos de un usuario.
        """
        self.layout.controls.clear()
        
        nuevo_nombre = ft.TextField(label="Nuevo Nombre", value=usuario.nombre)
        nuevo_apellido = ft.TextField(label="Nuevo Apellido", value=usuario.apellidos)
        nuevo_telefono = ft.TextField(label="Nuevo Teléfono", value=usuario.telefono)
        nuevo_estado = ft.Dropdown(
            label="Nuevo Estado",
            options=[
                ft.dropdown.Option("matriculado"),
                ft.dropdown.Option("pendiente"),
                ft.dropdown.Option("expulsado")
            ],
            value=usuario.estado
        )

        btn_guardar = ft.ElevatedButton(
            "Guardar Cambios",
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
            on_click=lambda e: self.editar_usuario(usuario.id, nuevo_nombre.value, nuevo_apellido.value, nuevo_estado.value, nuevo_telefono.value)
        )

        btn_cancelar = ft.ElevatedButton(
            "Cancelar",
            on_click=lambda e: self.mostrar_info_usuario(usuario)
        )

        self.layout.controls.append(ft.Column([nuevo_nombre, nuevo_apellido, nuevo_telefono, nuevo_estado, btn_guardar, btn_cancelar]))
        self.page.update()

    
    def editar_usuario(self, usuario_id, nuevo_nombre=None, nuevo_apellido=None, nuevo_estado=None, nuevo_telefono=None, nuevo_correo=None, nueva_identificación = None, callback=None):
        """
        Edita los datos de un usuario y, si se proporciona un callback, ejecuta una acción después de guardar.
        
        Parámetros:
        - usuario_id (int): ID del usuario a modificar.
        - nuevo_nombre (str, opcional): Nuevo nombre del usuario.
        - nuevo_apellido (str, opcional): Nuevo apellido del usuario.
        - nuevo_estado (str, opcional): Nuevo estado del usuario.
        - nuevo_telefono (str, opcional): Nuevo número de teléfono.
        - callback (function, opcional): Función a ejecutar después de la edición.
        """
        for usuario in self.usuarios:
            if usuario.id == usuario_id:
                if nuevo_nombre:
                    usuario.nombre = nuevo_nombre
                if nuevo_apellido:
                    usuario.apellidos = nuevo_apellido
                if nuevo_estado:
                    usuario.estado = nuevo_estado
                if nuevo_telefono:
                    usuario.telefono = nuevo_telefono
                if nuevo_correo:
                    usuario.correo = nuevo_correo
                if nueva_identificación:
                    usuario.num_identificacion = nueva_identificación

                self.guardar_usuarios()
                print(f"✅ Usuario {usuario_id} editado correctamente.")

                # Si hay un callback, lo ejecutamos (redirige a la lista de usuarios)
                if callback:
                    callback()

                return usuario
        
        print(f"❌ No se encontró el usuario con ID {usuario_id}.")
        return None

    
    
    
    def eliminar_usuario(self, usuario_id):
        """
        Elimina un usuario de la lista y actualiza la base de datos JSON.
        
        Parámetros:
        - usuario_id (int): ID del usuario a eliminar.
        """
        usuarios_filtrados = [u for u in self.usuarios if u.id != usuario_id]
        
        if len(usuarios_filtrados) < len(self.usuarios):
            self.usuarios = usuarios_filtrados
            self.guardar_usuarios()
            print(f"🗑 Usuario {usuario_id} eliminado correctamente.")
        else:
            print(f"❌ No se encontró el usuario con ID {usuario_id}.")

