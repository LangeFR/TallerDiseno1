import flet as ft
from modelos.informe import Informe
import json


def main(page: ft.Page):
    page.title = "Club de Tenis"
    page.theme_mode = ft.ThemeMode.DARK

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

    # --- Funcionalidades ---
    inscritos = []

    # Inscripción
    def inscribir_persona(e):
        if not nombre_field.value or not edad_field.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, complete todos los campos"), bgcolor=ft.colors.ERROR)
            page.snack_bar.open()
            return

        inscritos.append({
            "nombre": nombre_field.value,
            "edad": edad_field.value,
            "contacto": contacto_field.value,
            "identificación": id_field.value,
            "correo": correo_field.value,
            "telefono": telefono_field.value
        })

        nombre_field.value = ""
        edad_field.value = ""
        contacto_field.value = ""
        id_field.value = ""
        correo_field = ""
        telefono_field = ""
        page.update()
        page.snack_bar = ft.SnackBar(ft.Text("Persona inscrita exitosamente"), bgcolor=ft.colors.SUCCESS)
        page.snack_bar.open()

    nombre_field = ft.TextField(label="Nombre", width=300)
    edad_field = ft.TextField(label="Edad", width=300)
    contacto_field = ft.TextField(label="Contacto", width=300)
    id_field = ft.TextField(label=" Inscripción", width=300)
    correo_field = ft.TextField(label=" Correo", width=300)
    telefono_field = ft.TextField(label=" Correo", width=300)

    inscribir_button = ft.ElevatedButton("Inscribir", on_click=inscribir_persona)

    inscripcion_view = ft.Column([
        ft.Text("Inscripción", size=20, weight=ft.FontWeight.BOLD),
        nombre_field, edad_field, contacto_field, id_field, correo_field, telefono_field, inscribir_button
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
    def generar_informes(mes, año):
        # Cargar los datos de los miembros desde el archivo JSON
        try:
            with open("base_de_datos/miembros.json", "r") as archivo_miembros:
                miembros = json.load(archivo_miembros)
        except FileNotFoundError:
            print("El archivo de miembros no se encuentra.")
            return
        except json.JSONDecodeError:
            print("El archivo de miembros no está en el formato correcto.")
            return

        # Filtrar miembros con estado 'matriculado'
        miembros_matriculados = [miembro for miembro in miembros if miembro['estado'] == 'matriculado']

        # Generar un informe para cada miembro matriculado
        for miembro in miembros_matriculados:
            Informe.crear_informe(miembro['id'], mes, año)

        print(f"Informes generados para el mes {mes} del año {año}")

        
        informe_view.update()


    informe_view = ft.Column([], spacing=10)
    generar_informe_button = ft.ElevatedButton("Generar Informe", on_click=generar_informes('2025-01'))

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
