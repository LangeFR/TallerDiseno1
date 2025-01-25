import flet as ft
import re
import json
from typing import List
from modelos.informe import Informe
from modelos.entrenamiento import Entrenamiento
from modelos.torneo import Torneo
from modelos.asistencia_torneos import Asistencia_Torneo
from modelos.asistencia_entrenamientos import Asistencia_Entrenamiento
from datetime import datetime
import os

# ------------------------- MODELO -------------------------
# Clase base para persistencia de datos
class BaseModel:
    @staticmethod
    def guardar_datos(nombre_archivo, datos):
        base_path = os.path.join('base_de_datos', nombre_archivo) 
        with open(base_path, 'w') as file:
            json.dump(datos, file, indent=4)

    @staticmethod
    def cargar_datos(nombre_archivo):
        base_path = os.path.join('base_de_datos', nombre_archivo)  
        try:
            with open(base_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

# Clase Usuario
class Usuario(BaseModel):
    def __init__(self, nombre, edad, num_identificacion, correo, telefono, estado="inscrito"):
        self.id = self.nuevo_id()  # Generar un nuevo ID para cada usuario creado
        self.nombre = nombre
        self.edad = edad
        self.num_identificacion = num_identificacion
        self.correo = correo
        self.telefono = telefono
        self.estado = estado

    def to_dict(self):
        return {
            "id": self.id,  # Incluir el ID en el diccionario para guardarlo
            "nombre": self.nombre,
            "edad": self.edad,
            "num_identificacion": self.num_identificacion,
            "correo": self.correo,
            "telefono": self.telefono,
            "estado": self.estado,
        }
        
    def from_dict(data):
        # Asegúrate de pasar el ID y los otros datos al crear un usuario desde un diccionario
        usuario = Usuario(data["nombre"], data["edad"], data["num_identificacion"], data["correo"], data["telefono"], data["estado"])
        usuario.id = data["id"]  # Establecer el ID del usuario desde el diccionario
        return usuario

    @staticmethod
    def nuevo_id():
        """Genera un nuevo ID para el usuario basado en los usuarios existentes."""
        usuarios = Usuario.cargar_datos("usuarios.json")
        if not usuarios:
            return 1  # Si no hay usuarios, empezamos con ID 1
        return max(usuario["id"] for usuario in usuarios) + 1

# ------------------------- CONTROLADOR -------------------------
class ClubController:
    def __init__(self):
        self.usuarios: List[Usuario] = self.cargar_usuarios()

    def agregar_usuario(self, usuario: Usuario):
        self.usuarios.append(usuario)
        self.guardar_usuarios()
        print(f"Agregado: {usuario.to_dict()}")

    def cargar_usuarios(self):
        datos = BaseModel.cargar_datos("usuarios.json")
        return [Usuario.from_dict(d) for d in datos]

    def guardar_usuarios(self):
        datos = [usuario.to_dict() for usuario in self.usuarios]
        BaseModel.guardar_datos("usuarios.json", datos)

    def generar_informe(self):
        return self.usuarios
    
     # Método para filtrar usuarios por estado (inscrito o matriculado)
    def filtrar_usuarios(self, estado: str):
        """Filtra los usuarios por su estado ('inscrito' o 'matriculado')."""
        return [usuario for usuario in self.usuarios if usuario.estado == estado]

# ------------------------- VISTA -------------------------
def main(page: ft.Page):
    page.title = "Club de Tenis"
    page.theme_mode = ft.ThemeMode.DARK

    controller = ClubController()

    # Cambiar tema
    def change_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        theme_icon_button.icon = ft.icons.DARK_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.LIGHT_MODE
        page.update()

    theme_icon_button = ft.IconButton(
        icon=ft.icons.LIGHT_MODE,
        tooltip="Cambiar tema",
        on_click=change_theme,
    )

    titulo = ft.Text("Club de Tenis", size=24, weight=ft.FontWeight.BOLD)

    app_bar = ft.AppBar(
        title=titulo,
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[theme_icon_button],
    )

    # Diálogo de aviso
    def cerrar_dialogo(e):
        aviso_dialog.open = False
        page.update()

    aviso_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Advertencia"),
        content=ft.Text("Por favor, complete todos los campos."),
        actions=[
            ft.TextButton("Cerrar", on_click=cerrar_dialogo),
        ],
    )

    # Inscripción
    def inscribir_persona(e):
        if not nombre_field.value or not id_field.value or not correo_field.value:
            page.dialog = aviso_dialog
            aviso_dialog.open = True
            page.update()
            return

        nuevo_usuario = Usuario(
            nombre=nombre_field.value,
            edad=edad_field.value,
            num_identificacion=id_field.value,
            correo=correo_field.value,
            telefono=telefono_field.value,
            
        )

        controller.agregar_usuario(nuevo_usuario)

        nombre_field.value = ""
        edad_field.value = ""
        id_field.value = ""
        correo_field.value = ""
        telefono_field.value = ""
        page.update()
        page.snack_bar = ft.SnackBar(ft.Text("Usuario inscrito exitosamente"), bgcolor=ft.colors.SUCCESS)
        page.snack_bar.open()

    # Validación para permitir solo números en el campo de identificación
    def validar_identificacion(e):
        if not e.control.value.isdigit():
            e.control.error_text = "Solo se permiten números."
            e.control.value = ''.join(filter(str.isdigit, e.control.value))
        else:
            e.control.error_text = None
        e.control.update()

    # Validación del correo electrónico
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    def validar_email(e):
        if not re.match(email_regex, e.control.value):
            e.control.error_text = "Ingrese un correo válido."
        else:
            e.control.error_text = None
        e.control.update()

    nombre_field = ft.TextField(label="Nombre", width=300)
    edad_field = ft.TextField(label="Edad", width=300, on_change=validar_identificacion)
    id_field = ft.TextField(label="Número de identificación", width=300, on_change=validar_identificacion)
    correo_field = ft.TextField(label="Correo", width=300, on_change=validar_email)
    telefono_field = ft.TextField(label="Teléfono", width=300, on_change=validar_identificacion)
    inscribir_button = ft.ElevatedButton("Inscribir", on_click=inscribir_persona)

    inscripcion_view = ft.Column([
        ft.Text("Inscripción de Miembros", size=20, weight=ft.FontWeight.BOLD),
        nombre_field, edad_field,id_field, correo_field, telefono_field, inscribir_button
    ], spacing=10)

    # Usuarios View
    def mostrar_usuarios(estado):
        usuarios_filtrados = controller.filtrar_usuarios(estado)
        usuarios_list = [ft.Text(f"{usuario.nombre} - {usuario.estado}") for usuario in usuarios_filtrados]
        return ft.Column(usuarios_list, spacing=5)
    
     # Filtros para mostrar matriculados e inscritos
    def mostrar_matriculados(e):
        content.controls.clear()
        content.controls.append(mostrar_usuarios("matriculado"))
        page.update()

    def mostrar_inscritos(e):
        content.controls.clear()
        content.controls.append(mostrar_usuarios("inscrito"))
        page.update()
        
    matriculados_button = ft.ElevatedButton("Mostrar Matriculados", on_click=mostrar_matriculados)
    inscritos_button = ft.ElevatedButton("Mostrar Inscritos", on_click=mostrar_inscritos)

    Usuarios_view = ft.Column([
        ft.Text("Usuarios", size=20, weight=ft.FontWeight.BOLD),
        matriculados_button,
        inscritos_button
    ], spacing=10)
    

    # Seguimiento
    torneos_view = ft.Column([
        ft.Text("Seguimiento", size=20, weight=ft.FontWeight.BOLD),
        ft.Text("Aquí se implementará la funcionalidad de seguimiento.")
    ], spacing=10)

    # Informes
    def generar_informes(anio, mes):
        informe_view.controls.clear()
        informe_view.controls.append(ft.Text("Informe de Miembros", size=20, weight=ft.FontWeight.BOLD))
        
        # Asegurarse de que el mes tiene dos dígitos
        mes_formateado = str(mes).zfill(2)
        
        # Cargar los datos de los usuarios desde el archivo JSON
        try:
            with open("base_de_datos/usuarios.json", "r") as archivo_usuarios:
                usuarios = json.load(archivo_usuarios)
        except FileNotFoundError:
            print("El archivo de usuarios no se encuentra.")
            print(os.getcwd())
            return
        except json.JSONDecodeError:
            print("El archivo de usuarios no está en el formato correcto.")
            return

        # Filtrar usuarios con estado 'matriculado'
        usuarios_matriculados = [usuario for usuario in usuarios if usuario['estado'] == 'matriculado']

        # Generar un informe para cada miembro matriculado
        for usuario in usuarios_matriculados:
            Informe.crear_informe(usuario['id'], mes_formateado, anio)


        print(f"Informes generados para el mes {mes} del anio {anio}")

        #informe_view.update()

    informe_view = ft.Column([], spacing=10)
    #Ejemplo
    anio = 2025
    mes = 1
    generar_informe_button = ft.ElevatedButton("Generar Informe", on_click=lambda e: generar_informes(anio, mes)) #Modificar para que sea dinamico en el front

    entrenamientos_view = ft.Column([
        ft.Text("Informes", size=20, weight=ft.FontWeight.BOLD),
        generar_informe_button,
        informe_view
    ], spacing=10)

    pagos_view = ft.Column([
        ft.Text("Infome de Pagos Mensuales", size=20, weight=ft.FontWeight.BOLD),
        generar_informe_button,
        informe_view
    ], spacing=10)

    def crear_entrenamiento(anio, mes, dia):
        # Formatear día y mes para asegurar el formato de dos dígitos
        dia_formateado = str(dia).zfill(2)
        mes_formateado = str(mes).zfill(2)
        
        # Componer la fecha en formato aaaa-mm-dd
        fecha = f"{anio}-{mes_formateado}-{dia_formateado}"
        
        # Intentar crear un nuevo objeto de Entrenamiento
        try:
            nuevo_entrenamiento = Entrenamiento(id=Entrenamiento.nuevo_id(), fecha=fecha)
            nuevo_entrenamiento.guardar()  # Guarda el entrenamiento en la base de datos
            nuevo_entrenamiento.crear_asistencia_entrenamientos()  # Crea asistencias para todos los usuarios
            print(f"Entrenamiento creado para la fecha {fecha}")
        except Exception as e:
            print(f"No se pudo crear el entrenamiento: {e}")
    
    # crear_entrenamiento_button = ft.ElevatedButton("Crear Entrenamiento", on_click=lambda e: crear_entrenamiento(anio, mes, dia)) #Modificar para que sea dinamico en el front
    
    def crear_torneo(anio, mes, dia):
        # Formatear día y mes para asegurar el formato de dos dígitos
        dia_formateado = str(dia).zfill(2)
        mes_formateado = str(mes).zfill(2)
        
        # Componer la fecha en formato aaaa-mm-dd
        fecha = f"{anio}-{mes_formateado}-{dia_formateado}"
        
        # Intentar crear un nuevo objeto de Torneo
        nuevo_torneo = Torneo(
            id=Torneo.nuevo_id(),
            nombre="Nombre del Torneo",  # Asumiendo que el nombre se proveerá o se manejará de otra manera
            fecha=fecha
        )
        nuevo_torneo.guardar()
        print(f"Torneo creado para la fecha {fecha}")

    #crear_torneo_button = ft.ElevatedButton("Crear Torneo", on_click=lambda e: crear_torneo(anio, mes, dia)) #Modificar para que sea dinamico en el front

    def crear_asistencia_torneo(torneo_id, miembro_id, puesto):
        Asistencia_Torneo.crear_asistencia(
            torneo_id=torneo_id,
            miembro_id=miembro_id,
            puesto=puesto
        )
        print(f"Asistencia para el torneo {torneo_id} creada para el miembro {miembro_id} con puesto {puesto}")

    #crear_asistencia_torneo_button = ft.ElevatedButton("Aceptar", on_click=lambda e: crear_asistencia_torneo(usuario_id, torneo_id, puesto)) #Modificar para que sea dinamico en el front



    def tomar_asistencia_entrenamiento(usuario_id, entrenamiento_id, estado):
        # Verificar que el estado sea válido
        if estado not in ["ausente", "presente"]:
            print("Error: Estado no válido. Debe ser 'ausente' o 'presente'.")
            return
        
        # Encontrar el ID de la asistencia correspondiente
        asistencia_id = Asistencia_Entrenamiento.find_by_user_and_entrenamiento_id(usuario_id, entrenamiento_id)
        
        if asistencia_id is None:
            print("No se encontró una asistencia correspondiente con los datos proporcionados.")
            return
        
        # Cargar el objeto Asistencia_Entrenamiento usando el ID encontrado
        try:
            with open("base_de_datos/asistencia_entrenamientos.json", "r") as archivo:
                asistencias = json.load(archivo)
            
            # Encontrar el objeto asistencia específico y cambiar su estado
            asistencia = next((item for item in asistencias if item["id"] == asistencia_id), None)
            if asistencia:
                asistencia_obj = Asistencia_Entrenamiento(id=asistencia['id'], usuario_id=asistencia['usuario_id'], entrenamiento_id=asistencia['entrenamiento_id'], estado=asistencia['estado'])
                asistencia_obj.cambiar_estado(estado)
                print(f"Estado de asistencia actualizado correctamente a {estado}.")
            else:
                print("No se pudo cargar la asistencia correctamente.")
        except FileNotFoundError:
            print("Archivo de asistencias no encontrado.")
        except json.JSONDecodeError:
            print("Error al decodificar el archivo de asistencias.")
        
    #tomar_asistencia_entrenamiento_button = ft.ElevatedButton("Aceptar", on_click=lambda e: tomar_asistencia_entrenamiento(usuario_id, entrenamiento_id, estado)) #Modificar para que sea dinamico en el front



    # Cambiar vistas
    def destination_change(e):
        index = e.control.selected_index
        content.controls.clear()
        if index == 0:
            content.controls.append(inscripcion_view)
        elif index == 1:
            content.controls.append(Usuarios_view)
        elif index == 2:
            content.controls.append(torneos_view)
        elif index == 3:
            content.controls.append(entrenamientos_view)
        elif index ==4:
            content.controls.append(pagos_view)
        page.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.PERSON_ADD, label="Inscripción"),
            ft.NavigationRailDestination(icon=ft.icons.GROUP, label="Usuarios"),
            ft.NavigationRailDestination(icon=ft.icons.SPORTS_TENNIS, label="Torneos"),
            ft.NavigationRailDestination(icon=ft.icons.FITNESS_CENTER, label="Entrenamientos"),
            ft.NavigationRailDestination(icon=ft.icons.REPORT, label="Informe"),
            ft.NavigationRailDestination(icon=ft.icons.ATTACH_MONEY,label="Pagos"),
        ],
        on_change=destination_change,
    )

    content = ft.Column([inscripcion_view], expand=True)

    page.add(app_bar, ft.Row([rail, ft.VerticalDivider(width=1), content], expand=True))

ft.app(target=main)