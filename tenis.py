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

from views.entrenamientos_view import create_entrenamientos_view
from views.pagos_view import create_pagos_view

from views.usuarios_view import ContenedorUsuario, ContenedorUsuarioAdmin
from views.informes_view import ContenedorInformeSuper, ContenedorInformeView
from views.torneos_view import ContenedorTorneosSuper, ContenedorTorneos



# ------------------------- VISTA -------------------------
def main(page: ft.Page):
    page.title = "TopSpinTracker"
    page.theme_mode = ft.ThemeMode.DARK

    controller = ClubController()

    current_user = None
    content = ft.Column([], expand=True)
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,  
    )
    titulo = ft.Text("TopSpinTracker", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    def change_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        theme_icon_button.icon = ft.icons.DARK_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.LIGHT_MODE
        page.update()
    theme_icon_button = ft.IconButton(
        icon=ft.icons.LIGHT_MODE,
        tooltip="Cambiar tema",
        on_click=change_theme,
    )
    app_bar = ft.AppBar(
        title=titulo,
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[theme_icon_button],
    )
    
    page.add(app_bar, ft.Row([rail, ft.VerticalDivider(width=1), content], expand=True))

    def setup_navigation(user_role):
        global view_functions  # Declara globalmente para que sea accesible en otras funciones
        if user_role == "admin":
            destinations = [
                ft.NavigationRailDestination(icon=ft.icons.PERSON_ADD, label="Inscripción"),
                ft.NavigationRailDestination(icon=ft.icons.GROUP, label="Usuarios"),
                ft.NavigationRailDestination(icon=ft.icons.SPORTS_TENNIS, label="Torneos"),
                ft.NavigationRailDestination(icon=ft.icons.FITNESS_CENTER, label="Entrenamiento"),
                ft.NavigationRailDestination(icon=ft.icons.BAR_CHART, label="Informes"),
                ft.NavigationRailDestination(icon=ft.icons.ATTACH_MONEY, label="Pagos"),
                ft.NavigationRailDestination(icon=ft.icons.PERSON_SEARCH, label="Usuarios Pendientes"),
            ]
            view_functions = [
                lambda: content.controls.append(inscripcion_view),
                lambda: content.controls.append(ContenedorUsuarioAdmin(controller, page).get_contenedor()),
                lambda: content.controls.append(ContenedorTorneosSuper(controller, torneos, page).get_contenedor()),
                lambda: content.controls.append(entrenamientos_view),
                lambda: content.controls.append(ContenedorInformeSuper(controller, page).get_contenedor()),
                lambda: content.controls.append(create_pagos_view(controller, page)),
                lambda: mostrar_lista_usuarios_pendientes(),
            ]
        elif user_role == "coach":
            destinations = [
                ft.NavigationRailDestination(icon=ft.icons.GROUP, label="Usuarios"),
                ft.NavigationRailDestination(icon=ft.icons.FITNESS_CENTER, label="Entrenamiento"),
                ft.NavigationRailDestination(icon=ft.icons.BAR_CHART, label="Informes"),
            ]
            view_functions = [
                lambda: content.controls.append(ContenedorUsuario(controller, page, content, current_user["id"]).get_contenedor()),
                lambda: content.controls.append(entrenamientos_view),
                lambda: content.controls.append(ContenedorInformeSuper(controller, page).get_contenedor()),
            ]
        elif user_role == "miembro":
            destinations = [
                ft.NavigationRailDestination(icon=ft.icons.GROUP, label="Usuarios"),
                ft.NavigationRailDestination(icon=ft.icons.SPORTS_TENNIS, label="Torneos"),
                ft.NavigationRailDestination(icon=ft.icons.BAR_CHART, label="Informes"),
                ft.NavigationRailDestination(icon=ft.icons.ATTACH_MONEY, label="Pagos"),
            ]
            view_functions = [
                lambda: content.controls.append(ContenedorUsuario(controller, page, current_user["id"]).get_contenedor()),
                lambda: content.controls.append(ContenedorTorneos(controller, torneos, page, current_user['id']).get_contenedor()),
                lambda: content.controls.append(ContenedorInformeView(controller, page, current_user["id"]).get_contenedor()),
                lambda: content.controls.append(create_pagos_view(controller, page)),
            ]
        else:
            destinations = []  # No visible tabs if no role or unrecognized role
            view_functions = []

        rail.destinations = destinations
        rail.update()

        return view_functions

    def update_current_user(user_id):
        nonlocal current_user  # Use nonlocal to modify the variable defined in the outer scope
        try:
            with open('base_de_datos/usuarios.json', 'r') as file:
                users = json.load(file)
            for user in users:
                if user['id'] == user_id:
                    current_user = user
                    setup_navigation(user.get("rol"))  # Update navigation based on role
                    print("Navigation setup for:", user.get("rol"))
                    break
            else:
                print("Usuario no encontrado.")
        except FileNotFoundError:
            print("El archivo de base de datos no fue encontrado.")
        except Exception as e:
            print(f"Error al actualizar el usuario: {e}")

    def test_current_user_setup():
        """
        Esta función configura el entorno de prueba actualizando el usuario actual a diferentes roles.
        Está diseñada para ser llamada antes de cada prueba para garantizar que el contexto del usuario esté correctamente configurado.
        """
        print("Configurando entorno de prueba...")

        # Cambiar a 'admin' para la prueba
        update_current_user(1)  # ID de usuario para 'admin'
        print("Configurado como Admin para la prueba.")

        # Cambiar a 'miembro' para la prueba
        #update_current_user(17)  # ID de usuario para 'jugador'
        #print("Configurado como Jugador para la prueba.")

        # Cambiar a 'coach' para la prueba
        # update_current_user(17)  # ID de usuario para 'coach'
        # print("Configurado como Admin para la prueba.")

    # Ejecutar la configuración de prueba antes de iniciar cualquier otra operación
    print("----------------------------------------------------------------")
    test_current_user_setup()
    
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
    
    #usuarios_view, mostrar_usuarios_view = create_usuarios_view(controller, page, content)
    torneos = controller.cargar_torneos()  # Esto cargará la lista de torneos
    #torneos_view, torneos_list, dropdown_torneos, actualizar_data_torneos = create_torneos_view(controller, torneos, page)
    entrenamientos_view, entrenamientos_list, dropdown_entrenamientos, actualizar_entrenamientos = create_entrenamientos_view(controller, page)
    #informes_view, input_anio, input_mes, informe_container = create_informes_view(controller, page)
        

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


    def destination_change(e):
        index = e.control.selected_index
        content.controls.clear()
        if index < len(view_functions):
            view_functions[index]()  # Call the function associated with the current index
        else:
            content.controls.append(ft.Text("Esta sección no está disponible.", size=18))
        page.update()

    rail.on_change = lambda e: destination_change(e)

       

ft.app(target=main)
