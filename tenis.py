import flet as ft
import re
import json
from typing import List
from modelos.informe import Informe
from modelos.entrenamiento import Entrenamiento
from modelos.torneo import Torneo
from modelos.asistencia_torneos import Asistencia_Torneo
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
        usuario = Usuario(data["nombre"], data["edad"], data["num_identificacion"], data["correo"], data["telefono"], data["estado"])
        usuario.id = data["id"]  # Establecer el ID del usuario desde el diccionario
        return usuario

    @staticmethod
    def nuevo_id():
        usuarios = Usuario.cargar_datos("usuarios.json")
        if not usuarios:
            return 1
        return max(usuario["id"] for usuario in usuarios) + 1

# ------------------------- CONTROLADOR -------------------------
class ClubController:
    def __init__(self):
        self.usuarios: List[Usuario] = self.cargar_usuarios()

    def agregar_usuario(self, usuario: Usuario):
        self.usuarios.append(usuario)
        self.guardar_usuarios()

    def cargar_usuarios(self):
        datos = BaseModel.cargar_datos("usuarios.json")
        return [Usuario.from_dict(d) for d in datos]

    def guardar_usuarios(self):
        datos = [usuario.to_dict() for usuario in self.usuarios]
        BaseModel.guardar_datos("usuarios.json", datos)

    def filtrar_usuarios(self, estado: str):
        return [usuario for usuario in self.usuarios if usuario.estado == estado]
    
    def cargar_torneos(self):
        datos = BaseModel.cargar_datos("torneos.json")
        return [Torneo(**d) for d in datos]

