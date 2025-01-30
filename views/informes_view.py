# tallerdiseno1/views/informes_view.py
import flet as ft
import json
from modelos.informe import Informe

def create_informes_view(controller, page):
    """
    Crea y retorna la vista de generación y visualización de informes.

    Parámetros:
        controller: Controlador de la aplicación.
        page: Página de Flet para actualizar UI y mostrar SnackBars.

    Retorna:
        tuple: (Vista de informes, campos de año y mes, contenedor de informes)
    """

    # Campos de texto para ingresar año y mes
    input_anio = ft.TextField(
        label="Ingresar Año",
        width=100,
        hint_text="2025",
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    input_mes = ft.TextField(
        label="Ingresar Mes",
        width=50,
        hint_text="01",
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    # Contenedor donde se mostrarán los informes generados
    informe_container = ft.Column([], expand=True, spacing=10)

    # Función que crea informes en disco con base en anio y mes
    def crear_informes(anio, mes):
        print("Generando informes...")
        # Validar que sean dígitos
        if not anio.isdigit() or not mes.isdigit():
            page.snack_bar = ft.SnackBar(
                ft.Text("Año y mes deben ser números."), bgcolor=ft.colors.ERROR
            )
            page.snack_bar.open = True
            page.update()
            return

        anio_int = int(anio)
        mes_int = int(mes)

        if not (1 <= mes_int <= 12):
            page.snack_bar = ft.SnackBar(
                ft.Text("Mes debe estar entre 1 y 12."), bgcolor=ft.colors.ERROR
            )
            page.snack_bar.open = True
            page.update()
            return

        # Formatear mes con dos dígitos
        mes_formateado = str(mes_int).zfill(2)

        # Filtrar usuarios con estado 'matriculado' usando el controlador
        usuarios_matriculados = controller.filtrar_usuarios('matriculado')

        # Generar un informe para cada miembro matriculado
        for usuario in usuarios_matriculados:
            Informe.crear_informe(usuario.id, mes_formateado, anio_int)

        print(f"Informes generados para el mes {mes_int} del año {anio_int}")
        page.snack_bar = ft.SnackBar(
            ft.Text(f"Informes generados para el mes {mes_int} del año {anio_int}."),
            bgcolor=ft.colors.GREEN
        )
        page.snack_bar.open = True
        page.update()

    # Función para generar (mostrar) informes en el contenedor
    def generar_informes(e):
        anio_val = input_anio.value
        mes_val = input_mes.value

        # Primero, crear informes en disco
        crear_informes(anio_val, mes_val)

        # Luego, limpiar el contenedor e intentar mostrar los informes creados
        informe_container.controls.clear()
        try:
            with open("base_de_datos/informes.json", "r") as file:
                content = file.read().strip()
                if not content:
                    informes = []
                else:
                    informes = json.loads(content)

            # Filtrar informes por año y mes
            informes_filtrados = [
                inf for inf in informes
                if str(inf["anio"]) == str(anio_val)
                and str(inf["mes"]).zfill(2) == str(mes_val).zfill(2)
            ]

            print(f"Cantidad de informes filtrados: {len(informes_filtrados)}")

            # Mostrar cada informe con sus datos en un Card
            for inf in informes_filtrados:
                informe_card = ft.Card(
                    content=ft.Container(
                        ft.Column([
                            ft.Text(f"Informe ID: {inf['id']}"),
                            ft.Text(f"Usuario ID: {inf['usuario_id']}"),
                            ft.Text(f"Año: {inf['anio']}  |  Mes: {inf['mes']}"),
                            ft.Text(f"Clases del Mes: {inf['clases_mes']}"),
                            ft.Text(f"Clases Asistidas: {inf['clases_asistidas']}"),
                            ft.Text(f"Torneos Asistidos: {inf['torneos_asistidos']}"),
                            ft.Text(f"Top Torneos: {inf['top_torneos']}")
                        ]),
                        padding=10
                    ),
                    width=300,
                )
                informe_container.controls.append(informe_card)

            page.update()

        except Exception as ex:
            print("Error al cargar informes:", ex)
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Error al cargar informes: {str(ex)}"), 
                bgcolor=ft.colors.ERROR
            )
            page.snack_bar.open = True
            page.update()

    # Botón para generar informes
    generar_informe_button = ft.ElevatedButton(
        "Generar Informes",
        on_click=generar_informes
    )

    # Vista principal de informes
    informes_view = ft.Column(
        [
            ft.Row([input_anio, input_mes]),
            generar_informe_button,
            informe_container
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START
    )

    # Retornar la vista principal y los campos si es necesario
    return informes_view, input_anio, input_mes, informe_container
