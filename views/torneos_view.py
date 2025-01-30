# tallerdiseno1/views/torneos_view.py
import flet as ft
from modelos.base_model import BaseModel

def create_torneos_view(controller, torneos, page):
    """
    Crea y retorna la vista de gestión de torneos.
    
    Parámetros:
        controller: El controlador de la aplicación que gestiona los datos y lógica de negocio.
        torneos: Lista de torneos disponibles.
        page: Página de Flet para actualizar UI y mostrar SnackBars.
    
    Retorna:
        tuple: Contiene la vista de torneos y los componentes necesarios como objetos de Flet.
    """
    
    # Función para mostrar SnackBar
    def mostrar_snackbar(mensaje, tipo):
        color = ft.colors.GREEN if tipo == "SUCCESS" else ft.colors.RED
        snack_bar = ft.SnackBar(ft.Text(mensaje, color=ft.colors.WHITE), bgcolor=color)
        page.snack_bar = snack_bar
        snack_bar.open = True
        page.update()
    
    # Función para inscribir en torneo
    def inscribir_a_torneo(e):
        usuario_nombre = dropdown_usuarios.value
        torneo_nombre = dropdown_torneos.value
        if not usuario_nombre or not torneo_nombre:
            mostrar_snackbar("Debe seleccionar un usuario y un torneo", "ERROR")
            return
        # Obtener torneo_id desde el nombre usando el mapeo
        torneo_id = torneo_id_map.get(torneo_nombre)
        if torneo_id is None:
            mostrar_snackbar("El torneo seleccionado no existe.", "ERROR")
            return
        # Agregar una nueva inscripción
        inscripciones = controller.cargar_inscripciones()
        inscripciones.append({
            "usuario": usuario_nombre,
            "torneo_id": torneo_id
        })
        BaseModel.guardar_datos("inscripciones.json", inscripciones)
        mostrar_snackbar(f"Usuario {usuario_nombre} inscrito en torneo {torneo_id}", "SUCCESS")
    
    # Función para agregar torneo
    def agregar_torneo(e):
        # Abrir un diálogo para ingresar nombre y fecha del torneo
        nombre_input = ft.TextField(label="Nombre del Torneo", autofocus=True)
        fecha_input = ft.TextField(label="Fecha del Torneo", hint_text="YYYY-MM-DD")
        agregar_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Agregar Torneo"),
            content=ft.Column([nombre_input, fecha_input], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.dialog.close()),
                ft.TextButton("Agregar", on_click=lambda e: agregar_torneo_confirm(nombre_input.value, fecha_input.value)),
            ]
        )
        page.dialog = agregar_dialog
        agregar_dialog.open = True
        page.update()
    
    # Confirmar agregar torneo
    def agregar_torneo_confirm(nombre, fecha):
        if not nombre or not fecha:
            mostrar_snackbar("Por favor, complete todos los campos.", "ERROR")
            return
        # Crear el torneo, assuming torneo es un dict con 'id', 'nombre', 'fecha'
        nuevo_id = max([t['id'] for t in torneos], default=0) + 1
        nuevo_torneo = {
            "id": nuevo_id,
            "nombre": nombre,
            "fecha": fecha
        }
        # Guardar torneo
        torneos.append(nuevo_torneo)
        BaseModel.guardar_datos("torneos.json", torneos)
        # Actualizar el mapeo de nombres a IDs
        torneo_id_map[nombre] = nuevo_id
        # Actualizar la lista de torneos en la UI
        torneos_list.controls.append(
            ft.ListTile(
                title=ft.Text(nuevo_torneo["nombre"]),
                on_click=lambda e, t=nuevo_torneo["id"]: on_torneo_click(t),
                data=nuevo_torneo["id"]  # Almacenar torneo.id como data
            )
        )
        mostrar_snackbar(f"Torneo '{nombre}' agregado exitosamente.", "SUCCESS")
        page.dialog.close()
        page.update()
    
    # Función para mostrar inscripciones al hacer clic en un torneo
    def on_torneo_click(torneo_id):
        # Obtener las inscripciones para este torneo
        inscripciones = controller.get_inscripciones_by_torneo(torneo_id)
        print(torneo_id)
        # Limpiar y actualizar inscripciones_list
        inscripciones_list.controls.clear()
        if not inscripciones:
            inscripciones_list.controls.append(ft.Text("No hay inscripciones para este torneo."))
        else:
            for insc in inscripciones:
                inscripciones_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(insc['usuario']),
                        leading=ft.Icon(ft.icons.PERSON),
                    )
                )
        page.update()
    
    # Dropdown de usuarios matriculados
    dropdown_usuarios = controller.dropdown_usuarios_matriculados()
    
    # Mapeo de nombres de torneos a IDs para uso interno
    torneo_id_map = {torneo.nombre: torneo.id for torneo in torneos}
    
    # Dropdown de torneos
    dropdown_torneos = ft.Dropdown(
        label="Seleccione un torneo",
        options=[ft.dropdown.Option(torneo.nombre) for torneo in torneos],
        value=None  # Inicialmente sin selección
    )
    
    # Lista de torneos como ListTile con manejo de clics basado en IDs
    torneos_list = ft.Column()
    for torneo in torneos:
        torneos_list.controls.append(
            ft.ListTile(
                title=ft.Text(torneo.nombre),
                on_click=lambda e, t=torneo.id: on_torneo_click(t),
                data=torneo.id  # Almacenar torneo.id en data
            )
        )
    
    # Botón para inscribir en torneo
    inscribir_button = ft.ElevatedButton(
        "Inscribir en Torneo", 
        icon=ft.icons.CHECK, 
        on_click=inscribir_a_torneo
    )
    
    # Botón flotante para agregar torneo
    agregar_torneo_button = ft.FloatingActionButton(
        icon=ft.icons.ADD, 
        on_click=agregar_torneo, 
        tooltip="Añadir Torneo"
    )
    
    # Lista para inscripciones
    inscripciones_list = ft.Column([])
    
    # Vista de inscripciones
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
    
    # Vista principal de torneos
    torneos_view = ft.Row(
        [
            # Columna de dropdowns y botón de inscripción
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
            # Columna de lista de torneos y botón para agregar
            ft.Container(
                ft.Column(
                    [
                        ft.Text("Torneos", size=24, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10, thickness=2),
                        torneos_list,
                        agregar_torneo_button,
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.START,
                ),
                expand=True,
                padding=20,
            ),
            ft.VerticalDivider(width=1),
            # Columna de inscripciones registradas
            inscripciones_view,
        ],
        expand=True,
    )
    
    return torneos_view, torneos_list, dropdown_torneos
