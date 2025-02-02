import flet as ft
import re
import json
from modelos.base_model import BaseModel  # Importar BaseModel desde base_model.py
from modelos.usuario import Usuario  # Importar la nueva clase Usuario
from modelos.Inscripcion import Inscripcion
from modelos.informe import Informe
from modelos.entrenamiento import Entrenamiento
from modelos.torneo import Torneo
from modelos.asistencia_torneos import Asistencia_Torneo
from modelos.asistencia_entrenamientos import Asistencia_Entrenamiento
from datetime import datetime
import os
from controllers.club_controller import ClubController

from utils.validations import validar_identificacion, validar_email, validar_apellidos, validar_nombre, validar_fecha, validar_telefono,es_dia_valido, validar_edad

# ------------------------- CONTROLADOR -------------------------
from controllers.club_controller import ClubController  

# ------------------------- VISTAS -------------------------
from views.inscripcion_view import create_inscripcion_view
from views.usuarios_view import create_usuarios_view
from views.torneos_view import create_torneos_view
from views.entrenamientos_view import create_entrenamientos_view
from views.informes_view import create_informes_view
from views.pagos_view import create_pagos_view



# ------------------------- VISTA -------------------------
def main(page: ft.Page):
    page.title = "TopSpinTracker"
    page.theme_mode = ft.ThemeMode.DARK

    controller = ClubController()

    current_user = None
    # Crear las vistas y recibir las referencias necesarias
    inscripcion_view, nombre_field, apellidos_field, edad_field, id_field, correo_field, telefono_field = create_inscripcion_view(
        page,
        controller, 
        validar_identificacion, 
        validar_email, 
        validar_apellidos, 
        validar_nombre, 
        validar_telefono, 
        validar_edad
    )
    content = ft.Column([], expand=True)
    usuarios_view, mostrar_usuarios_view = create_usuarios_view(controller, page, content)
    torneos = controller.cargar_torneos()  # Esto cargará la lista de torneos
    torneos_view, torneos_list, dropdown_torneos, actualizar_data_torneos = create_torneos_view(controller, torneos, page)
    entrenamientos_view, entrenamientos_list, dropdown_entrenamientos, actualizar_entrenamientos = create_entrenamientos_view(controller, page)
    informes_view, input_anio, input_mes, informe_container = create_informes_view(controller, page)
    
    
    def change_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        theme_icon_button.icon = ft.icons.DARK_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.LIGHT_MODE
        page.update()

    theme_icon_button = ft.IconButton(
        icon=ft.icons.LIGHT_MODE,
        tooltip="Cambiar tema",
        on_click=change_theme,
    )

    titulo = ft.Text("TopSpinTracker", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

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

    def update_current_user(user_id):
        global current_user
        # Carga la base de datos de usuarios
        try:
            with open('base_de_datos/usuarios.json', 'r') as file:
                users = json.load(file)
        except FileNotFoundError:
            print("El archivo de base de datos no fue encontrado.")
            return

        # Busca el usuario con el ID proporcionado
        for user in users:
            if user['id'] == user_id:
                current_user = user
                break
        else:
            print("Usuario no encontrado.")


    #Obtener usuario pendiente
    def mostrar_lista_usuarios_pendientes():
        usuarios_pendientes = ClubController.obtener_usuarios_pendientes()
        print(json.dumps(usuarios_pendientes, indent=4))


        usuarios_view.controls.clear()

        for usuario in usuarios_pendientes:
            usuarios_view.controls.append(
                ft.Row([
                    ft.Text(f"{usuario['nombre']} - {usuario['correo']}"),
                    ft.ElevatedButton(
                        "Rellenar datos",
                        icon=ft.icons.ARROW_FORWARD,
                        on_click=lambda e, u=usuario: (
                            llenar_campos_inscripcion(
                                u, nombre_field, apellidos_field, edad_field, id_field, correo_field, telefono_field
                            ),  # Llenar los campos de inscripción
                            destination_change(ft.ControlEvent(selected_index=0))  # Cambiar a la pestaña de inscripción
                        )
                    )
                ])
            )

        page.update()


    def llenar_campos_inscripcion(usuario, nombre_field, apellidos_field, edad_field, id_field, correo_field, telefono_field):
        """
        Llena los campos de inscripción con los datos del usuario seleccionado.
        """
        # Llenar los campos con la información del usuario
        nombre_field.value = usuario.get("nombre", "")
        apellidos_field.value = usuario.get("apellidos", "")
        edad_field.value = str(usuario.get("edad", ""))
        id_field.value = usuario.get("num_identificacion", "")
        correo_field.value = usuario.get("correo", "")
        telefono_field.value = usuario.get("telefono", "")
    
        # Actualizar los campos para reflejar los cambios en la interfaz
        nombre_field.update()
        apellidos_field.update()
        edad_field.update()
        id_field.update()
        correo_field.update()
        telefono_field.update()
    
        # Cambiar a la vista de inscripción automáticamente
        destination_change(ft.ControlEvent(selected_index=0))  # 0 es la pestaña de inscripción
    
        # Actualizar la página
        page.update()

    def destination_change(e):
        index = e.control.selected_index if hasattr(e, 'control') else e.selected_index  # Soporta llamado manual

        content.controls.clear()
        if index == 0:
            content.controls.append(inscripcion_view)  # Mostrar vista de inscripción
        elif index == 1:
            content.controls.append(usuarios_view)
        elif index == 2:
            content.controls.append(torneos_view)
            page.update()
            actualizar_data_torneos()
        elif index == 3:
            content.controls.append(entrenamientos_view)
            page.update()
            actualizar_entrenamientos()
            return
        elif index == 4:
            content.controls.append(informes_view)
        elif index == 5:
            pagos_view = create_pagos_view(controller, page)
            content.controls.append(pagos_view)
        elif index == 6:
            content.controls.append(usuarios_view)
            mostrar_lista_usuarios_pendientes()

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
            ft.NavigationRailDestination(icon=ft.icons.FITNESS_CENTER, label="Entrenamiento"),
            ft.NavigationRailDestination(icon=ft.icons.BAR_CHART, label="Informes"),
            ft.NavigationRailDestination(icon=ft.icons.ATTACH_MONEY, label="Pagos"),
            ft.NavigationRailDestination(icon=ft.icons.PERSON_SEARCH, label="Usuarios Pendientes"),
        ],
        on_change=lambda e: destination_change(e)
    )

    page.add(app_bar, ft.Row([rail, ft.VerticalDivider(width=1), content], expand=True))

ft.app(target=main)