# ------------------------- VISTA -------------------------
def main(page: ft.Page):
    page.title = "Club de Tenis"
    page.theme_mode = ft.ThemeMode.DARK

    controller = ClubController()

    def change_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        theme_icon_button.icon = ft.icons.DARK_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.LIGHT_MODE
        page.update()

    theme_icon_button = ft.IconButton(
        icon=ft.icons.LIGHT_MODE,
        tooltip="Cambiar tema",
        on_click=change_theme,
    )

    titulo = ft.Text("Club de Tenis", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    app_bar = ft.AppBar(
        title=titulo,
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[theme_icon_button],
    )

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
        page.snack_bar = ft.SnackBar(
            ft.Text("Usuario inscrito exitosamente", color=ft.colors.WHITE), bgcolor=ft.colors.GREEN
        )
        page.snack_bar.open()
        page.update()

    def validar_identificacion(e):
        if not e.control.value.isdigit():
            e.control.error_text = "Solo se permiten números."
            e.control.value = ''.join(filter(str.isdigit, e.control.value))
        else:
            e.control.error_text = None
        e.control.update()

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    def validar_email(e):
        if not re.match(email_regex, e.control.value):
            e.control.error_text = "Ingrese un correo válido."
        else:
            e.control.error_text = None
        e.control.update()

    nombre_field = ft.TextField(label="Nombre", width=400, border_color=ft.colors.OUTLINE, expand=True)
    edad_field = ft.TextField(label="Edad", width=400, border_color=ft.colors.OUTLINE, expand=True, on_change=validar_identificacion)
    id_field = ft.TextField(label="Número de identificación", width=400, border_color=ft.colors.OUTLINE, expand=True, on_change=validar_identificacion)
    correo_field = ft.TextField(label="Correo", width=400, border_color=ft.colors.OUTLINE, expand=True, on_change=validar_email)
    telefono_field = ft.TextField(label="Teléfono", width=400, border_color=ft.colors.OUTLINE, expand=True, on_change=validar_identificacion)
    inscribir_button = ft.ElevatedButton(
        "Inscribir",
        on_click=inscribir_persona,
        icon=ft.icons.PERSON_ADD,
        bgcolor=ft.colors.PRIMARY,
        color=ft.colors.WHITE,
    )

    inscripcion_view = ft.Column(
        [
            ft.Text("Inscripción de Miembros", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(height=10, thickness=2),
            nombre_field,
            edad_field,
            id_field,
            correo_field,
            telefono_field,
            inscribir_button,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
    )

    def mostrar_info_usuario(usuario):
        usuario_info = ft.Column(
            [
                ft.Text("Información del Usuario", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10, thickness=2),
                ft.Text(f"Nombre: {usuario.nombre}"),
                ft.Text(f"Edad: {usuario.edad}"),
                ft.Text(f"Identificación: {usuario.num_identificacion}"),
                ft.Text(f"Correo: {usuario.correo}"),
                ft.Text(f"Teléfono: {usuario.telefono}"),
                ft.Text(f"Estado: {usuario.estado}"),
                ft.ElevatedButton("Regresar", on_click=lambda e: mostrar_usuarios_view("inscrito")),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        )
        content.controls.clear()
        content.controls.append(usuario_info)
        page.update()

    def mostrar_usuarios_view(estado):
        usuarios_filtrados = controller.filtrar_usuarios(estado)
        usuarios_list = [
            ft.ListTile(
                title=ft.Text(usuario.nombre, weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(f"Estado: {usuario.estado}"),
                leading=ft.Icon(ft.icons.PERSON),
                on_click=lambda e, u=usuario: mostrar_info_usuario(u),
            )
            for usuario in usuarios_filtrados
        ]
        usuarios_view = ft.ListView(
            [
                ft.Text("Usuarios", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10, thickness=2),
                *usuarios_list,
            ],
            spacing=10,
            expand=True,
        )
        content.controls.clear()
        content.controls.append(usuarios_view)
        page.update()


    matriculados_button = ft.ElevatedButton("Mostrar Matriculados", on_click=lambda e: mostrar_usuarios_view("matriculado"))
    inscritos_button = ft.ElevatedButton("Mostrar Inscritos", on_click=lambda e: mostrar_usuarios_view("inscrito"))

    usuarios_menu_view = ft.Column(
        [
            ft.Text("Usuarios", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(height=10, thickness=2),
            matriculados_button,
            inscritos_button,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
    )

    def inscribir_a_torneo(e):
        if not dropdown_usuarios.value or not dropdown_torneos.value:
            page.snack_bar = ft.SnackBar(ft.Text("Debe seleccionar un usuario y un torneo"), bgcolor=ft.colors.ERROR)
            page.snack_bar.open()
            return

        # Aquí se manejaría la lógica para inscribir al usuario seleccionado en el torneo seleccionado
        page.dialog = ft.AlertDialog(
            title=ft.Text("Inscripción Exitosa"),
            content=ft.Text(f"El usuario '{dropdown_usuarios.value}' ha sido inscrito exitosamente en el torneo '{dropdown_torneos.value}'!"),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: page.dialog.close()),
            ],
        )
        page.dialog.open()
        page.update()

    def agregar_torneo(e):
        nuevo_torneo = Torneo(id=Torneo.nuevo_id(), nombre="Nuevo Torneo", fecha="2025-01-01")
        nuevo_torneo.guardar()
        actualizar_torneos()
        page.snack_bar = ft.SnackBar(ft.Text("Torneo añadido"), bgcolor=ft.colors.GREEN)
        page.snack_bar.open()

    def actualizar_torneos():
        torneos = controller.cargar_torneos()
        dropdown_torneos.options = [ft.dropdown.Option(torneo.nombre) for torneo in torneos]
        torneos_list.controls.clear()
        torneos_list.controls.append(
            ft.ListView(
                [
                    ft.ListTile(title=ft.Text(torneo.nombre), subtitle=ft.Text(torneo.fecha)) for torneo in torneos
                ],
                expand=True,
                spacing=10,
            )
        )
        page.update()

    dropdown_usuarios = ft.Dropdown(
        label="Seleccionar Usuario",
        options=[ft.dropdown.Option(usuario.nombre) for usuario in controller.filtrar_usuarios("matriculado")],
    )

    dropdown_torneos = ft.Dropdown(label="Seleccionar Torneo", options=[])

    inscribir_button = ft.ElevatedButton(
        "Inscribir en Torneo", icon=ft.icons.CHECK, on_click=inscribir_a_torneo
    )

    torneos_list = ft.Column([])

    agregar_torneo_button = ft.FloatingActionButton(
        icon=ft.icons.ADD, on_click=agregar_torneo, tooltip="Añadir Torneo"
    )

    torneos_view = ft.Row(
        [
            ft.Container(
                ft.Column(
                    [
                        dropdown_usuarios,
                        dropdown_torneos,
                        inscribir_button,
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.START,
                ),
                width=300,
                padding=20,
                bgcolor=ft.colors.SURFACE_VARIANT,
                border_radius=10,
            ),
            ft.VerticalDivider(width=1),
            ft.Container(
                ft.Column(
                    [
                        ft.Text("Torneos", size=24, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10, thickness=2),
                        torneos_list,
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.START,
                ),
                expand=True,
                padding=20,
            ),
        ],
        expand=True,
    )

    actualizar_torneos()

    informe_view = ft.Column(
        [
            ft.Text("Informes", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(height=10, thickness=2),
            ft.ElevatedButton("Generar Informe", icon=ft.icons.BAR_CHART),
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
    )

    pagos_view = ft.Column(
        [
            ft.Text("Informe de Pagos Mensuales", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(height=10, thickness=2),
            ft.ElevatedButton("Generar Informe de Pagos", icon=ft.icons.ATTACH_MONEY),
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
    )

    def destination_change(e):
        index = e.control.selected_index
        content.controls.clear()
        if index == 0:
            content.controls.append(inscripcion_view)
        elif index == 1:
            content.controls.append(usuarios_menu_view)
        elif index == 2:
            content.controls.append(torneos_view)
        elif index == 3:
            content.controls.append(informe_view)
        elif index == 4:
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
            ft.NavigationRailDestination(icon=ft.icons.BAR_CHART, label="Informes"),
            ft.NavigationRailDestination(icon=ft.icons.ATTACH_MONEY, label="Pagos"),
        ],
        on_change=destination_change,
    )

    content = ft.Column([inscripcion_view], expand=True)

    page.add(app_bar, ft.Row([rail, ft.VerticalDivider(width=1), content], expand=True))

ft.app(target=main)
