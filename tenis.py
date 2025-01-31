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
    page.title = "Club de Tenis"
    page.theme_mode = ft.ThemeMode.DARK

    controller = ClubController()

    # Crear las vistas y recibir las referencias necesarias
    # Crear las vistas y recibir las referencias necesarias
    inscripcion_view, nombre_field, apellidos_field, edad_field, id_field, correo_field, telefono_field = create_inscripcion_view(
        controller, 
        validar_identificacion, 
        validar_email, 
        validar_apellidos, 
        validar_nombre, 
        validar_telefono, 
        validar_edad
    )
    usuarios_view = create_usuarios_view(controller)
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
        # Validar campos vacíos
        if not nombre_field.value or not apellidos_field.value or not id_field.value or not correo_field.value:
            page.dialog = aviso_dialog
            aviso_dialog.open = True
            page.update()
            return

        # Validar edad (no puede ser mayor a 116 años)
        try:
            edad = int(edad_field.value)
            if not validar_edad(edad):
                page.snack_bar = ft.SnackBar(
                    ft.Text("La edad no puede ser mayor a 116 años", color=ft.colors.WHITE), bgcolor=ft.colors.RED
                )
                page.snack_bar.open = True
                page.update()
                return
        except ValueError:
            page.snack_bar = ft.SnackBar(
                ft.Text("Edad inválida", color=ft.colors.WHITE), bgcolor=ft.colors.RED
            )
            page.snack_bar.open = True
            page.update()
            return

        # Llamar a las funciones de validación
        if not (validar_nombre(nombre_field) and validar_apellidos(apellidos_field) and 
                validar_email(correo_field) and validar_telefono(telefono_field)) and validar_identificacion(id_field):
            page.snack_bar = ft.SnackBar(
                ft.Text("Corrija los errores en los campos", color=ft.colors.WHITE), bgcolor=ft.colors.RED
            )
            page.snack_bar.open = True
            page.update()
            return

        # Validar número de identificación (máximo 10 dígitos)
        if len(id_field.value) > 10 or len(id_field.value) < 8 or not id_field.value.isdigit():
            page.snack_bar = ft.SnackBar(
                ft.Text("La identificación debe ser numérica y tener entre 8 y 10 dígitos.", color=ft.colors.WHITE), bgcolor=ft.colors.RED
            )
            page.snack_bar.open = True
            page.update()
            return

        # Validar número de celular (de 8 a 12 dígitos)
        if len(telefono_field.value) < 8 or len(telefono_field.value) > 12 or not telefono_field.value.isdigit():
            page.snack_bar = ft.SnackBar(
                ft.Text("El número de celular debe tener entre 8 y 12 dígitos y solo contener números", color=ft.colors.WHITE), bgcolor=ft.colors.RED
            )
            page.snack_bar.open = True
            page.update()
            return

        # Verificar si ya existe una persona registrada con el mismo número de identificación
        if controller.existe_usuario(id_field.value):
            page.snack_bar = ft.SnackBar(
                ft.Text("Ya existe una persona registrada con este número de identificación", color=ft.colors.WHITE), bgcolor=ft.colors.RED
            )
            page.snack_bar.open = True
            page.update()
            return

        
        # Crear un nuevo usuario
        nuevo_usuario = Usuario(
            id=Usuario.nuevo_id(),  # Generar un nuevo ID
            nombre=nombre_field.value,
            apellidos=apellidos_field.value,  # Obtener 'apellidos'
            edad=edad,
            num_identificacion=id_field.value,
            correo=correo_field.value,
            telefono=telefono_field.value,
            estado="inscrito"  # Estado por defecto
        )


        controller.agregar_usuario(nuevo_usuario)

        # Limpiar los campos después de la inscripción
        nombre_field.value = ""
        apellidos_field.value = ""  # Limpiar 'apellidos_field'
        edad_field.value = ""
        id_field.value = ""
        correo_field.value = ""
        telefono_field.value = ""
        page.snack_bar = ft.SnackBar(
            ft.Text("Usuario inscrito exitosamente", color=ft.colors.WHITE), bgcolor=ft.colors.GREEN
        )
        # age.snack_bar.open = True
        page.update()

    

    inscripcion_view = create_inscripcion_view(
        inscribir_persona=inscribir_persona, 
        validar_identificacion=validar_identificacion, 
        validar_email=validar_email, 
        validar_apellidos=validar_apellidos,
        validar_telefono=validar_telefono,
        validar_nombre=validar_nombre,
        validar_edad=validar_edad
    )
    
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
            apellidos_field,  
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


    Usuarios_view = create_usuarios_view(mostrar_usuarios_view)


    inscripciones_list = ft.Column([])

    inscripciones_view = ft.Container(
        ft.Column(
            [
                ft.Text("Inscripciones", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10, thickness=2),
                inscripciones_list,
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
        ),
        expand=True,
        padding=20,
    )


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
            page.update()
            actualizar_data_torneos()
        elif index == 3:
            content.controls.append(entrenamientos_view)
            page.update()  # Actualizar la página para agregar entrenamientos_view primero
            actualizar_entrenamientos()  # Luego actualizar el ListView
            return  # Salir para evitar llamar a page.update() nuevamente
        elif index == 4:
            content.controls.append(informes_view)
        elif index == 5:
            pagos_view = create_pagos_view(controller, page) 
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
            ft.NavigationRailDestination(icon=ft.icons.FITNESS_CENTER, label="Entrenamiento"),
            ft.NavigationRailDestination(icon=ft.icons.BAR_CHART, label="Informes"),
            ft.NavigationRailDestination(icon=ft.icons.ATTACH_MONEY, label="Pagos"),
        ],
        on_change=lambda e: destination_change(e)
    )

    content = ft.Column([inscripcion_view], expand=True)

    page.add(app_bar, ft.Row([rail, ft.VerticalDivider(width=1), content], expand=True))

ft.app(target=main)
