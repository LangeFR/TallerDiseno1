import flet as ft
import re
import json
from typing import List
from modelos.informe import Informe
import os

# ------------------------- MODELO -------------------------
# Clase base para persistencia de datos
class BaseModel:
    @staticmethod
    def guardar_datos(nombre_archivo, datos):
        with open(nombre_archivo, 'w') as file:
            json.dump(datos, file, indent=4)

    @staticmethod
    def cargar_datos(nombre_archivo):
        try:
            with open(nombre_archivo, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

# Clase Miembro
class Miembro(BaseModel):
    def __init__(self, nombre, edad, contacto, identificacion, correo, telefono):
        self.nombre = nombre
        self.edad = edad
        self.contacto = contacto
        self.identificacion = identificacion
        self.correo = correo
        self.telefono = telefono


    def to_dict(self):
        return {
            "nombre": self.nombre,
            "edad": self.edad,
            "contacto": self.contacto,
            "identificacion": self.identificacion,
            "correo": self.correo,
            "telefono": self.telefono,

        }

    @staticmethod
    def from_dict(data):
        return Miembro(
            data["nombre"],
            data["edad"],          # Asegúrate de pasar la edad
            data["contacto"],      # Asegúrate de pasar el contacto
            data["identificacion"], # Asegúrate de pasar la identificación
            data["correo"],        # Asegúrate de pasar el correo
            data["telefono"],      # Asegúrate de pasar el teléfono
        )

# ------------------------- CONTROLADOR -------------------------
class ClubController:
    def __init__(self):
        self.miembros: List[Miembro] = self.cargar_miembros()

    def agregar_miembro(self, miembro: Miembro):
        self.miembros.append(miembro)
        self.guardar_miembros()

    def cargar_miembros(self):
        datos = BaseModel.cargar_datos("usuarios.json")
        return [Miembro.from_dict(d) for d in datos]

    def guardar_miembros(self):
        datos = [miembro.to_dict() for miembro in self.miembros]
        BaseModel.guardar_datos("usuarios.json", datos)

    def generar_informe(self):
        return self.miembros

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

        nuevo_miembro = Miembro(
            nombre=nombre_field.value,
            edad=edad_field.value,
            contacto=contacto_field.value,
            identificacion=id_field.value,
            correo=correo_field.value,
            telefono=telefono_field.value,
            
        )

        controller.agregar_miembro(nuevo_miembro)

        nombre_field.value = ""
        edad_field.value = ""
        contacto_field.value = ""
        id_field.value = ""
        correo_field.value = ""
        telefono_field.value = ""
        page.update()
        page.snack_bar = ft.SnackBar(ft.Text("Miembro inscrito exitosamente"), bgcolor=ft.colors.SUCCESS)
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
    contacto_field = ft.TextField(label="Contacto", width=300)
    id_field = ft.TextField(label="Número de identificación", width=300, on_change=validar_identificacion)
    correo_field = ft.TextField(label="Correo", width=300, on_change=validar_email)
    telefono_field = ft.TextField(label="Teléfono", width=300, on_change=validar_identificacion)
    inscribir_button = ft.ElevatedButton("Inscribir", on_click=inscribir_persona)

    inscripcion_view = ft.Column([
        ft.Text("Inscripción de Miembros", size=20, weight=ft.FontWeight.BOLD),
        nombre_field, edad_field, contacto_field ,id_field, correo_field, telefono_field, inscribir_button
    ], spacing=10)

    # Matrícula
    matricula_view = ft.Column([
        ft.Text("Matrícula", size=20, weight=ft.FontWeight.BOLD),
        ft.Text("Aquí se implementará la funcionalidad de matrícula.")
    ], spacing=10)

    # Seguimiento
    seguimiento_view = ft.Column([
        ft.Text("Seguimiento", size=20, weight=ft.FontWeight.BOLD),
        ft.Text("Aquí se implementará la funcionalidad de seguimiento.")
    ], spacing=10)

    # Informes
    def generar_informes(mes, anio):
        informe_view.controls.clear()
        informe_view.controls.append(ft.Text("Informe de Miembros", size=20, weight=ft.FontWeight.BOLD))
        
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
            Informe.crear_informe(usuario['id'], mes, anio)

        print(f"Informes generados para el mes {mes} del anio {anio}")

        informe_view.update()

    informe_view = ft.Column([], spacing=10)
    generar_informe_button = ft.ElevatedButton("Generar Informe", on_click=generar_informes(1, 2025))

    informes_view = ft.Column([
        ft.Text("Informes", size=20, weight=ft.FontWeight.BOLD),
        generar_informe_button,
        informe_view
    ], spacing=10)

    # Cambiar vistas
    def destination_change(e):
        index = e.control.selected_index
        content.controls.clear()
        if index == 0:
            content.controls.append(inscripcion_view)
        elif index == 1:
            content.controls.append(matricula_view)
        elif index == 2:
            content.controls.append(seguimiento_view)
        elif index == 3:
            content.controls.append(informes_view)
        page.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.PERSON_ADD, label="Inscripción"),
            ft.NavigationRailDestination(icon=ft.icons.BOOKMARK, label="Matrícula"),
            ft.NavigationRailDestination(icon=ft.icons.TIMELINE, label="Seguimiento"),
            ft.NavigationRailDestination(icon=ft.icons.REPORT, label="Informes"),
        ],
        on_change=destination_change,
    )

    content = ft.Column([inscripcion_view], expand=True)

    page.add(app_bar, ft.Row([rail, ft.VerticalDivider(width=1), content], expand=True))

ft.app(target=main)